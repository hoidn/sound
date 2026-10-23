"""Analyst-only packaging of retained audio/data. Never executes original code."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct

HERE = Path(__file__).resolve().parent
OUT = HERE.with_name('device-collision-v1')
ROOT = HERE.parents[3]
SOURCE = ROOT/'analysis/ableton-live-12.4.3/r2/t12-collision-v1'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=1, allow_nan=False)+'\n')


def label(name):
    name = name.replace('DummyPerNotePitchBendRange', 'Reserved per note pitch bend range')
    name = name.replace('/', ' ').replace('OnOff', 'enabled').replace('ListeningXL', 'left listening position').replace('ListeningXR', 'right listening position').replace('HitX', 'hit position')
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = re.sub(r'([a-zA-Z])([12])', r'\1 \2', name)
    return name


def main():
    manifest = json.loads((SOURCE/'manifest.json').read_text())
    recovered = {'run_collision.py': 'recovery/originals/run_collision.py', 'results/collision.json': 'recovery/originals/collision.json'}
    verified = []
    for logical, entry in manifest['files'].items():
        physical = recovered.get(logical, logical)
        data = (SOURCE/physical).read_bytes()
        assert digest(data) == entry['sha256'] and len(data) == entry['bytes'], logical
        verified.append({'logical':logical, 'physical':physical, 'sha256':digest(data), 'bytes':len(data)})
    assert len(verified) == 103
    results = json.loads((SOURCE/recovered['results/collision.json']).read_text())
    table = SOURCE.parent/'n6-device-tables-v1/out/conversions.tsv'
    table_record = next(v for k,v in manifest['external_inputs'].items() if k.endswith('/n6-device-tables-v1/out/conversions.tsv'))
    assert digest(table.read_bytes()) == table_record['sha256']
    names = {int(r['index']): label(r['stored_name']) for r in csv.DictReader(table.open(),delimiter='\t') if r['device']=='Collision' and r['index']}
    assert set(names) == set(range(139))
    cases, traces = [], []
    for caseid, tag, metric in [('DEVICE-COLLISION-001','ctor_c4',{'kind':'peak','maximum':1e-18}), ('DEVICE-COLLISION-002','wg_pipe',{'kind':'stereo_relative_rms','maximum':0.003})]:
        lines = [x.split() for x in (SOURCE/f'raw/{tag}.script').read_text().splitlines()]
        params = [(int(x[1]),float(x[2])) for x in lines if x[0]=='param']
        assert [x[0] for x in params] == list(range(139))
        processes = [x for x in lines if x[0]=='process']
        assert len(processes)==2 and processes[0]==['process','11264','512']
        frames=int(processes[1][1]);assert processes[1][2]=='512'
        events = [{'frame':int(x[1]),'status':int(x[2],0),'key':int(x[3]),'velocity':int(x[4])} for x in lines if x[0]=='event']
        wav=(SOURCE/f'raw/{tag}.wav').read_bytes();assert digest(wav)==results['reference_renders'][tag]['sha256']
        assert wav[:4]==b'RIFF' and wav[8:12]==b'WAVE'
        chunks={};pos=12
        while pos+8<=len(wav):
            name=wav[pos:pos+4];size=struct.unpack_from('<I',wav,pos+4)[0];chunks[name]=wav[pos+8:pos+8+size];pos+=8+size+(size%2)
        fmt=struct.unpack_from('<HHIIHH',chunks[b'fmt ']);assert fmt==(3,2,44100,352800,8,32)
        data=chunks[b'data'];assert len(data)==frames*8
        dest=f'reference/{caseid}.f32';(OUT/dest).write_bytes(data)
        cases.append({'id':caseid,'requirements':['REQ-DEVICE-COLLISION-001','REQ-DEVICE-COLLISION-002','REQ-DEVICE-COLLISION-003'] if caseid=='DEVICE-COLLISION-001' else ['REQ-DEVICE-COLLISION-001','REQ-DEVICE-COLLISION-014'], 'label':'Disabled resonators produce effectively silent output' if caseid=='DEVICE-COLLISION-001' else 'Pipe resonator, held C4', 'sample_rate_hz':44100,'frames':frames,'channels':2,'parameter_values':[{'name':names[i], 'binary32_hex':struct.pack('<f',v).hex(),'value':struct.unpack('<f',struct.pack('<f',v))[0]} for i,v in params], 'events':events,'reference':dest,'reference_sha256':digest(data),'metric':metric,'window_frames':[0,frames]})
        traces.append({'case':caseid, 'draft_case':'DCL-001' if caseid=='DEVICE-COLLISION-001' else 'DCL-031','source_wav':f'raw/{tag}.wav','source_script':f'raw/{tag}.script','source_wav_sha256':digest(wav),'source_script_sha256':digest((SOURCE/f'raw/{tag}.script').read_bytes()),'extraction':'RIFF IEEE-float data chunk copied verbatim; no sample conversion','output_sha256':digest(data),'source_result_row':f'reference_renders.{tag}'})
    save(OUT/'cases.json',{'schema':'device-audio-cases-v1','cases':cases})
    calibration=json.loads((SOURCE/'results/libm_sensitivity.json').read_text())
    pipe=next(x for x in calibration if x['case']=='pipe')
    assert max(pipe[d]['rel_rms_all'] for d in ['+1','-1'])<0.003
    save(HERE/'traceability.json',{'source':str(SOURCE.relative_to(ROOT)), 'source_manifest_sha256':digest((SOURCE/'manifest.json').read_bytes()),'mapping':recovered,'cases':traces,'calibration':{'path':'results/libm_sensitivity.json','sha256':digest((SOURCE/'results/libm_sensitivity.json').read_bytes()),'row':pipe,'method':'libm_sensitivity.py:rel; whole 32768-frame stereo relative RMS','limitation':'perturbed audio not retained; summaries establish x86_64 libm sensitivity only, no arm64 bound'},'excluded':'Every other DCL case; modal log-radius/complex-amplitude perturbation calibration missing; no noise metric; no Tube/pitch-envelope portable calibration'})
    save(HERE/'source-validation.json',{'pass':True,'original_payloads_verified':len(verified),'files':verified,'no_original_execution':True})
    inventory=[]
    for p in sorted(OUT.rglob('*')):
        if p.is_file() and p.name!='manifest.json':
            b=p.read_bytes();inventory.append({'path':str(p.relative_to(OUT)),'sha256':digest(b),'bytes':len(b)})
    reqs=sorted({r for c in cases for r in c['requirements']})
    save(OUT/'manifest.json',{'schema':'handoff-manifest-v1','release_id':'device-collision-v1','release_status':'staged-unreviewed','release_date':None,'target':'Ableton Live 12 Suite 12.4.3 / macOS; references are prior original x86_64 extracted execution','specification':{'id':'SPEC-DEVICE-COLLISION','parent_revision':1,'release_revision':1},'feature_ids':['FEAT-DEVICES'],'partial_requirement_scopes':{r:'Only the listed fixed-vector two-case boundary and Pipe output measurements; no general synthesis law or host integration' for r in reqs},'unreleased_requirements':[f'REQ-DEVICE-COLLISION-{n:03}' for n in range(1,19) if f'REQ-DEVICE-COLLISION-{n:03}' not in reqs], 'compatibility_dimensions':{'audio':'Two finite outputs, proposed project metrics; no arm64 bound','behavior':'Fixed vectors, silent input and listed events only','timing':'Fixed warm-up and partitions only; no event-grid generalization','files':'excluded','ui':'excluded','real-time':'excluded'},'fixture_origin':'Original-device output captures from synthetic note input; no executable, recovered source or shipped music','approved_public_sources':[], 'review':{'status':'pending','reviewers':[],'date':None,'findings':[],'disposition':'Unreviewed finite candidate; metric acceptance and source exclusion require separate review'},'reference_execution':'Previously extracted original x86_64 device code; whole application and arm64 not run','candidate_execution':'not-run','entrypoint':'README.md','case_count':len(cases),'evaluation_count':len(cases),'inventory_excludes':['manifest.json'],'files':inventory})
    print('Built two-case unreviewed Collision candidate; verified 103 original payloads through recovery mapping')


if __name__=='__main__':
    main()
