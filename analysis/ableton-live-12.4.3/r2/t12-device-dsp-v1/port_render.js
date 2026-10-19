// Render cases through the traced-engine port embedded in
// analysis/ableton-live-12.4.3/demos/corpus-traced/index.html (first <script> block), for comparison
// with extracted-execution renders. Analyst material only.
//
//   node port_render.js CASES.json OUTDIR
//
// CASES.json: [{name, fs, block, input (interleaved stereo binary32 file), frames, params: {host index: value}}].
// The port takes Live parameter names; each host value is passed unchanged, except FilterMidFreq,
// which the port converts from Hz itself (so Hz = 50 * 360^value is passed). Writes OUTDIR/<name>.f32.
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '../../demos/corpus-traced/index.html'), 'utf8');
const start = html.indexOf('<script>') + 8, end = html.indexOf('</script>', start);
const sandbox = {module: {exports: {}}, Math, Float32Array, Float64Array, console};
vm.runInNewContext(html.slice(start, end), sandbox);
const {CorpusEngine, HOST} = sandbox.module.exports;
const NAME = {};
for (const [name, h] of Object.entries(HOST)) NAME[h[0]] = name;

const [casesFile, outDir] = process.argv.slice(2);
for (const c of JSON.parse(fs.readFileSync(casesFile, 'utf8'))) {
  const e = new CorpusEngine(c.fs);
  for (const [idx, v] of Object.entries(c.params)) {
    const name = NAME[idx];
    if (name) e.setLive(name, name === 'FilterMidFreq' ? 50 * Math.pow(360, v) : v);
  }
  const buf = fs.readFileSync(c.input), x = new Float32Array(buf.buffer, buf.byteOffset, buf.length / 4);
  const out = new Float32Array(2 * c.frames);
  for (let s = 0; s < c.frames; s += c.block) {
    const n = Math.min(c.block, c.frames - s);
    const inL = new Float32Array(n), inR = new Float32Array(n), oL = new Float32Array(n), oR = new Float32Array(n);
    for (let i = 0; i < n; i++) { inL[i] = x[2 * (s + i)]; inR[i] = x[2 * (s + i) + 1]; }
    e.process(inL, inR, oL, oR);
    for (let i = 0; i < n; i++) { out[2 * (s + i)] = oL[i]; out[2 * (s + i) + 1] = oR[i]; }
  }
  fs.writeFileSync(path.join(outDir, c.name + '.f32'), Buffer.from(out.buffer));
}
