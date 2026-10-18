// Analyst-only. Disable analysis BEFORE recording the timed pass outcome.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.util.headless.HeadlessScript;
import java.nio.file.*;

public class RecoveryAnalysisOutcome extends HeadlessScript {
    @Override public void run()throws Exception {
        enableHeadlessAnalysis(false);
        setHeadlessContinuationOption(HeadlessContinuationOption.ABORT);
        boolean timeout=analysisTimeoutOccurred();JsonObject c=RecoverySupport.config(getScriptArgs());
        RecoverySupport.verifyProgram(c,currentProgram);JsonObject complete=RecoverySupport.completed(c);
        RecoverySupport.require(getStoredHeadlessValue("sound.recovery.complete") instanceof JsonObject,"Successful gate storage missing");
        JsonObject out=RecoverySupport.lineage(c);out.addProperty("status","pass");out.addProperty("pid",complete.get("pid").getAsLong());out.addProperty("start_ms",complete.get("start_ms").getAsLong());
        out.addProperty("gate_sha256",complete.get("gate_sha256").getAsString());out.addProperty("complete_sha256",RecoverySupport.sha(Path.of(RecoverySupport.str(c,"complete"))));
        out.addProperty("timeout",timeout);out.addProperty("analysis_enabled",false);out.addProperty("function_count",currentProgram.getFunctionManager().getFunctionCount());
        JsonArray issues=new JsonArray();issues.add("stdout.txt");issues.add("stderr.txt");issues.add("application.log");out.add("issues_retained_in",issues);
        out.addProperty("profile_sha256",RecoverySupport.str(c,"profile_sha256"));out.addProperty("checkpoint_sha256",RecoverySupport.str(c,"checkpoint_sha256"));
        if(c.get("fixture").getAsBoolean()){
            out.addProperty("fixture_setup_marker",currentProgram.getOptions("SoundRecoveryFixture").getString("setup",""));
            out.addProperty("fixture_timeout_marker",currentProgram.getOptions("SoundRecoveryFixture").getString("timeout",""));
            out.addProperty("fixture_counter_marker",currentProgram.getOptions("SoundRecoveryFixture").getString("counter",""));
        }
        RecoverySupport.write(Path.of(RecoverySupport.str(c,"outcome")),out);setHeadlessContinuationOption(HeadlessContinuationOption.CONTINUE);
        println("RECOVERY_OUTCOME_COMPLETE "+RecoverySupport.str(c,"nonce")+" timeout="+timeout);
    }
}
