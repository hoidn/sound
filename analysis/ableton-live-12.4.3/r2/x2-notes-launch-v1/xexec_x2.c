/*
 * xexec: load the x86_64 Mach-O slice of Live at its preferred addresses and
 * call one or more of its functions with System V AMD64 arguments.
 *
 * X2 copy (analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1): identical to tools/xexec/xexec.c
 * except for one added command, "poke EXPR EXPR", which stores the 8-byte value of the second
 * expression at the address given by the first. It lets a run place pointers to its own buffers
 * inside other buffers (hand-built objects). Nothing else changed.
 *
 * Usage:  xexec SLICE [--imports] {call ADDR ARG... | dump EXPR LEN | poke EXPR EXPR}...
 *   --imports  print each imported symbol as "import linux|trap SYMBOL slots=N" before the calls
 *   ARG:  i:N      next integer register (decimal or 0x hex)
 *         d:X      next xmm register, binary64        f:X  next xmm, binary32
 *         buf:N    new zeroed N-byte buffer bK, pointer in next integer register
 *         hex:HH   new buffer bK holding these bytes, pointer in next integer register
 *         str:S    new buffer bK holding S and a NUL, pointer in next integer register
 *         ref:E    value of expression E in next integer register
 *   EXPR: base (bK | rK | 0xADDR) then any of  *  (load a qword),  @  (load a uint32)
 *         and  +N / -N.
 *         rK is call K's rax.  Example: b0*+16 = (qword at b0) + 16.  LEN is an EXPR too.
 * Output: "call K ADDR rax=.. rdx=.. xmm0=.. xmm1=.." (hex bit patterns),
 *         "out bK ADDR HEX" for each buffer passed to that call, "dump EXPR ADDR HEX";
 *         at exit "used SYMBOL N" for each Linux-bound code import called N > 0 times.
 * A call into an unbound import prints "TRAP <symbol>" and exits 86.
 * A fault prints "FAULT addr=.. rip=.." and exits 87.
 *
 * Dependencies: only the slice file, glibc and libm. Rebases (slide 0), binds and
 * lazy binds come from LC_DYLD_INFO_ONLY (the slice has no chained fixups; the
 * loader refuses one that does). Lazy binds are resolved eagerly. Weak binds are
 * not applied: the slice's own weak definitions stay in place. Static
 * initializers are not run; a caller runs the ones it needs as ordinary calls.
 * Imports listed in `fixed` and `libm` below are bound to glibc functions with the
 * same contract (or a small adapter); every other import, data or code, is bound
 * to a per-symbol trap. Single-threaded: the C++ guard and pthread-key adapters
 * assume one thread. Stack arguments (more than 6 integer or 8 fp) are unsupported.
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <locale.h>
#include <stdarg.h>
#include <math.h>
#include <pthread.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <ucontext.h>
#include <unistd.h>

#define die(...) do { fprintf(stderr, "xexec: " __VA_ARGS__); fputc('\n', stderr); exit(2); } while (0)

typedef struct { char name[17]; uint64_t vmaddr, vmsize, fileoff, filesize; int prot; } seg_t;
static seg_t segs[16];
static int nsegs;
static uint8_t *file;

/* ---- imports bound to Linux equivalents ------------------------------- */
static void say(const char *m) { if (write(2, m, strlen(m)) < 0) _exit(88); }
static long guard_value = 0x2f8a6b1c4d3e5f71;
__attribute__((force_align_arg_pointer, noreturn)) static void x_stack_chk_fail(void)
{ say("TRAP ___stack_chk_fail (stack smashed)\n"); _exit(86); }
static void *x_new(size_t n) { void *p = malloc(n ? n : 1); if (!p) die("operator new(%zu) failed", n); return p; }
static void x_delete(void *p) { free(p); }
static void x_delete_sized(void *p, size_t n) { (void)n; free(p); }
static void x_bzero(void *p, size_t n) { memset(p, 0, n); }
/* Itanium C++ ABI guards, single-threaded: byte 0 of the guard is the "done" flag. */
static int x_guard_acquire(uint8_t *g) { return *g == 0; }
static void x_guard_release(uint8_t *g) { *g = 1; }
static void x_guard_abort(uint8_t *g) { (void)g; }
/* Static destructors are registered but never run: the harness exits without them. */
static int x_atexit(void *f, void *a, void *d) { (void)f; (void)a; (void)d; return 0; }
/* macOS pthread_key_t is unsigned long; glibc's is unsigned int. */
static int x_key_create(unsigned long *k, void (*d)(void *))
{ pthread_key_t g; int r = pthread_key_create(&g, d); *k = g; return r; }
static void *x_getspecific(unsigned long k) { return pthread_getspecific((pthread_key_t)k); }
static int x_setspecific(unsigned long k, const void *v) { return pthread_setspecific((pthread_key_t)k, v); }
/* Only the C locale is supported: newlocale(mask, NULL or "C", base) on macOS gives the C locale. */
static locale_t x_newlocale(int mask, const char *name, locale_t base)
{
    if (name && strcmp(name, "C") && strcmp(name, "POSIX")) { say("TRAP _newlocale (non-C locale)\n"); _exit(86); }
    (void)mask; (void)base; return newlocale(LC_ALL_MASK, "C", 0);
}
static int x_vsnprintf_l(char *b, size_t n, locale_t loc, const char *fmt, va_list ap)
{
    locale_t old = uselocale(loc); int r = vsnprintf(b, n, fmt, ap); uselocale(old); return r;
}

static const struct { const char *mach; void *addr; } fixed[] = {
    {"_memcpy", memcpy}, {"_memmove", memmove}, {"_memset", memset}, {"_memcmp", memcmp},
    {"_bzero", x_bzero}, {"___bzero", x_bzero}, {"_strlen", strlen},
    {"_malloc", malloc}, {"_calloc", calloc}, {"_realloc", realloc}, {"_free", free},
    {"__Znwm", x_new}, {"__Znam", x_new}, {"__ZdlPv", x_delete}, {"__ZdaPv", x_delete},
    {"__ZdlPvm", x_delete_sized}, {"__ZdaPvm", x_delete_sized},
    {"_strchr", strchr}, {"_strcmp", strcmp}, {"_strncmp", strncmp},
    {"___cxa_guard_acquire", x_guard_acquire}, {"___cxa_guard_release", x_guard_release},
    {"___cxa_guard_abort", x_guard_abort}, {"___cxa_atexit", x_atexit},
    {"_pthread_key_create", x_key_create}, {"_pthread_getspecific", x_getspecific},
    {"_pthread_setspecific", x_setspecific},
    {"_newlocale", x_newlocale}, {"_vsnprintf_l", x_vsnprintf_l},
    {"___stack_chk_guard", &guard_value}, {"___stack_chk_fail", x_stack_chk_fail},
};
/* libm: Mach-O "_name" binds to glibc "name"; "___exp10" style binds to "exp10". */
static const char *libm[] = {
    "log10f", "log10", "logf", "log", "log2f", "log2", "log1pf", "log1p", "expf", "exp",
    "exp2f", "exp2", "exp10f", "exp10", "expm1f", "expm1", "powf", "pow", "sqrtf", "sqrt",
    "cbrtf", "cbrt", "floorf", "floor", "ceilf", "ceil", "roundf", "round", "truncf", "trunc",
    "lroundf", "lround", "llroundf", "llround", "rintf", "rint", "lrintf", "lrint", "nearbyintf",
    "nearbyint", "fmodf", "fmod", "remainderf", "remainder", "fabsf", "fabs", "fminf", "fmin",
    "fmaxf", "fmax", "sinf", "sin", "cosf", "cos", "tanf", "tan", "asinf", "asin", "acosf",
    "acos", "atanf", "atan", "atan2f", "atan2", "sinhf", "sinh", "coshf", "cosh", "tanhf", "tanh",
    "hypotf", "hypot", "modff", "modf", "frexpf", "frexp", "ldexpf", "ldexp", "fmaf", "fma", NULL };

static void *linux_equivalent(const char *sym)
{
    for (size_t i = 0; i < sizeof fixed / sizeof *fixed; i++)
        if (!strcmp(sym, fixed[i].mach)) return fixed[i].addr;
    const char *base = sym[0] == '_' ? sym + 1 : sym;
    if (!strncmp(sym, "___", 3)) base = sym + 3;
    for (int i = 0; libm[i]; i++)
        if (!strcmp(base, libm[i])) {
            static void *h;
            if (!h && !(h = dlopen("libm.so.6", RTLD_NOW))) die("dlopen libm");
            return dlsym(h, base);
        }
    return NULL;
}

/* ---- one stub per imported symbol ------------------------------------ */
/* A Linux-bound code import goes through a stub that counts its calls (printed as
 * "used SYMBOL N" at exit); any other import goes to a trap that names it.     */
static struct { char *name; void *target; long slots, uses; int data; } stubs[8192];
static int nstubs;
static uint8_t *stub_code;
__attribute__((force_align_arg_pointer, noreturn)) static void trap(long idx)
{
    say("TRAP "); say(stubs[idx].name); say("\n"); _exit(86);
}
static uint64_t stub_for(const char *sym, void *target)
{
    int i;
    for (i = 0; i < nstubs && strcmp(stubs[i].name, sym); i++) ;
    uint8_t *c = stub_code + 32 * i;
    if (i == nstubs) {
        if (nstubs == 8192) die("too many imported symbols");
        stubs[nstubs].name = strdup(sym); stubs[nstubs].target = target; nstubs++;
        stubs[i].data = target == (void *)&guard_value;     /* the one data import: bound to the variable */
        uint64_t t = target ? (uint64_t)target : (uint64_t)trap, u = (uint64_t)&stubs[i].uses;
        if (target) {                       /* movabs r11,&uses; lock incq (r11); movabs r11,target; jmp r11 */
            c[0] = 0x49; c[1] = 0xbb; memcpy(c + 2, &u, 8); c[10] = 0xf0; c[11] = 0x49; c[12] = 0xff; c[13] = 0x03;
            c[14] = 0x49; c[15] = 0xbb; memcpy(c + 16, &t, 8); c[24] = 0x41; c[25] = 0xff; c[26] = 0xe3;
        } else {                            /* mov rdi,idx; movabs rax,trap; jmp rax */
            c[0] = 0x48; c[1] = 0xc7; c[2] = 0xc7; memcpy(c + 3, &i, 4);
            c[7] = 0x48; c[8] = 0xb8; memcpy(c + 9, &t, 8); c[17] = 0xff; c[18] = 0xe0;
        }
    }
    stubs[i].slots++;
    return stubs[i].data ? (uint64_t)target : (uint64_t)c;
}

/* ---- dyld info -------------------------------------------------------- */
static uint64_t uleb(const uint8_t **p)
{ uint64_t v = 0; int s = 0; uint8_t b; do { b = *(*p)++; v |= (uint64_t)(b & 0x7f) << s; s += 7; } while (b & 0x80); return v; }
static int64_t sleb(const uint8_t **p)
{ int64_t v = 0; int s = 0; uint8_t b; do { b = *(*p)++; v |= (int64_t)(b & 0x7f) << s; s += 7; } while (b & 0x80);
  if (s < 64 && (b & 0x40)) v |= -((int64_t)1 << s);
  return v; }

static long nrebase;
static void rebase(const uint8_t *p, const uint8_t *end, int64_t slide)
{
    int seg = 0; uint64_t off = 0;
    while (p < end) {
        uint8_t op = *p & 0xf0, imm = *p & 0x0f; p++;
        uint64_t n, skip;
        switch (op) {
        case 0x00: return;
        case 0x10: break;                                       /* SET_TYPE_IMM (pointer) */
        case 0x20: seg = imm; off = uleb(&p); break;
        case 0x30: off += uleb(&p); break;
        case 0x40: off += imm * 8; break;
        case 0x50: for (n = imm; n--; off += 8) { *(uint64_t *)(segs[seg].vmaddr + off) += slide; nrebase++; } break;
        case 0x60: for (n = uleb(&p); n--; off += 8) { *(uint64_t *)(segs[seg].vmaddr + off) += slide; nrebase++; } break;
        case 0x70: *(uint64_t *)(segs[seg].vmaddr + off) += slide; nrebase++; off += uleb(&p) + 8; break;
        case 0x80: n = uleb(&p); skip = uleb(&p);
                   for (; n--; off += 8 + skip) { *(uint64_t *)(segs[seg].vmaddr + off) += slide; nrebase++; } break;
        default: die("rebase opcode 0x%x", op);
        }
    }
}

static int list_imports;
static long nbound, ntrapped;
static void bind_one(int seg, uint64_t off, const char *sym, int64_t addend)
{
    void *l = linux_equivalent(sym);
    uint64_t v = stub_for(sym, l);
    if (l) nbound++; else ntrapped++;
    *(uint64_t *)(segs[seg].vmaddr + off) = v + addend;
}
static void bind(const uint8_t *p, const uint8_t *end, int lazy)
{
    int seg = 0; uint64_t off = 0; int64_t addend = 0; const char *sym = "";
    while (p < end) {
        uint8_t op = *p & 0xf0, imm = *p & 0x0f; p++;
        uint64_t n, skip;
        switch (op) {
        case 0x00: if (!lazy) return; break;
        case 0x10: case 0x30: break;                            /* dylib ordinal: lookup is by name */
        case 0x20: uleb(&p); break;
        case 0x40: sym = (const char *)p; p += strlen(sym) + 1; break;
        case 0x50: if (imm != 1) die("bind type %d", imm); break;
        case 0x60: addend = sleb(&p); break;
        case 0x70: seg = imm; off = uleb(&p); break;
        case 0x80: off += uleb(&p); break;
        case 0x90: bind_one(seg, off, sym, addend); off += 8; break;
        case 0xa0: bind_one(seg, off, sym, addend); off += uleb(&p) + 8; break;
        case 0xb0: bind_one(seg, off, sym, addend); off += imm * 8 + 8; break;
        case 0xc0: n = uleb(&p); skip = uleb(&p);
                   for (; n--; off += 8 + skip) bind_one(seg, off, sym, addend);
                   break;
        default: die("bind opcode 0x%x", op);
        }
    }
}

static void load(const char *path)
{
    int fd = open(path, O_RDONLY); if (fd < 0) die("open %s", path);
    struct stat st; fstat(fd, &st);
    file = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (file == MAP_FAILED) die("mmap file");
    if (*(uint32_t *)file != 0xfeedfacf || *(int32_t *)(file + 4) != 0x01000007) die("not an x86_64 Mach-O");
    uint32_t ncmds = *(uint32_t *)(file + 16);
    const uint8_t *lc = file + 32, *dinfo = NULL;
    for (uint32_t i = 0; i < ncmds; i++, lc += *(uint32_t *)(lc + 4)) {
        uint32_t cmd = *(uint32_t *)lc;
        if (cmd == 0x19) {
            seg_t *s = &segs[nsegs++];
            memcpy(s->name, lc + 8, 16);
            memcpy(&s->vmaddr, lc + 24, 32);
            s->prot = *(int32_t *)(lc + 60);
        } else if (cmd == 0x80000022 || cmd == 0x22) dinfo = lc;
        else if (cmd == 0x80000034) die("chained fixups not supported (slice uses them)");
    }
    if (!dinfo) die("no LC_DYLD_INFO");
    for (int i = 0; i < nsegs; i++) {
        seg_t *s = &segs[i];
        if (!s->vmsize || !s->prot) continue;                  /* __PAGEZERO */
        int prot = (s->prot & 1 ? PROT_READ : 0) | (s->prot & 2 ? PROT_WRITE : 0) | (s->prot & 4 ? PROT_EXEC : 0);
        /* map writable for fixups first; final protections are applied after binding */
        uint64_t fsz = (s->filesize + 0xfff) & ~0xfffUL;
        void *a = mmap((void *)s->vmaddr, fsz, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_FIXED_NOREPLACE, fd, s->fileoff);
        if (a != (void *)s->vmaddr) die("cannot map %s at 0x%lx", s->name, s->vmaddr);
        if (s->vmsize > fsz &&      /* zero fill (__bss, __common) */
            mmap((void *)(s->vmaddr + fsz), s->vmsize - fsz, PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED_NOREPLACE, -1, 0) != (void *)(s->vmaddr + fsz))
            die("cannot map zero fill of %s", s->name);
        s->prot = prot;
    }
    const uint32_t *d = (const uint32_t *)(dinfo + 8);         /* rebase, bind, weak, lazy, export (off,size) */
    rebase(file + d[0], file + d[0] + d[1], 0);                 /* mapped at preferred base: slide 0 */
    stub_code = mmap(NULL, 32 * 8192, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    bind(file + d[2], file + d[2] + d[3], 0);
    bind(file + d[6], file + d[6] + d[7], 1);
    mprotect(stub_code, 32 * 8192, PROT_READ | PROT_EXEC);
    for (int i = 0; i < nsegs; i++)
        if (segs[i].vmsize && segs[i].prot) mprotect((void *)segs[i].vmaddr, segs[i].vmsize, segs[i].prot);
    close(fd);
}

/* ---- calling ---------------------------------------------------------- */
/* xcall(fn, ints[6], fps[8], out[4]): out = rax, rdx, xmm0, xmm1 */
void xcall(uint64_t fn, const uint64_t *ints, const uint64_t *fps, uint64_t *out);
__asm__(
    ".globl xcall\nxcall:\n"
    " push %rbp\n mov %rsp,%rbp\n push %rbx\n push %r12\n push %r13\n push %r14\n push %r15\n sub $8,%rsp\n"
    " mov %rdi,%r12\n mov %rcx,%r13\n mov %rsi,%r11\n"
    " movq 0(%rdx),%xmm0\n movq 8(%rdx),%xmm1\n movq 16(%rdx),%xmm2\n movq 24(%rdx),%xmm3\n"
    " movq 32(%rdx),%xmm4\n movq 40(%rdx),%xmm5\n movq 48(%rdx),%xmm6\n movq 56(%rdx),%xmm7\n"
    " mov 0(%r11),%rdi\n mov 8(%r11),%rsi\n mov 16(%r11),%rdx\n mov 24(%r11),%rcx\n"
    " mov 32(%r11),%r8\n mov 40(%r11),%r9\n mov $8,%eax\n"
    " call *%r12\n"
    " mov %rax,0(%r13)\n mov %rdx,8(%r13)\n movq %xmm0,16(%r13)\n movq %xmm1,24(%r13)\n"
    " add $8,%rsp\n pop %r15\n pop %r14\n pop %r13\n pop %r12\n pop %rbx\n pop %rbp\n ret\n");

static struct { uint8_t *p; size_t n; } bufs[256];
static int nbufs;
static uint64_t rets[256];
static int ncalls;

static uint64_t num(const char *s) { char *e; uint64_t v = strtoull(s, &e, 0); if (*e) die("bad number %s", s); return v; }
static uint64_t expr(const char *s)
{
    uint64_t v; char *e;
    if (*s == 'b' || *s == 'r') {
        long k = strtol(s + 1, &e, 10);
        if (*s == 'b') { if (k >= nbufs) die("no buffer %s", s); v = (uint64_t)bufs[k].p; }
        else { if (k >= ncalls) die("no call %s", s); v = rets[k]; }
    } else v = strtoull(s, &e, 0);
    while (*e) {
        if (*e == '*') { v = *(uint64_t *)v; e++; }
        else if (*e == '@') { v = *(uint32_t *)v; e++; }
        else if (*e == '+' || *e == '-') v += strtoll(e, &e, 0);
        else die("bad expression %s", s);
    }
    return v;
}
static void hexout(const uint8_t *p, size_t n) { for (size_t i = 0; i < n; i++) printf("%02x", p[i]); }
static int newbuf(size_t n, const void *src, size_t sn)
{
    if (nbufs == 256) die("too many buffers");
    uint8_t *p = aligned_alloc(16, (n + 15) & ~(size_t)15); memset(p, 0, (n + 15) & ~(size_t)15);
    if (src) memcpy(p, src, sn);
    bufs[nbufs].p = p; bufs[nbufs].n = n; return nbufs++;
}

static void fault(int sig, siginfo_t *si, void *ctx)
{
    ucontext_t *uc = ctx;
    fprintf(stderr, "FAULT sig=%d addr=%p rip=0x%llx\n", sig, si->si_addr, (unsigned long long)uc->uc_mcontext.gregs[REG_RIP]);
    _exit(87);
}

int main(int argc, char **argv)
{
    if (argc < 2) die("usage: xexec SLICE [--imports] {call ADDR ARG... | dump EXPR LEN | poke EXPR EXPR}...");
    int a = 2;
    if (a < argc && !strcmp(argv[a], "--imports")) { list_imports = 1; a++; }
    load(argv[1]);
    printf("loaded rebases=%ld binds-linux=%ld binds-trap=%ld symbols=%d\n", nrebase, nbound, ntrapped, nstubs);
    if (list_imports)
        for (int i = 0; i < nstubs; i++)
            printf("import %s %s slots=%ld\n", stubs[i].data ? "linux-data" : stubs[i].target ? "linux" : "trap",
                   stubs[i].name, stubs[i].slots);
    static uint8_t altstack[65536];
    stack_t ss = { .ss_sp = altstack, .ss_size = sizeof altstack };
    sigaltstack(&ss, NULL);
    struct sigaction sa = { .sa_sigaction = fault, .sa_flags = SA_SIGINFO | SA_ONSTACK };
    sigaction(SIGSEGV, &sa, NULL); sigaction(SIGBUS, &sa, NULL); sigaction(SIGILL, &sa, NULL); sigaction(SIGFPE, &sa, NULL);
    while (a < argc) {
        if (!strcmp(argv[a], "dump")) {
            if (a + 2 >= argc) die("dump EXPR LEN");
            uint64_t p = expr(argv[a + 1]); size_t n = expr(argv[a + 2]);
            printf("dump %s 0x%lx ", argv[a + 1], p); hexout((uint8_t *)p, n); printf("\n");
            a += 3; continue;
        }
        if (!strcmp(argv[a], "poke")) {
            if (a + 2 >= argc) die("poke EXPR EXPR");
            uint64_t p = expr(argv[a + 1]), v = expr(argv[a + 2]);
            *(uint64_t *)p = v;
            printf("poke 0x%lx 0x%lx\n", p, v);
            a += 3; continue;
        }
        if (strcmp(argv[a], "call") || a + 1 >= argc) die("expected call or dump at %s", argv[a]);
        uint64_t fn = num(argv[a + 1]), ints[6] = {0}, fps[8] = {0}, out[4];
        int ni = 0, nf = 0, first = nbufs;
        for (a += 2; a < argc && strcmp(argv[a], "call") && strcmp(argv[a], "dump") && strcmp(argv[a], "poke"); a++) {
            const char *s = argv[a], *v = strchr(s, ':');
            if (!v) die("bad argument %s", s);
            v++;
            if (!strncmp(s, "d:", 2) || !strncmp(s, "f:", 2)) {
                if (nf == 8) die("too many fp args");
                double x = strtod(v, NULL); float f = (float)x; uint64_t bits = 0;
                if (*s == 'd') memcpy(&bits, &x, 8); else memcpy(&bits, &f, 4);
                fps[nf++] = bits; continue;
            }
            if (ni == 6) die("too many integer args (stack arguments unsupported)");
            if (!strncmp(s, "i:", 2)) ints[ni++] = num(v);
            else if (!strncmp(s, "ref:", 4)) ints[ni++] = expr(v);
            else if (!strncmp(s, "buf:", 4)) ints[ni++] = (uint64_t)bufs[newbuf(num(v), NULL, 0)].p;
            else if (!strncmp(s, "str:", 4)) ints[ni++] = (uint64_t)bufs[newbuf(strlen(v) + 1, v, strlen(v) + 1)].p;
            else if (!strncmp(s, "hex:", 4)) {
                size_t n = strlen(v) / 2; uint8_t tmp[4096];
                if (n > sizeof tmp) die("hex too long");
                for (size_t i = 0; i < n; i++) sscanf(v + 2 * i, "%2hhx", &tmp[i]);
                ints[ni++] = (uint64_t)bufs[newbuf(n, tmp, n)].p;
            } else die("bad argument %s", s);
        }
        fflush(stdout);
        xcall(fn, ints, fps, out);
        rets[ncalls] = out[0];
        printf("call %d 0x%lx rax=0x%lx rdx=0x%lx xmm0=0x%lx xmm1=0x%lx\n", ncalls++, fn, out[0], out[1], out[2], out[3]);
        for (int k = first; k < nbufs; k++) { printf("out b%d 0x%lx ", k, (uint64_t)bufs[k].p); hexout(bufs[k].p, bufs[k].n); printf("\n"); }
        fflush(stdout);
    }
    for (int i = 0; i < nstubs; i++)
        if (stubs[i].uses) printf("used %s %ld\n", stubs[i].name, stubs[i].uses);
    return 0;
}
