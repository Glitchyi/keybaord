import {readFileSync,writeFileSync,mkdirSync,existsSync,copyFileSync,unlinkSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {heroFigure,auditHero} from './web/hero.mjs';
import {drawingSheets} from './engineering/drawings.mjs';
import {pageHTML} from './web/page.mjs';
import {runtimeScript} from './web/runtime.mjs';
import {validateRobuEstimates} from './web/procurement.mjs';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..'),read=name=>readFileSync(resolve(root,name),'utf8'),sha=value=>createHash('sha256').update(value).digest('hex');
if(!existsSync(resolve(root,'spec/resolved.json')))throw Error('Resolve the shared specification first: node scripts/resolve-spec.mjs');
const spec=JSON.parse(read('spec/resolved.json')),catalogue=JSON.parse(read('spec/parts.json'));
const procurementText=read('procurement/robu-estimates.json'),procurement=validateRobuEstimates(JSON.parse(procurementText)),procurementHash=sha(procurementText);
for(const row of procurement.rows)if(row.file&&sha(readFileSync(resolve(root,row.file)))!==row.fileSHA256)throw Error('Robu quote study changed since its estimate: '+row.id);
if(spec.sourceSpecHash!==sha(read('spec/keypad.json')+'\n'+read('spec/parts.json')))throw Error('Resolved specification is stale; run node scripts/resolve-spec.mjs');
for(const [file,hash] of Object.entries(spec.referenceHashes??{}))if(sha(read(file))!==hash)throw Error('Resolved manufacturer reference is stale: '+file);
const {svg,metadata}=heroFigure(spec),sheets=drawingSheets(spec),audit=auditHero(spec,metadata);
for(const id of Object.keys(spec.parts))if(!sheets.some(sheet=>sheet.partId===id))throw Error('Missing unique-part drawing: '+id);
const ids=sheets.map(s=>s.id);if(new Set(ids).size!==ids.length)throw Error('Duplicate drawing sheet ID');
const subtotal=Object.values(catalogue.parts).reduce((n,p)=>n+(typeof p.unitpriceINR==='number'?p.quantityPurchased*p.unitpriceINR:0),0);
if(Math.abs(subtotal-catalogue.pricing.knownPurchaseSubtotalINR)>.005)throw Error('Priced subtotal disagrees with sourced catalogue');
const output=resolve(root,'dist');mkdirSync(resolve(output,'previews'),{recursive:true});
const requiredMedia=['assembly.mp4','switch-motion.mp4','glow.mp4','assembled.png','underside.png','section.png','rear-usb.png'];
const previewDefinitions=[['assembly','assembly.mp4','assembled.png','Assembly and magnetic riser'],['switch','switch-motion.mp4','section.png','External BOX Jade stem motion'],['glow','glow.mp4','assembled.png','White key light and RGB base glow']];
const stillDefinitions=[['assembled','assembled.png','The assembled keypad'],['underside','underside.png','Underside and magnetic bar seat'],['section','section.png','Case and mounting-stack section'],['rear-usb','rear-usb.png','Near-flush rear USB-C opening']];
const nativeManifestPath=resolve(root,'design/fit-v1/media-manifest.json');let nativeMedia=null;try{if(existsSync(nativeManifestPath))nativeMedia=JSON.parse(readFileSync(nativeManifestPath,'utf8'));}catch{}
const mediaProblems=[];if(nativeMedia?.complete!==true)mediaProblems.push('native media render is incomplete');if(nativeMedia?.sourceSpecHash!==spec.sourceSpecHash)mediaProblems.push('native media source specification is missing or stale');if(nativeMedia?.geometryHash!==spec.geometryHash)mediaProblems.push('native media geometry hash is missing or stale');
for(const name of requiredMedia){const file=resolve(root,'design/fit-v1',name);if(!existsSync(file))mediaProblems.push('missing '+name);else if(!nativeMedia?.outputSHA256?.[name]||sha(readFileSync(file))!==nativeMedia.outputSHA256[name])mediaProblems.push('unverified bytes '+name);}
const mediaVerified=mediaProblems.length===0;
const previewManifest={sourceSpecHash:spec.sourceSpecHash,geometryHash:spec.geometryHash,verified:mediaVerified,clips:{},stills:{},outputSHA256:{},pending:mediaProblems};
if(mediaVerified){for(const name of requiredMedia){copyFileSync(resolve(root,'design/fit-v1',name),resolve(output,'previews',name));previewManifest.outputSHA256[name]=nativeMedia.outputSHA256[name];}for(const [id,name,poster,title]of previewDefinitions)previewManifest.clips[id]={src:'previews/'+name,poster:'previews/'+poster,title};for(const [id,name,title]of stillDefinitions)previewManifest.stills[id]={src:'previews/'+name,title};}
else{for(const name of requiredMedia){const file=resolve(output,'previews',name);if(existsSync(file))unlinkSync(file);}console.log('Preview media pending for current specification; stale media excluded.');}
writeFileSync(resolve(output,'previews/manifest.json'),JSON.stringify(previewManifest,null,2)+'\n');
const manifest={robuEstimates:{printEstimateSubtotalINR:procurement.printEstimateSubtotalINR??null,inputSHA256:procurementHash,observedAt:procurement.observedAt,rowCount:procurement.rows.length,pricedRows:procurement.rows.filter(row=>row.amountINR!==null).length,pendingRows:procurement.rows.filter(row=>row.amountINR===null).length},schemaVersion:1,revision:spec.revision,units:spec.units,sourceSpecHash:spec.sourceSpecHash,assemblyHash:spec.assemblyHash,partsHash:spec.partsHash,geometryHash:spec.geometryHash,referenceHashes:spec.referenceHashes,layout:spec.layout.keys.map(k=>({id:k.id,label:k.label,units:k.units,center:k.center,partId:k.partId})),encoder:spec.layout.encoder,canonicalInstances:spec.instances,poses:spec.poses,drawingSheets:sheets.map(({id,partId,variant,instances,concept})=>({id,partId,variant:variant??null,instances,concept:Boolean(concept)})),parts:Object.keys(spec.parts),priceDate:catalogue.priceDate,knownPurchaseSubtotalINR:subtotal,unknownPriceLines:Object.values(catalogue.parts).filter(p=>p.unitpriceINR===null).length,previewCount:Object.keys(previewManifest.clips).length,stillCount:Object.keys(previewManifest.stills).length,previewVerified:mediaVerified,audit};
writeFileSync(resolve(output,'web-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
const theme=process.argv.includes('--light')?'light':'dark',script=runtimeScript({keys:spec.layout.keys.map(({id,label,units})=>({id,label,units})),viewBoxes:metadata.viewBoxes,defaultAngle:spec.custom.riser.defaultAngle,angles:spec.custom.riser.angles,travel:spec.fitPolicy.switchNominalTravel,defaultSheet:sheets[0].id,sourceSpecHash:spec.sourceSpecHash});
let html=pageHTML({spec,catalogue,procurement,manifest,hero:svg,sheets,theme,script});
// Media stays optional during modelling, then becomes native video in this same static artifact.
for(const [id,item] of Object.entries(previewManifest.clips)){const marker=`<article class="panel preview-card" data-preview="${id}"><div class="placeholder-preview">`;const at=html.indexOf(marker);if(at<0)continue;const start=at+marker.length-'<div class="placeholder-preview">'.length,end=html.indexOf('</div>',start)+6;html=html.slice(0,start)+`<video controls preload="metadata" playsinline${item.poster?` poster="${item.poster}"`:''} aria-label="${item.title}"><source src="${item.src}" type="video/mp4">Your browser does not support this video preview.</video>`+html.slice(end);}
for(const [id,item]of Object.entries(previewManifest.stills)){const marker=`<article class="panel preview-card" data-still="${id}"><div class="placeholder-preview">`,at=html.indexOf(marker);if(at<0)continue;const start=at+marker.length-'<div class="placeholder-preview">'.length,end=html.indexOf('</div>',start)+6;html=html.slice(0,start)+`<img src="${item.src}" loading="lazy" decoding="async" alt="${item.title}">`+html.slice(end);}
const filename=theme==='light'?'index-light.html':'index.html';writeFileSync(resolve(output,filename),html);writeFileSync(resolve(root,filename),html);
console.log('Built '+theme+' website: '+spec.layout.keys.length+' keys, '+sheets.length+' drawing sheets, '+Object.keys(spec.parts).length+' BOM families; spec '+spec.sourceSpecHash);
if(process.argv.includes('--audit'))console.log('Website source/model audit passed: '+JSON.stringify(audit));
