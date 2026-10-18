# Source to run analyzeHeadless in the e-rea scratch area (6 CPUs, isolated Ghidra home).
S=/var/tmp/sound-analysis/scratch/e-rea
GHIDRA=$HOME/.local/opt/ghidra_12.1.4_PUBLIC
export JAVA_HOME=$HOME/.local/opt/jdk-21.0.12.1+1
unset JAVA_TOOL_OPTIONS _JAVA_OPTIONS GHIDRA_JAVA_OPTIONS
export PATH=$JAVA_HOME/bin:/usr/bin:/bin
export XDG_CONFIG_HOME=$S/ghidra-home/config XDG_CACHE_HOME=$S/ghidra-home/cache
export GHIDRA_HEADLESS_MAXMEM=8G
export GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$S/ghidra-home -Djava.io.tmpdir=$S/tmp -XX:ParallelGCThreads=4"
