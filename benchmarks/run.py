"""Reproducible selection benchmark; records are generated, not disk files."""
import csv, gc, hashlib, json, platform, random, statistics, sys, time, tracemalloc
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from smartfile.core import select_top_k
OUT=Path(__file__).parent

def records(n):
    rng=random.Random(18)
    for i in range(n):
        yield rng.randrange(1, 100000000), f'dataset/subfolder/file_{i:06d}.bin'

def run(mode,n,k):
    values=records(n)
    return select_top_k(values,k) if mode=='heap' else sorted(values,reverse=True)[:k]

def main():
    rows=[]
    for n in (10000,25000,50000):
        for k in (10,100,1000):
            expected=run('sort',n,k)
            for mode in ('heap','sort'):
                run(mode,n,k) # warmup
                for repeat in range(5):
                    gc.collect(); start=time.perf_counter(); result=run(mode,n,k); elapsed=time.perf_counter()-start
                    assert result==expected
                    gc.collect(); tracemalloc.start(); measured=run(mode,n,k); _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
                    assert measured==expected
                    rows.append(dict(n=n,k=k,algorithm=mode,repeat=repeat+1,seconds=elapsed,peak_python_bytes=peak,correct=True))
    with (OUT/'raw.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    summary=[]
    for n in (10000,25000,50000):
        for k in (10,100,1000):
            for mode in ('heap','sort'):
                group=[r for r in rows if (r['n'],r['k'],r['algorithm'])==(n,k,mode)]
                summary.append(dict(n=n,k=k,algorithm=mode,median_ms=statistics.median(r['seconds'] for r in group)*1000,median_peak_kib=statistics.median(r['peak_python_bytes'] for r in group)/1024))
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2))
    (OUT/'environment.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'processor':platform.processor(),'seed':18,'repeats':5,'measurement':'Separate untraced timing and traced allocation runs; excludes fixture disk IO; includes generator; peak is Python allocation, not RSS','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
    print(json.dumps([r for r in summary if r['n']==50000 and r['k']==10],indent=2))
if __name__=='__main__':main()
