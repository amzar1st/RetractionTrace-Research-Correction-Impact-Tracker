import {abi} from 'genlayer-js';
const stable=x=>JSON.stringify(x,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.entries(v).sort(([a],[b])=>a.localeCompare(b))):v);
export async function verifyEffect({prepared,receipt,readContract,address}){
 if(!prepared)throw new Error('No prepared call is linked to this transaction. Use the report reader to inspect state.');
 if((receipt.to_address||'').toLowerCase()!==address?.toLowerCase())throw new Error('This transaction targets a different contract.');
 const raw=receipt.data?.calldata?.raw;
 if(!Array.isArray(raw))throw new Error('Receipt calldata is unavailable; call identity cannot be verified.');
 const call=abi.calldata.decode(new Uint8Array(raw));
 const method=call instanceof Map?call.get(''):call[''];const args=call instanceof Map?call.get('args'):call.args;
 if(method!==prepared.method||stable(args)!==stable(prepared.args))throw new Error('Transaction arguments do not match the prepared call.');
 const [rid,second]=prepared.args;let value;
 if(prepared.method==='register_report'){
  value=await readContract('get_report',[rid]);const original=JSON.parse(second);
  for(const k of ['title','version','description','claims','sources'])if(stable(value[k])!==stable(original[k]))throw new Error('Registered report differs from the prepared definition.');
  if(value.owner.toLowerCase()!==receipt.from_address?.toLowerCase())throw new Error('Registered owner differs from transaction sender.');
 }else if(prepared.method==='link_claim_sources'){
  value=await readContract('get_report',[rid]);if(stable(value.links)!==stable(JSON.parse(second)))throw new Error('Current links differ from the prepared call. A later transaction may have changed them.');
 }else if(prepared.method==='submit_notice'){
  value=await readContract('get_notice',[rid,second]);if(value.doi!==prepared.args[3]||value.source_id!==prepared.args[2]||value.kind!==prepared.args[4])throw new Error('Notice state differs from prepared call.');
 }else if(prepared.method==='assess_impact'){
  value=await readContract('get_assessment',[rid,second]);if(value.report_id!==rid||value.notice_id!==second||!value.assessment_hash)throw new Error('Assessment state could not be verified.');
 }else throw new Error('Unsupported verification method.');
 return value;
}
