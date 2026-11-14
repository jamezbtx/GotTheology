# list body-text gaps (not in notes) in A64246 with page image no. and context
import re,json,sys
from lxml import etree
X='/workspace/gt-creeds-mock/sources/A64246.xml'
r=etree.parse(X).getroot()
body=r.find('.//{*}body')
out=[];page=None;chap=None
def txt(e):
    return ''.join(e.itertext())
for el in body.iter():
    if not isinstance(el.tag,str): continue
    t=el.tag.split('}')[1]
    if t=='pb' and el.get('rendition') is None: page=el.get('facs').split(':')[-1]
    if t=='div' and el.get('type') in('chapter','conclusion'): chap=el.get('type')+(el.get('n') or '')
    if t=='gap':
        if any(isinstance(a.tag,str) and a.tag.endswith('note') for a in el.iterancestors()): continue
        # context: text of parent paragraph around gap
        par=el.getparent()
        while par.tag.split('}')[1] not in('p','head'): par=par.getparent()
        mark='⟦GAP⟧'
        # build string with gap marker
        cp=etree.fromstring(etree.tostring(par,with_tail=False))
        idx=[g for g in par.iter('{*}gap')].index(el)
        gs=list(cp.iter('{*}gap'))
        for i,g in enumerate(gs):
            g.text=None
            for c in list(g): g.remove(c)
        gs[idx].text=mark
        for n in list(cp.iter('{*}note')):
            if mark not in txt(n): n.text=None; [n.remove(c) for c in list(n)]
        s=re.sub(r'\s+',' ',txt(cp)).replace('ſ','s')
        i=s.index(mark)
        out.append(dict(n=len(out)+1,img=page,chap=chap,ext=el.get('extent') or el.get('reason'),ctx=s[max(0,i-45):i]+'⟦'+(el.get('extent') or el.get('reason'))+'⟧'+s[i+len(mark):i+len(mark)+30]))
json.dump(out,open('/tmp/gaps.json','w'),ensure_ascii=False,indent=0)
for o in out: print(o['n'],o['img'],o['chap'],'|',o['ctx'])
print(len(out))
