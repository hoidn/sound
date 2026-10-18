// Analyst-only, read-only exports of EXACT functions in this checkpoint.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.util.headless.HeadlessScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.Symbol;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class RecoveryNativeExport extends HeadlessScript {
    private JsonObject config;private Path output;private final Gson compact=new Gson();
    @Override public void run()throws Exception {
        enableHeadlessAnalysis(false);setHeadlessContinuationOption(HeadlessContinuationOption.ABORT);
        config=RecoverySupport.config(getScriptArgs());RecoverySupport.verifyProgram(config,currentProgram);RecoverySupport.completed(config);
        output=Path.of(RecoverySupport.str(config,"stage"));JsonObject outcome=RecoverySupport.read(Path.of(RecoverySupport.str(config,"outcome")));RecoverySupport.bind(outcome,config);
        String mode=RecoverySupport.str(config,"export_mode");
        if(mode.equals("inventory"))inventory(outcome);else if(mode.equals("functions"))functions(outcome);else throw new IOException("Unknown export mode");
        setHeadlessContinuationOption(HeadlessContinuationOption.CONTINUE);
    }
    private String offset(Address address){return "0x"+Long.toUnsignedString(address.getOffset(),16);}
    private String key(Address address){return address.getAddressSpace().getName()+":"+offset(address);}
    private JsonObject entry(Function fn){
        Address address=fn.getEntryPoint();JsonObject o=new JsonObject();o.addProperty("key",key(address));o.addProperty("entry_space",address.getAddressSpace().getName());o.addProperty("entry_offset",offset(address));
        o.addProperty("name",fn.getName());o.addProperty("external",fn.isExternal());o.addProperty("thunk",fn.isThunk());o.addProperty("body_bytes",fn.getBody().getNumAddresses());
        JsonArray ranges=new JsonArray();for(AddressRange range:fn.getBody().getAddressRanges()){
            JsonObject r=new JsonObject();r.addProperty("space",range.getMinAddress().getAddressSpace().getName());r.addProperty("start",offset(range.getMinAddress()));r.addProperty("end",offset(range.getMaxAddress()));ranges.add(r);
        }o.add("body_ranges",ranges);TreeSet<String> names=new TreeSet<>();for(Symbol symbol:currentProgram.getSymbolTable().getSymbols(address))names.add(symbol.getName(true));
        JsonArray aliases=new JsonArray();for(String name:names)aliases.add(name);o.add("aliases",aliases);return o;
    }
    private JsonObject summary(JsonObject outcome){
        JsonObject o=RecoverySupport.lineage(config);o.addProperty("status","pass");o.addProperty("profile_sha256",RecoverySupport.str(config,"profile_sha256"));
        o.addProperty("checkpoint_sha256",RecoverySupport.str(config,"checkpoint_sha256"));o.addProperty("outcome_sha256",RecoverySupport.shaQuiet(Path.of(RecoverySupport.str(config,"outcome"))));
        o.addProperty("partial",outcome.get("timeout").getAsBoolean()||config.get("checkpoint_partial").getAsBoolean());return o;
    }
    private void inventory(JsonObject outcome)throws Exception {
        Path payload=output.resolve("inventory.jsonl");int ordinary=0;Set<String> keys=new HashSet<>();
        try(BufferedWriter writer=Files.newBufferedWriter(payload,StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)){
            for(Function fn:currentProgram.getFunctionManager().getFunctions(true)){
                monitor.checkCancelled();JsonObject e=entry(fn);RecoverySupport.require(!fn.isExternal()&&keys.add(RecoverySupport.str(e,"key")),"Duplicate/external ordinary iterator");
                writer.write(compact.toJson(e));writer.newLine();ordinary++;
            }
            List<Function> externals=new ArrayList<>();for(Function fn:currentProgram.getFunctionManager().getExternalFunctions())externals.add(fn);
            externals.sort(Comparator.comparing(fn->key(fn.getEntryPoint())));
            for(Function fn:externals){monitor.checkCancelled();JsonObject e=entry(fn);RecoverySupport.require(fn.isExternal()&&keys.add(RecoverySupport.str(e,"key")),"Duplicate/nonexternal external iterator");writer.write(compact.toJson(e));writer.newLine();}
            RecoverySupport.require(ordinary+externals.size()==currentProgram.getFunctionManager().getFunctionCount(),"Iterator total mismatch");
            writer.flush();JsonObject sum=summary(outcome);sum.addProperty("ordinary",ordinary);sum.addProperty("external",externals.size());sum.addProperty("total",ordinary+externals.size());
            // Hash only after closing writer below.
            storeHeadlessValue("sound.recovery.inventory-summary",sum);
        }
        JsonObject sum=(JsonObject)getStoredHeadlessValue("sound.recovery.inventory-summary");sum.addProperty("payload_sha256",RecoverySupport.sha(payload));sum.addProperty("payload_bytes",Files.size(payload));
        RecoverySupport.write(output.resolve("inventory-summary.json"),sum);println("RECOVERY_INVENTORY_COMPLETE "+sum.get("total"));
    }
    private void functions(JsonObject outcome)throws Exception {
        JsonArray requests=config.getAsJsonArray("entries");RecoverySupport.require(requests.size()>=1&&requests.size()<=5,"One to five exact entries required");
        Set<String> wanted=new LinkedHashSet<>();for(JsonElement value:requests)RecoverySupport.require(wanted.add(value.getAsString()),"Duplicate requested entry");
        Path inventory=Path.of(RecoverySupport.str(config,"inventory"));RecoverySupport.require(RecoverySupport.sha(inventory).equals(RecoverySupport.str(config,"inventory_sha256")),"Inventory bytes mismatch");
        Map<String,JsonObject> exact=new HashMap<>();
        try(BufferedReader reader=Files.newBufferedReader(inventory,StandardCharsets.UTF_8)){
            String line;while((line=reader.readLine())!=null){monitor.checkCancelled();JsonObject e=JsonParser.parseString(line).getAsJsonObject();String k=RecoverySupport.str(e,"key");if(wanted.contains(k)){RecoverySupport.require(!exact.containsKey(k),"Duplicate own entry");exact.put(k,e);}}
        }
        RecoverySupport.require(exact.size()==wanted.size(),"Requested entry absent");Path exports=output.resolve("exports");Files.createDirectory(exports);JsonArray captures=new JsonArray();
        for(String k:wanted){JsonObject record=exact.get(k);RecoverySupport.require(!record.get("external").getAsBoolean(),"External entry excluded");
            AddressSpace space=currentProgram.getAddressFactory().getAddressSpace(RecoverySupport.str(record,"entry_space"));RecoverySupport.require(space!=null,"Unknown address space");
            Address address=space.getAddress(Long.parseUnsignedLong(RecoverySupport.str(record,"entry_offset").substring(2),16));Function fn=currentProgram.getFunctionManager().getFunctionAt(address);
            RecoverySupport.require(fn!=null&&entry(fn).equals(record),"Exact checkpoint entry differs; no body repair allowed");
            captures.add(exportOne(exports,fn,record,outcome));
        }
        JsonObject sum=summary(outcome);sum.add("captures",captures);sum.addProperty("total",captures.size());RecoverySupport.write(output.resolve("export-summary.json"),sum);println("RECOVERY_EXPORT_COMPLETE "+captures.size());
    }
    private JsonObject exportOne(Path exports,Function fn,JsonObject record,JsonObject outcome)throws Exception {
        String id="capture-"+RecoverySupport.str(config,"nonce")+"-"+RecoverySupport.hexDigest(RecoverySupport.str(record,"key").getBytes(StandardCharsets.UTF_8)).substring(0,16);
        Path stage=exports.resolve("staging-"+id),dest=exports.resolve(id);Files.createDirectory(stage);JsonObject meta=summary(outcome);meta.addProperty("capture_id",id);meta.add("entry",record);meta.addProperty("decompile_seconds",60);meta.addProperty("state","failed");
        JsonArray warnings=new JsonArray();meta.add("warnings",warnings);DecompInterface decompiler=null;Map<ProcessHandle,JsonObject> nativeChildren=new LinkedHashMap<>();
        try{
            RecoverySupport.require(RecoverySupport.sha(Path.of(RecoverySupport.str(config,"native_decompiler"))).equals(config.getAsJsonObject("methods").get("native_decompiler").getAsString()),"Native decompiler method mismatch");
            RecoverySupport.require(!fn.getBody().isEmpty(),"Missing body");decompiler=new DecompInterface();decompiler.toggleCCode(true);decompiler.toggleSyntaxTree(true);
            RecoverySupport.require(decompiler.openProgram(currentProgram),"Decompiler open: "+decompiler.getLastMessage());
            for(ProcessHandle child:ProcessHandle.current().children().toList())if(child.info().command().orElse("").endsWith("/decompile")){
                RecoverySupport.require(Path.of(child.info().command().orElseThrow()).toRealPath().equals(Path.of(RecoverySupport.str(config,"native_decompiler")).toRealPath()),"Native decompiler executable mismatch");
                JsonObject observed=new JsonObject();observed.addProperty("pid",child.pid());observed.addProperty("start_ms",child.info().startInstant().orElseThrow().toEpochMilli());observed.addProperty("executable",child.info().command().orElseThrow());nativeChildren.put(child,observed);
            }
            DecompileResults result=decompiler.decompileFunction(fn,60,monitor);
            meta.addProperty("completed",result.decompileCompleted());meta.addProperty("timed_out",result.isTimedOut());meta.addProperty("cancelled",result.isCancelled());meta.addProperty("failed_to_start",result.failedToStart());
            String diagnostic=result.getErrorMessage();if(diagnostic!=null&&!diagnostic.isBlank())warnings.add(diagnostic);
            DecompiledFunction recovered=result.getDecompiledFunction();String code=recovered==null?null:recovered.getC();meta.addProperty("null_code",code==null);
            if(code!=null&&!code.isEmpty()){
                Files.writeString(stage.resolve("pseudocode.c"),code,StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW);
                for(String line:code.split("\\R"))if(line.toUpperCase(Locale.ROOT).contains("WARNING"))warnings.add(line.trim());
                meta.addProperty("code_sha256",RecoverySupport.sha(stage.resolve("pseudocode.c")));meta.addProperty("code_bytes",Files.size(stage.resolve("pseudocode.c")));
            }
            boolean codePresent=code!=null&&!code.isEmpty();meta.addProperty("state",result.decompileCompleted()&&codePresent?(warnings.isEmpty()?"exported":"exported-with-warnings"):(codePresent?"failed-with-partial-code":"failed"));
        }catch(Exception failure){if(Files.isRegularFile(stage.resolve("pseudocode.c")))meta.addProperty("state","failed-with-partial-code");meta.addProperty("error",failure.getClass().getName()+": "+failure.getMessage());}
        finally{
            if(decompiler!=null)decompiler.dispose();JsonArray children=new JsonArray();
            for(ProcessHandle child:nativeChildren.keySet()){
                long until=System.nanoTime()+3_000_000_000L;while(child.isAlive()&&System.nanoTime()<until)Thread.sleep(10);
                JsonObject p=nativeChildren.get(child);p.addProperty("closed",!child.isAlive());children.add(p);
                RecoverySupport.require(!child.isAlive(),"Native decompiler child survived dispose");
            }meta.add("native_children",children);
        }
        RecoverySupport.write(stage.resolve("metadata.json"),meta);JsonObject manifest=new JsonObject();manifest.addProperty("schema",1);manifest.addProperty("capture_id",id);JsonArray pins=new JsonArray();
        for(String name:new String[]{"metadata.json","pseudocode.c"})if(Files.isRegularFile(stage.resolve(name))){JsonObject pin=new JsonObject();pin.addProperty("path",name);pin.addProperty("bytes",Files.size(stage.resolve(name)));pin.addProperty("sha256",RecoverySupport.sha(stage.resolve(name)));pins.add(pin);}
        manifest.add("files",pins);RecoverySupport.write(stage.resolve("manifest.json"),manifest);Files.move(stage,dest,StandardCopyOption.ATOMIC_MOVE);
        JsonObject capture=new JsonObject();capture.addProperty("capture_id",id);capture.addProperty("manifest_sha256",RecoverySupport.sha(dest.resolve("manifest.json")));capture.addProperty("state",RecoverySupport.str(meta,"state"));return capture;
    }
}
