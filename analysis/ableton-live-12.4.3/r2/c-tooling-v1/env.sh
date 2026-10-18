# Source before running analyzeHeadless for C-tooling tests (scratch only).
S=/var/tmp/sound-analysis/scratch/c-tooling
export GHIDRA_INSTALL_DIR=$HOME/.local/opt/ghidra_12.1.4_PUBLIC
export JAVA_HOME=$HOME/.local/opt/jdk-21.0.12.1+1
unset JAVA_TOOL_OPTIONS _JAVA_OPTIONS GHIDRA_JAVA_OPTIONS
export PATH=$JAVA_HOME/bin:/usr/bin:/bin
export XDG_CONFIG_HOME=$S/home/config XDG_CACHE_HOME=$S/home/cache
export GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$S/home -Djava.io.tmpdir=$S/tmp -XX:ParallelGCThreads=4"
export GHIDRA_HEADLESS_MAXMEM=8G
