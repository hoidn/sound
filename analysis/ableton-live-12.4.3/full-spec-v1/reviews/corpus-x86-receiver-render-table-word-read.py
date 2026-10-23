"""Root one selected8B nominal table word as DATA; never follow/execute its value."""
from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
IMAGE=B/'depth-corpus-x86-selected-entry-actual-r5/input/Corpus.x86_64'
HEADER=B/'depth-corpus-x86-receiver-construction-entry-preparation/header-map.json'
PEER=B/'reviews/corpus-x86-receiver-construction-entry-actual-review.json'
OUT=B/'depth-corpus-x86-receiver-render-table-word'
VA,OFFSET,LENGTH=0x30648,0x30648,8

def identity(p):
 d=p.read_bytes();return dict(path=str(p),bytes=len(d),sha256=hashlib.sha256(d).hexdigest())
def save(n,v):
 with (OUT/n).open('x') as f:json.dump(v,f,indent=2);f.write('\n')

assert not OUT.exists()
assert identity(PEER)['sha256']=='6d6c1fc710fcb7fe4e7a5966d1e4f588f13f69452c8c3bb09ea1483a0d09531a'
assert identity(HEADER)['sha256']=='de3147e1fdf55348164e76a8a5ab45cf246778a1e69637ae89c782c3c5890ce7'
OUT.mkdir()
save('selection.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),selector='Root separateone8Bnominaltableword afterfull7877B actualpeer',nominal_firstword='0x30628',slot='0x20',va=hex(VA),length=8,peer=identity(PEER),method=identity(Path(__file__).resolve()),scope='Exactoneword only; no tableinventory, pointedtarget/rawbody, currentinstance/relocation/runtime or nativeextent proof.'))
paths=[IMAGE,HEADER,PEER,Path(__file__).resolve(),OUT/'selection.json']
before=[identity(p) for p in paths];save('before-map.json',before)
assert before[0]['bytes']==250352 and before[0]['sha256']=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
m=json.loads(HEADER.read_text())
segments=[s for s in m['segments'] if s['vmaddr']<=VA and VA+LENGTH<=s['vmaddr']+s['filesize']]
assert segments==[dict(name='__DATA',vmaddr=196608,vmsize=16384,fileoff=196608,filesize=16384,maxprot=3,initprot=3,nsects=7,flags=0)]
assert OFFSET==segments[0]['fileoff']+VA-segments[0]['vmaddr']
with IMAGE.open('rb') as f:
 h=f.read(32);assert h.hex()==m['header_hex'] and struct.unpack_from('<II',h,16)==(14,1696)
 lc=f.read(1696);assert hashlib.sha256(lc).hexdigest()==m['load_commands_sha256']
 f.seek(OFFSET);raw=f.read(LENGTH)
assert len(raw)==8
assert struct.unpack('<Q',bytes.fromhex('0100000000000000'))[0]==1
assert struct.unpack('<Q',bytes.fromhex('ffffffffffffffff'))[0]==2**64-1
save('result.json',dict(va=hex(VA),raw_hex=raw.hex(),unsigned_little64=hex(struct.unpack('<Q',raw)[0]),decoder_children=0,original_calls=0,limits='Rawnominaltableword only. No pointedtarget interpretation or actualruntimevptr/table/type/model/ABI/codebinding proof.'))
after=[identity(p) for p in paths];save('after-map.json',after);assert before==after
save('manifest.json',dict(files=[dict(path=p.name,bytes=identity(p)['bytes'],sha256=identity(p)['sha256']) for p in sorted(OUT.iterdir()) if p.is_file()],unchanged=True,scope='Fivefixedpairs/no globalpreservation/pretryIOguarantee.'))
print(json.dumps(dict(raw=raw.hex(),unsigned_little64=hex(struct.unpack('<Q',raw)[0]),unchanged=True)))
