"""Transport lifecycle tests use a fake protocol peer; never open a binary."""
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'run_native_analysis.mjs'
PEER = r'''import {createInterface} from 'node:readline';
if(process.env.HOPPER_TARGET_PATH)process.exit(51);
const r=createInterface({input:process.stdin});
r.on('line',s=>{let m=JSON.parse(s);if(!m.id)return;
if(m.method==='tools/call')return;
process.stdout.write(JSON.stringify({jsonrpc:'2.0',id:m.id,result:m.method==='initialize'?{protocolVersion:'2024-11-05',capabilities:{},serverInfo:{name:'fake',version:'1'}}:{tools:[]}})+'\n');});
'''

class TransportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.spool=self.base/'spool'
        self.peer=self.base/'peer.mjs';self.peer.write_text(PEER);self.proc=None
    def tearDown(self):
        if self.proc and self.proc.poll() is None:self.proc.kill();self.proc.wait()
        if self.proc:
            self.proc.stdout.close();self.proc.stderr.close()
        self.tmp.cleanup()
    def wait_file(self,path,timeout=5):
        stop=time.monotonic()+timeout
        while time.monotonic()<stop:
            if path.exists():return json.loads(path.read_text())
            time.sleep(.03)
        self.fail(f'Timeout waiting for {path}')
    def start(self):
        self.proc=subprocess.Popen(['node',str(SCRIPT),str(self.spool)],env={**os.environ,'NATIVE_REA_ENTRY':str(self.peer),'HOPPER_TARGET_PATH':'MUST_NOT_OPEN'},stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.wait_file(self.spool/'tools.json')
    def request(self,name,value):
        path=self.spool/'requests'/name;path.write_text(json.dumps(value));return self.spool/'results'/name
    def test_handshake_shutdown_and_request_hash(self):
        self.start();p=self.request('001.json',{'method':'tools/list'})
        r=self.wait_file(p);self.assertTrue(r['ok']);self.assertEqual(len(r['request_sha256']),64)
        self.request('999.json',{'method':'shutdown'});self.assertEqual(self.proc.wait(5),0)
    def test_timeout_halts_queue(self):
        self.start();self.request('001.json',{'method':'tools/call','params':{'name':'slow'},'timeout_ms':50})
        self.request('002.json',{'method':'tools/list'})
        r=self.wait_file(self.spool/'results'/'001.json');self.assertFalse(r['ok']);self.proc.wait(5)
        self.assertFalse((self.spool/'results'/'002.json').exists())
    def test_signal_interrupts_active_call(self):
        self.start();self.request('001.json',{'method':'tools/call','params':{'name':'slow'}})
        self.wait_file(self.spool/'accepted'/'001.json');time.sleep(.1);self.proc.send_signal(signal.SIGTERM)
        self.proc.wait(5);r=json.loads((self.spool/'results'/'001.json').read_text());self.assertFalse(r['ok'])
    def test_mutated_replay_rejected(self):
        self.start();p=self.request('001.json',{'method':'tools/list'});self.wait_file(p)
        self.request('001.json',{'method':'tools/list','params':{'changed':True}})
        self.assertNotEqual(self.proc.wait(5),0)

if __name__=='__main__':unittest.main()
