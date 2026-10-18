const nonempty=value=>typeof value==='string'&&value.trim().length>0;
export function validateRobuEstimates(data){
 if(!data||data.schemaVersion!==1)throw Error('Unsupported Robu estimate schema');
 if(!/^\d{4}-\d{2}-\d{2}$/.test(data.observedAt)||new Date(data.observedAt).toISOString().slice(0,10)!==data.observedAt)throw Error('Robu observation date must be a calendar date');
 const robuURL=value=>{try{const url=new URL(value);return url.protocol==='https:'&&(url.hostname==='robu.in'||url.hostname.endsWith('.robu.in'))&&!/\.(?:stl|step|stp|blend|glb|zip)(?:$|\/)/i.test(url.pathname)}catch{return false}};
 if(!robuURL(data.sourceURL))throw Error('Robu source must be a direct HTTPS service or product URL');
 for(const field of ['quoteStatus','scope'])if(!nonempty(data[field]))throw Error('Missing Robu scope: '+field);
 if(!Array.isArray(data.rows)||data.rows.length===0)throw Error('Robu estimates need scoped rows');
 const ids=new Set(),statuses=new Set(['pending','unavailable','live-calculator','live-listing']);
 for(const row of data.rows){
  if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(row.id)||ids.has(row.id))throw Error('Invalid or duplicate Robu row ID');ids.add(row.id);
  for(const field of ['label','material','process','gstStatus','shippingStatus','finishLimitations'])if(!nonempty(row[field]))throw Error('Missing Robu row '+row.id+' field '+field);
  if(!Number.isInteger(row.quantity)||row.quantity<1)throw Error('Robu row quantity must be a positive integer: '+row.id);
  if(row.amountINR!==null&&(typeof row.amountINR!=='number'||!Number.isFinite(row.amountINR)||row.amountINR<0))throw Error('Robu amount must be numeric INR or explicit null: '+row.id);
  if(!statuses.has(row.priceStatus))throw Error('Unknown Robu evidence type: '+row.id);
  if(['pending','unavailable'].includes(row.priceStatus)&&row.amountINR!==null)throw Error('Pending Robu row cannot carry a verified amount: '+row.id);
  if(row.priceStatus.startsWith('live-')&&row.amountINR===null)throw Error('Live Robu evidence must carry its observed amount: '+row.id);
  if(!robuURL(row.evidenceURL))throw Error('Robu evidence must link to its service or product page: '+row.id);
  if(row.file!==undefined&&(!/^procurement\/robu\/stl\/[a-z0-9-]+\.stl$/.test(row.file)||!/^[a-f0-9]{64}$/.test(row.fileSHA256??'')))throw Error('Robu cost-study file needs a relative path and SHA256: '+row.id);
 }
 if(data.printEstimateSubtotalINR!==undefined){
  if(typeof data.printEstimateSubtotalINR!=='number'||!Number.isFinite(data.printEstimateSubtotalINR)||data.printEstimateSubtotalINR<0||!nonempty(data.printSubtotalScope))throw Error('Print subtotal needs a numeric amount and explicit partial scope');
  const printRows=data.rows.filter(row=>row.priceStatus==='live-calculator');
  if(!printRows.length||data.rows.some(row=>row.file&&row.priceStatus!=='live-calculator'))throw Error('Print subtotal requires completed calculator estimates for every cost-study model');
  if(Math.abs(printRows.reduce((sum,row)=>sum+row.amountINR,0)-data.printEstimateSubtotalINR)>.005)throw Error('Print subtotal must include calculator rows only; exclude component listings');
 }else if(data.printSubtotalScope!==undefined)throw Error('Print subtotal scope requires an explicit amount');
 if(data.selectedPrintBudget){
  const b=data.selectedPrintBudget;
  if(!Array.isArray(b.rowIds)||new Set(b.rowIds).size!==b.rowIds.length||b.rowIds.length!==3||!nonempty(b.scope))throw Error('Selected print budget needs three distinct scoped parts');
  const selected=b.rowIds.map(id=>data.rows.find(row=>row.id===id));
  if(selected.some(row=>!row||row.priceStatus!=='live-calculator'||row.quantity!==1))throw Error('Selected budget requires completed quantity-one calculator rows');
  if(!b.rowIds.includes('lower-case')||!b.rowIds.includes('knob')||!['riser-4deg','riser-7deg'].includes(b.riserId)||!b.rowIds.includes(b.riserId)||b.rowIds.filter(id=>id.startsWith('riser-')).length!==1)throw Error('One keyboard budget must include exactly one riser');
  if(!Number.isFinite(b.subtotalINR)||Math.abs(selected.reduce((sum,row)=>sum+row.amountINR,0)-b.subtotalINR)>.005)throw Error('Selected budget subtotal disagrees with included rows');
  if(b.hardwareQuantities?.riser!==1||b.hardwareQuantities.magnet!==4||b.hardwareQuantities.rubber_foot!==6||b.hardwareQuantities.fastener!==6||b.hardwareQuantities.fastener_nut!==6)throw Error('One-riser hardware quantities are inconsistent');
 }
 if(!Array.isArray(data.notes)||data.notes.some(note=>!nonempty(note)))throw Error('Robu exclusions must be explicit notes');
 return data;
}

export function validateFullKeyboardCost(data){
 if(data?.schemaVersion!==1||!/^\d{4}-\d{2}-\d{2}$/.test(data.reviewedAt)||!nonempty(data.scope)||!nonempty(data.closingRule))throw Error('Cost audit needs dated scope');
 if(data.totalINR!==null)throw Error('Incomplete cost audit must not imply a complete total');
 if(!data.counts||data.counts.riser!==1||data.counts.magnet!==4||data.counts.rubberFoot!==6||data.counts.keycap1u+data.counts.keycap2u!==28||data.counts.switchInstalled!==28||data.counts.switchPurchased<28)throw Error('Cost audit quantities disagree with one keyboard');
 const ids=new Set();
 if(!Array.isArray(data.rows)||!data.rows.length||!Array.isArray(data.optional))throw Error('Cost checklist is required');
 for(const row of data.rows){
  if(!/^[a-z0-9-]+$/.test(row.id)||ids.has(row.id))throw Error('Duplicate or invalid cost row');ids.add(row.id);
  for(const field of ['label','quantity','status','required'])if(!nonempty(row[field]))throw Error('Incomplete cost row: '+row.id);
  if(!Array.isArray(row.sources))throw Error('Cost row source list missing');
  for(const source of row.sources){if(!nonempty(source.title)||!/^https:\/\//.test(source.url))throw Error('Cost source needs title and HTTPS URL');}
 }
 for(const item of data.optional)if(!nonempty(item.label)||!nonempty(item.required))throw Error('Optional costs need explicit scope');
 return data;
}
