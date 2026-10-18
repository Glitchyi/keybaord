import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
const files={'/':'../index.html','/index.html':'../index.html','/index-light.html':'../index-light.html'};
const server=createServer(async(req,res)=>{const file=files[req.url];if(!file){res.writeHead(404);res.end('Not found');return}try{res.setHeader('Content-Type','text/html; charset=utf-8');res.end(await readFile(new URL(file,import.meta.url)))}catch{res.writeHead(500);res.end('Build the visualization first with npm run build.')}});
server.on('error',e=>{console.error('Preview server failed: '+e.message);process.exitCode=1});
server.listen(Number(process.env.PORT||8766),'127.0.0.1',()=>console.log('Preview: http://127.0.0.1:'+server.address().port));
