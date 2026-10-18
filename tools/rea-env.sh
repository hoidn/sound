# Analyst-only: source before running `rea` on the Linux workstation.
# Node 24 runs the Node 22-installed REA 6.5.0 so its SQLite inspector works (needs >=24.15).
# Hopper is found through ~/.local/share/rea/hopper -> /var/tmp/sound-tools/hopper-6.4.2-demo.
T=/var/tmp/sound-tools
export PATH=$T/node-v24.22.0-linux-x64/bin:$HOME/.nvm/versions/node/v22.23.2/bin:$PATH
export JAVA_HOME=$HOME/.local/opt/jdk-21.0.12.1+1
export GHIDRA_INSTALL_DIR=$HOME/.local/opt/ghidra_12.1.4_PUBLIC
export REA_RIZIN_COMMAND=$T/rizin-v0.9.1/bin/rizin
