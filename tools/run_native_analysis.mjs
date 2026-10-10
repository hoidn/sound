#!/usr/bin/env node
// Analyst-only MCP transport. No implicit binary open or analysis.
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {createInterface} from 'node:readline';
import {mkdir, readFile, writeFile, rename, readdir, unlink, open} from 'node:fs/promises';
import {resolve, join} from 'node:path';

const root = resolve(process.argv[2] || '');
if (!process.argv[2]) throw new Error('Usage: node tools/run_native_analysis.mjs SPOOL_DIRECTORY');
await mkdir(root, {recursive:true});
const lock = await open(join(root,'transport.lock'),'wx');
await lock.writeFile(`${process.pid}\n`);
for (const name of ['requests','accepted','results']) await mkdir(join(root,name),{recursive:true});
const rea = process.env.NATIVE_REA_ENTRY || '/opt/homebrew/lib/node_modules/rea-agents/scripts/rea.mjs';
const childEnv={...process.env,
  HOPPER_TARGET_PATH: undefined,

  REA_GHIDRA_STARTUP_TIMEOUT_MS: process.env.REA_GHIDRA_STARTUP_TIMEOUT_MS || '3600000',
  GHIDRA_HEADLESS_MAXMEM: process.env.GHIDRA_HEADLESS_MAXMEM || '4G'};
delete childEnv.HOPPER_TARGET_PATH;
const child = spawn(process.execPath,[rea,'mcp'],{stdio:['pipe','pipe','pipe'],env:childEnv});
const pending = new Map();
let next = 1, stopping = false, dead = false;
const log = await open(join(root,`transport-${Date.now()}.jsonl`),'wx');
let logQueue=Promise.resolve();
const event = (value) => {logQueue=logQueue.then(()=>log.writeFile(JSON.stringify({at:new Date().toISOString(),...value})+'\n')); return logQueue;};
const exited=new Promise(resolve=>child.once('close',resolve));
child.stderr.on('data', bytes => event({kind:'stderr',text:bytes.toString()}));
function rejectAll(error) { dead=true; for (const {reject,timer} of pending.values()) {clearTimeout(timer);reject(error);} pending.clear(); }
child.on('error',rejectAll);
child.stdin.on('error',rejectAll);
child.on('exit',(code,signal) => {event({kind:'server-exit',code,signal}); rejectAll(new Error(`REA server exited ${code}/${signal}`));});
const lines=createInterface({input:child.stdout});
lines.on('line', line => {
  let message; try { message=JSON.parse(line); } catch {rejectAll(new Error('Non-JSON MCP stdout')); return;}
  if (message.id !== undefined && pending.has(message.id)) {
    const p=pending.get(message.id);pending.delete(message.id);clearTimeout(p.timer);
    message.error ? p.reject(Object.assign(new Error(message.error.message),{rpc:message.error})) : p.resolve(message.result);
  } else if (message.method && message.id !== undefined) {
    child.stdin.write(JSON.stringify({jsonrpc:'2.0',id:message.id,error:{code:-32601,message:'Client method unsupported'}})+'\n');
  }
});
function rpc(method,params,timeout=60000) {
  if (dead || stopping) return Promise.reject(new Error('REA transport is closed or stopping'));
  const id=next++;
  return new Promise((resolve,reject) => {
    const timer=setTimeout(()=>{stopping=true;pending.delete(id);cancel(id,'Controller deadline');reject(new Error(`Deadline exceeded for ${method}; session uncertain, queue halted`));},timeout);
    pending.set(id,{resolve,reject,timer});child.stdin.write(JSON.stringify({jsonrpc:'2.0',id,method,params})+'\n');
  });
}
async function save(path,value) {
  const content=JSON.stringify(value,null,2)+'\n';
  try {const existing=await readFile(path,'utf8');if(existing!==content) throw new Error(`Refusing overwrite: ${path}`);return;}catch(e){if(e.code!=='ENOENT')throw e;}
  const temp=path+`.tmp-${process.pid}`;await writeFile(temp,content,{flag:'wx'});await rename(temp,path);
}
function cancel(id,reason) {if(!child.stdin.destroyed)child.stdin.write(JSON.stringify({jsonrpc:'2.0',method:'notifications/cancelled',params:{requestId:id,reason}})+'\n');}
function stop(signal) {stopping=true;for(const [id,p] of pending){clearTimeout(p.timer);cancel(id,signal);p.reject(new Error(`${signal}: session uncertain, queue halted`));}pending.clear();}
process.on('SIGINT',()=>stop('SIGINT'));process.on('SIGTERM',()=>stop('SIGTERM'));
try {
  const init=await rpc('initialize',{protocolVersion:'2024-11-05',capabilities:{},clientInfo:{name:'sound-native-export',version:'1'}});
  child.stdin.write(JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})+'\n');
  await save(join(root,'initialize.json'),init);
  await save(join(root,'tools.json'),await rpc('tools/list',{}));
  await event({kind:'ready',pid:process.pid,server_pid:child.pid,rea});
  while (!stopping && !dead) {
    for (const file of (await readdir(join(root,'requests'))).sort()) {
      if(stopping||dead)break;
      if (!/^[a-zA-Z0-9_-]+\.json$/.test(file)) continue;
      const resultPath=join(root,'results',file);
      const requestBytes=await readFile(join(root,'requests',file));
      const requestHash=createHash('sha256').update(requestBytes).digest('hex');
      const request=JSON.parse(requestBytes);
      const accepted={request_sha256:requestHash,request};
      try {const previous=JSON.parse(await readFile(resultPath,'utf8'));if(previous.request_sha256!==requestHash)throw new Error(`Request changed after completion: ${file}`);continue;}catch(e){if(e.code!=='ENOENT')throw e;}
      const acceptedPath=join(root,'accepted',file);
      try {await readFile(acceptedPath);throw new Error(`Interrupted request requires new identifier and owner reconciliation: ${file}`);}catch(e){if(e.code!=='ENOENT')throw e;}
      await save(acceptedPath,accepted);
      if(request.method==='shutdown') {await save(resultPath,{...accepted,shutdown:true});stopping=true;break;}
      if(!['tools/call','tools/list'].includes(request.method)) throw new Error('Only tools/call, tools/list, shutdown accepted');
      const start=Date.now(); await event({kind:'request-start',file,method:request.method,name:request.params?.name});
      let result;try {result={ok:true,result:await rpc(request.method,request.params || {},request.timeout_ms || 3660000)};}
      catch(e) {result={ok:false,error:{message:e.message,rpc:e.rpc || null}};}
      await save(resultPath,{...accepted,...result,elapsed_ms:Date.now()-start});await event({kind:'request-complete',file,ok:result.ok});
      if(stopping||dead)break;
    }
    if(!stopping&&!dead)await new Promise(r=>setTimeout(r,250));
  }
} finally {
  child.stdin.end();
  const term=setTimeout(()=>child.kill('SIGTERM'),3000);
  const kill=setTimeout(()=>child.kill('SIGKILL'),6000);
  await Promise.race([exited,new Promise((_,reject)=>{const timer=setTimeout(()=>reject(new Error('Owned REA server did not close within 9s; inspect watchdog descendants')),9000);timer.unref();})]);clearTimeout(term);clearTimeout(kill);
  await event({kind:'transport-stop'});await logQueue;await log.close();await lock.close();await unlink(join(root,'transport.lock'));
}
