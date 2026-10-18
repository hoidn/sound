// Fixture-only cooperative cancellation injector; imported bytes never executed.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.util.headless.HeadlessScript;
import ghidra.app.services.*;
import ghidra.app.plugin.core.analysis.AutoAnalysisManager;
import ghidra.app.util.importer.MessageLog;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.Program;
import ghidra.util.task.TaskMonitor;
import ghidra.util.exception.CancelledException;

public class RecoveryFixtureTimeout extends HeadlessScript {
    @Override public void run()throws Exception {
        JsonObject c=RecoverySupport.config(getScriptArgs());RecoverySupport.fixture(c,currentProgram);RecoverySupport.completed(c);
        String nonce=RecoverySupport.str(c,"nonce");
        AbstractAnalyzer analyzer=new AbstractAnalyzer("Sound cooperative timeout fixture","Independent scheduler probe",AnalyzerType.BYTE_ANALYZER){
            {setPriority(AnalysisPriority.HIGHEST_PRIORITY);setSupportsOneTimeAnalysis();}
            @Override public boolean added(Program program,AddressSetView set,TaskMonitor monitor,MessageLog log)throws CancelledException {
                program.getOptions("SoundRecoveryFixture").setString("timeout",nonce);
                while(true){monitor.checkCancelled();try{Thread.sleep(10);}catch(InterruptedException e){Thread.currentThread().interrupt();throw new CancelledException();}}
            }
        };
        AutoAnalysisManager.getAnalysisManager(currentProgram).scheduleOneTimeAnalysis(analyzer,currentProgram.getMemory());println("RECOVERY_TIMEOUT_INJECTOR_QUEUED");
    }
}
