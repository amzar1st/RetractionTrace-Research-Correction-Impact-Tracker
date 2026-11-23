import assert from 'node:assert/strict';import fs from 'node:fs';import crypto from 'node:crypto';
import {CONFIG as C} from '../src/config.js';import {client,readContract} from '../src/chain.js';import {classifyTransaction} from '../src/lifecycle.js';import {verifyEffect} from '../src/verify-effect.js';
const fixture=JSON.parse(fs.readFileSync('public/fixture.json','utf8'));const progress=JSON.parse(fs.readFileSync('docs/deployment-progress.json','utf8'));
const source=fs.readFileSync('contracts/retractiontrace.py','utf8');
const deployed=await client.getContractCode(C.address);
assert.equal(typeof deployed==='string'?deployed:new TextDecoder().decode(deployed),source,'Deployed source differs');
const [report,notice,assessment]=await Promise.all([readContract('get_report',[C.demoReport]),readContract('get_notice',[C.demoReport,C.demoNotice]),readContract('get_assessment',[C.demoReport,C.demoNotice])]);
const claims=await Promise.all(report.claims.map(c=>readContract('get_claim_status',[C.demoReport,c.id])));
assert.deepEqual(assessment.findings.map(f=>f.status),fixture.expected);
assert.equal(report.sources.length,3);assert.equal(report.claims.length,5);assert.equal(report.links.length,5);assert.equal(notice.report_hash,report.content_hash);assert.equal(assessment.report_hash,report.content_hash);assert.equal(assessment.notice_hash,notice.publisher_hash);
const norm=s=>s.replace(/\s+/g,' ').trim();
for(const f of assessment.findings){assert.ok(norm(notice.verified_body).includes(norm(f.notice_quote)));for(const c of f.citations){const p=report.sources.find(s=>s.id===c.source_id).passages.find(p=>p.id===c.passage_id);assert.ok(norm(p.text).includes(norm(c.quote)));assert.equal(assessment.verified_sources[c.source_id].passages[c.passage_id],true)}}
assert.equal(assessment.verified_sources.QAB.passages.MISSING,false);
for(let i=0;i<claims.length;i++)assert.equal(claims[i].status,fixture.expected[i]);
const transactions=[];
for(const t of progress.transactions){const tx=await client.getTransaction({hash:t.hash});const state=classifyTransaction(tx);assert.equal(tx.statusName,'FINALIZED',t.method+' not finalized');assert.equal(tx.execution_mode,'NORMAL');if(t.expectedFailure)assert.equal(state.phase,'failed');else assert.equal(state.phase,'finalized',t.method+' execution failed');assert.equal(tx.to_address.toLowerCase(),C.address.toLowerCase());
 if(!t.expectedFailure&&t.method!=='deploy'){const n=fixture.notice;const args=t.method==='register_report'?[fixture.report_id,JSON.stringify(fixture.report)]:t.method==='link_claim_sources'?[fixture.report_id,JSON.stringify(fixture.links)]:t.method==='submit_notice'?[fixture.report_id,n.notice_id,n.source_id,n.doi,n.kind,n.excerpt]:[fixture.report_id,n.notice_id];await verifyEffect({prepared:{method:t.method,args},receipt:tx,readContract,address:C.address})}
 transactions.push({...t,status:tx.statusName,execution:tx.txExecutionResultName,mode:tx.execution_mode,from:tx.from_address,to:tx.to_address,votes:tx.last_round?.validator_votes_name||[],url:C.explorer+'/tx/'+t.hash});
}
const manifest={project:C.name,network:C.network,chainId:C.chainId,rpc:C.rpc,contract:C.address,contractExplorer:C.explorer+'/address/'+C.address,website:'https://retractiontrace.wirymink515.chatgpt.site',verifiedAt:new Date().toISOString(),sourceSha256:crypto.createHash('sha256').update(source).digest('hex'),reportId:C.demoReport,noticeId:C.demoNotice,reportHash:report.content_hash,noticeHash:notice.publisher_hash,assessmentHash:assessment.assessment_hash,checks:{deployedSourceMatches:true,officialNoticeVerified:true,allFiveExpectedStatusesMatch:true,citationsGrounded:true,unverifiablePassageRejected:true,transactionEffectsVerified:true,allTransactionsFinalized:true,normalConsensusMode:true},transactions};
fs.writeFileSync('public/verification.json',JSON.stringify(manifest,null,2)+'\n');fs.writeFileSync('docs/verified-state.json',JSON.stringify({verifiedAt:manifest.verifiedAt,report,notice,assessment,claims},null,2)+'\n');
console.log(JSON.stringify({checks:manifest.checks,statuses:assessment.findings.map(f=>({id:f.claim_id,status:f.status})),transactions:transactions.map(t=>({method:t.method,status:t.status,execution:t.execution}))},null,2));
