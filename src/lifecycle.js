export const validHash=h=>/^0x[0-9a-fA-F]{64}$/.test(h);
export function classifyTransaction(tx){
 if(!tx)return {phase:'unknown',terminal:false,message:'The RPC has not returned a transaction. Keep the hash and check again.'};
 const status=String(tx.statusName??tx.status??'UNKNOWN').toUpperCase();
 const raw=tx.consensus_data?.leader_receipt;
 const receipt=Array.isArray(raw)?raw.find(r=>r.mode==='leader')||raw[0]:raw;
 const result=tx.txExecutionResultName??tx.execution_result??receipt?.execution_result;
 const name=String(typeof result==='string'?result:result?.result_name??'').toUpperCase();
 const number=typeof result==='number'?result:result?.result;
 const failed=['FAILED','CANCELED','CANCELLED','UNDETERMINED','LEADER_TIMEOUT','VALIDATORS_TIMEOUT','REJECTED'].includes(status)||['ERROR','REVERT','VM_ERROR','INTERNAL_ERROR','FAILURE','FINISHED_WITH_ERROR','FINISHED_WITH_REVERT','TIMEOUT'].includes(name)||(typeof number==='number'&&number!==0);
 if(failed)return {phase:'failed',terminal:true,status,message:'Execution or consensus failed. Inspect the receipt before preparing another transaction.'};
 const executionVerified=['SUCCESS','RETURN','FINISHED_WITH_RETURN'].includes(name)||number===0;
 if(status==='FINALIZED')return {phase:executionVerified?'finalized':'unverified',terminal:true,status,executionVerified,message:executionVerified?'Finalized with successful execution. Read contract state to verify the result.':'Finalized; the execution result could not be verified from this receipt.'};
 if(status==='ACCEPTED')return {phase:'accepted',terminal:false,status,message:'Accepted by consensus. Waiting for network finality.'};
 return {phase:'pending',terminal:false,status,message:'The network is processing this transaction.'};
}
export async function trackTransaction({hash,getTransaction,onUpdate,signal,attempts=90,interval=4000,delay=ms=>new Promise(r=>setTimeout(r,ms))}){
 if(!validHash(hash))throw new Error('Enter a 32-byte transaction hash beginning with 0x.');
 for(let i=0;i<attempts;i++){
  if(signal?.aborted)return {phase:'stopped',terminal:false};
  let tx;try{tx=await getTransaction(hash)}catch(error){onUpdate({phase:'rpc_error',terminal:false,message:'Receipt lookup failed: '+(error.shortMessage||error.message)});throw error}
  if(signal?.aborted)return {phase:'stopped',terminal:false};
  const state=classifyTransaction(tx);onUpdate({...state,receipt:tx,hash});if(state.terminal)return state;
  await delay(interval);
 }
 const state={phase:'timeout',terminal:false,message:'Tracking paused after six minutes. The transaction may still finalize; resume with the same hash.'};onUpdate(state);return state;
}
export const escapeHtml=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
