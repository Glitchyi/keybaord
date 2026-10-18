import {createServer} from 'node:http';
import {readFile, stat} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=fileURLToPath(new URL('../dist/',import.meta.url));
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp','.mp4':'video/mp4','.ico':'image/x-icon'};
const server=createServer(async(req,res)=>{
  try{
    let pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    if(pathname==='/keybaord')pathname='/keybaord/';
    if(pathname.startsWith('/keybaord/'))pathname=pathname.slice('/keybaord'.length);
    if(pathname.endsWith('/'))pathname+='index.html';
    const file=path.resolve(root,'.'+pathname);
    if(!file.startsWith(root)||!mime[path.extname(file)]||!(await stat(file)).isFile()){res.writeHead(404);res.end('Not found');return}
    res.setHeader('Content-Type',mime[path.extname(file)]);res.setHeader('Cache-Control','no-store');res.end(await readFile(file));
  }catch{res.writeHead(404);res.end('Not found. Run npm run build first.');}
});
server.on('error',e=>{console.error('Preview server failed: '+e.message);process.exitCode=1});
server.listen(Number(process.env.PORT||8766),'127.0.0.1',()=>console.log('Preview: http://127.0.0.1:'+server.address().port+'/keybaord/'));
