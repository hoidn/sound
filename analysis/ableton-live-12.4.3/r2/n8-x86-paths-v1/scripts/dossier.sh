#!/bin/sh
# usage: dossier.sh <out-dir> <query>...   One-shot read-only R2FunctionDossier on the Live x86_64 project
# (r2-query-route.md step 4), with the helper directory's own XDG and Java temp settings.
set -eu
H=/var/tmp/sound-analysis/helpers/Live_x86_64
export JAVA_HOME=$HOME/.local/opt/jdk-21.0.12.1+1 PATH=$HOME/.local/opt/jdk-21.0.12.1+1/bin:/usr/bin:/bin
export XDG_CONFIG_HOME=$H/home/config XDG_CACHE_HOME=$H/home/cache GHIDRA_HEADLESS_MAXMEM=24G
export GHIDRA_HEADLESS_JAVA_OPTIONS="-Duser.home=$H/home -Djava.io.tmpdir=$H/tmp"
out=$1; shift
test ! -e "$out"
exec $HOME/.local/opt/ghidra_12.1.4_PUBLIC/support/analyzeHeadless $H/project H \
  -process Live_x86_64.x86_64 -noanalysis -readOnly -max-cpu 4 \
  -scriptPath /home/ollie/Documents/sound/tools/ghidra \
  -postScript R2FunctionDossier.java "$out" "$@"
