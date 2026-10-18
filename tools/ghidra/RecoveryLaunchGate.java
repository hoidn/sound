// Analyst-only machine attestation gate. Every launch starts -noanalysis.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.util.headless.HeadlessScript;
import ghidra.util.SystemUtilities;
import ghidra.framework.Application;
import java.lang.management.ManagementFactory;
import java.nio.file.*;

public class RecoveryLaunchGate extends HeadlessScript {
    @Override public void run()throws Exception {
        enableHeadlessAnalysis(false);
        setHeadlessContinuationOption(HeadlessContinuationOption.ABORT);
        JsonObject c=RecoverySupport.config(getScriptArgs());RecoverySupport.verifyProgram(c,currentProgram);
        RecoverySupport.require(RecoverySupport.str(c,"nonce").equals(System.getProperty("sound.recovery.nonce")),"JVM nonce mismatch");
        RecoverySupport.require(Runtime.getRuntime().availableProcessors()==2,"Available processors mismatch");
        RecoverySupport.require(SystemUtilities.getDefaultThreadPoolSize()==2,"Default pool mismatch");
        RecoverySupport.require("2".equals(System.getProperty("cpu.core.override"))&&"2".equals(System.getProperty("cpu.core.limit")),"CPU properties mismatch");
        RecoverySupport.require(Runtime.getRuntime().maxMemory()==4294967296L,"Maximum heap mismatch");
        for(String key:new String[]{"home","tmp","jdk"}){
            String property=key.equals("home")?"user.home":key.equals("tmp")?"java.io.tmpdir":"java.home";
            RecoverySupport.require(RecoverySupport.str(c,key).equals(System.getProperty(property)),"Effective "+property+" mismatch");
        }
        RecoverySupport.require(System.getProperty("java.version").equals("21.0.12.1"),"JDK version mismatch");
        ProcessHandle self=ProcessHandle.current();long started=self.info().startInstant().orElseThrow().toEpochMilli();
        String executable=self.info().command().orElseThrow();
        RecoverySupport.require(Path.of(executable).toRealPath().equals(Path.of(RecoverySupport.str(c,"jdk"),"bin","java").toRealPath()),"JVM executable mismatch");
        JsonObject gate=RecoverySupport.lineage(c);gate.addProperty("status","pass");gate.addProperty("pid",self.pid());gate.addProperty("start_ms",started);
        gate.addProperty("created_ms",System.currentTimeMillis());gate.addProperty("executable",executable);gate.addProperty("java_home",System.getProperty("java.home"));
        gate.addProperty("java_version",System.getProperty("java.version"));gate.addProperty("ghidra_version",Application.getApplicationVersion());
        gate.addProperty("program_sha256",currentProgram.getExecutableSHA256());gate.addProperty("program_name",currentProgram.getName());
        gate.addProperty("language",currentProgram.getLanguageID().toString());gate.addProperty("compiler",currentProgram.getCompilerSpec().getCompilerSpecID().toString());
        gate.addProperty("image_base",currentProgram.getImageBase().toString());gate.addProperty("processors",Runtime.getRuntime().availableProcessors());
        gate.addProperty("default_pool",SystemUtilities.getDefaultThreadPoolSize());gate.addProperty("max_heap",Runtime.getRuntime().maxMemory());
        gate.addProperty("home",System.getProperty("user.home"));gate.addProperty("tmp",System.getProperty("java.io.tmpdir"));
        gate.add("jvm_arguments",new Gson().toJsonTree(ManagementFactory.getRuntimeMXBean().getInputArguments()));
        Path gatePath=Path.of(RecoverySupport.str(c,"gate")),ackPath=Path.of(RecoverySupport.str(c,"ack"));RecoverySupport.write(gatePath,gate);
        long deadline=System.nanoTime()+10_000_000_000L;
        while(!Files.exists(ackPath)){monitor.checkCancelled();if(System.nanoTime()>=deadline)throw new IllegalStateException("Machine acknowledgment deadline");Thread.sleep(25);}
        RecoverySupport.require(System.nanoTime()<deadline,"Late acknowledgment");JsonObject ack=RecoverySupport.read(ackPath);RecoverySupport.bind(ack,c);
        RecoverySupport.require(RecoverySupport.str(ack,"status").equals("pass")&&RecoverySupport.str(ack,"gate_sha256").equals(RecoverySupport.sha(gatePath)),"Ack report hash/status mismatch");
        RecoverySupport.require(RecoverySupport.integer(ack,"pid")==self.pid()&&RecoverySupport.integer(ack,"start_ms")==started,"Ack JVM identity mismatch");
        long created=RecoverySupport.integer(ack,"created_ms");RecoverySupport.require(created>=gate.get("created_ms").getAsLong()&&created<=System.currentTimeMillis(),"Stale/future acknowledgment");
        String mode=RecoverySupport.str(c,"mode");RecoverySupport.require(mode.equals("verify-only")||mode.equals("enable-analysis-after-ack"),"Unknown mode");
        boolean enabled=mode.equals("enable-analysis-after-ack");if(enabled)enableHeadlessAnalysis(true);
        JsonObject complete=RecoverySupport.lineage(c);complete.addProperty("status","pass");complete.addProperty("pid",self.pid());complete.addProperty("start_ms",started);
        complete.addProperty("gate_sha256",RecoverySupport.sha(gatePath));complete.addProperty("ack_sha256",RecoverySupport.sha(ackPath));complete.addProperty("mode",mode);complete.addProperty("analysis_enabled",enabled);
        RecoverySupport.write(Path.of(RecoverySupport.str(c,"complete")),complete);storeHeadlessValue("sound.recovery.complete",complete);
        setHeadlessContinuationOption(HeadlessContinuationOption.CONTINUE);println("RECOVERY_GATE_COMPLETE "+RecoverySupport.str(c,"nonce"));
    }
}
