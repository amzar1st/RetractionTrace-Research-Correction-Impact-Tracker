/** A single notice needs no extra per-claim RPC reads: its committed findings
 * are already the complete aggregate. Multiple notices use the contract getter. */
export function singleNoticeStatuses(report,notice,assessment){
 if(report.notice_ids.length>1)return null;
 const pending=report.notice_ids.length>0&&!notice?.assessed;
 return Object.fromEntries(report.claims.map(c=>{
  const finding=assessment?.findings.find(f=>f.claim_id===c.id);
  return [c.id,{claim_id:c.id,status:finding?.status||'INSUFFICIENT_EVIDENCE',pending_notices:pending?report.notice_ids:[],history:finding?[{notice_id:notice.id,assessment_hash:assessment.assessment_hash,finding}]:[],scope:'Registered notices only; not an automatic literature monitor'}];
 }));
}
