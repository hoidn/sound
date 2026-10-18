# Throughput from chunk commit times: start = last commit - in-JVM decompile_seconds.
import os, json, glob, re, sys
def rates(run):
    inv = json.loads(re.search(r'R2_INVOCATION (\{.*?\})', open(f'{run}/stdout.txt').read()).group(1))
    times = sorted(os.path.getmtime(f) for f in glob.glob(f'{run}/corpus/chunks/chunk-*.jsonl'))
    start = times[-1] - inv['decompile_seconds']
    t50 = times[len(times)//2 - 1] - start
    cov = json.load(open(f'{run}/corpus/coverage.json'))
    tm = open(f'{run}/time.txt').read()
    cpu = re.search(r'Percent of CPU this job got: (\d+)%', tm).group(1)
    wall = re.search(r'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\S+)', tm).group(1)
    peak = json.load(open(f'{run}/result.json'))['peak_group_rss_kb']
    return dict(run=os.path.basename(run), threads=inv['threads'], instances=inv.get('instances',1), wall=wall, decompile_s=round(inv['decompile_seconds'],1),
                t50_s=round(t50,1), fn_per_s_first_half=round(0.5*12626/t50), latency_sum_s=round(cov['latency_ms']['sum']/1000), cpu_pct=int(cpu), peak_group_rss_mib=round(peak/1024))
for run in sys.argv[1:]: print(json.dumps(rates(run)))
