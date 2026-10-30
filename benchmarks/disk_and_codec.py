"""Actual directory scan and compression experiments, generated fixtures."""
import sys, tempfile, time, json, random, platform, tracemalloc, gc, statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from smartfile.core import top_k, scan_files, select_top_k
from smartfile.operations import process, sha256
out={}
with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    for j in range(100):
        sub=root/f'd{j:03d}';sub.mkdir()
        for i in range(100):
            (sub/f'f{i:03d}.bin').write_bytes(b'x'*((i*131+j*97)%2048))
    oracle=sorted(((p.stat().st_size,str(p)) for p in root.rglob('*.bin')),reverse=True)[:10]
    times=[]
    for _ in range(5):
        t=time.perf_counter();rows,n,errors=top_k(root,10);times.append(time.perf_counter()-t)
        assert rows==oracle and n==10000 and not errors
    comparison=[]
    for mode in ('heap','sort'):
        def run():
            records=scan_files(root)
            return select_top_k(records,10) if mode=='heap' else sorted(records,reverse=True)[:10]
        run()
        for repeat in range(5):
            gc.collect();t=time.perf_counter();result=run();elapsed=time.perf_counter()-t
            assert result==oracle
            gc.collect();tracemalloc.start();result=run();_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
            assert result==oracle
            comparison.append(dict(algorithm=mode,repeat=repeat+1,seconds=elapsed,peak_python_bytes=peak))
    out['disk_comparison']=comparison
    out['disk_scan']={'actual_files':n,'k':10,'seconds':times,'oracle_match':True,'bytes':'0..2047','layout':'100 directories x 100 regular files'}
with tempfile.TemporaryDirectory() as d:
    root=Path(d);rows=[]
    for name,data in [('repeated_text',('CTDL GT: Min-Heap va Huffman.\n'*20000).encode()),('uniform_bytes',bytes(range(256))*2048),('seeded_random',random.Random(18).randbytes(524288)),('empty',b'')]:
        a=root/name;b=root/(name+'.huf');c=root/(name+'.restored');a.write_bytes(data)
        t=time.perf_counter();result=process('compress',a,b);ct=time.perf_counter()-t
        t=time.perf_counter();dec=process('decompress',b,c);dt=time.perf_counter()-t
        assert sha256(a)==sha256(c)
        rows.append(dict(dataset=name,**result,compress_s=ct,decompress_s=dt,sha256_match=True))
    out['huffman']=rows
Path(__file__).with_name('disk_and_codec.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
