/* xdev_load.c: map the x86_64 slice of a universal Mach-O bundle at XDEV_SLIDE, apply its
 * LC_DYLD_INFO rebases (with the slide), binds and lazy binds (eagerly), and run its
 * __mod_init_func initializers. Adapted from tools/xexec/xexec.c; see xdev.h.
 * Bound code imports go through a counting stub ("used SYMBOL N"); bound data imports get the
 * host address itself; every unbound import gets its own 256-byte slot in a PROT_NONE guard
 * region, so the first call or read through it faults and the handler prints "TRAP <symbol>". */
#define _GNU_SOURCE
#include "xdev.h"
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <ucontext.h>
#include <unistd.h>

#define die(...) do { fprintf(stderr, "xdev: " __VA_ARGS__); fputc('\n', stderr); exit(2); } while (0)
#define MAXSYM 4096
#define GUARD_SLOT 256

typedef struct { char name[17]; uint64_t vmaddr, vmsize, fileoff, filesize; int prot; } seg_t;
static seg_t segs[16];
static int nsegs;
static uint8_t *file;                    /* the slice bytes */
static uint64_t slice_off, slice_size;
static const uint8_t *symtab_lc, *dysymtab_lc;

static struct { char *name; void *target; long slots, uses; int data; } stubs[MAXSYM];
static int nstubs;
static uint8_t *stub_code, *guard;

uint64_t xdev_slice_offset(void) { return slice_off; }
uint64_t xdev_slice_size(void) { return slice_size; }

static void say(const char *m) { if (write(2, m, strlen(m)) < 0) _exit(88); }

static uint64_t stub_for(const char *sym)
{
    int i;
    for (i = 0; i < nstubs && strcmp(stubs[i].name, sym); i++) ;
    if (i == nstubs) {
        if (nstubs == MAXSYM) die("too many imported symbols");
        int data = 0;
        void *t = xdev_binding(sym, &data);
        stubs[i].name = strdup(sym); stubs[i].target = t; stubs[i].data = data; nstubs++;
        if (t && !data) {                /* movabs r11,&uses; lock incq (r11); movabs r11,target; jmp r11 */
            uint8_t *c = stub_code + 32 * i;
            uint64_t u = (uint64_t)&stubs[i].uses, tt = (uint64_t)t;
            c[0] = 0x49; c[1] = 0xbb; memcpy(c + 2, &u, 8); c[10] = 0xf0; c[11] = 0x49; c[12] = 0xff; c[13] = 0x03;
            c[14] = 0x49; c[15] = 0xbb; memcpy(c + 16, &tt, 8); c[24] = 0x41; c[25] = 0xff; c[26] = 0xe3;
        }
    }
    stubs[i].slots++;
    if (!stubs[i].target) return (uint64_t)(guard + GUARD_SLOT * i);
    return stubs[i].data ? (uint64_t)stubs[i].target : (uint64_t)(stub_code + 32 * i);
}

static uint64_t uleb(const uint8_t **p)
{ uint64_t v = 0; int s = 0; uint8_t b; do { b = *(*p)++; v |= (uint64_t)(b & 0x7f) << s; s += 7; } while (b & 0x80); return v; }
static int64_t sleb(const uint8_t **p)
{ int64_t v = 0; int s = 0; uint8_t b; do { b = *(*p)++; v |= (int64_t)(b & 0x7f) << s; s += 7; } while (b & 0x80);
  if (s < 64 && (b & 0x40)) v |= -((int64_t)1 << s);
  return v; }

static uint64_t *at(int seg, uint64_t off) { return (uint64_t *)(XDEV_SLIDE + segs[seg].vmaddr + off); }

static void rebase(const uint8_t *p, const uint8_t *end)
{
    int seg = 0; uint64_t off = 0, n, skip;
    while (p < end) {
        uint8_t op = *p & 0xf0, imm = *p & 0x0f; p++;
        switch (op) {
        case 0x00: return;
        case 0x10: break;                                           /* SET_TYPE_IMM (pointer) */
        case 0x20: seg = imm; off = uleb(&p); break;
        case 0x30: off += uleb(&p); break;
        case 0x40: off += imm * 8; break;
        case 0x50: for (n = imm; n--; off += 8) *at(seg, off) += XDEV_SLIDE; break;
        case 0x60: for (n = uleb(&p); n--; off += 8) *at(seg, off) += XDEV_SLIDE; break;
        case 0x70: *at(seg, off) += XDEV_SLIDE; off += uleb(&p) + 8; break;
        case 0x80: n = uleb(&p); skip = uleb(&p);
                   for (; n--; off += 8 + skip) *at(seg, off) += XDEV_SLIDE;
                   break;
        default: die("rebase opcode 0x%x", op);
        }
    }
}

static void bind(const uint8_t *p, const uint8_t *end, int lazy)
{
    int seg = 0; uint64_t off = 0, n, skip; int64_t addend = 0; const char *sym = "";
    while (p < end) {
        uint8_t op = *p & 0xf0, imm = *p & 0x0f; p++;
        switch (op) {
        case 0x00: if (!lazy) return; break;
        case 0x10: case 0x30: break;                                /* dylib ordinal: lookup is by name */
        case 0x20: uleb(&p); break;
        case 0x40: sym = (const char *)p; p += strlen(sym) + 1; break;
        case 0x50: if (imm != 1) die("bind type %d", imm); break;
        case 0x60: addend = sleb(&p); break;
        case 0x70: seg = imm; off = uleb(&p); break;
        case 0x80: off += uleb(&p); break;
        case 0x90: *at(seg, off) = stub_for(sym) + addend; off += 8; break;
        case 0xa0: *at(seg, off) = stub_for(sym) + addend; off += uleb(&p) + 8; break;
        case 0xb0: *at(seg, off) = stub_for(sym) + addend; off += imm * 8 + 8; break;
        case 0xc0: n = uleb(&p); skip = uleb(&p);
                   for (; n--; off += 8 + skip) *at(seg, off) = stub_for(sym) + addend;
                   break;
        default: die("bind opcode 0x%x", op);
        }
    }
}

/* Pick the x86_64 slice out of a universal (fat) file, or accept a thin x86_64 file. */
static void find_slice(const uint8_t *f, uint64_t fsize)
{
    uint32_t magic = __builtin_bswap32(*(uint32_t *)f);
    if (magic != 0xcafebabe) { slice_off = 0; slice_size = fsize; return; }
    uint32_t n = __builtin_bswap32(*(uint32_t *)(f + 4));
    for (uint32_t i = 0; i < n; i++) {
        const uint32_t *a = (const uint32_t *)(f + 8 + 20 * i);
        if (__builtin_bswap32(a[0]) == 0x01000007) {
            slice_off = __builtin_bswap32(a[2]); slice_size = __builtin_bswap32(a[3]); return;
        }
    }
    die("no x86_64 slice");
}

/* The k-th section header (section_64) over all LC_SEGMENT_64 commands, or NULL past the end. */
static const uint8_t *section(uint32_t ncmds, int k)
{
    const uint8_t *lc = file + 32;
    for (uint32_t i = 0; i < ncmds; i++, lc += *(uint32_t *)(lc + 4)) {
        if (*(uint32_t *)lc != 0x19) continue;
        uint32_t nsect = *(uint32_t *)(lc + 64);
        if ((uint32_t)k < nsect) return lc + 72 + 80 * k;
        k -= nsect;
    }
    return NULL;
}

/* S_ZEROFILL (1) and S_GB_ZEROFILL (0xc) sections have no file bytes: clear them. */
static void zero_fill_sections(uint32_t ncmds)
{
    const uint8_t *sc;
    for (int k = 0; (sc = section(ncmds, k)); k++) {
        uint32_t type = *(uint32_t *)(sc + 64) & 0xff;
        if (type == 1 || type == 0xc)
            memset((void *)(XDEV_SLIDE + *(uint64_t *)(sc + 32)), 0, *(uint64_t *)(sc + 40));
    }
}

void xdev_load(const char *path)
{
    int fd = open(path, O_RDONLY); if (fd < 0) die("open %s", path);
    struct stat st; fstat(fd, &st);
    uint8_t *whole = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (whole == MAP_FAILED) die("mmap file");
    find_slice(whole, st.st_size);
    file = whole + slice_off;
    if (*(uint32_t *)file != 0xfeedfacf || *(int32_t *)(file + 4) != 0x01000007) die("not an x86_64 Mach-O");
    if (*(uint32_t *)(file + 12) != 8 && *(uint32_t *)(file + 12) != 6) die("not an MH_BUNDLE or MH_DYLIB");
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
        else if (cmd == 0x2) symtab_lc = lc;
        else if (cmd == 0xb) dysymtab_lc = lc;
        else if (cmd == 0x80000034) die("chained fixups not supported");
    }
    if (!dinfo || !symtab_lc) die("no LC_DYLD_INFO or LC_SYMTAB");
    for (int i = 0; i < nsegs; i++) {
        seg_t *s = &segs[i];
        if (!s->vmsize || !s->prot) continue;
        uint64_t va = XDEV_SLIDE + s->vmaddr, fsz = (s->filesize + 0xfff) & ~0xfffUL;
        if (mmap((void *)va, fsz, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_FIXED_NOREPLACE, fd,
                 slice_off + s->fileoff) != (void *)va) die("cannot map %s", s->name);
        if (s->vmsize > fsz && mmap((void *)(va + fsz), s->vmsize - fsz, PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED_NOREPLACE, -1, 0) != (void *)(va + fsz))
            die("cannot map zero fill of %s", s->name);
        /* the file's tail of the last page past filesize must read as zero (zerofill sections) */
        if (s->filesize < fsz) memset((void *)(va + s->filesize), 0, fsz - s->filesize);
        s->prot = (s->prot & 1 ? PROT_READ : 0) | (s->prot & 2 ? PROT_WRITE : 0) | (s->prot & 4 ? PROT_EXEC : 0);
    }
    zero_fill_sections(ncmds);
    const uint32_t *d = (const uint32_t *)(dinfo + 8);              /* rebase, bind, weak, lazy, export */
    stub_code = mmap(NULL, 32 * MAXSYM, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    guard = mmap(NULL, GUARD_SLOT * MAXSYM, PROT_NONE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_NORESERVE, -1, 0);
    if (stub_code == MAP_FAILED || guard == MAP_FAILED) die("mmap stubs");
    rebase(file + d[0], file + d[0] + d[1]);
    bind(file + d[2], file + d[2] + d[3], 0);
    bind(file + d[6], file + d[6] + d[7], 1);                         /* weak binds (d[4]) not applied */
    mprotect(stub_code, 32 * MAXSYM, PROT_READ | PROT_EXEC);
    for (int i = 0; i < nsegs; i++)
        if (segs[i].vmsize && segs[i].prot)
            mprotect((void *)(XDEV_SLIDE + segs[i].vmaddr), segs[i].vmsize, segs[i].prot);
    close(fd);
    /* Run __mod_init_func pointers (section type 9), in order, as dyld does for a loaded image. */
    const uint8_t *sc;
    for (int k = 0; (sc = section(ncmds, k)); k++) {
        if ((*(uint32_t *)(sc + 64) & 0xff) != 9) continue;
        uint64_t addr = *(uint64_t *)(sc + 32), size = *(uint64_t *)(sc + 40);
        for (uint64_t o = 0; o < size; o += 8) {
            void (*init)(void) = (void (*)(void))*(uint64_t *)(XDEV_SLIDE + addr + o);
            printf("init 0x%lx\n", (uint64_t)init - XDEV_SLIDE);
            fflush(stdout);
            init();
        }
    }
}

uint64_t xdev_symbol(const char *name)
{
    const uint32_t *s = (const uint32_t *)(symtab_lc + 8);       /* symoff, nsyms, stroff, strsize */
    for (uint32_t i = 0; i < s[1]; i++) {
        const uint8_t *nl = file + s[0] + 16 * i;
        uint8_t type = nl[4];
        if ((type & 0x0e) != 0x0e || !(type & 0x01)) continue;  /* N_SECT and N_EXT */
        if (!strcmp((const char *)file + s[2] + *(uint32_t *)nl, name))
            return XDEV_SLIDE + *(uint64_t *)(nl + 8);
    }
    return 0;
}

void xdev_print_imports(void)
{
    for (int i = 0; i < nstubs; i++)
        printf("import %s %s slots=%ld\n", !stubs[i].target ? "trap" : stubs[i].data ? "data" : "linux",
               stubs[i].name, stubs[i].slots);
}

void xdev_print_used(void)
{
    for (int i = 0; i < nstubs; i++)
        if (stubs[i].uses) printf("used %s %ld\n", stubs[i].name, stubs[i].uses);
}

static void fault(int sig, siginfo_t *si, void *ctx)
{
    ucontext_t *uc = ctx;
    uint64_t rip = uc->uc_mcontext.gregs[REG_RIP], a = (uint64_t)si->si_addr, g = (uint64_t)guard;
    uint64_t hit = (rip >= g && rip < g + GUARD_SLOT * MAXSYM) ? rip : (a >= g && a < g + GUARD_SLOT * MAXSYM) ? a : 0;
    fflush(stdout);
    if (hit) {
        say("TRAP "); say(stubs[(hit - g) / GUARD_SLOT].name);
        say(rip == hit ? " (call)\n" : " (data read)\n");
        _exit(86);
    }
    fprintf(stderr, "FAULT sig=%d addr=%p rip=0x%llx (image 0x%llx)\n", sig, si->si_addr,
            (unsigned long long)rip, (unsigned long long)(rip - XDEV_SLIDE));
    _exit(87);
}

void xdev_install_fault_handler(void)
{
    static uint8_t altstack[65536];
    stack_t ss = { .ss_sp = altstack, .ss_size = sizeof altstack };
    sigaltstack(&ss, NULL);
    struct sigaction sa = { .sa_sigaction = fault, .sa_flags = SA_SIGINFO | SA_ONSTACK };
    sigaction(SIGSEGV, &sa, NULL); sigaction(SIGBUS, &sa, NULL);
    sigaction(SIGILL, &sa, NULL); sigaction(SIGFPE, &sa, NULL);
}
