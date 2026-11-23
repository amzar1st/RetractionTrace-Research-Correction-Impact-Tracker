"""Contract logic tests with an explicit in-memory GenVM boundary double.
These do not claim to emulate GenVM execution, real web fetches, or model consensus.
"""
import unittest, sys, types, importlib.util, json, copy
from pathlib import Path
NS=types.SimpleNamespace
class Return:
    def __init__(self,value):self.calldata=value
class Storage:
    def __class_getitem__(cls,_):return dict
class Array:
    def __class_getitem__(cls,_):return list
class Contract:pass
class VM:
    Return=Return
    @staticmethod
    def run_nondet_unsafe(leader,validator):
        value=leader()
        if not validator(Return(copy.deepcopy(value))):raise ValueError('Independent validator rejected result')
        return value
G=types.ModuleType('genlayer');G.__all__=['gl','TreeMap','DynArray'];G.gl=G;G.Contract=Contract;G.TreeMap=Storage;G.DynArray=Array;G.contract=NS(Contract=Contract);G.storage=NS(TreeMap=Storage,DynArray=Array)
G.public=NS(view=lambda f:f,write=lambda f:f);G.message=NS(sender_address='owner');G.vm=VM;G.nondet=NS(web=NS(),exec_prompt=None)
sys.modules['genlayer']=G;sys.modules['genlayer.types']=types.ModuleType('genlayer.types')
spec=importlib.util.spec_from_file_location('contract',Path(__file__).parents[1]/'contracts/retractiontrace.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
F=json.loads((Path(__file__).parents[1]/'public/fixture.json').read_text())

def xml(doi,body,kind='research-article',author='Smith',target=''):
    return f'<article article-type="{kind}"><front><article-meta><article-id pub-id-type="doi">{doi}</article-id><contrib><surname>{author}</surname></contrib><related-article xlink:href="info:doi/{target}"/></article-meta></front><body>{body}</body></article>'

class Tests(unittest.TestCase):
    def setUp(self):
        G.message.sender_address='owner'
        self.c=m.RetractionTrace();self.c.reports={};self.c.report_ids=[];self.c.notices={};self.c.assessments={}
        self.docs={s['doi']:xml(s['doi'],' '.join(p['text'] for p in s['passages'] if p['id']!='MISSING'),author=s['id']) for s in F['report']['sources']}
        self.docs[F['notice']['doi']]=xml(F['notice']['doi'],F['notice']['excerpt'],'correction',target=F['report']['sources'][0]['doi'])
        G.nondet.web.get=lambda url:NS(status=200,body=self.docs[url.split('id=')[1].split('&')[0]].encode())
        self.c.register_report('R',json.dumps(F['report']));self.c.link_claim_sources('R',json.dumps(F['links']))
    def notice(self):
        n=F['notice'];self.c.submit_notice('R','N',n['source_id'],n['doi'],n['kind'],n['excerpt'])
    def result(self):
        fs=[]
        for i,c in enumerate(F['report']['claims']):
            linked=F['links'][i];sid=linked['source_id'];pid=linked['passage_ids'][0]
            passage=next(p for s in F['report']['sources'] if s['id']==sid for p in s['passages'] if p['id']==pid)
            fs.append({'claim_id':c['id'],'relation':'AFFECTED' if i==0 else 'UNCLEAR' if i==4 else 'UNRELATED','remaining_sources':[],
            'citations':[{'source_id':sid,'passage_id':pid,'quote':passage['text']}] if i<3 else [],'notice_quote':F['notice']['excerpt'] if sid=='QAB' else '', 'reason':'Exact notice limits the correction to the scoring macro.'})
        return {'findings':fs}
    def test_report_and_schema_bounds(self):
        self.assertEqual(json.loads(self.c.get_report('R'))['owner'],'owner')
        with self.assertRaises(ValueError):self.c.register_report('R',json.dumps(F['report']))
        p=copy.deepcopy(F['report']);p['sources'][0]['doi']='http://127.0.0.1'
        with self.assertRaises(ValueError):m.parse_report(json.dumps(p))
    def test_links_reject_duplicates_unknown_passages(self):
        with self.assertRaises(ValueError):self.c.link_claim_sources('R',json.dumps(F['links']+[F['links'][0]]))
        l=copy.deepcopy(F['links']);l[0]['passage_ids']=['FAKE']
        with self.assertRaises(ValueError):self.c.link_claim_sources('R',json.dumps(l))
    def test_owner_guard(self):
        G.message.sender_address='attacker'
        with self.assertRaises(ValueError):self.c.link_claim_sources('R','[]')
        with self.assertRaises(ValueError):self.notice()
    def test_notice_authentication_seal_and_duplicate(self):
        self.notice()
        with self.assertRaises(ValueError):self.notice()
        with self.assertRaises(ValueError):self.c.link_claim_sources('R','[]')
        n=F['notice']
        with self.assertRaises(ValueError):self.c.submit_notice('R','N2',n['source_id'],n['doi'],n['kind'],n['excerpt'])
    def test_reference_in_body_does_not_authenticate_target(self):
        d=F['notice']['doi'];self.docs[d]=xml(d,F['notice']['excerpt']+' '+F['report']['sources'][0]['doi'],'correction',target='10.1371/journal.pone.0000001')
        with self.assertRaises(ValueError):self.notice()
    def test_notice_wrong_kind_and_forged_excerpt(self):
        d=F['notice']['doi'];self.docs[d]=self.docs[d].replace('article-type="correction"','article-type="research-article"')
        with self.assertRaises(ValueError):self.notice()
    def test_end_to_end_assessment_and_immutable_history(self):
        self.notice();G.nondet.exec_prompt=lambda *a,**k:copy.deepcopy(self.result())
        self.c.assess_impact('R','N');a=json.loads(self.c.get_assessment('R','N'))
        self.assertEqual([f['status'] for f in a['findings']],F['expected'])
        self.assertEqual(json.loads(self.c.get_claim_status('R','C1'))['status'],'REVIEW_REQUIRED')
        with self.assertRaises(ValueError):self.c.assess_impact('R','N')
    def test_unassessed_notices_are_not_unaffected(self):
        self.notice();self.assertEqual(json.loads(self.c.get_claim_status('R','C2'))['status'],'INSUFFICIENT_EVIDENCE')
    def test_fabricated_quote_rejected(self):
        self.notice();r=self.result();r['findings'][0]['citations'][0]['quote']='invented result';G.nondet.exec_prompt=lambda *a,**k:r
        with self.assertRaises(ValueError):self.c.assess_impact('R','N')
    def test_validator_independently_disagrees(self):
        self.notice();count=[0]
        def model(*a,**k):
            r=self.result();count[0]+=1
            if count[0]>1:r['findings'][0]['relation']='UNRELATED'
            return r
        G.nondet.exec_prompt=model
        with self.assertRaisesRegex(ValueError,'rejected'):self.c.assess_impact('R','N')
    def test_retraction_never_proves_false_or_unaffected(self):
        self.assertEqual(m.derive_status('AFFECTED',[],'RETRACTION'),'REVIEW_REQUIRED')
        self.notice();r=self.result();notice=json.loads(self.c.get_notice('R','N'));notice['kind']='RETRACTION'
        verified={s['id']:{'authors':[s['id']],'passages':{p['id']:True for p in s['passages']}} for s in F['report']['sources']}
        with self.assertRaises(ValueError):m.validate_result(r,json.loads(self.c.get_report('R')),notice,verified)
    def test_battery_correction_and_independent_support(self):
        self.assertEqual(m.derive_status('AFFECTED',['INDEPENDENT_BATTERY_STUDY'],'CORRECTION'),'SUPPORT_WEAKENED')
        self.assertEqual(m.derive_status('AFFECTED',[],'CORRECTION'),'REVIEW_REQUIRED')
        self.assertEqual(m.derive_status('UNRELATED',[],'CORRECTION'),'UNAFFECTED')
        self.assertEqual(m.derive_status('UNCLEAR',[],'CORRECTION'),'INSUFFICIENT_EVIDENCE')
    def test_same_source_cannot_be_independent(self):
        self.notice();r=self.result();r['findings'][0]['remaining_sources']=['QAB'];G.nondet.exec_prompt=lambda *a,**k:r
        with self.assertRaises(ValueError):self.c.assess_impact('R','N')
    def test_publisher_doi_mismatch(self):
        d=F['notice']['doi'];self.docs[d]=self.docs[d].replace('<article-id pub-id-type="doi">'+d,'<article-id pub-id-type="doi">10.1371/journal.pone.0000000')
        with self.assertRaises(ValueError):self.notice()
    def test_missing_paper_and_missing_quote_fail_closed(self):
        self.notice();del self.docs[F['report']['sources'][0]['doi']];G.nondet.exec_prompt=lambda *a,**k:self.result()
        with self.assertRaises(ValueError):self.c.assess_impact('R','N')

    def test_independent_support_is_committed_and_overlap_rejected(self):
        report=json.loads(self.c.get_report('R'))
        report['links'].append({'claim_id':'C1','source_id':'RAT','passage_ids':['AUTOMATION']})
        self.c.reports['R']=m.canonical(report)
        self.notice()
        def supported(*a,**k):
            r=self.result();r['findings'][0]['remaining_sources']=['RAT']
            r['findings'][0]['citations'].append({'source_id':'RAT','passage_id':'AUTOMATION','quote':F['report']['sources'][1]['passages'][0]['text']})
            return r
        G.nondet.exec_prompt=supported
        self.c.assess_impact('R','N')
        self.assertEqual(json.loads(self.c.get_assessment('R','N'))['findings'][0]['status'],'SUPPORT_WEAKENED')
        # This tests structural independence gates with a mocked semantic model,
        # not whether RAT semantically corroborates the actual QAB macro claim.
        r=supported();v={x['id']:{'authors':['same'],'passages':{p['id']:True for p in x['passages']}} for x in F['report']['sources']}
        with self.assertRaisesRegex(ValueError,'Overlapping authors'):
            m.validate_result(r,report,json.loads(self.c.get_notice('R','N')),v)

    def test_newer_notice_cannot_erase_prior_review(self):
        self.notice();G.nondet.exec_prompt=lambda *a,**k:self.result();self.c.assess_impact('R','N')
        r=json.loads(self.c.get_report('R'));r['notice_ids'].append('N2');self.c.reports['R']=m.canonical(r)
        self.assertEqual(json.loads(self.c.get_claim_status('R','C1'))['status'],'REVIEW_REQUIRED')
        self.assertEqual(json.loads(self.c.get_claim_status('R','C2'))['status'],'INSUFFICIENT_EVIDENCE')
        a=json.loads(self.c.get_assessment('R','N'));a['findings'][0]['status']='UNAFFECTED';self.c.assessments['R/N2']=m.canonical(a)
        self.assertEqual(json.loads(self.c.get_claim_status('R','C1'))['status'],'REVIEW_REQUIRED')

if __name__=='__main__':unittest.main()
