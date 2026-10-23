/* xdev_cxx.c: the libc++ (std::__1, x86_64 macOS ABI) members that the device bundles import,
 * reimplemented in C on the same object layouts. The bundles use them only to build module
 * descriptions in string streams and to save and reload engine state through them.
 * Layouts (checked against the bundles' inline code): std::string uses the standard layout
 * (bit 0 of byte 0 = long; short size = byte 0 >> 1, text at +1; long = {alloc|1, size, data});
 * ios_base fields at fmtflags +8, precision +16, width +24, rdstate +32, exceptions +36,
 * rdbuf +40, locale +48; basic_ios tie +136, fill +144; basic_streambuf pointers eback..epptr at
 * +16..+56 and virtual slots underflow 0x48, uflow 0x50, pbackfail 0x58, xsputn 0x60,
 * overflow 0x68, seekoff 0x20, seekpos 0x28, sync 0x30; the virtual base offset of a stream is
 * at vptr[-3]. Semantics follow libc++: num_put formats a double with "%.*g" (precision from the
 * stream) in the C locale, num_get parses base-10 integers with strtoll/strtoull and sets
 * failbit on no digits or overflow. Exceptions are never thrown: any path that would throw
 * traps. Only the C locale exists. XDEV_TRACE_OSTREAM=1 prints each float insertion (precision, text) to stderr. */
#define _GNU_SOURCE
#include "xdev.h"
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

long xdev_cxx_failbits;
static void trap(const char *why) { fflush(stdout); fprintf(stderr, "TRAP %s\n", why); _exit(86); }

/* ---- std::string --------------------------------------------------------------------- */
typedef uint8_t str;    /* 24-byte object */
static int s_long(const str *s) { return s[0] & 1; }
static uint64_t *w(const str *s) { return (uint64_t *)s; }
static size_t s_size(const str *s) { return s_long(s) ? w(s)[1] : (size_t)(s[0] >> 1); }
static char *s_data(str *s) { return s_long(s) ? (char *)w(s)[2] : (char *)s + 1; }
static size_t s_cap(const str *s) { return s_long(s) ? (w(s)[0] & ~1ULL) - 1 : 22; }
static void s_setsize(str *s, size_t n) { if (s_long(s)) w(s)[1] = n; else s[0] = (uint8_t)(n << 1); s_data(s)[n] = 0; }
static void s_init(str *s) { memset(s, 0, 24); }
static void s_grow(str *s, size_t need)            /* capacity >= need; keeps content */
{
    if (need <= s_cap(s)) return;
    size_t alloc = (need + 1 + 15) & ~(size_t)15, n = s_size(s);
    char *p = malloc(alloc);
    memcpy(p, s_data(s), n + 1);
    if (s_long(s)) free(s_data(s));
    w(s)[0] = alloc | 1; w(s)[1] = n; w(s)[2] = (uint64_t)p;
}
static void s_assign(str *s, const char *t, size_t n)
{
    char *tmp = malloc(n + 1); memcpy(tmp, t, n); tmp[n] = 0;   /* t may alias s */
    s_grow(s, n); memcpy(s_data(s), tmp, n + 1); s_setsize(s, n); free(tmp);
}
static void s_append(str *s, const char *t, size_t n)
{
    size_t m = s_size(s);
    if (m + n > s_cap(s)) s_grow(s, m + n > 2 * s_cap(s) ? m + n : 2 * s_cap(s));
    memmove(s_data(s) + m, t, n); s_setsize(s, m + n);
}
static int str_compare(const str *s, size_t pos, size_t n1, const char *t, size_t n2)
{
    size_t sz = s_size(s);
    if (pos > sz) trap("std::string::compare out_of_range");
    size_t r = sz - pos < n1 ? sz - pos : n1;
    int c = memcmp(s_data((str *)s) + pos, t, r < n2 ? r : n2);
    return c ? c : r < n2 ? -1 : r > n2 ? 1 : 0;
}
static str *str_append(str *s, const char *t) { s_append(s, t, strlen(t)); return s; }
static str *str_assign(str *s, const char *t) { s_assign(s, t, strlen(t)); return s; }
static void str_resize(str *s, size_t n, char c)
{
    size_t m = s_size(s);
    if (n > m) { s_grow(s, n); memset(s_data(s) + m, c, n - m); }
    s_setsize(s, n);
}
static void str_reserve(str *s, size_t n) { s_grow(s, n); }
static void str_push_back(str *s, char c) { s_append(s, &c, 1); }
static void str_copy(str *d, const str *s) { s_init(d); s_assign(d, s_data((str *)s), s_size(s)); }
static str *str_operator_eq(str *d, const str *s) { if (d != s) s_assign(d, s_data((str *)s), s_size(s)); return d; }
static void str_dtor(str *s) { if (s_long(s)) free(s_data(s)); }

/* ---- locale and ctype<char> ---------------------------------------------------------- */
static char ctype_id[16];                  /* stands for std::ctype<char>::id */
static long locale_imp;                    /* the one locale object */
static void *ctype_vt[11];
static struct { void **vt; long owners; const uint32_t *tab; long del; } ctype_facet = { ctype_vt + 0, 0, 0, 0 };
static char ct_id(void *f, char c) { (void)f; return c; }
static const char *ct_range(void *f, char *lo, const char *hi) { (void)f; (void)lo; return hi; }
static const char *ct_widen_r(void *f, const char *lo, const char *hi, char *to) { (void)f; memcpy(to, lo, hi - lo); return hi; }
static char ct_narrow(void *f, char c, char d) { (void)f; (void)d; return c; }
static const char *ct_narrow_r(void *f, const char *lo, const char *hi, char d, char *to) { (void)f; (void)d; memcpy(to, lo, hi - lo); return hi; }
static void ct_trap(void) { trap("ctype<char> destructor"); }
static void **loc_getloc(void **ret, void *ios) { (void)ios; *ret = &locale_imp; return ret; }
/* The classic table is _DefaultRuneLocale.__runetype (offset 60), as in libc++ on Apple. */
static const uint32_t *ctype_table(void)
{
    if (!ctype_facet.tab) {
        int data;
        ctype_facet.tab = (const uint32_t *)((char *)xdev_binding("__DefaultRuneLocale", &data) + 60);
        void *v[11] = { ct_trap, ct_trap, ct_trap, ct_id, ct_range, ct_id, ct_range, ct_id, ct_widen_r, ct_narrow, ct_narrow_r };
        memcpy(ctype_vt, v, sizeof v);
    }
    return ctype_facet.tab;
}
static void *loc_use_facet(void *loc, void *id)
{
    (void)loc;
    if (id != ctype_id) trap("locale::use_facet for a facet other than ctype<char>");
    ctype_table();
    return &ctype_facet;
}
static void noop(void) {}

/* ---- ios_base ------------------------------------------------------------------------- */
typedef struct {
    void **vt; uint32_t flags, pad; long precision, width; uint32_t rdstate, exceptions;
    void *rdbuf, *loc, *fn, *index; size_t ev[2]; void *ia; size_t ian[2]; void *pa; size_t pan[2];
    void *tie; int fill;
} ios_t;
_Static_assert(__builtin_offsetof(ios_t, rdbuf) == 40 && __builtin_offsetof(ios_t, tie) == 136
               && __builtin_offsetof(ios_t, fill) == 144, "libc++ ios layout");
enum { goodbit = 0, badbit = 1, eofbit = 2, failbit = 4, skipws = 0x1000, dec = 2, basefield = 0x4a,
       left = 0x20, internal = 0x10, adjustfield = 0xb0, showpos = 0x800, showpoint = 0x400,
       uppercase = 0x4000, fixed = 4, scientific = 0x100, boolalpha = 1 };
static void ios_init(ios_t *b, void *sb)
{
    memset((char *)b + 8, 0, 128);                 /* the caller has already set the vptr */
    b->rdbuf = sb; b->rdstate = sb ? goodbit : badbit; b->flags = skipws | dec; b->precision = 6;
    b->loc = &locale_imp;
}
static void ios_clear(ios_t *b, unsigned st)
{
    b->rdstate = b->rdbuf ? st : st | badbit;
    if (b->rdstate & b->exceptions) trap("ios_base::clear would throw");
}
static void ios_setstate(ios_t *b, unsigned st) { ios_clear(b, b->rdstate | st); }
static void ios_set_badbit(ios_t *b) { b->rdstate |= badbit; if (b->exceptions & badbit) trap("badbit rethrow"); }
static ios_t *ios_of(void *stream) { return (ios_t *)((char *)stream + (*(long **)stream)[-3]); }

/* ---- basic_streambuf<char> ------------------------------------------------------------ */
typedef struct { char st[128]; long off; } fpos;
typedef struct sb { void **vt; void *loc; char *binp, *ninp, *einp, *bout, *nout, *eout; } sb;
#define VF(o, off, T) ((T)((*(void ***)(o))[(off) / 8]))
static int sb_underflow(sb *b) { return VF(b, 0x48, int (*)(sb *))(b); }
static int sb_uflow_v(sb *b) { return VF(b, 0x50, int (*)(sb *))(b); }
static int sb_pbackfail(sb *b, int c) { return VF(b, 0x58, int (*)(sb *, int))(b, c); }
static long sb_xsputn_v(sb *b, const char *s, long n) { return VF(b, 0x60, long (*)(sb *, const char *, long))(b, s, n); }
static int sb_overflow(sb *b, int c) { return VF(b, 0x68, int (*)(sb *, int))(b, c); }
static int sb_sync_v(sb *b) { return VF(b, 0x30, int (*)(sb *))(b); }
static int sgetc(sb *b) { return b->ninp == b->einp ? sb_underflow(b) : (uint8_t)*b->ninp; }
static int sbumpc(sb *b) { return b->ninp == b->einp ? sb_uflow_v(b) : (uint8_t)*b->ninp++; }
static int sputc(sb *b, char c) { if (b->nout == b->eout) return sb_overflow(b, (uint8_t)c); *b->nout++ = c; return (uint8_t)c; }

static void *sb_trap_vt[16];
static void sb_trap(void) { trap("basic_streambuf base vtable called"); }
static void sb_ctor(sb *b)
{
    for (int i = 0; i < 16; i++) sb_trap_vt[i] = sb_trap;
    memset(b, 0, sizeof *b); b->vt = sb_trap_vt; b->loc = &locale_imp;
}
static void sb_imbue(sb *b, void *loc) { (void)b; (void)loc; }
static sb *sb_setbuf(sb *b, char *s, long n) { (void)s; (void)n; return b; }
static int sb_sync(sb *b) { (void)b; return 0; }
static long sb_showmanyc(sb *b) { (void)b; return 0; }
static long sb_xsgetn(sb *b, char *s, long n)
{
    long i = 0; int c;
    while (i < n) {
        if (b->ninp < b->einp) {
            long k = b->einp - b->ninp < n - i ? b->einp - b->ninp : n - i;
            memcpy(s + i, b->ninp, k); b->ninp += k; i += k;
        } else if ((c = sb_uflow_v(b)) != EOF) s[i++] = (char)c;
        else break;
    }
    return i;
}
static int sb_uflow(sb *b) { if (sb_underflow(b) == EOF) return EOF; return (uint8_t)*b->ninp++; }
static long sb_xsputn(sb *b, const char *s, long n)
{
    long i = 0;
    while (i < n) {
        if (b->nout < b->eout) {
            long k = b->eout - b->nout < n - i ? b->eout - b->nout : n - i;
            memcpy(b->nout, s + i, k); b->nout += k; i += k;
        } else if (sb_overflow(b, (uint8_t)s[i]) == EOF) break;
        else i++;
    }
    return i;
}

/* ---- basic_istream<char> -------------------------------------------------------------- */
typedef struct { void **vt; long gc; } istream_t;
static void isentry(uint8_t *ok, istream_t *is, int noskipws)
{
    ios_t *b = ios_of(is);
    *ok = 0;
    if (b->rdstate) { ios_setstate(b, failbit); return; }
    if (b->tie) trap("istream sentry with a tied stream");
    if (!noskipws && (b->flags & skipws)) {
        int c;
        while ((c = sgetc(b->rdbuf)) != EOF && c < 128 && (ctype_table()[c] & 0x4000)) sbumpc(b->rdbuf);
        if (c == EOF) ios_setstate(b, failbit | eofbit);
    }
    *ok = b->rdstate == 0;
}
static int is_get(istream_t *is)
{
    uint8_t ok; int r = EOF; ios_t *b = ios_of(is);
    is->gc = 0;
    isentry(&ok, is, 1);
    if (ok) { r = sbumpc(b->rdbuf); if (r == EOF) ios_setstate(b, failbit | eofbit); else is->gc = 1; }
    return r;
}
static istream_t *is_putback(istream_t *is, char c)
{
    uint8_t ok; ios_t *b = ios_of(is); sb *s = b->rdbuf;
    is->gc = 0; ios_clear(b, b->rdstate & ~eofbit);
    isentry(&ok, is, 1);
    if (!ok) { ios_setstate(b, failbit); return is; }
    int r = (s->binp == s->ninp || c != s->ninp[-1]) ? sb_pbackfail(s, (uint8_t)c) : (uint8_t)*--s->ninp;
    if (r == EOF) ios_setstate(b, badbit);
    return is;
}
static istream_t *is_unget(istream_t *is)
{
    uint8_t ok; ios_t *b = ios_of(is); sb *s = b->rdbuf;
    is->gc = 0; ios_clear(b, b->rdstate & ~eofbit);
    isentry(&ok, is, 1);
    if (!ok) { ios_setstate(b, failbit); return is; }
    int r = s->binp == s->ninp ? sb_pbackfail(s, EOF) : (uint8_t)*--s->ninp;
    if (r == EOF) ios_setstate(b, badbit);
    return is;
}
static fpos is_tellg(istream_t *is)
{
    uint8_t ok; fpos r; memset(&r, 0, sizeof r); r.off = -1;
    isentry(&ok, is, 1);
    if (ok) r = VF(ios_of(is)->rdbuf, 0x20, fpos (*)(void *, long, int, unsigned))(ios_of(is)->rdbuf, 0, 1, 8);
    return r;
}
static istream_t *is_seekg(istream_t *is, fpos pos)
{
    uint8_t ok; ios_t *b = ios_of(is);
    ios_clear(b, b->rdstate & ~eofbit);
    isentry(&ok, is, 1);
    if (ok && VF(b->rdbuf, 0x28, fpos (*)(void *, fpos, unsigned))(b->rdbuf, pos, 8).off == -1) ios_setstate(b, failbit);
    return is;
}
/* num_get stage 2 for base 10: optional leading sign, then digits; returns chars read. */
static int scan_int(istream_t *is, char *buf, unsigned *st)
{
    uint8_t ok; ios_t *b = ios_of(is); int n = 0, c;
    if ((b->flags & basefield) != dec) trap("istream integer extraction in a base other than 10");
    isentry(&ok, is, 0);
    if (!ok) return -1;
    while ((c = sgetc(b->rdbuf)) != EOF && n < 63) {
        if (!((n == 0 && (c == '+' || c == '-')) || (c >= '0' && c <= '9'))) break;
        buf[n++] = (char)c; sbumpc(b->rdbuf);
    }
    buf[n] = 0;
    if (c == EOF) *st |= eofbit;
    return n;
}
static istream_t *is_get_int(istream_t *is, int *v)
{
    char buf[64], *e; unsigned st = 0; int n = scan_int(is, buf, &st);
    if (n < 0) return is;
    errno = 0; long long x = strtoll(buf, &e, 10);
    if (n == 0 || *e) { st |= failbit; *v = 0; }
    else if (errno == ERANGE || x < INT_MIN || x > INT_MAX) { st |= failbit; *v = x > 0 ? INT_MAX : INT_MIN; }
    else *v = (int)x;
    if (st & failbit) xdev_cxx_failbits++;
    if (st) ios_setstate(ios_of(is), st);
    return is;
}
static istream_t *is_get_uint(istream_t *is, unsigned *v)
{
    char buf[64], *e, *p = buf; unsigned st = 0; int n = scan_int(is, buf, &st), neg = buf[0] == '-';
    if (n < 0) return is;
    if (neg) p++;
    errno = 0; unsigned long long x = strtoull(p, &e, 10);
    if (n == 0 || !*p || *e) { st |= failbit; *v = 0; }
    else if (errno == ERANGE || x > UINT_MAX) { st |= failbit; *v = UINT_MAX; }
    else *v = neg ? (unsigned)-(unsigned)x : (unsigned)x;
    if (st & failbit) xdev_cxx_failbits++;
    if (st) ios_setstate(ios_of(is), st);
    return is;
}

/* ---- basic_ostream<char> -------------------------------------------------------------- */
typedef struct { uint8_t ok; void *os; } osentry_t;
static void osentry(osentry_t *s, void *os)
{
    ios_t *b = ios_of(os);
    s->ok = 0; s->os = os;
    if (b->rdstate == 0) { if (b->tie) trap("ostream sentry with a tied stream"); s->ok = 1; }
}
static void osentry_dtor(osentry_t *s)
{
    ios_t *b = ios_of(s->os);
    if (b->rdbuf && b->rdstate == 0 && (b->flags & 0x2000) && sb_sync_v(b->rdbuf) == -1) ios_setstate(b, badbit);
}
/* __pad_and_output: pad to width with fill at the position given by adjustfield, width(0). */
static void put_padded(void *os, const char *t, int n)
{
    osentry_t s; ios_t *b = ios_of(os);
    osentry(&s, os);
    if (s.ok) {
        int fill = b->fill == EOF ? (b->fill = ' ') : b->fill, pad = b->width > n ? (int)b->width - n : 0, at = 0;
        if ((b->flags & adjustfield) == left) at = n;
        else if ((b->flags & adjustfield) == internal && n && (t[0] == '+' || t[0] == '-')) at = 1;
        char *o = malloc(n + pad);
        memcpy(o, t, at); memset(o + at, fill, pad); memcpy(o + at + pad, t + at, n - at);
        if (sb_xsputn_v(b->rdbuf, o, n + pad) != n + pad) ios_setstate(b, badbit | failbit);
        free(o);
        b->width = 0;
    }
    osentry_dtor(&s);
}
static void *os_put_long(void *os, long v)
{
    ios_t *b = ios_of(os); char t[32];
    if ((b->flags & basefield) != dec) trap("ostream integer insertion in a base other than 10");
    put_padded(os, t, snprintf(t, sizeof t, b->flags & showpos ? "%+ld" : "%ld", v));
    return os;
}
static void *os_int(void *os, int v) { return os_put_long(os, v); }
static void *os_ulong(void *os, unsigned long v)
{
    char t[32];
    if ((ios_of(os)->flags & basefield) != dec) trap("ostream integer insertion in a base other than 10");
    put_padded(os, t, snprintf(t, sizeof t, "%lu", v));
    return os;
}
static void *os_bool(void *os, int v)
{
    if (ios_of(os)->flags & boolalpha) { put_padded(os, (v & 1) ? "true" : "false", (v & 1) ? 4 : 5); return os; }
    return os_put_long(os, v & 1);
}
static void *os_double(void *os, double v);
static void *os_float(void *os, float v) { return os_double(os, v); }
static void *os_double(void *os, double v)
{
    ios_t *b = ios_of(os); char f[16], *p = f, t[512];
    unsigned ff = b->flags & (fixed | scientific);
    *p++ = '%';
    if (b->flags & showpos) *p++ = '+';
    if (b->flags & showpoint) *p++ = '#';
    if (ff != (fixed | scientific)) { *p++ = '.'; *p++ = '*'; }
    *p++ = ff == fixed ? 'f' : ff == scientific ? 'e' : ff ? 'a' : 'g';
    if (b->flags & uppercase) p[-1] -= 32;
    *p = 0;
    int n = ff == (fixed | scientific) ? snprintf(t, sizeof t, f, v) : snprintf(t, sizeof t, f, (int)b->precision, v);
    if (n >= (int)sizeof t) trap("ostream float text too long");
    if (getenv("XDEV_TRACE_OSTREAM")) fprintf(stderr, "ostream-float precision=%ld flags=%#x text=%s\n", b->precision, b->flags, t);
    put_padded(os, t, n);
    return os;
}
static void *os_put(void *os, char c)
{
    osentry_t s; ios_t *b = ios_of(os);
    osentry(&s, os);
    if (s.ok && sputc(b->rdbuf, c) == EOF) ios_setstate(b, badbit);
    osentry_dtor(&s);
    return os;
}
static void *os_flush(void *os)
{
    ios_t *b = ios_of(os);
    if (b->rdbuf) {
        osentry_t s; osentry(&s, os);
        if (s.ok && sb_sync_v(b->rdbuf) == -1) ios_setstate(b, badbit);
        osentry_dtor(&s);
    }
    return os;
}

/* ---- symbol table ------------------------------------------------------------------- */
#define NS "__ZNSt3__1"
#define STR "12basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE"
#define IS "13basic_istreamIcNS_11char_traitsIcEEE"
#define OS "13basic_ostreamIcNS_11char_traitsIcEEE"
#define IOS "14basic_iostreamIcNS_11char_traitsIcEEE"
#define SB "15basic_streambufIcNS_11char_traitsIcEEE"
static void d0_trap(void) { trap("deleting destructor of a libc++ stream base"); }
static const struct { const char *sym; void *fn; int data; } table[] = {
    {"__ZNKSt3__1" STR "7compareEmmPKcm", str_compare}, {NS STR "6appendEPKc", str_append},
    {NS STR "6assignEPKc", str_assign}, {NS STR "6resizeEmc", str_resize}, {NS STR "7reserveEm", str_reserve},
    {NS STR "9push_backEc", str_push_back}, {NS STR "C1ERKS5_", str_copy}, {NS STR "aSERKS5_", str_operator_eq},
    {NS STR "D1Ev", str_dtor},
    {"__ZNKSt3__18ios_base6getlocEv", loc_getloc}, {"__ZNKSt3__16locale9use_facetERNS0_2idE", loc_use_facet},
    {"__ZNSt3__16localeD1Ev", noop}, {"__ZNSt3__15ctypeIcE2idE", ctype_id, 1},
    {"__ZNSt3__18ios_base4initEPv", ios_init}, {"__ZNSt3__18ios_base5clearEj", ios_clear},
    {"__ZNSt3__18ios_base33__set_badbit_and_consider_rethrowEv", ios_set_badbit},
    {"__ZNSt3__19basic_iosIcNS_11char_traitsIcEEED2Ev", noop},
    {NS SB "C2Ev", sb_ctor}, {NS SB "D2Ev", noop}, {NS SB "4syncEv", sb_sync}, {NS SB "5imbueERKNS_6localeE", sb_imbue},
    {NS SB "5uflowEv", sb_uflow}, {NS SB "6setbufEPcl", sb_setbuf}, {NS SB "6xsgetnEPcl", sb_xsgetn},
    {NS SB "6xsputnEPKcl", sb_xsputn}, {NS SB "9showmanycEv", sb_showmanyc},
    {NS IS "3getEv", is_get}, {NS IS "5seekgENS_4fposI11__mbstate_tEE", is_seekg}, {NS IS "5tellgEv", is_tellg},
    {NS IS "5ungetEv", is_unget}, {NS IS "6sentryC1ERS3_b", isentry}, {NS IS "7putbackEc", is_putback},
    {NS IS "rsERi", is_get_int}, {NS IS "rsERj", is_get_uint},
    {NS IS "D1Ev", noop}, {NS IS "D2Ev", noop}, {NS IS "D0Ev", d0_trap},
    {NS OS "3putEc", os_put}, {NS OS "5flushEv", os_flush}, {NS OS "6sentryC1ERS3_", osentry},
    {NS OS "6sentryD1Ev", osentry_dtor}, {NS OS "lsEb", os_bool}, {NS OS "lsEf", os_float}, {NS OS "lsEd", os_double}, {NS OS "lsEi", os_int}, {NS OS "lsEm", os_ulong},
    {NS OS "D1Ev", noop}, {NS OS "D0Ev", d0_trap},
    {NS IOS "D1Ev", noop}, {NS IOS "D2Ev", noop}, {NS IOS "D0Ev", d0_trap},
    {"__ZThn16_NSt3__1" IOS "D1Ev", noop}, {"__ZThn16_NSt3__1" IOS "D0Ev", d0_trap},
    {"__ZTv0_n24_NSt3__1" IS "D1Ev", noop}, {"__ZTv0_n24_NSt3__1" IS "D0Ev", d0_trap},
    {"__ZTv0_n24_NSt3__1" OS "D1Ev", noop}, {"__ZTv0_n24_NSt3__1" OS "D0Ev", d0_trap},
    {"__ZTv0_n24_NSt3__1" IOS "D1Ev", noop}, {"__ZTv0_n24_NSt3__1" IOS "D0Ev", d0_trap},
};

void *xdev_cxx_binding(const char *sym, int *is_data)
{
    for (size_t i = 0; i < sizeof table / sizeof *table; i++)
        if (!strcmp(sym, table[i].sym)) { *is_data = table[i].data; return table[i].fn; }
    return NULL;
}
