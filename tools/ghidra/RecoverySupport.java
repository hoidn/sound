// Analyst-only shared schema, lineage and fresh-file helpers.
import com.google.gson.*;
import com.google.gson.stream.*;
import ghidra.framework.Application;
import ghidra.program.model.listing.Program;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

public final class RecoverySupport {
    public static final String TARGET="3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad";
    public static final String FIXTURE=hexDigest(new byte[]{0,0,(byte)0x80,0x52,(byte)0xc0,3,0x5f,(byte)0xd6});
    public static final Gson GSON=new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create();
    private RecoverySupport() {}
    public static String hexDigest(byte[] bytes) {
        try{return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));}
        catch(Exception e){throw new IllegalStateException(e);}
    }
    public static String sha(Path path)throws Exception {
        MessageDigest digest=MessageDigest.getInstance("SHA-256");byte[] buf=new byte[1048576];
        try(InputStream in=Files.newInputStream(path)){int n;while((n=in.read(buf))!=-1)digest.update(buf,0,n);}
        return HexFormat.of().formatHex(digest.digest());
    }
    public static String shaQuiet(Path path){try{return sha(path);}catch(Exception e){throw new IllegalStateException(e);}}
    public static void safe(Path path)throws Exception {
        for(Path p=path.toAbsolutePath();p!=null;p=p.getParent())if(Files.isSymbolicLink(p))throw new IOException("Symlink path: "+p);
    }
    public static JsonObject read(Path path)throws Exception {
        safe(path);if(Files.size(path)>16777216)throw new IOException("Oversized JSON");
        try(JsonReader reader=new JsonReader(Files.newBufferedReader(path,StandardCharsets.UTF_8))){
            reader.setLenient(false);JsonElement value=parse(reader,0);if(reader.peek()!=JsonToken.END_DOCUMENT)throw new IOException("Trailing JSON");
            return value.getAsJsonObject();
        }
    }
    private static JsonElement parse(JsonReader r,int depth)throws Exception {
        if(depth>32)throw new IOException("JSON nesting limit");
        switch(r.peek()){
            case BEGIN_OBJECT:
                JsonObject object=new JsonObject();r.beginObject();while(r.hasNext()){
                    String key=r.nextName();if(object.has(key))throw new IOException("Duplicate JSON key: "+key);object.add(key,parse(r,depth+1));
                }r.endObject();return object;
            case BEGIN_ARRAY:
                JsonArray array=new JsonArray();r.beginArray();while(r.hasNext())array.add(parse(r,depth+1));r.endArray();return array;
            case STRING:return new JsonPrimitive(r.nextString());
            case NUMBER:return new JsonPrimitive(new java.math.BigDecimal(r.nextString()));
            case BOOLEAN:return new JsonPrimitive(r.nextBoolean());
            case NULL:r.nextNull();return JsonNull.INSTANCE;
            default:throw new IOException("Malformed JSON");
        }
    }
    public static JsonObject config(String[] args)throws Exception {
        if(args.length!=2||!args[1].matches("[0-9a-f]{64}"))throw new IOException("Config and exact SHA required");
        Path path=Path.of(args[0]);if(!sha(path).equals(args[1]))throw new IOException("Config SHA mismatch");
        JsonObject c=read(path);if(integer(c,"schema")!=1)throw new IOException("Unknown schema");
        if(!str(c,"nonce").matches("[0-9a-f]{32}"))throw new IOException("Bad nonce");
        c.addProperty("config_sha256",args[1]);return c;
    }
    public static String str(JsonObject o,String k){if(!o.has(k)||!o.get(k).isJsonPrimitive()||!o.get(k).getAsJsonPrimitive().isString())throw new IllegalArgumentException("String required: "+k);return o.get(k).getAsString();}
    public static long integer(JsonObject o,String k){
        if(!o.has(k)||!o.get(k).isJsonPrimitive()||!o.get(k).getAsJsonPrimitive().isNumber())throw new IllegalArgumentException("Integer required: "+k);
        return o.get(k).getAsBigDecimal().longValueExact();
    }
    public static boolean bool(JsonObject o,String k){
        if(!o.has(k)||!o.get(k).isJsonPrimitive()||!o.get(k).getAsJsonPrimitive().isBoolean())throw new IllegalArgumentException("Boolean required: "+k);
        return o.get(k).getAsBoolean();
    }
    public static void require(boolean value,String reason)throws IOException {if(!value)throw new IOException(reason);}
    public static JsonObject lineage(JsonObject c){JsonObject o=new JsonObject();o.addProperty("schema",1);o.addProperty("nonce",str(c,"nonce"));o.addProperty("config_sha256",str(c,"config_sha256"));return o;}
    public static void bind(JsonObject o,JsonObject c)throws Exception {
        require(integer(o,"schema")==1&&str(o,"nonce").equals(str(c,"nonce"))&&str(o,"config_sha256").equals(str(c,"config_sha256")),"Stale lineage");
    }
    public static void verifyProgram(JsonObject c,Program p)throws Exception {
        require(p!=null,"Program absent");
        boolean fixture=bool(c,"fixture");String expected=fixture?FIXTURE:TARGET;
        require(str(c,"target_sha256").equals(expected),"Pinned mode mismatch");
        require(expected.equalsIgnoreCase(p.getExecutableSHA256()),"Program SHA mismatch");
        require(p.getName().equals(str(c,"program_name")),"Program name mismatch");
        require(p.getLanguageID().toString().equals(str(c,"language")),"Language mismatch");
        require(p.getCompilerSpec().getCompilerSpecID().toString().equals(str(c,"compiler")),"Compiler mismatch");
        require(Application.getApplicationVersion().equals(str(c,"ghidra_version")),"Ghidra version mismatch");
    }
    public static void fixture(JsonObject c,Program p)throws Exception {
        verifyProgram(c,p);require(bool(c,"fixture")&&FIXTURE.equalsIgnoreCase(p.getExecutableSHA256()),"Fixture unavailable for target");
    }
    public static void write(Path path,JsonObject value)throws Exception {
        safe(path);Path temp=path.resolveSibling("."+path.getFileName()+"."+UUID.randomUUID());
        byte[] bytes=(GSON.toJson(value)+"\n").getBytes(StandardCharsets.UTF_8);
        try(java.nio.channels.FileChannel channel=java.nio.channels.FileChannel.open(temp,StandardOpenOption.CREATE_NEW,StandardOpenOption.WRITE)){
            java.nio.ByteBuffer buffer=java.nio.ByteBuffer.wrap(bytes);while(buffer.hasRemaining())channel.write(buffer);channel.force(true);
        }
        try{Files.createLink(path,temp);}finally{Files.delete(temp);}
    }
    public static JsonObject completed(JsonObject c)throws Exception {
        JsonObject done=read(Path.of(str(c,"complete")));bind(done,c);require(str(done,"status").equals("pass"),"No successful gate");
        require(str(done,"gate_sha256").equals(sha(Path.of(str(c,"gate")))),"Gate bytes changed");
        require(str(done,"ack_sha256").equals(sha(Path.of(str(c,"ack")))),"Ack bytes changed");
        require(integer(done,"pid")==ProcessHandle.current().pid(),"Gate PID mismatch");
        require(integer(done,"start_ms")==ProcessHandle.current().info().startInstant().orElseThrow().toEpochMilli(),"Gate creation mismatch");return done;
    }
}
