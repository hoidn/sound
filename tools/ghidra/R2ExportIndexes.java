// Analyst-only roadmap revision 2 item C2: derived JSONL indexes rebuilt from a saved, analyzed program.
//
// analyzeHeadless PROJECT_DIR PROJECT -process PROGRAM -noanalysis -readOnly -scriptPath tools/ghidra
//     [-postScript R2BulkDecompile.java out=CORPUS ...] -postScript R2ExportIndexes.java out=DIR
//
// Reads the program only. Writes, each by temp file and rename, in deterministic address order:
//   strings.jsonl   defined strings; each reference into the string with its containing function, or,
//                   for a reference from data (pointer table, CFString), the functions referencing that data
//   calls.jsonl     direct call edges caller -> callee with call site; "tail-jump" marks a non-computed
//                   jump to another function's entry; thunk callees carry their resolved target
//   indirect.jsonl  computed call and jump sites per function, with any targets the analysis resolved
//   vtables.jsonl   __ZTV / "vtable" symbol addresses with function-pointer slots (Itanium layout,
//                   scanning from +16 until the next named symbol or three non-function words)
//   aliases.jsonl   every function entry (non-external, then external) with all its symbol names
//   manifest.json   program identity and line count, bytes and SHA-256 per file (written last)
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.script.GhidraScript;
import ghidra.framework.Application;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.*;
import ghidra.program.model.symbol.*;
import ghidra.program.util.DefinedStringIterator;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class R2ExportIndexes extends GhidraScript {
    static final String[] FILES = {"strings.jsonl", "calls.jsonl", "indirect.jsonl", "vtables.jsonl", "aliases.jsonl"};
    static final int MAX_VTABLE_WORDS = 4096;
    private final Gson gson = new GsonBuilder().disableHtmlEscaping().serializeNulls().create();
    private Path out;
    private ReferenceManager refs;
    private FunctionManager functions;

    @Override
    public void run() throws Exception {
        out = Path.of(R2BulkDecompile.parseArgs(getScriptArgs(), "out").get("out"));
        Files.createDirectories(out);
        refs = currentProgram.getReferenceManager();
        functions = currentProgram.getFunctionManager();
        long start = System.nanoTime();
        try (Jsonl s = new Jsonl(FILES[0])) { strings(s); s.commit(); }
        try (Jsonl calls = new Jsonl(FILES[1]); Jsonl indirect = new Jsonl(FILES[2])) {
            flows(calls, indirect);
            calls.commit();
            indirect.commit();
        }
        try (Jsonl v = new Jsonl(FILES[3])) { vtables(v); v.commit(); }
        try (Jsonl a = new Jsonl(FILES[4])) { aliases(a); a.commit(); }
        JsonObject manifest = manifest();
        R2BulkDecompile.commit(out.resolve("manifest.json"), (RecoverySupport.GSON.toJson(manifest) + "\n").getBytes(StandardCharsets.UTF_8), true);
        println(String.format("R2_INDEXES %.1f s %s", (System.nanoTime() - start) / 1e9, gson.toJson(manifest.get("files"))));
    }

    /** One JSONL output; replaces DIR/name only when commit() is called, otherwise discards its temp file. */
    final class Jsonl implements AutoCloseable {
        final Path path, temp;
        final BufferedWriter writer;
        long lines;
        boolean committed;

        Jsonl(String name) throws IOException {
            path = out.resolve(name);
            temp = out.resolve("." + name + "." + UUID.randomUUID() + ".tmp");
            writer = Files.newBufferedWriter(temp, StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW);
        }

        void add(JsonObject record) throws IOException {
            writer.write(gson.toJson(record));
            writer.write('\n');
            lines++;
        }

        void commit() throws IOException {
            writer.close();
            try (FileChannel channel = FileChannel.open(temp, StandardOpenOption.WRITE)) { channel.force(true); }
            Files.move(temp, path, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
            committed = true;
        }

        @Override
        public void close() throws IOException {
            writer.close();
            if (!committed) Files.deleteIfExists(temp);
        }
    }

    String key(Address a) {
        String offset = "0x" + Long.toHexString(a.getOffset());
        AddressSpace space = a.getAddressSpace();
        return space.equals(currentProgram.getAddressFactory().getDefaultAddressSpace()) ? offset : space.getName() + ":" + offset;
    }

    private void putFunction(JsonObject o, String field, Function fn) {
        o.addProperty(field, fn == null ? null : key(fn.getEntryPoint()));
        o.addProperty(field + "_name", fn == null ? null : fn.getName(true));
    }

    private Reference[] sorted(Reference[] found) {
        Arrays.sort(found, Comparator.comparing(Reference::getFromAddress).thenComparing(Reference::getToAddress)
            .thenComparing(r -> r.getReferenceType().getName()).thenComparingInt(Reference::getOperandIndex));
        return found;
    }

    private Reference[] referencesTo(Address target) {
        List<Reference> found = new ArrayList<>();
        refs.getReferencesTo(target).forEach(found::add);
        return sorted(found.toArray(new Reference[0]));
    }

    private void strings(Jsonl sink) throws Exception {
        for (Data d : DefinedStringIterator.forProgram(currentProgram)) {
            monitor.checkCancelled();
            Address start = d.getAddress();
            JsonArray from = new JsonArray();
            for (Address target : refs.getReferenceDestinationIterator(new AddressSet(start, d.getMaxAddress()), true))
                for (Reference ref : referencesTo(target)) from.add(stringReference(ref, target.subtract(start)));
            Object value = d.getValue();
            JsonObject r = new JsonObject();
            r.addProperty("address", key(start));
            r.addProperty("type", d.getDataType().getName());
            r.addProperty("length", d.getLength());
            r.addProperty("value", value instanceof String s ? s : d.getDefaultValueRepresentation());
            r.add("refs", from);
            sink.add(r);
        }
    }

    private JsonObject stringReference(Reference ref, long offset) {
        JsonObject o = new JsonObject();
        o.addProperty("from", key(ref.getFromAddress()));
        o.addProperty("offset", offset);
        o.addProperty("type", ref.getReferenceType().getName());
        Function fn = functions.getFunctionContaining(ref.getFromAddress());
        putFunction(o, "function", fn);
        if (fn == null) o.add("via", dataUsers(ref.getFromAddress()));
        return o;
    }

    /** Functions referencing the start of the defined data item that contains a data-origin reference. */
    private JsonArray dataUsers(Address from) {
        JsonArray users = new JsonArray();
        Data holder = currentProgram.getListing().getDataContaining(from);
        if (holder == null) return users;
        for (Reference ref : referencesTo(holder.getAddress())) {
            Function fn = functions.getFunctionContaining(ref.getFromAddress());
            if (fn == null) continue;
            JsonObject o = new JsonObject();
            o.addProperty("data", key(holder.getAddress()));
            o.addProperty("from", key(ref.getFromAddress()));
            putFunction(o, "function", fn);
            users.add(o);
        }
        return users;
    }

    private Function target(Reference ref) {
        if (ref.isExternalReference()) return ((ExternalReference) ref).getExternalLocation().getFunction();
        return functions.getFunctionAt(ref.getToAddress());
    }

    private void flows(Jsonl calls, Jsonl indirect) throws Exception {
        Listing listing = currentProgram.getListing();
        for (Function fn : functions.getFunctions(true)) {
            monitor.checkCancelled();
            for (Instruction ins : listing.getInstructions(fn.getBody(), true)) {
                FlowType flow = ins.getFlowType();
                Reference[] from = sorted(ins.getReferencesFrom());
                if (flow.isComputed() && (flow.isCall() || flow.isJump())) indirect.add(indirectSite(fn, ins, flow, from));
                for (Reference ref : from) {
                    JsonObject edge = directEdge(fn, ins, ref);
                    if (edge != null) calls.add(edge);
                }
            }
        }
    }

    private JsonObject directEdge(Function caller, Instruction ins, Reference ref) {
        RefType type = ref.getReferenceType();
        if (!type.isFlow() || type.isComputed() || !(type.isCall() || type.isJump())) return null;
        Function callee = target(ref);
        boolean tailJump = type.isJump() && callee != null && !callee.isExternal()
            && !callee.getEntryPoint().equals(caller.getEntryPoint()) && callee.getEntryPoint().equals(ref.getToAddress());
        if (!type.isCall() && !tailJump) return null;
        JsonObject o = new JsonObject();
        putFunction(o, "caller", caller);
        o.addProperty("site", key(ins.getAddress()));
        o.addProperty("kind", type.isCall() ? "call" : "tail-jump");
        o.addProperty("ref_type", type.getName());
        o.addProperty("to", key(ref.getToAddress()));
        putFunction(o, "callee", callee);
        putFunction(o, "callee_resolved", callee != null && callee.isThunk() ? callee.getThunkedFunction(true) : null);
        return o;
    }

    private JsonObject indirectSite(Function fn, Instruction ins, FlowType flow, Reference[] from) {
        JsonObject o = new JsonObject();
        putFunction(o, "function", fn);
        o.addProperty("in_thunk", fn.isThunk());
        o.addProperty("site", key(ins.getAddress()));
        o.addProperty("kind", flow.isCall() ? "call" : "jump");
        o.addProperty("flow", flow.getName());
        o.addProperty("instruction", ins.toString());
        JsonArray targets = new JsonArray();
        for (Reference ref : from) {
            if (!ref.getReferenceType().isFlow()) continue;
            JsonObject t = new JsonObject();
            t.addProperty("to", key(ref.getToAddress()));
            t.addProperty("ref_type", ref.getReferenceType().getName());
            putFunction(t, "function", target(ref));
            targets.add(t);
        }
        o.add("resolved_targets", targets);
        return o;
    }

    private static boolean isVtableName(String name) {
        return name.startsWith("__ZTV") || name.startsWith("_ZTV") || name.equals("vtable") || name.startsWith("vtable for");
    }

    private void vtables(Jsonl sink) throws Exception {
        TreeMap<Address, TreeSet<String>> starts = new TreeMap<>();
        for (Symbol s : currentProgram.getSymbolTable().getAllSymbols(false)) {
            monitor.checkCancelled();
            if (!s.isExternal() && s.getAddress().isMemoryAddress() && isVtableName(s.getName()))
                starts.computeIfAbsent(s.getAddress(), a -> new TreeSet<>()).add(s.getName(true));
        }
        for (Map.Entry<Address, TreeSet<String>> e : starts.entrySet()) sink.add(vtable(e.getKey(), e.getValue()));
    }

    private boolean hasNamedSymbol(Address a) {
        for (Symbol s : currentProgram.getSymbolTable().getSymbols(a)) if (s.getSource() != SourceType.DEFAULT) return true;
        return false;
    }

    /** Function stored in the pointer-sized word at slot, via an external reference or the word's value. */
    private Function slotFunction(Address slot) throws MemoryAccessException {
        for (Reference ref : refs.getReferencesFrom(slot)) if (ref.isExternalReference()) return target(ref);
        long value = currentProgram.getMemory().getLong(slot);
        try {
            return functions.getFunctionAt(slot.getAddressSpace().getAddress(value));
        } catch (AddressOutOfBoundsException notAnAddress) {
            return null;
        }
    }

    private JsonObject vtable(Address start, Set<String> names) {
        JsonObject r = new JsonObject();
        r.addProperty("address", key(start));
        JsonArray symbols = new JsonArray();
        names.forEach(symbols::add);
        r.add("symbols", symbols);
        JsonArray slots = new JsonArray();
        boolean imported = currentProgram.getMemory().isExternalBlockAddress(start);
        r.addProperty("stop", imported ? "external-block" : scanSlots(start, slots));
        r.add("slots", slots);
        return r;
    }

    /** Appends function-pointer slots from start+16 and returns why the scan stopped. */
    private String scanSlots(Address start, JsonArray slots) {
        MemoryBlock block = currentProgram.getMemory().getBlock(start);
        int nonFunctionRun = 0;
        for (int i = 2; i < MAX_VTABLE_WORDS; i++) {
            long offset = 8L * i;
            if (block == null || start.getOffset() + offset + 7 > block.getEnd().getOffset()) return "block-end";
            Address slot = start.add(offset);
            if (hasNamedSymbol(slot)) return "next-symbol";
            Function fn;
            try { fn = slotFunction(slot); }
            catch (MemoryAccessException unreadable) { return "unreadable"; }
            if (fn == null) {
                if (++nonFunctionRun == 3) return "non-function-run";
                continue;
            }
            nonFunctionRun = 0;
            JsonObject s = new JsonObject();
            s.addProperty("offset", offset);
            putFunction(s, "function", fn);
            slots.add(s);
        }
        return "max-words";
    }

    private void aliases(Jsonl sink) throws Exception {
        List<Function> all = new ArrayList<>();
        functions.getFunctions(true).forEach(all::add);
        List<Function> external = new ArrayList<>();
        functions.getExternalFunctions().forEach(external::add);
        external.sort(Comparator.comparing(Function::getEntryPoint));
        all.addAll(external);
        for (Function fn : all) {
            monitor.checkCancelled();
            JsonObject r = new JsonObject();
            r.addProperty("entry", key(fn.getEntryPoint()));
            r.addProperty("name", fn.getName(true));
            r.addProperty("external", fn.isExternal());
            r.addProperty("thunk", fn.isThunk());
            putFunction(r, "thunk_target", fn.isThunk() ? fn.getThunkedFunction(true) : null);
            r.addProperty("library", fn.isExternal() ? fn.getExternalLocation().getLibraryName() : null);
            TreeMap<String, JsonObject> named = new TreeMap<>();
            for (Symbol s : currentProgram.getSymbolTable().getSymbols(fn.getEntryPoint())) {
                JsonObject o = new JsonObject();
                o.addProperty("name", s.getName(true));
                o.addProperty("source", s.getSource().toString());
                o.addProperty("primary", s.isPrimary());
                named.put(s.getName(true) + "\u0000" + s.getSource(), o);
            }
            JsonArray symbols = new JsonArray();
            named.values().forEach(symbols::add);
            r.add("symbols", symbols);
            sink.add(r);
        }
    }

    private JsonObject manifest() throws Exception {
        JsonObject m = new JsonObject();
        m.addProperty("schema", 1);
        m.addProperty("tool", "R2ExportIndexes");
        m.addProperty("program", currentProgram.getName());
        m.addProperty("executable_sha256", currentProgram.getExecutableSHA256());
        m.addProperty("ghidra_version", Application.getApplicationVersion());
        JsonObject files = new JsonObject();
        for (String name : FILES) {
            Path path = out.resolve(name);
            long lines;
            try (var stream = Files.lines(path, StandardCharsets.UTF_8)) { lines = stream.count(); }
            JsonObject f = new JsonObject();
            f.addProperty("lines", lines);
            f.addProperty("bytes", Files.size(path));
            f.addProperty("sha256", RecoverySupport.sha(path));
            files.add(name, f);
        }
        m.add("files", files);
        return m;
    }
}
