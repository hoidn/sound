// Analyst-only read-only query script for a saved, analyzed Ghidra project.
// Never re-runs analysis and never saves: run with -process <program> -noanalysis -readOnly.
//
// One-shot:  -postScript R2FunctionDossier.java <fresh-out-dir> <query>...
// Server:    -postScript R2FunctionDossier.java --serve <spool-dir>
//
// A query is "0x<hex address>", a symbol name (optionally "Ns::name"), "str:<exact string value>",
// or "@<file>" with one query per line. An address inside a function, or a function name, yields
// a function dossier (functions/<entry>.json + .c) plus incoming references to the given address.
// Any other address yields a reference report (refs/<addr>.json); "str:" yields one per matching
// defined string. Each output directory gets queries.json and a SHA-256 manifest.json. Outputs
// contain no timings, so an unchanged program and query list reproduce identical bytes.
//
// Server mode serves several investigators from one JVM (Ghidra lets one process hold a project):
// write <spool>/requests/<name>.tmp, rename it to <name>.txt (queries, one per line); results
// appear atomically as <spool>/results/<name>/ and the request moves to <spool>/done/. Create
// <spool>/requests/STOP to end the server. Requests are served one at a time in name order.
// Depends on: Ghidra 12.1.4 program/listing/reference APIs, the decompiler, bundled Gson.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.decompiler.*;
import ghidra.app.script.GhidraScript;
import ghidra.framework.Application;
import ghidra.program.model.address.*;
import ghidra.program.model.data.StringDataInstance;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.util.DefinedStringIterator;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.stream.Stream;

public class R2FunctionDossier extends GhidraScript {
    static final int DECOMPILE_TIMEOUT_S = 60;
    static final int MAX_REFERENCES = 10_000;   // ponytail: per-address cap, reported as truncated
    static final int MAX_HOP_DATA_BYTES = 64;   // one-hop pointer/CFString follow only for small items
    static final int MAX_DATA_SCAN_BYTES = 4096;
    private final Gson gson = new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().serializeNulls().create();
    private DecompInterface decompiler;
    private Path out;

    @Override public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) throw new IllegalArgumentException("Usage: <out-dir> <query>... | --serve <spool-dir>");
        decompiler = new DecompInterface();
        decompiler.toggleCCode(true);
        decompiler.toggleSyntaxTree(true);
        if (!decompiler.openProgram(currentProgram)) throw new IllegalStateException("Decompiler open failed: " + decompiler.getLastMessage());
        try {
            if (args[0].equals("--serve")) serve(Path.of(args[1]));
            else answer(Path.of(args[0]), expand(Arrays.asList(args).subList(1, args.length)));
        } finally {
            decompiler.dispose();
        }
    }

    private void serve(Path spool) throws Exception {
        Path requests = spool.resolve("requests"), results = spool.resolve("results"), done = spool.resolve("done");
        for (Path p : List.of(requests, results, done)) Files.createDirectories(p);
        println("R2FunctionDossier serving " + spool);
        while (!Files.exists(requests.resolve("STOP"))) {
            monitor.checkCancelled();
            List<Path> pending;
            try (Stream<Path> s = Files.list(requests)) {
                pending = s.filter(p -> p.getFileName().toString().endsWith(".txt")).sorted().toList();
            }
            for (Path request : pending) serveOne(request, results, done);
            if (pending.isEmpty()) Thread.sleep(250);
        }
        println("R2FunctionDossier stopped");
    }

    private void serveOne(Path request, Path results, Path done) throws Exception {
        String name = request.getFileName().toString().replaceFirst("\\.txt$", "");
        Path staging = results.resolve(name + ".partial"), target = results.resolve(name);
        if (Files.exists(target) || Files.exists(staging)) throw new IllegalStateException("Result already exists for request " + name);
        long start = System.nanoTime();
        try {
            answer(staging, expand(Files.readAllLines(request, StandardCharsets.UTF_8)));
        } catch (Exception failure) {   // a bad request must not stop the shared server; it is reported
            Files.createDirectories(staging);
            write(staging.resolve("error.json"), gson.toJson(kv("error", String.valueOf(failure))));
        }
        Files.move(staging, target, StandardCopyOption.ATOMIC_MOVE);
        Files.move(request, done.resolve(request.getFileName()), StandardCopyOption.REPLACE_EXISTING);
        println(String.format("request %s served in %.3f s", name, (System.nanoTime() - start) / 1e9));
    }

    private List<String> expand(List<String> raw) throws Exception {
        List<String> queries = new ArrayList<>();
        for (String q : raw) {
            if (q.startsWith("@")) queries.addAll(expand(Files.readAllLines(Path.of(q.substring(1)), StandardCharsets.UTF_8)));
            else if (!q.isBlank() && !q.startsWith("#")) queries.add(q.strip());
        }
        if (queries.isEmpty()) throw new IllegalArgumentException("No queries");
        return queries;
    }

    private void answer(Path dir, List<String> queries) throws Exception {
        if (Files.exists(dir)) try (Stream<Path> s = Files.list(dir)) {
            if (s.findAny().isPresent()) throw new IllegalArgumentException("Output directory is not empty: " + dir);
        }
        out = dir;
        Files.createDirectories(out.resolve("functions"));
        Files.createDirectories(out.resolve("refs"));
        List<Object> records = new ArrayList<>();
        for (String q : queries) {
            monitor.checkCancelled();
            try {
                records.add(query(q));
            } catch (IllegalArgumentException malformed) {   // e.g. bad hex; reported, other queries still run
                records.add(kv("query", q, "matches", List.of(), "error", malformed.toString()));
            }
        }
        write(out.resolve("queries.json"), gson.toJson(records));
        writeManifest();
    }

    private Map<String, Object> query(String q) throws Exception {
        Map<String, Object> rec = new LinkedHashMap<>();
        rec.put("query", q);
        List<Map<String, Object>> matches = new ArrayList<>();
        rec.put("matches", matches);
        for (Address a : q.startsWith("str:") ? stringsEqualTo(q.substring(4)) : resolve(q)) {
            Function f = q.startsWith("str:") ? null : getFunctionContaining(a);
            if (f == null && !q.startsWith("str:")) f = getFunctionAt(a);   // external functions have no body
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("address", hex(a));
            m.put("function", f == null ? null : dossier(f));
            // An entry's incoming references are in its dossier; any other address gets its own report.
            m.put("refs", f != null && a.equals(f.getEntryPoint()) ? null : refsReport(a));
            matches.add(m);
        }
        if (matches.isEmpty()) rec.put("error", "No address, symbol or defined string matched");
        return rec;
    }

    private List<Address> resolve(String q) {
        if (q.startsWith("0x")) {
            Address a = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(Long.parseUnsignedLong(q.substring(2), 16));
            return currentProgram.getMemory().contains(a) ? List.of(a) : List.of();
        }
        String simple = q.contains("::") ? q.substring(q.lastIndexOf("::") + 2) : q;
        TreeSet<Address> found = new TreeSet<>();
        for (Symbol s : currentProgram.getSymbolTable().getSymbols(simple))
            if (!q.contains("::") || s.getName(true).equals(q)) found.add(s.getAddress());
        return new ArrayList<>(found);
    }

    private List<Address> stringsEqualTo(String value) {
        List<Address> found = new ArrayList<>();
        for (Data d : DefinedStringIterator.forProgram(currentProgram))
            if (value.equals(stringValue(d))) found.add(d.getMinAddress());
        return found;
    }

    private String dossier(Function f) throws Exception {
        String rel = "functions/" + fileName(f.getEntryPoint());
        Path json = out.resolve(rel + ".json");
        if (!Files.exists(json)) {
            Map<String, Object> d = new LinkedHashMap<>();
            d.put("schema", "r2-function-dossier-v1");
            d.putAll(functionRef(f));
            d.put("signature", f.getPrototypeString(false, false));
            d.put("calling_convention", f.getCallingConventionName());
            d.put("signature_source", f.getSignatureSource().toString());
            d.put("is_external", f.isExternal());
            d.put("is_thunk", f.isThunk());
            Function thunked = f.getThunkedFunction(true);
            d.put("thunk_target", thunked == null ? null : functionRef(thunked));
            d.put("body_ranges", ranges(f.getBody()));
            d.put("body_bytes", f.getBody().getNumAddresses());
            d.put("callers", functionRefs(f.getCallingFunctions(monitor)));
            d.put("callees", functionRefs(f.getCalledFunctions(monitor)));
            d.put("references_from_body", referencesFrom(f.getBody()));
            d.put("incoming_references_to_entry", referencesTo(f.getEntryPoint()));
            d.put("decompile", decompile(f, out.resolve(rel + ".c")));
            d.put("disassembly", disassembly(f.getBody()));
            write(json, gson.toJson(d));
        }
        return rel + ".json";
    }

    private Map<String, Object> decompile(Function f, Path cFile) throws Exception {
        Map<String, Object> r = new LinkedHashMap<>();
        if (f.isExternal() || f.getBody().isEmpty()) {
            r.put("status", "not-applicable");
            return r;
        }
        DecompileResults res = decompiler.decompileFunction(f, DECOMPILE_TIMEOUT_S, monitor);
        DecompiledFunction df = res.getDecompiledFunction();
        String code = df == null ? null : df.getC();
        List<String> warnings = new ArrayList<>();
        String error = res.getErrorMessage();
        if (error != null && !error.isBlank()) warnings.add(error.strip());
        if (code != null) {
            for (String line : code.split("\\R")) if (line.contains("WARNING")) warnings.add(line.strip());
            write(cFile, code);
        }
        r.put("status", res.isTimedOut() ? "timeout" : res.decompileCompleted() && code != null ? "ok" : "failed");
        r.put("timeout_s", DECOMPILE_TIMEOUT_S);
        r.put("pseudocode_file", code == null ? null : cFile.getFileName().toString());
        r.put("warnings", warnings);
        return r;
    }

    private List<Map<String, Object>> disassembly(AddressSetView body) {
        List<Map<String, Object>> lines = new ArrayList<>();
        for (Instruction i : currentProgram.getListing().getInstructions(body, true)) {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("address", hex(i.getAddress()));
            try { m.put("bytes", HexFormat.of().formatHex(i.getBytes())); }
            catch (Exception e) { m.put("bytes", null); }   // unreadable bytes are recorded, not fatal
            m.put("text", i.toString());
            lines.add(m);
        }
        return lines;
    }

    private List<Map<String, Object>> referencesFrom(AddressSetView body) {
        ReferenceManager rm = currentProgram.getReferenceManager();
        List<Map<String, Object>> refs = new ArrayList<>();
        AddressIterator sources = rm.getReferenceSourceIterator(body, true);
        while (sources.hasNext()) {
            Address from = sources.next();
            Reference[] here = rm.getReferencesFrom(from);
            Arrays.sort(here, Comparator.comparing(Reference::getToAddress).thenComparing(r -> r.getReferenceType().toString()));
            for (Reference r : here) {
                if (r.getReferenceType().isFlow() && !r.getReferenceType().isCall()) continue;   // intra-body jumps
                if (!r.getToAddress().isMemoryAddress() && !r.getToAddress().isExternalAddress()) continue;   // stack/register
                Map<String, Object> m = new LinkedHashMap<>();
                m.put("from", hex(from));
                m.put("to", hex(r.getToAddress()));
                m.put("type", r.getReferenceType().toString());
                m.put("target", describeTarget(r.getToAddress(), true));
                refs.add(m);
            }
        }
        return refs;
    }

    private Map<String, Object> describeTarget(Address to, boolean hop) {
        Map<String, Object> m = new LinkedHashMap<>();
        Function f = getFunctionAt(to);
        Symbol s = currentProgram.getSymbolTable().getPrimarySymbol(to);
        m.put("symbol", s == null ? null : s.getName(true));
        if (f != null) { m.put("kind", "function"); m.put("function", functionRef(f)); return m; }
        Data d = to.isMemoryAddress() ? currentProgram.getListing().getDataContaining(to) : null;
        if (d == null) { m.put("kind", "undefined"); return m; }
        String str = stringValue(d);
        m.put("kind", str != null ? "string" : "data");
        m.put("data_start", hex(d.getMinAddress()));
        m.put("data_type", d.getDataType().getName());
        m.put("string", str);
        if (hop && str == null && d.getLength() <= MAX_HOP_DATA_BYTES) m.put("points_to_strings", stringsReferencedBy(d));
        return m;
    }

    /** One hop: strings referenced from inside a small data item (pointer, CFString struct). */
    private List<Map<String, Object>> stringsReferencedBy(Data d) {
        List<Map<String, Object>> found = new ArrayList<>();
        ReferenceManager rm = currentProgram.getReferenceManager();
        for (Address a = d.getMinAddress(); a != null && a.compareTo(d.getMaxAddress()) <= 0; a = a.next()) {
            for (Reference r : rm.getReferencesFrom(a)) {
                Data target = currentProgram.getListing().getDataContaining(r.getToAddress());
                String str = target == null ? null : stringValue(target);
                if (str != null) found.add(kv("from", hex(a), "to", hex(r.getToAddress()), "string", str));
            }
        }
        return found;
    }

    private String refsReport(Address a) throws Exception {
        String rel = "refs/" + fileName(a) + ".json";
        Path json = out.resolve(rel);
        if (Files.exists(json)) return rel;
        Map<String, Object> r = new LinkedHashMap<>();
        r.put("schema", "r2-references-v1");
        r.put("address", hex(a));
        var block = currentProgram.getMemory().getBlock(a);
        r.put("block", block == null ? null : block.getName());
        r.put("target", describeTarget(a, true));
        Data d = currentProgram.getListing().getDataContaining(a);
        Address start = d != null && d.getLength() <= MAX_DATA_SCAN_BYTES ? d.getMinAddress() : a;
        Address end = d != null && d.getLength() <= MAX_DATA_SCAN_BYTES ? d.getMaxAddress() : a;
        List<Map<String, Object>> incoming = new ArrayList<>();
        for (Address x = start; x != null && x.compareTo(end) <= 0; x = x.next()) incoming.addAll(referencesTo(x));
        r.put("scanned_range", kv("start", hex(start), "end", hex(end)));
        r.put("incoming_references", incoming);
        write(json, gson.toJson(r));
        return rel;
    }

    /** Incoming references to one address; references from data get one hop back to their referrers. */
    private List<Map<String, Object>> referencesTo(Address to) {
        List<Reference> refs = new ArrayList<>();
        for (Reference r : currentProgram.getReferenceManager().getReferencesTo(to)) refs.add(r);
        refs.sort(Comparator.comparing(Reference::getFromAddress).thenComparing(r -> r.getReferenceType().toString()));
        List<Map<String, Object>> list = new ArrayList<>();
        for (Reference r : refs.subList(0, Math.min(refs.size(), MAX_REFERENCES))) {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("to", hex(to));
            m.put("from", hex(r.getFromAddress()));
            m.put("type", r.getReferenceType().toString());
            Function f = r.getFromAddress().isMemoryAddress() ? getFunctionContaining(r.getFromAddress()) : null;
            m.put("from_function", f == null ? null : functionRef(f));
            if (f == null) m.put("from_data_referrers", dataReferrers(r.getFromAddress()));
            list.add(m);
        }
        if (refs.size() > MAX_REFERENCES) list.add(kv("truncated", true, "total", refs.size()));
        return list;
    }

    private List<Map<String, Object>> dataReferrers(Address from) {
        Data d = from.isMemoryAddress() ? currentProgram.getListing().getDataContaining(from) : null;
        List<Map<String, Object>> list = new ArrayList<>();
        if (d == null) return list;
        List<Reference> refs = new ArrayList<>();
        for (Reference r : currentProgram.getReferenceManager().getReferencesTo(d.getMinAddress())) refs.add(r);
        refs.sort(Comparator.comparing(Reference::getFromAddress));
        for (Reference r : refs.subList(0, Math.min(refs.size(), MAX_REFERENCES))) {
            Function f = r.getFromAddress().isMemoryAddress() ? getFunctionContaining(r.getFromAddress()) : null;
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("data_start", hex(d.getMinAddress()));
            m.put("from", hex(r.getFromAddress()));
            m.put("type", r.getReferenceType().toString());
            m.put("from_function", f == null ? null : functionRef(f));
            list.add(m);
        }
        return list;
    }

    private String stringValue(Data d) {
        if (!StringDataInstance.isString(d)) return null;
        return StringDataInstance.getStringDataInstance(d).getStringValue();
    }

    private Map<String, Object> functionRef(Function f) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("entry", hex(f.getEntryPoint()));
        m.put("name", f.getName(true));
        return m;
    }

    private List<Map<String, Object>> functionRefs(Set<Function> fs) {
        return fs.stream().sorted(Comparator.comparing(Function::getEntryPoint)).map(this::functionRef).toList();
    }

    private List<Map<String, Object>> ranges(AddressSetView set) {
        List<Map<String, Object>> list = new ArrayList<>();
        for (AddressRange r : set.getAddressRanges()) list.add(kv("start", hex(r.getMinAddress()), "end", hex(r.getMaxAddress())));
        return list;
    }

    /** Ordered map: Map.of iteration order varies between JVM runs and would break determinism. */
    private static Map<String, Object> kv(Object... pairs) {
        Map<String, Object> m = new LinkedHashMap<>();
        for (int i = 0; i < pairs.length; i += 2) m.put((String) pairs[i], pairs[i + 1]);
        return m;
    }

    private String hex(Address a) {
        return a.getAddressSpace().equals(currentProgram.getAddressFactory().getDefaultAddressSpace())
            ? "0x" + Long.toHexString(a.getOffset()) : a.toString();
    }

    private String fileName(Address a) {
        return hex(a).replace(':', '_');
    }

    private void write(Path path, String content) throws Exception {
        Files.writeString(path, content.endsWith("\n") ? content : content + "\n", StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW);
    }

    private void writeManifest() throws Exception {
        TreeMap<String, Object> files = new TreeMap<>();
        List<Path> paths;
        try (Stream<Path> s = Files.walk(out)) { paths = s.filter(Files::isRegularFile).toList(); }
        for (Path p : paths) {
            byte[] bytes = Files.readAllBytes(p);
            files.put(out.relativize(p).toString(), kv("sha256",
                HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes)), "bytes", bytes.length));
        }
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("schema", "r2-dossier-manifest-v1");
        m.put("program", currentProgram.getName());
        m.put("executable_sha256", currentProgram.getExecutableSHA256());
        m.put("ghidra_version", Application.getApplicationVersion());
        m.put("decompile_timeout_s", DECOMPILE_TIMEOUT_S);
        m.put("files", files);
        write(out.resolve("manifest.json"), gson.toJson(m));
    }
}
