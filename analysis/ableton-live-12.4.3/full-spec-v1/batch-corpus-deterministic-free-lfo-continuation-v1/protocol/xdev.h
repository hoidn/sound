/* xdev: load the x86_64 slice of a Live device bundle (MH_BUNDLE) and drive its seven C exports.
 * Adapted from tools/xexec/xexec.c (which loads Live itself at its preferred base).
 * Differences: the bundle's image base is 0, so it is mapped at a fixed slide; the slice is
 * picked out of the universal file; unbound imports point into a PROT_NONE guard region, so a
 * call *or* a data read through one faults and is reported as "TRAP <symbol>"; the bundle's
 * __mod_init_func initializers run after binding, as dyld would run them.
 * Single-threaded. Dependencies: glibc, libm, libstdc++ (only __dynamic_cast and the
 * Itanium type_info vtables). */
#ifndef XDEV_H
#define XDEV_H
#include <stdint.h>
#include <stddef.h>

#define XDEV_SLIDE ((uint64_t)0x200000000)     /* image VA = XDEV_SLIDE + Mach-O vmaddr */

/* Loader (xdev_load.c). */
void xdev_load(const char *universal_path);     /* maps, rebases, binds, runs initializers */
uint64_t xdev_symbol(const char *name);         /* defined external symbol -> loaded address, 0 if absent */
uint64_t xdev_slice_offset(void), xdev_slice_size(void);
void xdev_print_imports(void);                  /* "import linux|data|trap SYMBOL slots=N" */
void xdev_print_used(void);                     /* "used SYMBOL N" for every bound code import called */
void xdev_install_fault_handler(void);

/* Bindings (xdev_bind.c): Mach-O symbol -> host address, or NULL to leave it trapped.
 * *is_data is set for data symbols (bound to the address itself, not through a counting stub). */
void *xdev_binding(const char *sym, int *is_data);

/* libc++ shim (xdev_cxx.c): returns the shim for a libc++ symbol, or NULL. */
void *xdev_cxx_binding(const char *sym, int *is_data);
extern long xdev_cxx_failbits;                  /* stream extractions that set failbit (reported) */

#endif
