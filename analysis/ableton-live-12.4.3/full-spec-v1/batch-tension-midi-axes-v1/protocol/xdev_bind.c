/* xdev_bind.c: which macOS import gets which Linux definition. Each binding keeps the contract
 * the call site relies on. Anything not listed stays trapped (see xdev_load.c).
 * Substitutions that can change numbers (libm, rand, time) are listed in the evidence README. */
#define _GNU_SOURCE
#include "xdev.h"
#include <dlfcn.h>
#include <locale.h>
#include <math.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

static void say(const char *m) { if (write(2, m, strlen(m)) < 0) _exit(88); }

static long guard_value = 0x2f8a6b1c4d3e5f71;
__attribute__((noreturn)) static void x_stack_chk_fail(void) { say("TRAP ___stack_chk_fail (stack smashed)\n"); _exit(86); }
static void *x_new(size_t n) { void *p = malloc(n ? n : 1); if (!p) { say("xdev: operator new failed\n"); _exit(2); } return p; }
static void x_delete(void *p) { free(p); }
static void x_bzero(void *p, size_t n) { memset(p, 0, n); }
static int x_atexit(void *f, void *a, void *d) { (void)f; (void)a; (void)d; return 0; }  /* destructors never run */
/* macOS memset_pattern16(b, pattern16, len): repeat the 16-byte pattern, last copy truncated. */
static void x_memset_pattern16(void *b, const void *pat, size_t n)
{ for (size_t i = 0; i < n; i += 16) memcpy((char *)b + i, pat, n - i < 16 ? n - i : 16); }
/* macOS newlocale(mask, "C" or NULL, base) gives the C locale; masks differ from glibc's. */
static locale_t x_newlocale(int mask, const char *name, locale_t base)
{
    if (name && strcmp(name, "C") && strcmp(name, "POSIX")) { say("TRAP _newlocale (non-C locale)\n"); _exit(86); }
    (void)mask; (void)base; return newlocale(LC_ALL_MASK, "C", 0);
}
/* Sensitivity test only: with XDEV_LIBM_ULP=+1 or -1 in the environment, every inexact libm result
 * (not floor, modf, ldexp, fabs, sqrt, which are exact everywhere) is moved one ulp up or down. */
static int ulp_dir;
/* Integer-valued results (expf(0) = 1, logf(1) = 0, powf(2, 3) = 8, ...) are exact in any libm that
 * returns exact cases exactly, so they are never perturbed (change for the Tension packet; the
 * t12-device-dsp-v1 copy perturbs them too). */
static float pf(float r) { return ulp_dir && r != rintf(r) ? nextafterf(r, ulp_dir > 0 ? INFINITY : -INFINITY) : r; }
static double pd(double r) { return ulp_dir && r != rint(r) ? nextafter(r, ulp_dir > 0 ? INFINITY : -INFINITY) : r; }
#define WF(f) static float w_##f(float x) { return pf(f(x)); }
#define WD(f) static double w_##f(double x) { return pd(f(x)); }
WF(sinf) WF(cosf) WF(tanf) WF(atanf) WF(expf) WF(logf) WF(log10f) WF(exp2f) WF(tanhf)
WD(sin) WD(cos) WD(tan) WD(atan) WD(exp) WD(log) WD(log10) WD(exp2) WD(tanh) WD(cbrt)
static float w_powf(float x, float y) { return pf(powf(x, y)); }
static double w_pow(double x, double y) { return pd(pow(x, y)); }
static float w_atan2f(float y, float x) { return pf(atan2f(y, x)); }
static double w_atan2(double y, double x) { return pd(atan2(y, x)); }
static const struct { const char *name; void *fn; } perturbed[] = {
    {"sinf", w_sinf}, {"cosf", w_cosf}, {"tanf", w_tanf}, {"atanf", w_atanf}, {"expf", w_expf}, {"logf", w_logf},
    {"log10f", w_log10f}, {"exp2f", w_exp2f}, {"tanhf", w_tanhf}, {"sin", w_sin}, {"cos", w_cos}, {"tan", w_tan},
    {"atan", w_atan}, {"exp", w_exp}, {"log", w_log}, {"log10", w_log10}, {"exp2", w_exp2}, {"tanh", w_tanh},
    {"cbrt", w_cbrt}, {"powf", w_powf}, {"pow", w_pow}, {"atan2f", w_atan2f}, {"atan2", w_atan2} };

/* macOS __sincosf_stret(x) returns {sinf x, cosf x} packed in xmm0. */
typedef struct { float s, c; } sincos_pair;
static sincos_pair x_sincosf_stret(float x) { sincos_pair r; sincosf(x, &r.s, &r.c); r.s = pf(r.s); r.c = pf(r.c); return r; }
/* macOS __sincos_stret(x) returns {sin x, cos x} in xmm0 and xmm1. */
typedef struct { double s, c; } sincos_pair_d;
static sincos_pair_d x_sincos_stret(double x) { sincos_pair_d r; sincos(x, &r.s, &r.c); r.s = pd(r.s); r.c = pd(r.c); return r; }
static double x_exp10(double x) { return pd(exp10(x)); }
static float x_exp10f(float x) { return pf(exp10f(x)); }
__attribute__((noreturn)) static void x_exit(int c) { (void)c; say("TRAP _exit (the bundle called exit)\n"); _exit(86); }
/* macOS libc rand(): Park-Miller "minimal standard" generator, x' = 16807 x mod (2^31 - 1), as in
 * FreeBSD-derived libc (seed 0 replaced by 123459876). Inferred from that source lineage, not
 * read from Apple's binary. Every use is counted ("used _rand N"). */
static unsigned long rand_next = 1;
static int x_rand(void)
{
    long hi, lo, x;
    if (rand_next == 0) rand_next = 123459876;
    hi = rand_next / 127773; lo = rand_next % 127773;
    x = 16807 * lo - 2836 * hi;
    if (x < 0) x += 0x7fffffff;
    return (int)((rand_next = x) % 0x80000000UL);
}
static void x_srand(unsigned seed) { rand_next = seed; }
/* time() is fixed so that srand(time(0)) seeds identically in every run (Live seeds with the clock).
 * XDEV_TIME=N in the environment fixes it at N instead of 0 (seed-dependence test). */
static long x_time(long *t)
{
    long v = getenv("XDEV_TIME") ? atol(getenv("XDEV_TIME")) : 0;
    if (t) *t = v;
    return v;
}
/* macOS ctype: __maskrune(c, mask) for c outside 0..127; the C locale has no such classes. */
static unsigned long x_maskrune(int c, unsigned long mask) { (void)c; (void)mask; return 0; }

/* _DefaultRuneLocale: magic[8], encoding[32], two function pointers, invalid_rune (int32),
 * then __runetype[256] at offset 60, __maplower[256], __mapupper[256]. C-locale classes with
 * Apple's _CTYPE_* bits: A 0x100, C 0x200, D 0x400, G 0x800, L 0x1000, P 0x2000, S 0x4000,
 * U 0x8000, X 0x10000, B 0x20000, R 0x40000; printable characters also carry SW1 0x40000000. */
static struct __attribute__((packed)) {
    char magic[8], encoding[32]; void *sget, *sput; int32_t invalid; uint32_t runetype[256];
    int32_t maplower[256], mapupper[256];
} rune;
static void init_rune(void)
{
    memcpy(rune.magic, "RuneMagA", 8); strcpy(rune.encoding, "NONE"); rune.invalid = 0xfffd;
    for (int c = 0; c < 256; c++) {
        uint32_t m = 0;
        if (c < 128) {
            if (c < 32 || c == 127) m |= 0x200;
            if ((c >= 9 && c <= 13) || c == 32) m |= 0x4000;
            if (c == 9 || c == 32) m |= 0x20000;
            if (c >= 32 && c < 127) m |= 0x40000 | 0x40000000;
            if (c > 32 && c < 127) m |= 0x800;
            if (c >= '0' && c <= '9') m |= 0x400 | 0x10000 | (uint32_t)(c - '0');
            if (c >= 'A' && c <= 'Z') m |= 0x8000 | 0x100;
            if (c >= 'a' && c <= 'z') m |= 0x1000 | 0x100;
            if ((c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f')) m |= 0x10000 | (uint32_t)((c | 32) - 'a' + 10);
            if (c > 32 && c < 127 && !(m & (0x400 | 0x100))) m |= 0x2000;
        }
        rune.runetype[c] = m;
        rune.maplower[c] = (c >= 'A' && c <= 'Z') ? c + 32 : c;
        rune.mapupper[c] = (c >= 'a' && c <= 'z') ? c - 32 : c;
    }
}

static const struct { const char *mach; void *addr; int data; } fixed[] = {
    {"_memcpy", memcpy}, {"_memmove", memmove}, {"_memset", memset}, {"_memcmp", memcmp},
    {"_bzero", x_bzero}, {"___bzero", x_bzero}, {"_memset_pattern16", x_memset_pattern16},
    {"_strlen", strlen}, {"_strcmp", strcmp}, {"_strncmp", strncmp}, {"_strcpy", strcpy}, {"_strdup", strdup},
    {"_malloc", malloc}, {"_calloc", calloc}, {"_realloc", realloc}, {"_free", free},
    {"__Znwm", x_new}, {"__Znam", x_new}, {"__ZdlPv", x_delete}, {"__ZdaPv", x_delete},
    {"___cxa_atexit", x_atexit},
    {"_atof", atof}, {"_atoi", atoi}, {"_sscanf", sscanf}, {"_sprintf", sprintf},
    {"_fprintf", fprintf}, {"_fwrite", fwrite},
    {"_newlocale", x_newlocale}, {"_uselocale", uselocale}, {"_freelocale", freelocale},
    {"___sincosf_stret", x_sincosf_stret}, {"___sincos_stret", x_sincos_stret}, {"___exp10", x_exp10},
    {"___exp10f", x_exp10f}, {"_div", div}, {"_exit", x_exit}, {"_rand", x_rand}, {"_srand", x_srand}, {"_time", x_time},
    {"___maskrune", x_maskrune},
    {"___stack_chk_guard", &guard_value, 1}, {"___stack_chk_fail", x_stack_chk_fail},
    {"___stderrp", &stderr, 1}, {"__DefaultRuneLocale", &rune, 1},
};
static const char *libm[] = {
    "atanf", "cbrt", "cos", "cosf", "exp", "expf", "floorf", "ldexpf", "logf", "log", "modf", "modff",
    "sin", "sinf", "tanf", "tan", "pow", "powf", "sqrt", "sqrtf", "floor", "ceil", "ceilf", "fmod",
    "fmodf", "log10", "log10f", "exp2f", "exp2", "atan", "atan2", "atan2f", "tanh", "tanhf", "ldexp", NULL };

/* Itanium RTTI: libstdc++ implements the same ABI (type_info layouts, __dynamic_cast). */
static void *libstdcxx(const char *sym, int *is_data)
{
    static const char *code[] = { "___dynamic_cast", NULL };
    static const char *data[] = { "__ZTVN10__cxxabiv117__class_type_infoE", "__ZTVN10__cxxabiv120__si_class_type_infoE",
                                  "__ZTVN10__cxxabiv121__vmi_class_type_infoE", NULL };
    static void *h;
    for (int d = 0; d < 2; d++)
        for (const char **n = d ? data : code; *n; n++)
            if (!strcmp(sym, *n)) {
                if (!h && !(h = dlopen("libstdc++.so.6", RTLD_NOW))) { say("xdev: dlopen libstdc++\n"); _exit(2); }
                *is_data = d;
                return dlsym(h, sym + 1);
            }
    return NULL;
}

/* Sensitivity test only: XDEV_LIBM_ONLY=name[,name...] restricts the XDEV_LIBM_ULP perturbation to the
 * listed functions (names without the leading underscore: expf, exp, __exp10f, __sincosf_stret, ...). */
static int perturb_this(const char *name)
{
    const char *only = getenv("XDEV_LIBM_ONLY");
    if (!only) return 1;
    size_t n = strlen(name);
    for (const char *p = only; (p = strstr(p, name)); p += n)
        if ((p == only || p[-1] == ',') && (p[n] == 0 || p[n] == ',')) return 1;
    return 0;
}
static sincos_pair p_sincosf_stret(float x) { sincos_pair r; sincosf(x, &r.s, &r.c); return r; }
static sincos_pair_d p_sincos_stret(double x) { sincos_pair_d r; sincos(x, &r.s, &r.c); return r; }
static double p_exp10(double x) { return exp10(x); }
static float p_exp10f(float x) { return exp10f(x); }

void *xdev_binding(const char *sym, int *is_data)
{
    static int ready;
    if (!ready) { init_rune(); ready = 1; }
    void *r = libstdcxx(sym, is_data);
    if (r) return r;
    if (getenv("XDEV_LIBM_ONLY") && !perturb_this(sym + 1)) {
        static const struct { const char *mach; void *addr; } plain[] = {
            {"___sincosf_stret", p_sincosf_stret}, {"___sincos_stret", p_sincos_stret}, {"___exp10", p_exp10}, {"___exp10f", p_exp10f} };
        for (size_t i = 0; i < sizeof plain / sizeof *plain; i++)
            if (!strcmp(sym, plain[i].mach)) { *is_data = 0; return plain[i].addr; }
    }
    for (size_t i = 0; i < sizeof fixed / sizeof *fixed; i++)
        if (!strcmp(sym, fixed[i].mach)) { *is_data = fixed[i].data; return fixed[i].addr; }
    if (getenv("XDEV_LIBM_ULP")) ulp_dir = atoi(getenv("XDEV_LIBM_ULP"));
    for (size_t i = 0; ulp_dir && i < sizeof perturbed / sizeof *perturbed; i++)
        if (sym[0] == '_' && !strcmp(sym + 1, perturbed[i].name) && perturb_this(perturbed[i].name)) return perturbed[i].fn;
    for (int i = 0; libm[i]; i++)
        if (sym[0] == '_' && !strcmp(sym + 1, libm[i])) {
            static void *h;
            if (!h && !(h = dlopen("libm.so.6", RTLD_NOW))) { say("xdev: dlopen libm\n"); _exit(2); }
            return dlsym(h, libm[i]);
        }
    return xdev_cxx_binding(sym, is_data);
}
