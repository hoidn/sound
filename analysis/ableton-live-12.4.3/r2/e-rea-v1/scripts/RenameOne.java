// Scratch helper: make one saved edit (writable-session hardlink probe).
import ghidra.app.script.GhidraScript;
import ghidra.program.model.symbol.SourceType;
public class RenameOne extends GhidraScript {
    @Override public void run() throws Exception { getFunctionAt(toAddr(0x100005058L)).setName("probe_renamed", SourceType.USER_DEFINED); }
}
