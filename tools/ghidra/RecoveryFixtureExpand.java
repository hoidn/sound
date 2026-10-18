// Fixture-only extra independently authored return functions and external symbol.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.util.headless.HeadlessScript;
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.program.model.address.*;
import ghidra.program.model.symbol.SourceType;

public class RecoveryFixtureExpand extends HeadlessScript {
    @Override public void run()throws Exception {
        JsonObject c=RecoverySupport.config(getScriptArgs());RecoverySupport.fixture(c,currentProgram);RecoverySupport.completed(c);
        int tx=currentProgram.startTransaction("Independent five-function fixture");boolean commit=false;
        try{
            byte[] bytes=new byte[]{0,0,(byte)0x80,0x52,(byte)0xc0,3,0x5f,(byte)0xd6};
            for(int i=1;i<=4;i++){
                Address start=currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(i*16);AddressSet body=new AddressSet(start,start.addNoWrap(7));
                currentProgram.getMemory().createInitializedBlock("fixture_return_"+i,start,8,(byte)0,monitor,false).setExecute(true);currentProgram.getMemory().setBytes(start,bytes);
                DisassembleCommand command=new DisassembleCommand(start,body,true);command.enableCodeAnalysis(false);RecoverySupport.require(command.applyTo(currentProgram,monitor),"Fixture disassembly failed");
                currentProgram.getFunctionManager().createFunction("fixture_constant_zero_"+i,start,body,SourceType.USER_DEFINED);
            }
            currentProgram.getExternalManager().addExtFunction("fixtureLibrary","fixtureExternal",null,SourceType.USER_DEFINED);
            currentProgram.getOptions("SoundRecoveryFixture").setString("expanded",RecoverySupport.str(c,"nonce"));commit=true;
        }finally{currentProgram.endTransaction(tx,commit);}
        println("RECOVERY_FIXTURE_EXPAND_COMPLETE");
    }
}
