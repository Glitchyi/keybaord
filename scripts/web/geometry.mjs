const add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]),mul=(a,n)=>a.map(v=>v*n),dot=(a,b)=>a.reduce((n,v,i)=>n+v*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],unit=a=>mul(a,1/Math.hypot(...a));
export function circularFillet(points,radius){
 const out=[[...points[0]]];let analyticLength=points.slice(1).reduce((n,p,i)=>n+Math.hypot(...sub(p,points[i])),0);
 for(let i=1;i<points.length-1;i++){
  const prev=points[i-1],p=points[i],next=points[i+1],u=unit(sub(p,prev)),v=unit(sub(next,p)),theta=Math.acos(Math.max(-1,Math.min(1,dot(u,v))));
  if(theta<1e-8){out.push([...p]);continue;}
  const dist=radius*Math.tan(theta/2);if(dist>=Math.hypot(...sub(p,prev))*.49||dist>=Math.hypot(...sub(next,p))*.49)throw Error('Shared FPC route is too short for its circular fillet');
  const start=sub(p,mul(u,dist)),normal=mul(sub(v,mul(u,Math.cos(theta))),1/Math.sin(theta)),center=add(start,mul(normal,radius)),rad=sub(start,center),axis=unit(cross(u,v));out.push(start);
  for(let j=1;j<=24;j++){const a=theta*j/24,rotated=add(add(mul(rad,Math.cos(a)),mul(cross(axis,rad),Math.sin(a))),mul(axis,dot(axis,rad)*(1-Math.cos(a))));out.push(add(center,rotated));}
  analyticLength-=2*dist-radius*theta;
 }
 out.push([...points.at(-1)]);return {points:out,analyticLength,polylineLength:out.slice(1).reduce((n,p,i)=>n+Math.hypot(...sub(p,out[i])),0),nominalRadius:radius};
}
export function ribbonFaces(points,width,thickness){
 const rings=points.map((p,i)=>{const tangent=unit(sub(points[Math.min(i+1,points.length-1)],points[Math.max(i-1,0)])),side=mul(unit(cross(tangent,[0,0,1])),width/2);return [[-1,-1],[1,-1],[1,1],[-1,1]].map(([sgn,z])=>add(add(p,mul(side,sgn)),[0,0,z*thickness/2]));});
 const faces=[];for(let i=0;i<rings.length-1;i++)for(let j=0;j<4;j++)faces.push([rings[i][j],rings[i][(j+1)%4],rings[i+1][(j+1)%4],rings[i+1][j]]);faces.push([...rings[0]].reverse(),rings.at(-1));return faces;
}
