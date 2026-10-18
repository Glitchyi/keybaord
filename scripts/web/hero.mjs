import {circularFillet,ribbonFaces} from './geometry.mjs';
import {readFileSync} from 'node:fs';
import * as k from '../../vendor/anatomy/kit/iso-kit.mjs';
import {escape as e} from './page.mjs';
const WIDTH=920,HEIGHT=640;
const round=n=>Number(n.toFixed(4));
const path=points=>k.pathOf(points,true);
function hull(points){const q=[...points].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);const turn=(a,b,c)=>(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);const lo=[],hi=[];for(const p of q){while(lo.length>1&&turn(lo.at(-2),lo.at(-1),p)<=0)lo.pop();lo.push(p);}for(const p of [...q].reverse()){while(hi.length>1&&turn(hi.at(-2),hi.at(-1),p)<=0)hi.pop();hi.push(p);}return [...lo.slice(0,-1),...hi.slice(0,-1)];}
const dot=(a,b)=>a.reduce((n,v,i)=>n+v*b[i],0);
const sub=(a,b)=>a.map((v,i)=>v-b[i]);
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const mean=points=>points[0].map((_,i)=>points.reduce((n,p)=>n+p[i],0)/points.length);
function rotate([x,y,z],pose){const a=pose.rotationX;return [x+pose.translation[0],y*Math.cos(a)-z*Math.sin(a)+pose.translation[1],y*Math.sin(a)+z*Math.cos(a)+pose.translation[2]];}
function rounded(w,d,r,cx=0,cy=0){return k.roundedPlan({x:cx-w/2,y:cy-d/2,w,d,r},8);}
function solidXZ(ring,y0,y1){const a=ring.map(([x,z])=>[x,y0,z]),b=ring.map(([x,z])=>[x,y1,z]),faces=[a,[...b].reverse()];for(let i=0;i<ring.length;i++)faces.push([a[i],b[i],b[(i+1)%ring.length],a[(i+1)%ring.length]]);return faces;}
function ringAt(ring,z){return ring.map(([x,y])=>[x,y,z]);}
function solid(ring,z,h,topRing=ring){const lo=ringAt(ring,z),hi=ringAt(topRing,z+h);const faces=[];for(let i=0;i<lo.length;i++){const j=(i+1)%lo.length;faces.push([lo[i],lo[j],hi[j],hi[i]]);}faces.push(hi);return faces;}
function footFaces(x,y,zTop,diameter,height,localAngle=0){const R=(diameter**2/4+height**2)/(2*height),faces=[],rings=[];for(let j=0;j<=10;j++){const q=height*j/10,r=Math.sqrt(Math.max(0,2*R*q-q*q)),z=-height+q;rings.push(Array.from({length:48},(_,i)=>{const xx=r*Math.cos(i*Math.PI/24),yy=r*Math.sin(i*Math.PI/24);return[x+xx,y+yy*Math.cos(localAngle)-z*Math.sin(localAngle),zTop+yy*Math.sin(localAngle)+z*Math.cos(localAngle)];}));}for(let j=0;j<10;j++)for(let i=0;i<48;i++)faces.push([rings[j][i],rings[j][(i+1)%48],rings[j+1][(i+1)%48],rings[j+1][i]]);faces.push(rings.at(-1));return faces;}
function cylinder(x,y,r,z,h){return solid(Array.from({length:64},(_,i)=>[x+r*Math.cos(i*Math.PI/32),y+r*Math.sin(i*Math.PI/32)]),z,h);}
export function heroFigure(s){
 const C=s.custom,D=s.datums,parts=s.parts;
 const corners=[];for(const pose of Object.values(s.poses))for(const x of [-C.case.width/2,C.case.width/2])for(const y of [-C.case.depth/2,C.case.depth/2])for(const z of [C.case.bottomZ-16,C.knob.topZ+57])corners.push(rotate([x,y,z],pose));
 const P=k.fitProjection(corners,WIDTH,HEIGHT,{pad:54,azimuth:-55,elevation:42});
 const project=point=>{const [x,y]=k.iso(point,P);return [WIDTH-x,y];};
 const cam=k.cameraOf(P),viewer=[cam.cosA*cam.cosE,cam.sinA*cam.cosE,cam.sinE];
 const crop=(extra)=>{const pts=[];for(const pose of Object.values(s.poses))for(const x of [-C.case.width/2,C.case.width/2])for(const y of [-C.case.depth/2,C.case.depth/2])for(const z of [C.case.bottomZ-C.rubberFoot.height-12*extra,C.knob.topZ+65*extra])pts.push(project(rotate([x,y,z],pose)));const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]),w=Math.max(...xs)-Math.min(...xs)+70,h=Math.max(...ys)-Math.min(...ys)+70,W=Math.max(w,h*1.64),H=W/1.64;return [(Math.max(...xs)+Math.min(...xs)-W)/2,(Math.max(...ys)+Math.min(...ys)-H)/2,W,H];};
 const viewBoxes={assembled:crop(0),exploded:crop(1)};
 const metadata={viewBoxes,sourceSpecHash:s.sourceSpecHash,geometryHash:s.geometryHash,revision:s.revision,units:s.units,projection:P,poses:s.poses,riserBottoms:[],keyCount:s.layout.keys.length,drawnFamilies:new Set(),instances:[],surfaceCount:0};
 const poseMarkup=[];
 const colors={cap:['#10213b','#0a1427','#0c192e','#102039','#132743'],black:['#12161d','#05070a','#080b10','#0d1118','#131922'],frost:['#8795a4','#3a4757','#566574','#748494','#95a5b3'],board:['#2a3341','#17202b','#1b2633','#232f40','#2c394b'],switch:['#c8d2d8','#4d5b64','#75828a','#a3b0b8','#c9d3da'],stem:['#49b09b','#216c5e','#288873','#35a18a','#61c3ae'],metal:['#adb8c4','#465262','#667486','#8998a9','#bdc8d3'],rubber:['#3d4754','#222a36','#2a3442','#344151','#465568'],warm:['#bba27b','#65573e','#887652','#ac976f','#d1bb92']};
 function renderMesh(faces,material,pose,inner=''){
  const palette=colors[material]??colors.metal,visible=[];
  for(const original of faces){const face=original.map(p=>rotate(p,pose));const normal=cross(sub(face[1],face[0]),sub(face[2],face[0]));const length=Math.hypot(...normal);if(length<1e-9)continue;const N=normal.map(v=>v/length);if(dot(N,viewer)<-1e-6)continue;const at=mean(face),light=Math.max(0,Math.min(1,(N[2]*.8+N[0]*-.3+N[1]*-.45+1)/2));const shade=Math.max(1,Math.min(4,1+Math.floor(light*4)));const top=N[2]>.8;visible.push({depth:k.depthOf(at,P),d:path(face.map(project)),fill:palette[top?0:shade]});}
  visible.sort((a,b)=>a.depth-b.depth);metadata.surfaceCount+=visible.length;
  return visible.map(q=>`<path d="${q.d}" fill="${q.fill}" stroke="none"/>`).join('')+(material==='cap'?`<path class="key-outline" d="${path(hull(faces.flat().map(p=>project(rotate(p,pose)))))}" fill="none" stroke="#1e3049" stroke-width=".7"/>`:'')+inner;
 }
 for(const [angleText,pose] of Object.entries(s.poses)){
  const angle=Number(angleText),items=[];
  const vec=vector=>{const zero=project(rotate([0,0,0],pose)),p=project(rotate(vector,pose));return sub(p,zero).map(round);};
  const worldMove=vector=>{const a=rotate(vector,{...pose,translation:[0,0,0]});return a;};
  const append=(id,family,faces,material,{move=[0,0,0],key,stem,overlay,extra='',at}={})=>{
   const points=faces.flat();const center=at??mean(points),worldCenter=rotate(center,pose),m=vec(move),lift=move[2]*1000+dot(worldMove(move),viewer),depth=Math.max(...points.map(p=>p[2]))*1000+k.depthOf(worldCenter,P);
   let svg=renderMesh(faces,material,pose,extra);
   const attrs=`data-item="${e(id)}" data-world-move='${JSON.stringify(move)}'${family==='fpc_cable'?' data-disconnected-cable="true"':''} data-part-id="${e(family)}" data-depth="${depth}" data-lift="${lift}" data-move='${JSON.stringify(m)}'${key?` data-key="${e(key)}" data-travel='${JSON.stringify(vec([0,0,-1]))}' role="button" tabindex="${key==='w'?0:-1}" aria-label="Press ${e(s.layout.keys.find(k=>k.id===key)?.label??key)}" aria-pressed="false"`:''}${stem?` data-stem="${e(stem)}" data-travel='${JSON.stringify(vec([0,0,-1]))}'`:''}${overlay?` data-overlay="${e(overlay)}" hidden`:''}`;
   items.push({id,depth,svg:`<g ${attrs}>${svg}</g>`});
   if(angle===C.riser.defaultAngle){metadata.drawnFamilies.add(family);metadata.instances.push({id,partId:family,center:center.map(round),move,faces:faces.length});}
  };
  const slab=(id,family,w,dep,z,h,center,material,options={})=>append(id,family,solid(rounded(w,dep,options.radius??0,center[0],center[1]),z,h),material,options);
  const body=C.case,bodyRing=rounded(body.width,body.depth,body.cornerRadius),innerRing=rounded(body.width-2*body.wall,body.depth-2*body.wall,Math.max(0,body.cornerRadius-body.wall));
  slab('case.floor','case',body.width,body.depth,body.bottomZ,body.floor,[0,0],'frost',{radius:body.cornerRadius});
  for(let i=0;i<bodyRing.length;i++){
   const j=(i+1)%bodyRing.length,outer=[...bodyRing[i]],outnext=[...bodyRing[j]],innext=[...innerRing[j]],inner=[...innerRing[i]];
   if(Math.abs(outer[1]-body.depth/2)<.0001&&Math.abs(outnext[1]-body.depth/2)<.0001){
    const usb=C.components.usb_adapter,[mouthW,mouthH,mouthR]=usb.mouthOuter,[cx,,cz]=usb.mouthCenter,xL=Math.min(outer[0],outnext[0]),xR=Math.max(outer[0],outnext[0]),left=cx-mouthW/2,right=cx+mouthW/2,bottom=cz-mouthH/2,top=cz+mouthH/2,y0=body.depth/2-body.wall,y1=body.depth/2,z0=body.bottomZ+body.floor;
    const pieces=[[[xL,z0],[left,z0],[left,body.topZ],[xL,body.topZ]],[[right,z0],[xR,z0],[xR,body.topZ],[right,body.topZ]],[[left,z0],[right,z0],[right,bottom],[left,bottom]],[[left,top],[right,top],[right,body.topZ],[left,body.topZ]]];
    const outline=rounded(mouthW,mouthH,mouthR,cx,cz),corners=[[right,bottom],[right,top],[left,top],[left,bottom]];for(let q=0;q<4;q++)pieces.push([corners[q],...outline.slice(q*9,q*9+9)]);
    pieces.forEach((ring,j)=>append('case.rear.'+j,'case',solidXZ(ring,y0,y1),'frost'));
   }else append('case.wall.'+i,'case',solid([outer,outnext,innext,inner],body.bottomZ+body.floor,body.topZ-body.bottomZ-body.floor),'frost');
  }
  // A shell-shaped, clipped preview field follows the physical lower enclosure.
  const glowRing=ringAt(bodyRing,body.bottomZ+body.floor/2).map(p=>project(rotate(p,pose)));
  items.push({depth:-999,svg:`<path data-glow="spill" d="${path(glowRing)}" fill="#dce8ff" opacity=".2" filter="url(#hero-glow)"/>`});
  const pcb=C.pcb;
  slab('pcb','pcb',pcb.width,pcb.depth,D.pcbBottom,pcb.thickness,[0,0],'board',{radius:C.plate.cornerRadius,move:[0,0,22]});
  const plate=C.plate,plateFaces=solid(rounded(plate.width,plate.depth,plate.cornerRadius),D.plateBottom,plate.thickness);
  const plateClip='plate-clip-'+angle;
  const plateTopOutline=path(ringAt(rounded(plate.width,plate.depth,plate.cornerRadius),D.plateTop).map(p=>project(rotate(p,pose))));
  const openings=s.layout.keys.map(key=>{const [x,y]=key.center,a=plate.switchOpening;return path(ringAt(rounded(a,a,plate.openingRadiusMax,x,y),D.plateTop).map(p=>project(rotate(p,pose))));});
  const [ex,ey]=s.layout.encoder.center;openings.push(path(ringAt(rounded(plate.encoderOpening[0],plate.encoderOpening[1],0,ex,ey),D.plateTop).map(p=>project(rotate(p,pose)))));
  const plateArt=renderMesh(plateFaces,'black',pose);
  append('plate','plate',plateFaces,'black',{move:[0,0,22],extra:''});
  const plateItem=items.at(-1);plateItem.svg=plateItem.svg.replace(plateArt,`<g clip-path="url(#${plateClip})">${plateArt}</g>`).replace('data-item=',`data-item=`);plateItem.svg=`<defs><clipPath id="${plateClip}"><path d="${plateTopOutline}${openings.join('')}" fill-rule="evenodd" clip-rule="evenodd"/></clipPath></defs>`+plateItem.svg;
  const sw=parts.switch.dimensions;
  for(const key of s.layout.keys){
   const [x,y]=key.center,q=key.capDimensions;
   slab('switch.'+key.id,'switch',sw.mountBodyWidth,sw.mountBodyDepth,D.pcbTop,sw.housingRoofAbovePCB,[x,y],'switch',{radius:plate.openingRadiusMax,move:[0,0,22]});
   const stemSize=q.stemSocket.crossLength;
   slab('stem.'+key.id,'switch',stemSize,stemSize,D.pcbTop+sw.housingRoofAbovePCB,sw.stemProjection,[x,y],'stem',{radius:0,move:[0,0,22],stem:key.id});
   const outer=rounded(q.width,q.depth,q.cornerRadius,x,y),crown=rounded(q.crownWidth,q.crownDepth,q.cornerRadius,x,y);
   const capFaces=solid(outer,q.bottomZ,q.crownTopZ-q.bottomZ,crown).slice(0,-1);
   // Concentric, shallow dish surfaces are derived from crown and dish depth.
   let previous=crown;
   for(let level=0;level<5;level++){
    const nextFactor=1-(level+1)/5,next=nextFactor>0?rounded(q.crownWidth*nextFactor,q.crownDepth*nextFactor,q.cornerRadius*nextFactor,x,y):previous.map(()=>[x,y]);
    const z1=q.crownTopZ-q.dishDepth*(1-(1-level/5)**2),z2=q.crownTopZ-q.dishDepth*(1-nextFactor**2);
    for(let i=0;i<previous.length;i++){const j=(i+1)%previous.length;capFaces.push([[...previous[i],z1],[...previous[j],z1],[...next[j],z2],[...next[i],z2]]);}previous=next;
   }
   capFaces.push(ringAt(previous,q.crownTopZ-q.dishDepth));
   const center=[x,y,q.crownTopZ-q.dishDepth+.015],origin=project(rotate(center,pose)),u=sub(project(rotate([x+1,y,center[2]],pose)),origin),v=sub(project(rotate([x,y-1,center[2]],pose)),origin);
   const font=key.label.length>3?2.35:key.label.length>1?2.65:3.35;
   const legend=`<g transform="matrix(${u[0]} ${u[1]} ${v[0]} ${v[1]} ${origin[0]} ${origin[1]})"><text data-legend="${e(key.id)}" x="0" y="1" text-anchor="middle" fill="#f4f8ff" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="${font}" font-weight="500">${e(key.label)}</text></g>`;
   append('cap.'+key.id,key.partId,capFaces,'cap',{move:[0,0,42],key:key.id,extra:legend,at:[x,y,(q.bottomZ+q.crownTopZ)/2]});
   const led=parts.key_led.dimensions,ledAt=s.instances.find(i=>i.id==='key-led-'+key.id).origin;
   slab('led.'+key.id,'key_led',led.width,led.depth,ledAt[2],led.height,ledAt,'metal',{move:[0,0,22]});
   const diode=parts.diode.dimensions,diodeAt=s.instances.find(i=>i.id==='diode-'+key.id).origin;
   slab('diode.'+key.id,'diode',diode.bodyLength,diode.bodyWidth,diodeAt[2],diode.height,diodeAt,'black',{move:[0,0,22]});
  }
  const enc=parts.encoder.dimensions;
  slab('encoder.body','encoder',enc.bodyWidth,enc.bodyDepth,D.pcbTop,enc.bodyHeight,[ex,ey],'metal',{move:[0,0,22]});
  append('encoder.shaft','encoder',cylinder(ex,ey,enc.shaftDiameter/2,D.pcbTop+enc.bodyHeight,enc.shaftLength),'metal',{move:[0,0,22]});
  append('knob','knob',cylinder(ex,ey,C.knob.diameter/2,C.knob.bottomZ,C.knob.height),'cap',{move:[0,0,42]});
  for(const [x,y] of C.mounting.caseScrewPositions)append('case.post.'+x+'.'+y,'case',cylinder(x,y,C.mounting.postDiameter/2,body.bottomZ+body.floor,D.plateBottom-body.bottomZ-body.floor),'frost');
  for(const [i,[x,y]] of C.mounting.caseScrewPositions.entries())append('case.screw.'+i,'fastener',cylinder(x,y,parts.fastener.dimensions.headDiameter/2,D.plateTop,parts.fastener.dimensions.headHeight),'metal',{move:[0,0,50]});
  const control=C.components.controller,cd=parts.controller.dimensions;
  slab('controller','controller',cd.width,cd.depth,control.center[2],cd.height,control.center,'board',{move:[0,0,22]});
  const usb=C.components.usb_adapter,ud=parts.usb_adapter.dimensions,source=JSON.parse(readFileSync(new URL('../../spec/references/waveshare/adapter-datums.json',import.meta.url),'utf8')),usbMesh=JSON.parse(readFileSync(new URL('../../spec/references/waveshare/adapter-source-mesh.json',import.meta.url),'utf8')),shell=usbMesh.solids.find(q=>q.index===source.usb.stepSolidIndexShell),shellBack=Math.min(...shell.vertices.map(p=>p[1]))+source.normalization.translate[1]+usb.boardOrigin[1];
  slab('usb.board','usb_adapter',ud.pcbWidth,ud.pcbDepth,usb.boardOrigin[2]+source.pcb.bottomZ,-source.pcb.bottomZ,usb.boardOrigin,'board',{move:[0,0,0]});
  const U=source.usb,outerXZ=rounded(U.mouthOuterWidth,U.mouthOuterHeight,U.mouthOuterRadius,usb.mouthCenter[0],usb.mouthCenter[2]),innerXZ=rounded(U.mouthInnerWidth,U.mouthInnerHeight,U.mouthInnerRadius,usb.mouthCenter[0],usb.mouthCenter[2]),mouthY=usb.mouthCenter[1],usbFaces=[];
  for(let i=0;i<outerXZ.length;i++){const j=(i+1)%outerXZ.length,o=outerXZ[i],O=outerXZ[j],v=innerXZ[i],V=innerXZ[j];usbFaces.push([[o[0],shellBack,o[1]],[O[0],shellBack,O[1]],[O[0],mouthY,O[1]],[o[0],mouthY,o[1]]],[[o[0],mouthY,o[1]],[O[0],mouthY,O[1]],[V[0],mouthY,V[1]],[v[0],mouthY,v[1]]]);}
  append('usb.shell','usb_adapter',usbFaces,'metal',{move:[0,0,0]});
  for(const id of ['led_driver','logic_buffer']){const q={...parts[id].dimensions,...C.components[id]};slab(id,id,q.width,q.depth,q.center[2],q.height,q.center,'black',{move:[0,0,22]});}
  const route=circularFillet(C.components.fpc_cable.route,C.components.fpc_cable.minimumBendRadius);metadata.fpcRoute={analyticLength:route.analyticLength,polylineLength:route.polylineLength,nominalRadius:route.nominalRadius,nominalCableLength:C.components.fpc_cable.nominalCableLength,maximumRouteLength:C.components.fpc_cable.maximumRouteLength};
  append('fpc','fpc_cable',ribbonFaces(route.points,C.components.fpc_cable.width,C.components.fpc_cable.thickness),'warm',{move:[0,0,0]});
  for(const x of C.riser.magnetX)append('magnet.case.'+x,'magnet',cylinder(x,C.riser.magnetY,parts.magnet.dimensions.diameter/2,body.bottomZ+body.magnetPocketWeb,parts.magnet.dimensions.thickness),'metal');
  for(const [x,y] of C.riser.shearKeys.centers)append('case.shear.'+x,'case',cylinder(x,y,C.riser.shearKeys.diameter/2,body.bottomZ-C.riser.shearKeys.height,C.riser.shearKeys.height),'frost');
  // The strip is the sourced covered product, with its installed pixel count from the shared assembly.
  const strip={...parts.rgb_strip.dimensions,...C.components.rgb_strip},length=strip.pixels*strip.pixelPitch;
  slab('base.strip','rgb_strip',length,strip.width,strip.topZ-strip.height,strip.height,[0,strip.centerY],'warm',{move:[0,0,22]});

  const foot=parts.rubber_foot.dimensions;
  for(const [x,y] of C.rubberFoot.centers)append('foot.'+x+'.'+y,'rubber_foot',footFaces(x,y,body.bottomZ,foot.diameter,foot.height),'rubber');
  if(angle){
   const r=C.riser,y0=r.frontY,y1=r.rearY,bottomAt=y=>(foot.height-pose.translation[2]-y*Math.sin(pose.rotationX))/Math.cos(pose.rotationX),nose=body.bottomZ-bottomAt(y0),rear=body.bottomZ-bottomAt(y1);
   const left=[[-r.width/2,y0,body.bottomZ-nose],[-r.width/2,y1,body.bottomZ-rear],[-r.width/2,y1,body.bottomZ],[-r.width/2,y0,body.bottomZ]],right=left.map(q=>[r.width/2,q[1],q[2]]),faces=[left,[...right].reverse()];for(let i=0;i<4;i++)faces.push([left[i],right[i],right[(i+1)%4],left[(i+1)%4]]);
   metadata.riserBottoms.push({angle,localVertices:[left[0],left[1],right[0],right[1]],worldVertices:[left[0],left[1],right[0],right[1]].map(point=>rotate(point,pose)),noseHeight:nose,rearHeight:rear});
   append('riser.'+angle,'riser_'+angle,faces,'frost',{move:[0,0,-12]});
   for(const x of r.footX)append('riser.foot.'+angle+'.'+x,'rubber_foot',footFaces(x,r.footY,bottomAt(r.footY),foot.diameter,foot.height,-pose.rotationX),'rubber',{move:[0,0,-12]});
   for(const [i,x] of r.magnetX.entries())append('magnet.'+angle+'.'+i,'magnet',cylinder(x,r.magnetY,parts.magnet.dimensions.diameter/2,body.bottomZ-r.magnetPocketDepth,parts.magnet.dimensions.thickness),'metal',{move:[0,0,-12]});
  }
  for(const profile of C.overlay.profiles){
   const margin=body.wall,clear=C.knob.diameter/2+margin,ow=C.overlay.width,od=C.overlay.depth,outline=[[-ow/2,-od/2],[ow/2,-od/2],[ow/2,ey-clear],[ex-clear,ey-clear],[ex-clear,od/2],[-ow/2,od/2]];
   let icons='';for(const [index,key] of s.layout.keys.entries()){
    const z=C.overlay.bottomZ+C.overlay.thickness+.02,[x,y]=key.center,origin=project(rotate([x,y,z],pose)),u=sub(project(rotate([x+1,y,z],pose)),origin),v=sub(project(rotate([x,y-1,z],pose)),origin),kind=(index+C.overlay.profiles.indexOf(profile)*3)%9;
    const drawings=['<path d="M-3 0H3M0-3V3"/>','<rect x="-2.6" y="-2.6" width="5.2" height="5.2" rx=".6"/><path d="M-1.3-1.3H1.3V1.3H-1.3Z"/>','<circle cx="0" cy="0" r="2.7"/><path d="M0-3.5V3.5M-3.5 0H3.5"/>','<path d="M-3 2.5L0-3L3 2.5Z"/>','<path d="M-3-2.5L3 0L-3 2.5Z"/>','<path d="M-3 0H3M.5-2.5L3 0L.5 2.5"/>','<path d="M-2.5-3V2.5H3M-1-1.5H1.5V1"/>','<circle cx="-1.8" cy="1.8" r="1.1"/><circle cx="1.8" cy="1.8" r="1.1"/><path d="M-2.6-3L1 1M2.6-3L-1 1"/>','<path d="M-3-2H3M-3 0H1M-3 2H3"/>'];
    const symbol=key.units===2?'<path d="M-6-2V2H6V-2M-4 0H4"/>':drawings[kind];icons+='<g transform="matrix('+u[0]+' '+u[1]+' '+v[0]+' '+v[1]+' '+origin[0]+' '+origin[1]+')" fill="none" stroke="#f5f8ff" stroke-width=".5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+symbol+'</g>';
   }
   append('overlay.'+profile,'overlay',solid(outline,C.overlay.bottomZ,C.overlay.thickness),'cap',{move:[0,0,65],overlay:profile,extra:icons});
  }
  items.sort((a,b)=>a.depth-b.depth);
  poseMarkup.push(`<g data-pose="${angle}" ${angle===C.riser.defaultAngle?'':'hidden'}>${items.map(q=>q.svg).join('')}</g>`);
 }
 metadata.drawnFamilies=[...metadata.drawnFamilies];
 const svg=`<svg viewBox="${viewBoxes.assembled.join(' ')}" role="group" aria-roledescription="interactive assembly" aria-label="28-key ortholinear mechanical keypad in deep navy, glossy black and frosted translucent material; one 2u Space and a top-right rotary knob. Interactive drawing study; fit and optics unvalidated." data-source-hash="${s.sourceSpecHash}"><defs><filter id="hero-glow" x="-40%" y="-100%" width="180%" height="300%"><feGaussianBlur stdDeviation="19"/></filter><filter id="hero-small-glow" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="3"/></filter></defs>${poseMarkup.join('')}</svg>`;
 return {svg,metadata};
}
export function auditHero(s,metadata){
 const errors=[];
 if(s.units!=='mm')errors.push('shared model must use millimetres');
 if(s.layout.keys.length!==28)errors.push('expected exactly 28 keys');
 if(s.layout.keys.filter(k=>k.units===2).length!==1)errors.push('expected exactly one 2u Space');
 const occupied=new Set();for(const key of s.layout.keys)for(let u=0;u<key.units;u++){const cell=key.row+':'+(key.column+u);if(occupied.has(cell))errors.push('overlapping layout cell '+cell);occupied.add(cell);}const enc=s.layout.encoder;const dial=enc.row+':'+enc.column;if(occupied.has(dial))errors.push('dial overlaps a key');occupied.add(dial);if(occupied.size!==s.layout.columns*s.layout.rows)errors.push('grid occupancy is incomplete');
 for(const item of metadata.instances){if(!item.center.every(Number.isFinite))errors.push(item.id+' has a non-finite centre');if(!item.faces)errors.push(item.id+' has no real surfaces');if(!s.parts[item.partId])errors.push(item.id+' missing catalogue part '+item.partId);}
  const rigidFamilies=['pcb','plate','switch','encoder','key_led','diode','led_driver','logic_buffer','controller','rgb_strip'],motionGroups={};
 for(const partId of rigidFamilies){const instances=metadata.instances.filter(item=>item.partId===partId);if(!instances.length)errors.push('missing rigid assembly family '+partId);for(const item of instances)if(item.move.some((v,i)=>v!==[0,0,22][i]))errors.push(item.id+' detached from the soldered assembly');motionGroups[partId]={instances:instances.length,move:instances[0]?.move};}
 for(const [partId,expected]of [['keycap_1u',[0,0,42]],['keycap_2u',[0,0,42]],['knob',[0,0,42]],['fastener',[0,0,50]],['usb_adapter',[0,0,0]],['fpc_cable',[0,0,0]]]){const instances=metadata.instances.filter(item=>item.partId===partId);for(const item of instances)if(item.move.some((v,i)=>v!==expected[i]))errors.push(item.id+' has an inconsistent disassembly move');motionGroups[partId]={instances:instances.length,move:instances[0]?.move};}
 for(const bottom of metadata.riserBottoms){const worldZ=bottom.worldVertices.map(point=>point[2]);if(Math.max(...worldZ)-Math.min(...worldZ)>1e-8)errors.push(bottom.angle+' degree riser bottom is not parallel to the world desk');if(worldZ.some(z=>Math.abs(z-s.parts.rubber_foot.dimensions.height)>1e-8))errors.push(bottom.angle+' degree riser bottom misses the adhesive contact plane');if(bottom.noseHeight<s.custom.riser.minimumNoseHeight)errors.push(bottom.angle+' degree riser is below its minimum nose height');}
 if(metadata.fpcRoute.analyticLength>s.custom.components.fpc_cable.maximumRouteLength)errors.push('FPC nominal route exceeds shared length allowance');
 if(errors.length)throw new Error(errors.join('\n'));
 return {physicalFitValidated:false,comprehensiveCollisionAudit:false,scope:'Shared-source, grid, finite geometry, part-identity, rigid disassembly group and analytic riser-plane audit. Does not establish physical fit or full mesh collision clearance.',keyCount:s.layout.keys.length,occupiedCells:occupied.size,instanceCount:metadata.instances.length,surfaceCount:metadata.surfaceCount,motionGroups,riserBottoms:metadata.riserBottoms,fpcDisconnectedWhenApart:true,fpcRoute:metadata.fpcRoute,sourceSpecHash:s.sourceSpecHash,geometryHash:s.geometryHash,failures:0};
}
