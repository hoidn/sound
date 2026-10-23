/* xdev: drive a device bundle's x86_64 slice through its seven C exports.
 *
 * Usage: xdev UNIVERSAL_BUNDLE_EXECUTABLE SCRIPT OUT.f32 [--imports]
 * SCRIPT lines (one command each, '#' starts a comment):
 *   info                         GetPlugInfoU for selectors 1..6 (sizes 8,8,8,4,8,4)
 *   create                       CreateInstanceU()
 *   rate N                       SetSampleRateU(inst, N)
 *   param I V                    SetParameterA(inst, I, (float)V)
 *   reset                        ResetA(inst)
 *   transport PLAYING POS TEMPO  the struct passed as CalcA argument 7: {int32, pad, double, double}
 *   input FILE | input zero      interleaved stereo binary32 input, consumed by process; zero = silence
 *   inflag F                     value stored in *flag before each CalcA (the bundle reads it as "input present")
 *   event FRAME STATUS D1 D2     queue a 16-byte event {int64 frame; u8 status, d1, d2, 0; pad} at an
 *                                absolute output frame; delivered in the block that contains it, frame
 *                                relative to that block's start
 *   mxcsr HEX                    set MXCSR before every later call into the bundle
 *   process N B                  N frames in host blocks of B frames; output appended to OUT.f32
 *                                as interleaved stereo binary32
 *   destroy                      DestroyInstanceU(inst)
 * Prints one line per command and, at exit, "used SYMBOL N" for each bound import called.
 * CalcA is called as CalcA(inst, frames, L, R, nevents, events, &transport, &flag); input frames
 * are copied into L and R first, since the bundles process in place. */
#define _GNU_SOURCE
#include "xdev.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <xmmintrin.h>

#define die(...) do { fprintf(stderr, "xdev: " __VA_ARGS__); fputc('\n', stderr); exit(2); } while (0)

typedef struct { int32_t playing, pad; double position, tempo; } transport_t;
typedef struct { int64_t frame; uint8_t status, d1, d2, d3, pad[4]; } event_t;
typedef void *(*create_t)(void);
typedef void (*destroy_t)(void *);
typedef long (*rate_t)(void *, long);
typedef long (*info_t)(long, void *, long);
typedef long (*calc_t)(void *, long, float *, float *, long, event_t *, transport_t *, int *);
typedef void (*param_t)(void *, int, float);
typedef void (*reset_t)(void *);

static struct { create_t create; destroy_t destroy; rate_t rate; info_t info; calc_t calc; param_t param; reset_t reset; } x;
static unsigned mxcsr = 0x1f80;
static void enter(void) { _mm_setcsr(mxcsr); }
static void leave(void) { _mm_setcsr(0x1f80); }

static uint64_t need(const char *name)
{
    uint64_t a = xdev_symbol(name);
    if (!a) die("export %s missing", name);
    printf("export %s 0x%lx\n", name, a - XDEV_SLIDE);
    return a;
}

static event_t events[4096];
static int nevents;

/* Render N frames in blocks of B; returns the number of blocks. Prints the per-block flag and
 * return value as run-length pairs. */
static void process(void *inst, long n, long b, FILE *in, FILE *out, transport_t *tp, int inflag)
{
    float *L = calloc(b, 4), *R = calloc(b, 4), *io = calloc(2 * b, 4);
    event_t blk[4096];
    long done = 0, nb = 0, prev_ret = -2, prev_flag = -2, run = 0;
    printf("process %ld %ld flags:", n, b);
    while (done < n) {
        long k = n - done < b ? n - done : b;
        if (in) { if ((long)fread(io, 8, k, in) != k) die("input ended at frame %ld", done); }
        else memset(io, 0, 8 * k);
        for (long i = 0; i < k; i++) { L[i] = io[2 * i]; R[i] = io[2 * i + 1]; }
        int m = 0;
        for (int e = 0; e < nevents; e++)
            if (events[e].frame >= done && events[e].frame < done + k) { blk[m] = events[e]; blk[m++].frame -= done; }
        int flag = inflag;
        enter();
        long ret = x.calc(inst, k, L, R, m, m ? blk : NULL, tp, &flag);
        leave();
        if (ret != prev_ret || flag != prev_flag) {
            if (run) printf(" %ldx(ret=%ld,flag=%ld)", run, prev_ret, prev_flag);
            prev_ret = ret; prev_flag = flag; run = 0;
        }
        run++;
        for (long i = 0; i < k; i++) { io[2 * i] = L[i]; io[2 * i + 1] = R[i]; }
        fwrite(io, 8, k, out);
        done += k; nb++;
    }
    printf(" %ldx(ret=%ld,flag=%ld) blocks=%ld\n", run, prev_ret, prev_flag, nb);
    free(L); free(R); free(io);
}

int main(int argc, char **argv)
{
    if (argc < 4) die("usage: xdev BUNDLE_EXECUTABLE SCRIPT OUT.f32 [--imports]");
    xdev_install_fault_handler();
    xdev_load(argv[1]);
    printf("slice offset=%lu size=%lu\n", xdev_slice_offset(), xdev_slice_size());
    if (argc > 4 && !strcmp(argv[4], "--imports")) xdev_print_imports();
    x.create = (create_t)need("_CreateInstanceU"); x.destroy = (destroy_t)need("_DestroyInstanceU");
    x.rate = (rate_t)need("_SetSampleRateU"); x.info = (info_t)need("_GetPlugInfoU");
    x.calc = (calc_t)need("_CalcA"); x.param = (param_t)need("_SetParameterA"); x.reset = (reset_t)need("_ResetA");
    FILE *sc = fopen(argv[2], "r"), *out = fopen(argv[3], "wb"), *in = NULL;
    if (!sc || !out) die("cannot open script or output");
    void *inst = NULL;
    transport_t tp = { 0, 0, 0.0, 120.0 };
    int inflag = 0;
    char line[512], cmd[32], arg[400];
    while (fgets(line, sizeof line, sc)) {
        char *h = strchr(line, '#'); if (h) *h = 0;
        if (sscanf(line, "%31s", cmd) != 1) continue;
        long a = 0, b = 0, c = 0, d = 0; double v = 0;
        fflush(stdout);
        if (!strcmp(cmd, "info")) {
            static const long sz[] = { 8, 8, 8, 4, 8, 4 };
            for (long s = 1; s <= 6; s++) {
                uint64_t o = 0; enter(); long r = x.info(s, &o, sz[s - 1]); leave();
                printf("info %ld size=%ld ret=%ld value=%lu\n", s, sz[s - 1], r, sz[s - 1] == 4 ? (uint32_t)o : o);
            }
        } else if (!strcmp(cmd, "create")) {
            enter(); inst = x.create(); leave();
            printf("create %s\n", inst ? "ok" : "NULL");
        } else if (!strcmp(cmd, "rate") && sscanf(line, "%*s %ld", &a) == 1) {
            enter(); long r = x.rate(inst, a); leave();
            printf("rate %ld ret=%ld\n", a, r);
        } else if (!strcmp(cmd, "param") && sscanf(line, "%*s %ld %lf", &a, &v) == 2) {
            enter(); x.param(inst, (int)a, (float)v); leave();
            printf("param %ld %.9g\n", a, (float)v);
        } else if (!strcmp(cmd, "reset")) {
            enter(); x.reset(inst); leave(); printf("reset\n");
        } else if (!strcmp(cmd, "transport") && sscanf(line, "%*s %ld %lf %lf", &a, &tp.position, &tp.tempo) == 3) {
            tp.playing = (int32_t)a; printf("transport %d %.17g %.17g\n", tp.playing, tp.position, tp.tempo);
        } else if (!strcmp(cmd, "input") && sscanf(line, "%*s %399s", arg) == 1) {
            if (in) fclose(in);
            in = strcmp(arg, "zero") ? fopen(arg, "rb") : NULL;
            if (strcmp(arg, "zero") && !in) die("cannot open input %s", arg);
            printf("input %s\n", arg);
        } else if (!strcmp(cmd, "inflag") && sscanf(line, "%*s %ld", &a) == 1) {
            inflag = (int)a; printf("inflag %d\n", inflag);
        } else if (!strcmp(cmd, "event") && sscanf(line, "%*s %ld %li %li %li", &a, &b, &c, &d) == 4) {
            if (nevents == 4096) die("too many events");
            events[nevents++] = (event_t){ a, (uint8_t)b, (uint8_t)c, (uint8_t)d, 0, {0} };
            printf("event %ld 0x%02lx %ld %ld\n", a, b, c, d);
        } else if (!strcmp(cmd, "mxcsr") && sscanf(line, "%*s %lx", &a) == 1) {
            mxcsr = (unsigned)a; printf("mxcsr 0x%x\n", mxcsr);
        } else if (!strcmp(cmd, "process") && sscanf(line, "%*s %ld %ld", &a, &b) == 2) {
            if (b < 1 || b > 65536) die("bad block size");
            process(inst, a, b, in, out, &tp, inflag);
        } else if (!strcmp(cmd, "destroy")) {
            enter(); x.destroy(inst); leave(); inst = NULL; printf("destroy\n");
        } else die("bad script line: %s", line);
    }
    fclose(out);
    xdev_print_used();
    printf("cxx-failbits %ld\n", xdev_cxx_failbits);
    return 0;
}
