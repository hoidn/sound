// Analyst-only: summarize a saved program for the revision 2 reopen proof.
// Read-only; writes one JSON object to the path given as the first script argument.
// @category Sound.Analysis
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Function;
import ghidra.program.util.DefinedStringIterator;
import ghidra.program.util.GhidraProgramUtilities;
import java.nio.file.Files;
import java.nio.file.Path;

public class R2ProjectSummary extends GhidraScript {
    @Override
    public void run() throws Exception {
        long nonexternal = 0, thunks = 0, external = 0, strings = 0;
        for (Function f : currentProgram.getFunctionManager().getFunctions(true)) {
            monitor.checkCancelled();
            nonexternal++;
            if (f.isThunk()) thunks++;
        }
        for (Function f : currentProgram.getFunctionManager().getExternalFunctions()) external++;
        for (Data d : DefinedStringIterator.forProgram(currentProgram)) strings++;
        String json = String.format(
            "{\"program\":\"%s\",\"language\":\"%s\",\"compiler\":\"%s\",\"image_base\":\"%s\","
            + "\"executable_sha256\":\"%s\",\"analyzed\":%b,\"functions_nonexternal\":%d,"
            + "\"thunks\":%d,\"functions_external\":%d,\"defined_strings\":%d}%n",
            currentProgram.getName(), currentProgram.getLanguageID(),
            currentProgram.getCompilerSpec().getCompilerSpecID(), currentProgram.getImageBase(),
            currentProgram.getExecutableSHA256(), GhidraProgramUtilities.isAnalyzed(currentProgram),
            nonexternal, thunks, external, strings);
        Files.writeString(Path.of(getScriptArgs()[0]), json);
    }
}
