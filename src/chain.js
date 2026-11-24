import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {CONFIG} from './config.js';
export const client=createClient({chain:studionet,endpoint:CONFIG.rpc});
export async function readContract(functionName,args=[]){
 if(!CONFIG.address)throw new Error('Contract deployment has not yet been verified.');
 let result;try{result=await client.readContract({address:CONFIG.address,functionName,args,transactionHashVariant:'latest-final'});}catch(error){const detail=[error.message,error.details,error.cause?.message].filter(Boolean).join(' ');if(/rate limit|too many requests/i.test(detail))throw new Error('GenLayer rate limit reached. Wait one minute, then refresh.');throw error}
 return typeof result==='string'?JSON.parse(result):result;
}
export const getTransaction=hash=>client.getTransaction({hash});
