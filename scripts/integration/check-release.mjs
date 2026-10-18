import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const spec=read('spec/resolved.json'), report=read('design/fit-v1/model-report.json'), native=read('design/fit-v1/native-verification.json');
for(const evidence of [report,native]){assert.equal(evidence.sourceSpecHash,spec.sourceSpecHash);assert.equal(evidence.geometryHash,spec.geometryHash);assert.equal(evidence.physicalFitValidated,false);assert(!evidence.checks.some(c=>c.status==='FAIL'));}
assert.deepEqual(native.failures,[]);
const media=read('design/fit-v1/media-manifest.json');
assert.equal(media.sourceSpecHash,spec.sourceSpecHash);assert.equal(media.geometryHash,spec.geometryHash);assert.equal(media.complete,true);assert.equal(media.builtMeshHash,report.builtMeshHash);
const framing=read('design/fit-v1/framing-check.json');assert.equal(framing.sourceSpecHash,spec.sourceSpecHash);assert.equal(framing.geometryHash,spec.geometryHash);assert.equal(framing.checks.length,2);for(const camera of framing.checks)assert.equal(camera.allFramesInside,true,'Animation camera clips geometry');
const required=['assembled.png','underside.png','section.png','rear-usb.png','assembly.mp4','switch-motion.mp4','glow.mp4'];
const manifestFiles=Array.isArray(media.files)?Object.fromEntries(media.files.map(f=>[f.filename??f.file??f.path,f])):media.files;
for(const filename of required){
 const path='design/fit-v1/'+filename, file=manifestFiles[filename];assert(file,'Missing media provenance '+filename);
 const hash=crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex');assert.equal(file.sha256,hash,'Media digest mismatch '+filename);
 const deployed='dist/previews/'+filename;assert(fs.existsSync(deployed),'Missing public preview '+filename);assert.equal(crypto.createHash('sha256').update(fs.readFileSync(deployed)).digest('hex'),hash,'Public preview differs '+filename);
 if(filename.endsWith('.mp4')){
  const probe=spawnSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',path],{encoding:'utf8'});assert.equal(probe.status,0,probe.stderr);
  const data=JSON.parse(probe.stdout),v=data.streams.find(s=>s.codec_type==='video');assert.equal(v.width,960);assert.equal(v.height,720);assert.equal(v.avg_frame_rate,'24/1');
  const expected=filename==='assembly.mp4'?12:filename==='switch-motion.mp4'?4:8;assert(Math.abs(Number(data.format.duration)-expected)<.05,'Clip duration '+filename);
  const decode=spawnSync('ffmpeg',['-v','error','-i',path,'-f','null','-'],{encoding:'utf8'});assert.equal(decode.status,0,decode.stderr);assert.equal(decode.stderr,'','Video decode errors');
 }
}
const nativeFile='design/fit-v1/keypad-fit-v1.blend';assert.equal(crypto.createHash('sha256').update(fs.readFileSync(nativeFile)).digest('hex'),manifestFiles['keypad-fit-v1.blend'].sha256,'Native scene differs from rendered provenance');
console.log('Release media verified: 4 stills, 3 fully decoded 24 fps clips, matching specification and deployed asset digests.');
