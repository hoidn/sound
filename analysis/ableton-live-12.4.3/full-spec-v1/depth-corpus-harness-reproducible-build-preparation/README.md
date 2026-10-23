# Exclusive own-harness build preparation

Preparation only. As of author freeze, independent peer and Root preflight remain pending. Current disposition must be read through their separate reviews. Root must separately select any execution; this packet does not authorize itself through its CLI flag.

The proposed single top-level `/usr/bin/gcc` invocation compiles the four exact retained C sources with the historical flags and absolute source paths, from the historical t12 working directory. Its only compiler output is `xdev-rebuilt` inside a new exclusive destination. The historical `xdev` is never overwritten, and neither new nor old output is executed. Installed compiler metadata was read from filesystem bytes/path resolution only; no compiler version or other tool was invoked.

`plan.json` carries the exact argv, environment and limits. `inputs.json` pins five source providers, the recipe/manifest, historical binary, compiler path/real file and reviewed provenance context. The complete build recipe is carried from the reviewed query; the full five C bodies were not freshly reread. Normal compiler descendants are possible and not individually enumerated or hermetically pinned. One direct compiler attempt, PID after successful spawn, exit, stdout/stderr, and paired old-file maps are separate records. Timeout kills its process group and waits without retry.

Whole output bytes and hash are compared, including debug content, against the exact 149,632-byte historical binary. A mismatch remains unresolved; no normalization, ELF interpretation, section editing or retry is selected. Matching bytes would support this finite source/recipe/compiler-environment-to-file observation. It would not recover the historical build event or independently prove runtime import precedence, allocator success/usable extent, object bounds or Live compatibility.

`python3 -B check.py --check` performs read-only pin, AST and seven unsafe-scope controls; it evaluates only the new pure command/argument guard functions. It never imports or runs the collector, compiler or output. The future `build-once.py --build-selected` is for a later separately selected run only.

Root's outer coordinator must retain its own attempt/exception/exit and preservation receipt. Failures before destination creation, catastrophic inner filesystem I/O, or interruption can prevent inner receipts. Recorded old-file maps do not monitor the entire machine or all temporary compiler effects. All existing cases, 174 historical modal omissions, two note72 omissions and behavior grades remain unchanged.
