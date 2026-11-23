import {createClient} from 'genlayer-js';import {studionet} from 'genlayer-js/chains';import fs from 'node:fs';
const c=createClient({chain:studionet,endpoint:'https://studio.genlayer.com/api'});
let code=fs.readFileSync('contracts/retractiontrace.py','utf8');
if(process.argv.includes('--alias'))code=code.replace(/py-genlayer:[a-z0-9]+/,'py-genlayer:latest');
try{const s=await c.getContractSchemaForCode(code);fs.writeFileSync('docs/contract-schema.json',JSON.stringify(s,null,2));console.log(JSON.stringify(s));}catch(e){console.error(e.shortMessage||e.message);process.exitCode=1}
