// Analyst-only selected-entry exporter; original program bytes are never written.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.util.headless.HeadlessScript;
import ghidra.util.SystemUtilities;
import java.lang.management.ManagementFactory;
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.app.decompiler.*;
import ghidra.framework.Application;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.symbol.SourceType;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class CorpusX86SelectedExport extends HeadlessScript {
    private final Gson gson = new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create();
    private Path output;
    private JsonObject config;

    @Override public void run() throws Exception {
        enableHeadlessAnalysis(false);
        setHeadlessContinuationOption(HeadlessContinuationOption.ABORT);
        String[] args=getScriptArgs();
        if(args.length!=2) throw new IllegalArgumentException("Expected config and output paths");
        config=JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonObject();
        output=Path.of(args[1]);
        if(!"corpus-x86-two-entry-noanalysis-v1".equals(config.get("profile").getAsString()) ||
           !"x86_64".equals(config.get("architecture").getAsString()) ||
           !"x86:LE:64:default".equals(currentProgram.getLanguageID().toString()) ||
           !"gcc".equals(currentProgram.getCompilerSpec().getCompilerSpecID().toString()) ||
           currentProgram.getImageBase().getOffset()!=0)
            throw new IllegalArgumentException("Exact x86 language/compiler/base profile required");
        if(config.get("auto_analysis").getAsBoolean() || config.get("incremental_code_analysis").getAsBoolean())
            throw new IllegalArgumentException("Automatic analysis forbidden");
        if(!"21.0.12.1".equals(System.getProperty("java.version")) ||
           Runtime.getRuntime().maxMemory()!=4294967296L || Runtime.getRuntime().availableProcessors()!=2 ||
           SystemUtilities.getDefaultThreadPoolSize()!=2 ||
           !"2".equals(System.getProperty("cpu.core.override")) || !"2".equals(System.getProperty("cpu.core.limit")))
            throw new IllegalArgumentException("Effective JDK/4GiB heap/CPU2 identity mismatch");
        if(!config.get("target_sha256").getAsString().equalsIgnoreCase(currentProgram.getExecutableSHA256()))
            throw new IllegalArgumentException("Imported target SHA-256 mismatch");
        if(!config.get("ghidra_version").getAsString().equals(Application.getApplicationVersion()))
            throw new IllegalArgumentException("Ghidra version mismatch");
        JsonArray seeds=config.getAsJsonArray("seeds");
        if(seeds.size()!=2 || !"0x23b0".equals(seeds.get(0).getAsJsonObject().get("address").getAsString()) ||
           !"0x29c0".equals(seeds.get(1).getAsJsonObject().get("address").getAsString()))
            throw new IllegalArgumentException("Only the two fixed unique ordered entries are selected");
        for(JsonElement item:seeds) if(item.getAsJsonObject().get("window_bytes").getAsInt()!=1024)
            throw new IllegalArgumentException("Only fixed 1024-byte windows are selected");
        Map<String,Object> identity=new LinkedHashMap<>();
        identity.put("program",currentProgram.getName());identity.put("executable_sha256",currentProgram.getExecutableSHA256());
        identity.put("language",currentProgram.getLanguageID().toString());identity.put("compiler",currentProgram.getCompilerSpec().getCompilerSpecID().toString());
        identity.put("image_base",currentProgram.getImageBase().toString());identity.put("ghidra_version",Application.getApplicationVersion());
        identity.put("java_version",System.getProperty("java.version"));identity.put("java_home",System.getProperty("java.home"));
        identity.put("max_heap",Runtime.getRuntime().maxMemory());identity.put("processors",Runtime.getRuntime().availableProcessors());
        identity.put("default_pool",SystemUtilities.getDefaultThreadPoolSize());identity.put("pid",ProcessHandle.current().pid());
        identity.put("start_ms",ProcessHandle.current().info().startInstant().orElseThrow().toEpochMilli());
        identity.put("executable",ProcessHandle.current().info().command().orElseThrow());
        identity.put("user_home",System.getProperty("user.home"));identity.put("tmp",System.getProperty("java.io.tmpdir"));
        identity.put("jvm_arguments",ManagementFactory.getRuntimeMXBean().getInputArguments());
        identity.put("auto_analysis",false);identity.put("whole_program_available_to_decompiler",true);
        if(!config.get("jdk").getAsString().equals(System.getProperty("java.home")) ||
           !config.get("user_home").getAsString().equals(System.getProperty("user.home")) ||
           !config.get("tmp").getAsString().equals(System.getProperty("java.io.tmpdir")))
            throw new IllegalArgumentException("Effective private JDK/home/tmp mismatch");
        write(output.resolve("actual-identity.json"),gson.toJson(identity)+"\n");
        Files.createDirectory(output.resolve("functions"));
        for(JsonElement item:seeds) {monitor.checkCancelled();exportSeed(item.getAsJsonObject());}
        setHeadlessContinuationOption(HeadlessContinuationOption.CONTINUE);
    }

    private void exportSeed(JsonObject seed) throws Exception {
        String spelling=seed.get("address").getAsString();
        if(!spelling.matches("0x[0-9a-f]+")) throw new IllegalArgumentException("Canonical default-space seed required");
        Address entry=toAddr(spelling);int bytes=seed.get("window_bytes").getAsInt();
        if(bytes!=1024 || (entry.getOffset()!=0x23b0L && entry.getOffset()!=0x29c0L))
            throw new IllegalArgumentException("Invalid fixed byte-based x86 window");
        Address end=entry.addNoWrap(bytes-1);AddressSet window=new AddressSet(entry,end);
        Path stage=Files.createTempDirectory(output,"staging-"), finalPath=output.resolve("functions").resolve(spelling);
        Map<String,Object> meta=new LinkedHashMap<>();
        meta.put("schema",1);meta.put("provider","ghidra-headless-selected-script");
        meta.put("profile",config.get("profile").getAsString());meta.put("target_sha256",config.get("target_sha256").getAsString());
        meta.put("method_sha256",config.get("method_sha256").getAsString());meta.put("ghidra_version",Application.getApplicationVersion());
        meta.put("address",spelling);meta.put("seed",seed);meta.put("window_end",end.toString());
        meta.put("auto_analysis",false);meta.put("incremental_code_analysis",false);meta.put("decompile_timeout_seconds",60);
        meta.put("state","failed");meta.put("partial_code",false);meta.put("body_ranges",new ArrayList<>());
        List<String> warnings=new ArrayList<>();meta.put("warnings",warnings);
        meta.put("limitations",List.of("Selected entry only; no whole-image analyzed inventory.",
            "Function body and types are recovered within a restricted no-analysis context.",
            "Direct calls may name unanalyzed targets; runtime behavior is not established.",
            "Whole imported thin Program data/signatures are available to the decompiler; not a byte-read sandbox."));
        DecompInterface decompiler=null;
        try {
            MemoryBlock block=currentProgram.getMemory().getBlock(entry);
            if(block==null || !block.isExecute() || !block.isInitialized() || !block.contains(end))
                throw new IllegalArgumentException("Window must fit an initialized executable block");
            FunctionManager fm=currentProgram.getFunctionManager();Function existing=fm.getFunctionAt(entry);
            if(existing!=null && existing.isExternal())throw new IllegalArgumentException("External seed excluded");
            meta.put("imported_name",existing==null?null:existing.getName());
            DisassembleCommand disassemble=new DisassembleCommand(entry,window,true);
            disassemble.enableCodeAnalysis(false);
            if(!disassemble.applyTo(currentProgram,monitor))throw new IllegalStateException("Disassembly failed: "+disassemble.getStatusMsg());
            AddressSetView body=CreateFunctionCmd.getFunctionBody(currentProgram,entry,monitor);
            if(body.isEmpty() || !body.contains(entry) || !window.contains(body) || body.contains(end))
                throw new IllegalStateException("Body missing entry, outside window, or touching window boundary");
            Iterator<Function> overlapping=fm.getFunctionsOverlapping(body);
            while(overlapping.hasNext()) {
                Function other=overlapping.next();
                if(!other.getEntryPoint().equals(entry))throw new IllegalStateException("Body overlaps another imported function: "+other.getEntryPoint());
            }
            List<Map<String,String>> ranges=new ArrayList<>();
            for(AddressRange range:body.getAddressRanges())ranges.add(Map.of("start","0x"+Long.toUnsignedString(range.getMinAddress().getOffset(),16),"end","0x"+Long.toUnsignedString(range.getMaxAddress().getOffset(),16)));
            meta.put("body_ranges",ranges);meta.put("body_bytes",body.getNumAddresses());
            StringBuilder assembly=new StringBuilder();List<String> problems=new ArrayList<>();int count=0;
            for(Instruction instruction:currentProgram.getListing().getInstructions(body,true)) {
                monitor.checkCancelled();count++;
                assembly.append("0x").append(Long.toUnsignedString(instruction.getAddress().getOffset(),16)).append(": ").append(instruction).append('\n');
                if(!body.contains(instruction.getMinAddress(),instruction.getMaxAddress()))problems.add("Partial instruction body");
                if(instruction.getFlowType().isComputed() && instruction.getFlowType().isJump())problems.add("Unresolved computed transfer at "+instruction.getAddress());
                if(!instruction.getFlowType().isCall())for(Address destination:instruction.getFlows())
                    if(!body.contains(destination))problems.add("Non-call transfer outside recovered body: "+destination);
                Address fall=instruction.getFallThrough();
                if(fall!=null && !body.contains(fall))problems.add("Fallthrough outside recovered body: "+fall);
            }
            write(stage.resolve("assembly.txt"),assembly.toString());meta.put("instruction_count",count);
            if(count==0 || !problems.isEmpty())throw new IllegalStateException("Incomplete/ambiguous body: "+problems);
            Function function=existing;
            if(function==null)function=fm.createFunction(null,entry,body,SourceType.DEFAULT);
            else function.setBody(body);
            decompiler=new DecompInterface();decompiler.toggleCCode(true);decompiler.toggleSyntaxTree(true);
            if(!decompiler.openProgram(currentProgram))throw new IllegalStateException("Decompiler open failed: "+decompiler.getLastMessage());
            DecompileResults result=decompiler.decompileFunction(function,60,monitor);
            meta.put("completed",result.decompileCompleted());meta.put("timed_out",result.isTimedOut());
            meta.put("cancelled",result.isCancelled());meta.put("failed_to_start",result.failedToStart());
            String diagnostic=result.getErrorMessage();if(diagnostic!=null&&!diagnostic.isBlank())warnings.add(diagnostic);
            DecompiledFunction decompiled=result.getDecompiledFunction();String code=decompiled==null?null:decompiled.getC();
            if(code!=null&&!code.isEmpty()) {
                write(stage.resolve("pseudocode.c"),code);
                for(String line:code.split("\\R"))if(line.toUpperCase(Locale.ROOT).contains("WARNING"))warnings.add(line.trim());
            }
            if(!result.decompileCompleted() || code==null || code.isEmpty())throw new IllegalStateException("Decompiler failed, timed out, or returned no code");
            meta.put("signature",function.getSignature().toString());meta.put("state",warnings.isEmpty()?"exported":"exported-with-warnings");
        } catch(Exception failure) {
            meta.put("partial_code",Files.isRegularFile(stage.resolve("pseudocode.c")));
            meta.put("error",failure.getClass().getSimpleName()+": "+failure.getMessage());
        } finally {
            if(decompiler!=null)decompiler.dispose();
            write(stage.resolve("metadata.json"),gson.toJson(meta)+"\n");
            Files.move(stage,finalPath,StandardCopyOption.ATOMIC_MOVE);
            println("Selected export "+spelling+": "+meta.get("state"));
        }
    }
    private void write(Path path,String content) throws Exception {
        Files.writeString(path,content,StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW);
    }
}
