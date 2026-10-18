// Independently authored fixture-only mutations. Never available for Live bytes.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.util.headless.HeadlessScript;
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.program.model.address.*;
import ghidra.program.model.symbol.SourceType;

public class RecoveryFixtureSetup extends HeadlessScript {
    @Override public void run()throws Exception {
        JsonObject c=RecoverySupport.config(getScriptArgs());RecoverySupport.fixture(c,currentProgram);RecoverySupport.completed(c);
        int transaction=currentProgram.startTransaction("Independent fixture setup");boolean commit=false;
        try{
            Address start=currentProgram.getMinAddress();AddressSet body=new AddressSet(start,start.addNoWrap(7));
            DisassembleCommand command=new DisassembleCommand(start,body,true);command.enableCodeAnalysis(false);
            RecoverySupport.require(command.applyTo(currentProgram,monitor),"Fixture disassembly failed");
            if(currentProgram.getFunctionManager().getFunctionAt(start)==null)currentProgram.getFunctionManager().createFunction("fixture_constant_zero",start,body,SourceType.USER_DEFINED);
            currentProgram.getOptions("SoundRecoveryFixture").setString("setup",RecoverySupport.str(c,"nonce"));commit=true;
        }finally{currentProgram.endTransaction(transaction,commit);}
        println("RECOVERY_FIXTURE_SETUP_COMPLETE");
    }
}
