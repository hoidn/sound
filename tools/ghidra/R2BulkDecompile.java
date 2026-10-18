// Analyst-only roadmap revision 2 item C1: decompile every non-external function of a saved,
// analyzed program in one headless JVM, writing a resumable chunked JSONL corpus.
//
// analyzeHeadless PROJECT_DIR PROJECT -process PROGRAM -noanalysis -readOnly -scriptPath tools/ghidra
//     -postScript R2BulkDecompile.java out=DIR [threads=4] [instances=1] [chunk=200] [shard=i/n]
//
// Reads the program only (no transaction is opened). Eligible functions are the non-external
// functions in FunctionManager address order; chunk k holds eligible functions [k*chunk, (k+1)*chunk).
// shard=i/n attempts only chunks with k % n == i: a spread sample (shard=0/40) or one of n
// concurrent JVMs, each opening its own project copy, all writing disjoint chunk files into the
// same DIR. instances=K opens K-1 extra read-only instances of the same program file in this JVM
// and spreads worker threads across them: each instance has its own database lock, which the
// decompiler callbacks otherwise serialize on (measured on Push2; see wiki/research/r2-corpus-tooling.md).
// Writes:
//   DIR/run.json                 program and settings identity; a later run must match it exactly
//   DIR/chunks/chunk-NNNNN.jsonl one JSON record per function, committed by hard link (never replaced)
//   DIR/coverage.json            regenerated from every committed chunk at the end of each run
// A rerun validates and skips committed chunks; failed records stay failed. Decompiler start-up
// and I/O errors abort the run and leave the chunk pending rather than recording a function failure.
// @category Sound.Analysis
import com.google.gson.*;
import ghidra.app.decompiler.*;
import ghidra.app.script.GhidraScript;
import ghidra.framework.Application;
import ghidra.framework.model.DomainFile;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.util.GhidraProgramUtilities;
import ghidra.util.task.TaskMonitor;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.FileLock;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class R2BulkDecompile extends GhidraScript {
    static final int TIMEOUT_SECONDS = 60;
    static final Set<String> STATES = Set.of("exported", "exported-with-warnings", "failed");
    private final Gson gson = new GsonBuilder().disableHtmlEscaping().serializeNulls().create();
    record Worker(Program program, DecompInterface decompiler) {}
    private final Map<Thread, Worker> workers = new ConcurrentHashMap<>();
    private final List<Program> programs = new ArrayList<>();
    private final AtomicInteger nextWorker = new AtomicInteger();
    private Path out;
    private List<Function> eligible;
    private int chunkSize;

    @Override
    public void run() throws Exception {
        Map<String, String> args = parseArgs(getScriptArgs(), "out", "threads", "chunk", "instances", "shard");
        out = Path.of(args.get("out"));
        int threads = Integer.parseInt(args.getOrDefault("threads", "4"));
        chunkSize = Integer.parseInt(args.getOrDefault("chunk", "200"));
        int instances = Integer.parseInt(args.getOrDefault("instances", "1"));
        int[] shard = parseShard(args.getOrDefault("shard", "0/1"));
        if (threads < 1 || chunkSize < 1 || instances < 1) throw new IllegalArgumentException("threads, instances and chunk must be positive");
        if (!GhidraProgramUtilities.isAnalyzed(currentProgram))
            throw new IllegalStateException("Program is not marked analyzed: " + currentProgram.getName());
        Files.createDirectories(out.resolve("chunks"));
        long start = System.nanoTime();
        eligible = new ArrayList<>();
        for (Function fn : currentProgram.getFunctionManager().getFunctions(true))
            if (!fn.isExternal()) eligible.add(fn);
        pinRun();
        List<Integer> pending = pendingChunks(shard);
        programs.add(currentProgram);
        try {
            for (int i = 1; i < instances && !pending.isEmpty(); i++)
                programs.add((Program) currentProgram.getDomainFile().getReadOnlyDomainObject(this, DomainFile.DEFAULT_VERSION, monitor));
            decompileChunks(pending, threads);
        } finally {
            for (Program extra : programs.subList(1, programs.size())) extra.release(this);
        }
        JsonObject invocation = new JsonObject();
        invocation.addProperty("shard", shard[0] + "/" + shard[1]);
        invocation.addProperty("threads", threads);
        invocation.addProperty("instances", instances);
        invocation.addProperty("chunks_written", pending.size());
        invocation.addProperty("functions_written", pending.stream().mapToInt(k -> chunk(k).size()).sum());
        invocation.addProperty("decompile_seconds", (System.nanoTime() - start) / 1e9);
        JsonObject coverage = writeCoverage(invocation);
        println("R2_INVOCATION " + gson.toJson(invocation));
        println("R2_COVERAGE " + gson.toJson(coverage.get("counts")));
    }

    /** Parses key=value script arguments; unknown keys fail rather than silently using a default. */
    static Map<String, String> parseArgs(String[] values, String... allowed) {
        Map<String, String> args = new HashMap<>();
        for (String value : values) {
            int eq = value.indexOf('=');
            if (eq < 1 || !List.of(allowed).contains(value.substring(0, eq)))
                throw new IllegalArgumentException("Expected key=value script argument with key in " + List.of(allowed) + ": " + value);
            args.put(value.substring(0, eq), value.substring(eq + 1));
        }
        if (!args.containsKey("out")) throw new IllegalArgumentException("Script argument out=DIR is required");
        return args;
    }

    static int[] parseShard(String value) {
        String[] parts = value.split("/");
        int i = Integer.parseInt(parts[0]), n = parts.length == 2 ? Integer.parseInt(parts[1]) : -1;
        if (n < 1 || i < 0 || i >= n) throw new IllegalArgumentException("shard must be i/n with 0 <= i < n: " + value);
        return new int[] {i, n};
    }

    String key(Address a) {
        String offset = "0x" + Long.toHexString(a.getOffset());
        String space = a.getAddressSpace().getName();
        return space.equals(currentProgram.getAddressFactory().getDefaultAddressSpace().getName()) ? offset : space + ":" + offset;
    }

    private int chunkCount() { return (eligible.size() + chunkSize - 1) / chunkSize; }

    private List<Function> chunk(int k) {
        return eligible.subList(k * chunkSize, Math.min(eligible.size(), (k + 1) * chunkSize));
    }

    private Path chunkPath(int k) { return out.resolve("chunks").resolve(String.format("chunk-%05d.jsonl", k)); }

    private JsonObject identity() {
        StringBuilder keys = new StringBuilder();
        for (Function fn : eligible) keys.append(key(fn.getEntryPoint())).append('\n');
        JsonObject run = new JsonObject();
        run.addProperty("schema", 1);
        run.addProperty("tool", "R2BulkDecompile");
        run.addProperty("program", currentProgram.getName());
        run.addProperty("executable_sha256", currentProgram.getExecutableSHA256());
        run.addProperty("language", currentProgram.getLanguageID().toString());
        run.addProperty("compiler", currentProgram.getCompilerSpec().getCompilerSpecID().toString());
        run.addProperty("image_base", key(currentProgram.getImageBase()));
        run.addProperty("ghidra_version", Application.getApplicationVersion());
        run.addProperty("eligible", eligible.size());
        run.addProperty("eligible_keys_sha256", RecoverySupport.hexDigest(keys.toString().getBytes(StandardCharsets.UTF_8)));
        run.addProperty("chunk_size", chunkSize);
        run.addProperty("chunk_count", chunkCount());
        run.addProperty("timeout_seconds", TIMEOUT_SECONDS);
        run.addProperty("decompiler", "DecompInterface default options, C code and syntax tree");
        return run;
    }

    private void pinRun() throws Exception {
        JsonObject run = identity();
        Path path = out.resolve("run.json");
        if (Files.exists(path)) {
            JsonObject existing = JsonParser.parseString(Files.readString(path)).getAsJsonObject();
            if (!existing.equals(run))
                throw new IOException("Output " + out + " belongs to a different program or settings:\n" + existing + "\nnow:\n" + run);
            return;
        }
        commit(path, (RecoverySupport.GSON.toJson(run) + "\n").getBytes(StandardCharsets.UTF_8), true);
    }

    private List<Integer> pendingChunks(int[] shard) throws Exception {
        List<Integer> pending = new ArrayList<>();
        for (int k = shard[0]; k < chunkCount(); k += shard[1]) {
            if (Files.exists(chunkPath(k))) readChunk(k);
            else pending.add(k);
        }
        return pending;
    }

    private void decompileChunks(List<Integer> pending, int threads) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        try {
            List<Future<?>> futures = new ArrayList<>();
            for (int k : pending) futures.add(pool.submit(() -> { writeChunk(k); return null; }));
            for (Future<?> future : futures) {
                try { future.get(); }
                catch (ExecutionException failure) { pool.shutdownNow(); throw new IOException("Chunk failed; run aborted", failure.getCause()); }
            }
        } finally {
            pool.shutdownNow();
            pool.awaitTermination(TIMEOUT_SECONDS * 2, TimeUnit.SECONDS);
            for (Worker worker : workers.values()) worker.decompiler().dispose();
        }
    }

    /** This thread's decompiler, bound to one program instance (round-robin over instances). */
    private Worker worker() throws IOException {
        Worker worker = workers.get(Thread.currentThread());
        if (worker != null) return worker;
        Program program = programs.get(nextWorker.getAndIncrement() % programs.size());
        DecompInterface decompiler = new DecompInterface();
        decompiler.toggleCCode(true);
        decompiler.toggleSyntaxTree(true);
        worker = new Worker(program, decompiler);
        workers.put(Thread.currentThread(), worker);
        if (!decompiler.openProgram(program)) throw new IOException("Decompiler did not open program: " + decompiler.getLastMessage());
        return worker;
    }

    /** The same function in another read-only instance of the program file. */
    private static Function local(Program program, Function fn) {
        if (fn.getProgram() == program) return fn;
        Address entry = fn.getEntryPoint();
        Address same = program.getAddressFactory().getAddressSpace(entry.getAddressSpace().getName()).getAddress(entry.getOffset());
        Function found = program.getFunctionManager().getFunctionAt(same);
        if (found == null) throw new IllegalStateException("Program instance lacks function at " + entry);
        return found;
    }

    private void writeChunk(int k) throws Exception {
        long start = System.nanoTime();
        StringBuilder lines = new StringBuilder();
        Worker worker = worker();
        for (Function fn : chunk(k)) {
            if (Thread.currentThread().isInterrupted()) throw new InterruptedException("Chunk " + k + " cancelled");
            lines.append(gson.toJson(decompile(worker.decompiler(), local(worker.program(), fn)))).append('\n');
        }
        commit(chunkPath(k), lines.toString().getBytes(StandardCharsets.UTF_8), false);
        readChunk(k);
        progress(String.format("R2_CHUNK %d/%d %d functions %.1f s", k, chunkCount(), chunk(k).size(), (System.nanoTime() - start) / 1e9));
    }

    private synchronized void progress(String line) { println(line); }

    private JsonObject describe(Function fn) {
        JsonObject r = new JsonObject();
        r.addProperty("entry", key(fn.getEntryPoint()));
        r.addProperty("name", fn.getName(true));
        r.addProperty("thunk", fn.isThunk());
        r.addProperty("body_bytes", fn.getBody().getNumAddresses());
        JsonArray ranges = new JsonArray();
        for (AddressRange range : fn.getBody().getAddressRanges()) {
            JsonArray pair = new JsonArray();
            pair.add(key(range.getMinAddress()));
            pair.add(key(range.getMaxAddress()));
            ranges.add(pair);
        }
        r.add("body_ranges", ranges);
        r.addProperty("signature", fn.getPrototypeString(false, true));
        return r;
    }

    JsonObject decompile(DecompInterface decompiler, Function fn) throws IOException {
        JsonObject r = describe(fn);
        List<String> warnings = new ArrayList<>();
        String code = null, error = null;
        boolean ok = false, timedOut = false;
        long start = System.nanoTime();
        try {
            if (fn.getBody().isEmpty()) error = "Function has no body";
            else {
                DecompileResults result = decompiler.decompileFunction(fn, TIMEOUT_SECONDS, TaskMonitor.DUMMY);
                if (result.failedToStart()) throw new IOException("Decompiler failed to start at " + key(fn.getEntryPoint()) + ": " + result.getErrorMessage());
                timedOut = result.isTimedOut();
                DecompiledFunction recovered = result.getDecompiledFunction();
                code = recovered == null || recovered.getC() == null || recovered.getC().isEmpty() ? null : recovered.getC();
                ok = result.decompileCompleted() && code != null;
                String message = result.getErrorMessage() == null ? "" : result.getErrorMessage().trim();
                if (ok && !message.isEmpty()) warnings.add(message);
                if (!ok) error = !message.isEmpty() ? message : timedOut ? "Timed out after " + TIMEOUT_SECONDS + " s" : "Decompiler returned no code";
                if (code != null)
                    for (String line : code.split("\\R")) if (line.toUpperCase(Locale.ROOT).contains("WARNING")) warnings.add(line.trim());
            }
        } catch (RuntimeException failure) {
            ok = false;
            error = failure.getClass().getName() + ": " + failure.getMessage();
        }
        r.addProperty("state", ok ? (warnings.isEmpty() ? "exported" : "exported-with-warnings") : "failed");
        r.addProperty("error", error);
        r.addProperty("timed_out", timedOut);
        r.addProperty("partial_code", !ok && code != null);
        JsonArray w = new JsonArray();
        warnings.forEach(w::add);
        r.add("warnings", w);
        r.addProperty("ms", (System.nanoTime() - start) / 1_000_000);
        byte[] bytes = code == null ? null : code.getBytes(StandardCharsets.UTF_8);
        r.addProperty("code_bytes", bytes == null ? null : (Number) bytes.length);
        r.addProperty("code_sha256", bytes == null ? null : RecoverySupport.hexDigest(bytes));
        r.addProperty("code", code);
        return r;
    }

    /** Parses and validates committed chunk k against the pinned eligible list; throws on any mismatch. */
    List<JsonObject> readChunk(int k) throws IOException {
        Path path = chunkPath(k);
        List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);
        List<Function> expected = chunk(k);
        if (lines.size() != expected.size()) throw new IOException(path + ": " + lines.size() + " records, expected " + expected.size());
        List<JsonObject> records = new ArrayList<>();
        for (int i = 0; i < lines.size(); i++) {
            JsonObject r = JsonParser.parseString(lines.get(i)).getAsJsonObject();
            String problem = recordProblem(r, key(expected.get(i).getEntryPoint()));
            if (problem != null) throw new IOException(path + " line " + (i + 1) + ": " + problem);
            records.add(r);
        }
        return records;
    }

    static String recordProblem(JsonObject r, String entry) {
        if (!r.get("entry").getAsString().equals(entry)) return "entry " + r.get("entry") + " expected " + entry;
        String state = r.get("state").getAsString();
        if (!STATES.contains(state)) return "unknown state " + state;
        boolean hasCode = !r.get("code").isJsonNull();
        if (state.startsWith("exported") && (!hasCode || r.get("partial_code").getAsBoolean())) return "exported without complete code";
        if (state.equals("failed") && r.get("error").isJsonNull()) return "failure without error";
        if (!hasCode) return r.get("code_sha256").isJsonNull() && r.get("code_bytes").isJsonNull() ? null : "hash without code";
        byte[] bytes = r.get("code").getAsString().getBytes(StandardCharsets.UTF_8);
        if (bytes.length != r.get("code_bytes").getAsLong()) return "code_bytes mismatch";
        return RecoverySupport.hexDigest(bytes).equals(r.get("code_sha256").getAsString()) ? null : "code_sha256 mismatch";
    }

    private JsonObject writeCoverage(JsonObject invocation) throws Exception {
        // Concurrent shard JVMs serialize the scan and write, so the last writer reflects every commit.
        try (FileChannel channel = FileChannel.open(out.resolve("coverage.lock"), StandardOpenOption.CREATE, StandardOpenOption.WRITE);
             FileLock lock = channel.lock()) {
            JsonObject coverage = coverage(invocation);
            commit(out.resolve("coverage.json"), (RecoverySupport.GSON.toJson(coverage) + "\n").getBytes(StandardCharsets.UTF_8), true);
            return coverage;
        }
    }

    private JsonObject coverage(JsonObject invocation) throws Exception {
        Map<String, Long> counts = new TreeMap<>();
        STATES.forEach(s -> counts.put(s, 0L));
        counts.put("pending", 0L);
        JsonArray failures = new JsonArray();
        List<Long> latencies = new ArrayList<>();
        long codeBytes = 0, chunkBytes = 0, timedOut = 0, partial = 0, committed = 0;
        for (int k = 0; k < chunkCount(); k++) {
            if (!Files.exists(chunkPath(k))) { counts.merge("pending", (long) chunk(k).size(), Long::sum); continue; }
            committed++;
            chunkBytes += Files.size(chunkPath(k));
            for (JsonObject r : readChunk(k)) {
                counts.merge(r.get("state").getAsString(), 1L, Long::sum);
                latencies.add(r.get("ms").getAsLong());
                if (!r.get("code_bytes").isJsonNull()) codeBytes += r.get("code_bytes").getAsLong();
                if (r.get("timed_out").getAsBoolean()) timedOut++;
                if (r.get("partial_code").getAsBoolean()) partial++;
                if (r.get("state").getAsString().equals("failed")) {
                    JsonObject f = new JsonObject();
                    for (String field : new String[] {"entry", "name", "error", "timed_out", "partial_code", "ms"}) f.add(field, r.get(field));
                    failures.add(f);
                }
            }
        }
        long sum = counts.values().stream().mapToLong(Long::longValue).sum();
        if (sum != eligible.size()) throw new IllegalStateException("Coverage counts sum to " + sum + ", eligible " + eligible.size());
        JsonObject c = new JsonObject();
        c.addProperty("schema", 1);
        c.addProperty("run_sha256", RecoverySupport.sha(out.resolve("run.json")));
        c.addProperty("eligible", eligible.size());
        c.addProperty("external_excluded", currentProgram.getFunctionManager().getFunctionCount() - eligible.size());
        c.add("counts", gson.toJsonTree(counts));
        c.addProperty("attempted", eligible.size() - counts.get("pending"));
        c.addProperty("successful", counts.get("exported") + counts.get("exported-with-warnings"));
        c.addProperty("timed_out", timedOut);
        c.addProperty("partial_code", partial);
        c.addProperty("chunks_committed", committed);
        c.addProperty("chunk_count", chunkCount());
        c.addProperty("chunk_bytes", chunkBytes);
        c.addProperty("code_bytes", codeBytes);
        c.add("latency_ms", percentiles(latencies));
        c.add("last_invocation", invocation);
        c.add("failures", failures);
        return c;
    }

    static JsonObject percentiles(List<Long> values) {
        Collections.sort(values);
        JsonObject p = new JsonObject();
        if (values.isEmpty()) return p;
        for (int q : new int[] {50, 90, 99}) p.addProperty("p" + q, values.get((int) Math.min(values.size() - 1, (long) values.size() * q / 100)));
        p.addProperty("max", values.get(values.size() - 1));
        p.addProperty("sum", values.stream().mapToLong(Long::longValue).sum());
        return p;
    }

    /** Durable atomic write: temp file, fsync, then rename (replace) or hard link (first committer wins). */
    static void commit(Path path, byte[] bytes, boolean replace) throws IOException {
        Path temp = path.resolveSibling("." + path.getFileName() + "." + UUID.randomUUID() + ".tmp");
        try {
            try (FileChannel channel = FileChannel.open(temp, StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE)) {
                ByteBuffer buffer = ByteBuffer.wrap(bytes);
                while (buffer.hasRemaining()) channel.write(buffer);
                channel.force(true);
            }
            if (replace) Files.move(temp, path, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
            else Files.createLink(path, temp);
        } finally {
            Files.deleteIfExists(temp);
        }
    }
}
