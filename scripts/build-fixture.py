import json,xml.etree.ElementTree as E
from pathlib import Path
norm=lambda e:' '.join(''.join(e.itertext()).split())
def source(sid,doi,selectors):
 r=E.parse('/tmp/'+sid+'.xml').getroot(); ps=[norm(p) for p in r.findall('.//body//p')]
 return {'id':sid,'doi':doi,'title':norm(r.find('.//article-title')),'version':'Publisher JATS retrieved 2026-11-23; excerpt snapshot','passages':[{'id':pid,'text':next(p for p in ps if term in p)} for pid,term in selectors]}
q=source('QAB','10.1371/journal.pone.0192773',[('MACRO','A Macro is provided'),('RELIABILITY','Test-retest reliability was calculated based on the 16')])
r=source('RAT','10.1371/journal.pone.0258946',[('AUTOMATION','We created a custom Android-based')])
v=source('REVIEW','10.1371/journal.pone.0194143',[('METHOD','A wide range of language tests')])
q['passages'].append({'id':'MISSING','text':'The original macro uses the expression capacity = 160 mAh/g.'})
report={'title':'Language assessment evidence review','version':'1.0','description':'Demonstration research report. Claims are illustrative audit inputs, not clinical guidance. The PLOS correction and cited publications are real. C5 intentionally includes an unverifiable excerpt to test missing evidence.','claims':[{'id':'C1','text':'The original QAB S1 scoring macro computes all summary measures correctly and can be reused unchanged.'},{'id':'C2','text':'The QAB study reported test-retest reliability based on 16 individuals with chronic aphasia.'},{'id':'C3','text':'The QAB produces eight summary measures ranging from 0 to 10.'},{'id':'C4','text':'The Russian Aphasia Test uses a tablet application to score comprehension subtests automatically.'},{'id':'C5','text':'The original QAB macro contains a capacity calculation of 160 mAh/g.'}], 'sources':[q,r,v]}
links=[{'claim_id':c,'source_id':s,'passage_ids':p} for c,s,p in [('C1','QAB',['MACRO']),('C2','QAB',['RELIABILITY']),('C3','QAB',['MACRO']),('C4','RAT',['AUTOMATION']),('C5','QAB',['MISSING'])]]
root=E.parse('/tmp/qab-notice.xml').getroot(); excerpt=norm(root.find('.//body/p'))
notice={'notice_id':'QAB_CORRECTION_2018','source_id':'QAB','doi':'10.1371/journal.pone.0199469','kind':'CORRECTION','excerpt':excerpt}
fixture={'report_id':'LANGUAGE_REVIEW_V1','report':report,'links':links,'notice':notice,'expected':['REVIEW_REQUIRED','UNAFFECTED','UNAFFECTED','UNAFFECTED','INSUFFICIENT_EVIDENCE']}
Path('public/fixture.json').write_text(json.dumps(fixture,indent=2)+'\n')
print('Fixture saved')
