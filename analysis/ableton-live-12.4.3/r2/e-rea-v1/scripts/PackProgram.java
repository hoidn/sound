// Scratch helper: pack the opened program to a .gzf (option c measurement).
import ghidra.app.script.GhidraScript;
import java.io.File;
public class PackProgram extends GhidraScript {
    @Override public void run() throws Exception { currentProgram.getDomainFile().packFile(new File(getScriptArgs()[0]), monitor); }
}
