import fs from 'node:fs';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
const moduleName=process.env.PLAYWRIGHT_MODULE;
const imported=await import(moduleName?pathToFileURL(moduleName).href:'playwright');
const {chromium}=imported.default??imported;
const base=process.env.SITE_URL||'http://127.0.0.1:8766/keybaord/';
const output=process.env.CHECK_OUTPUT||'/private/tmp/keybaord-browser-check';fs.mkdirSync(output,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});
const errors=[],badResponses=[];page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)badResponses.push({url:r.url(),status:r.status()});});
await page.goto(base,{waitUntil:'networkidle'});
await page.waitForFunction(()=>window.keypadPreview?.state.sourceSpecHash);
assert.equal(await page.locator('[data-flat-key]').count(),28);
assert.equal(await page.locator('[data-bom-id]').count(),24);
assert.equal(await page.locator('[data-drawing-panel]').count()>=27,true);
const hash=await page.evaluate(()=>window.keypadPreview.state.sourceSpecHash);
const expected=JSON.parse(fs.readFileSync('spec/resolved.json','utf8')).sourceSpecHash;assert.equal(hash,expected);
await page.screenshot({path:output+'/desktop.png',fullPage:false});
const cap=page.locator('[data-pose="4"] [data-key="a"]');const box=await cap.boundingBox();assert(box,'Visible A cap');await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();assert((await page.evaluate(()=>window.keypadPreview.state.held)).includes('a'),'Actual pointer press on A');await page.mouse.up();assert.equal((await page.evaluate(()=>window.keypadPreview.state.held)).length,0);await page.keyboard.press('ArrowRight');assert.equal(await page.evaluate(()=>window.keypadPreview.state.selected),'s');
await page.locator('#exploded').click();await page.waitForFunction(()=>window.keypadPreview.state.explode>.98);
await page.screenshot({path:output+'/exploded.png',fullPage:false});
await page.locator('[data-riser="7"]').click();assert.equal(await page.evaluate(()=>window.keypadPreview.state.angle),7);
assert.equal(await page.locator('[data-pose="7"]').getAttribute('hidden'),null);
assert.notEqual(await page.locator('[data-pose="4"]').getAttribute('hidden'),null);
await page.locator('#assembled').click();await page.locator('#top-view').click();assert.equal(await page.locator('#flat-view').isVisible(),true);
await page.locator('[data-flat-key="space"]').focus();await page.keyboard.down(' ');assert((await page.evaluate(()=>window.keypadPreview.state.held)).includes('space'));await page.keyboard.up(' ');
await page.locator('#brightness').fill('20');assert.equal(await page.evaluate(()=>window.keypadPreview.state.brightness),.2);
await page.locator('#overlay-select').selectOption('Fusion');assert.equal(await page.evaluate(()=>window.keypadPreview.state.overlay),'Fusion');
await page.locator('#theme-toggle').click();assert.equal(await page.locator('body').getAttribute('data-theme'),'light');
await page.locator('#top-view').click();await page.locator('[data-riser="0"]').click();await page.screenshot({path:output+'/light-flat.png',fullPage:false});
await page.locator('[data-sheet="switch"]').click();assert.equal(await page.locator('[data-drawing-panel="switch"]').isVisible(),true);
await page.locator('#drawings').scrollIntoViewIfNeeded();await page.screenshot({path:output+'/drawing-switch.png',fullPage:false});
await page.locator('[data-sheet="riser_4"]').click();await page.screenshot({path:output+'/drawing-riser.png',fullPage:false});
for(const width of [900,390]){await page.setViewportSize({width,height:1000});await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:output+'/width-'+width+'.png',fullPage:false});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Horizontal page overflow '+width);}
await page.emulateMedia({reducedMotion:'reduce'});await page.locator('#exploded').click();await page.waitForFunction(()=>window.keypadPreview.state.explode===1);await page.locator('#tour-toggle').click();assert.equal(await page.evaluate(()=>window.keypadPreview.state.touring),false);
await page.evaluate(()=>{window.keypadPreview.press('w',true);window.dispatchEvent(new Event('blur'));});assert.equal((await page.evaluate(()=>window.keypadPreview.state.held)).length,0);
const statuses=await page.locator('video').evaluateAll(async videos=>Promise.all(videos.map(async v=>{
 if(v.readyState<1){v.load();await new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(new Error('Video metadata timeout '+v.currentSrc)),20000);v.addEventListener('loadedmetadata',()=>{clearTimeout(timer);resolve();},{once:true});v.addEventListener('error',()=>{clearTimeout(timer);reject(new Error('Video error '+v.currentSrc));},{once:true});});}
 return {src:v.currentSrc,ready:v.readyState,width:v.videoWidth,height:v.videoHeight,duration:v.duration,error:v.error?.message??null};
})));
if(process.env.REQUIRE_MEDIA==='1'){assert.equal(statuses.length,3,'Three native clips required');for(const v of statuses){assert(v.ready>=1);assert.equal(v.width,960);assert.equal(v.height,720);assert.equal(v.error,null);}assert.deepEqual(statuses.map(v=>Math.round(v.duration)).sort((a,b)=>a-b),[4,8,12]);}
assert.deepEqual(badResponses,[],'Failed web responses');
assert.deepEqual(errors,[],'Browser exceptions');
fs.writeFileSync(output+'/report.json',JSON.stringify({base,sourceSpecHash:hash,desktop:true,mobile:true,controls:true,reducedMotion:true,errors,badResponses,videos:statuses},null,2));
console.log(JSON.stringify({base,sourceSpecHash:hash,drawings:await page.locator('[data-drawing-panel]').count(),videos:statuses.length,screenshots:output,errors}));await browser.close();
