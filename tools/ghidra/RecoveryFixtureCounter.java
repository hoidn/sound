// Fixture-only: queue after disabling analysis and prove no untimed postpass.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.util.headless.HeadlessScript;
import ghidra.app.services.*;
import ghidra.app.plugin.core.analysis.AutoAnalysisManager;
import ghidra.app.util.importer.MessageLog;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.Program;
import ghidra.util.task.TaskMonitor;

public class RecoveryFixtureCounter extends HeadlessScript {
    @Override public void run()throws Exception {
        enableHeadlessAnalysis(false);JsonObject c=RecoverySupport.config(getScriptArgs());RecoverySupport.fixture(c,currentProgram);RecoverySupport.completed(c);
        AbstractAnalyzer analyzer=new AbstractAnalyzer("Sound forbidden postpass counter","Independent post-script queue probe",AnalyzerType.BYTE_ANALYZER){
            {setPriority(AnalysisPriority.HIGHEST_PRIORITY);setSupportsOneTimeAnalysis();}
            @Override public boolean added(Program program,AddressSetView set,TaskMonitor monitor,MessageLog log){program.getOptions("SoundRecoveryFixture").setString("counter","EXECUTED");return true;}
        };
        AutoAnalysisManager.getAnalysisManager(currentProgram).scheduleOneTimeAnalysis(analyzer,currentProgram.getMemory());println("RECOVERY_COUNTER_QUEUED_AFTER_DISABLE");
    }
}
