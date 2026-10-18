// Scratch helper: hold the opened program for N seconds (lock/concurrency probe).
import ghidra.app.script.GhidraScript;
public class HoldProgram extends GhidraScript {
    @Override public void run() throws Exception { Thread.sleep(Long.parseLong(getScriptArgs()[0]) * 1000); println("held " + currentProgram.getName()); }
}
