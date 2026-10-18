import fs from 'node:fs';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=name=>fs.readFileSync(path.join(root,name),'utf8');
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const assemblyText=read('spec/keypad.json'),partsText=read('spec/parts.json');
const a=JSON.parse(assemblyText),p=JSON.parse(partsText);
if(a.units!=='mm'||p.units!=='mm')throw new Error('Every geometry source must use millimetres');
const pitch=a.layout.pitch,w=a.custom.case.width,d=a.custom.case.depth;
const keys=a.layout.keys.map(k=>({...k,center:[(k.column+k.units/2)*pitch-a.layout.columns*pitch/2,a.layout.rows*pitch/2-(k.row+.5)*pitch,0],partId:k.units===2?'keycap_2u':'keycap_1u',capDimensions:k.units===2?a.custom.keycap_2u:a.custom.keycap_1u}));
if(keys.length!==28||new Set(keys.map(k=>k.id)).size!==28)throw new Error('Exactly28unique keyIDs required');
const occupancy=new Set();for(const k of keys)for(let c=k.column;c<k.column+k.units;c++){const cell=k.row+':'+c;if(occupancy.has(cell))throw new Error('Overlapping key cells');occupancy.add(cell)}
const e=a.layout.encoder,encoder={...e,center:[(e.column+.5)*pitch-3*pitch,2.5*pitch-(e.row+.5)*pitch,0]};if(occupancy.has(e.row+':'+e.column))throw new Error('Encoder clashes with key');occupancy.add(e.row+':'+e.column);if(occupancy.size!==30)throw new Error('Expected30 occupied cells');
const footH=a.custom.rubberFoot.height,footR=a.custom.rubberFoot.diameter/2,frontY=-d/2+9,sphereR=(footR*footR+footH*footH)/(2*footH);
const poses=Object.fromEntries(a.custom.riser.angles.map(deg=>{const r=deg*Math.PI/180;return [String(deg),{angleDegrees:deg,rotationX:r,translation:[0,0,sphereR-(a.datums.caseBottom+sphereR-footH)*Math.cos(r)-frontY*Math.sin(r)],contactDefinition:'analytic spherical-cap contact from sourced foot envelope; exact profile and compression unvalidated'}]}));
const model={schemaVersion:1,revision:a.revision,units:'mm',sourceSpecHash:sha(assemblyText+'\n'+partsText),assemblyHash:sha(assemblyText),partsHash:sha(partsText),coordinateSystem:a.coordinateSystem,layout:{...a.layout,keys,encoder},datums:a.datums,custom:a.custom,materials:a.materials,fitPolicy:a.fitPolicy,lighting:a.lighting,animations:a.animations,scope:a.scope,poses,parts:p.parts,sources:p.sources,bom:p.bom??null,priceDate:p.priceDate??'2026-10-18',rawParts:p};
model.referenceHashes=Object.fromEntries(fs.readdirSync(path.join(root,'spec/references/waveshare')).filter(n=>n.endsWith('.json')).sort().map(n=>['spec/references/waveshare/'+n,sha(read('spec/references/waveshare/'+n))]));
model.instances=[];
for(const k of keys){const [x,y]=k.center;model.instances.push({id:'cap-'+k.id,partId:k.partId,keyId:k.id,origin:[x,y,0]},{id:'switch-'+k.id,partId:'switch',keyId:k.id,origin:[x,y,a.datums.pcbTop]},{id:'key-led-'+k.id,partId:'key_led',origin:[x+a.custom.components.key_led.offset[0],y+a.custom.components.key_led.offset[1],a.custom.components.key_led.offset[2]]},{id:'diode-'+k.id,partId:'diode',origin:[x+a.custom.components.diode.offset[0],y+a.custom.components.diode.offset[1],a.custom.components.diode.offset[2]]});}
model.instances.push({id:'encoder',partId:'encoder',origin:[...encoder.center.slice(0,2),a.datums.pcbTop]},{id:'knob',partId:'knob',origin:[...encoder.center.slice(0,2),a.custom.knob.bottomZ]},{id:'controller',partId:'controller',origin:a.custom.components.controller.center},{id:'usb-adapter',partId:'usb_adapter',origin:a.custom.components.usb_adapter.boardOrigin},{id:'white-driver',partId:'led_driver',origin:a.custom.components.led_driver.center},{id:'logic-buffer',partId:'logic_buffer',origin:a.custom.components.logic_buffer.center});
model.geometryHash=sha(JSON.stringify({layout:model.layout,datums:model.datums,custom:model.custom,parts:model.parts,poses:model.poses,instances:model.instances,referenceHashes:model.referenceHashes}));
fs.writeFileSync(path.join(root,'spec/resolved.json'),JSON.stringify(model,null,2)+'\n');
console.log('Resolved '+model.revision+' '+model.sourceSpecHash+';28 keys,30 cells,mm');
