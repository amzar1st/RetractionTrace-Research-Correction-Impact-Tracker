export const METHODS=['register_report','link_claim_sources','submit_notice','assess_impact'];
export function prepareCall(method,reportId,values){
 if(!/^[A-Za-z0-9_-]{1,48}$/.test(reportId))throw new Error('Use a report ID of 1–48 letters, digits, underscores or hyphens.');
 if(!METHODS.includes(method))throw new Error('Unknown method.');
 if(method==='register_report'){const p=JSON.parse(values.payload);if(!p.title||!Array.isArray(p.claims)||!Array.isArray(p.sources))throw new Error('Report needs a title, claims and sources.');return [reportId,JSON.stringify(p)];}
 if(method==='link_claim_sources'){const p=JSON.parse(values.payload);if(!Array.isArray(p))throw new Error('Links must be a JSON array.');return [reportId,JSON.stringify(p)];}
 if(!/^[A-Za-z0-9_-]{1,48}$/.test(values.noticeId))throw new Error('Enter a valid notice ID.');
 if(method==='assess_impact')return [reportId,values.noticeId];
 if(!/^[A-Za-z0-9_-]{1,48}$/.test(values.sourceId)||!/^10\.1371\/journal\.pone\.[0-9]{7}$/.test(values.doi)||!['CORRECTION','RETRACTION'].includes(values.kind)||!values.excerpt?.trim())throw new Error('Enter the source ID, PLOS ONE notice DOI, kind and exact excerpt.');
 return [reportId,values.noticeId,values.sourceId,values.doi,values.kind,values.excerpt];
}
