import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const read=p=>fs.readFileSync(new URL('../../'+p,import.meta.url),'utf8');
const a=JSON.parse(read('spec/keypad.json')),p=JSON.parse(read('spec/parts.json')),m=JSON.parse(read('spec/resolved.json'));
const hash=crypto.createHash('sha256').update(read('spec/keypad.json')+'\n'+read('spec/parts.json')).digest('hex');
assert.equal(m.sourceSpecHash,hash,'Resolved specification is stale');
assert.equal(m.units,'mm');assert.equal(m.layout.keys.length,28);
const expected=[['Esc','1','2','3','4','dial'],['Tab','Q','W','E','R','T'],['Caps','A','S','D','F','G'],['Shift','Z','X','C','V','B'],['Ctrl','Alt','Space','Space','Fn','5']];
for(const k of m.layout.keys){assert.equal(expected[k.row][k.column],k.label);assert.equal(k.units,k.id==='space'?2:1);assert(k.center.every(Number.isFinite));}
assert.equal(m.layout.encoder.row,0);assert.equal(m.layout.encoder.column,5);
assert(Math.abs(m.custom.keycap_2u.width-m.custom.keycap_1u.width-m.layout.pitch)<1e-9);
assert.equal(m.datums.plateTop-m.datums.pcbTop,5);
assert.equal(m.datums.plateTop-m.datums.plateBottom,1.5);
assert.equal(m.datums.pcbTop-m.datums.pcbBottom,1.5);
assert(m.custom.keycap_1u.bottomZ-m.fitPolicy.switchWorstCaseTravel>=.3);
assert(m.custom.keycap_1u.minInnerRoofZ-m.fitPolicy.switchWorstCaseTravel-6.2>=.3);
assert.deepEqual(m.custom.riser.angles,[0,4,7]);
assert(m.custom.riser.minimumNoseHeight>=2&&m.custom.riser.endRadius>=2);
assert.equal(m.scope.physicalFitValidated,false);assert.equal(m.scope.firmware,false);
for(const pose of Object.values(m.poses))assert(pose.translation.every(Number.isFinite));
assert(p.parts&&Object.keys(p.parts).length>=15);
const reportPath=new URL('../../design/fit-v1/model-report.json',import.meta.url);
if(fs.existsSync(reportPath)){const report=JSON.parse(fs.readFileSync(reportPath,'utf8'));assert.equal(report.sourceSpecHash,hash,'Blender report is stale');assert.equal(report.physicalFitValidated,false);assert.equal(report.keys,28);}
console.log('Shared specification verified:28 keys,2u Space,source hash,datums,cap sweep allowance and3riser poses.');
// Reject stale native evidence and known failed checks when native deliverables exist.
const nativePath=new URL('../../design/fit-v1/native-verification.json',import.meta.url);
if(fs.existsSync(nativePath)){
 const native=JSON.parse(fs.readFileSync(nativePath,'utf8'));
 assert.equal(native.sourceSpecHash,hash,'Native Blender verification is stale');
 assert.equal(native.geometryHash,m.geometryHash,'Native Blender geometry differs');
 assert.equal(native.physicalFitValidated,false);
 assert.deepEqual(native.failures,[],'Native model has failed checks');
 assert(native.checks.length>=21,'Native verification incomplete');assert.equal(native.checks.find(c=>c.id==='visible_emissive_roof_for_all_28_legends')?.status,'PASS','Every legend needs a visible white roof');
 assert(!native.checks.some(c=>c.status==='FAIL'),'Failed native check');
}
const report=fs.existsSync(reportPath)?JSON.parse(fs.readFileSync(reportPath,'utf8')):null;
if(report){assert.equal(report.geometryHash,m.geometryHash);assert(!report.checks.some(c=>c.status==='FAIL'),'Failed model check');}
assert.equal(m.custom.components.usb_adapter.nominalMouthRecess,.65);
assert(m.custom.components.usb_adapter.minimumOuterWallSkin>=.5);
const cable=m.custom.components.fpc_cable;
assert(cable.maximumRouteLength<=cable.nominalCableLength-10,'Insufficient nominal flex engagement/slack allowance');
const mediaPath=new URL('../../design/fit-v1/media-manifest.json',import.meta.url);
if(fs.existsSync(mediaPath)){
 const media=JSON.parse(fs.readFileSync(mediaPath,'utf8'));
 assert.equal(media.sourceSpecHash,hash,'Rendered media is stale');
 assert.equal(media.geometryHash,m.geometryHash,'Rendered geometry is stale');
 // Filename and hash verification is completed by the release check.
}
console.log('Native evidence matches the shared model; physical fit remains unvalidated.');
