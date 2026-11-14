import json,re
from lxml import etree
r=etree.parse('/workspace/gt-creeds-mock/sources/A64246.xml').getroot()
body=r.find('.//{*}body')
# event stream
pos=0;page=None;pages={};gaps=[]
def innote(e): return any(isinstance(a.tag,str) and a.tag.endswith('note') for a in e.iterancestors()) or (isinstance(e.tag,str) and e.tag.endswith('note'))
def walk(e):
    global pos,page
    if isinstance(e.tag,str):
        t=e.tag.split('}')[1]
        if t=='pb' and e.get('rendition') is None:
            page=e.get('n') or 'x'+e.get('facs').split(':')[-1]; pages.setdefault(page,[pos,pos,e.get('facs').split(':')[-1]])
        if t=='gap' and not innote(e): gaps.append([page,pos])
        if t!='note' and e.text and t!='gap': pos+=len(e.text)
        if t!='note':
            for c in e: walk(c)
    if e.tail and not innote(e): pos+=len(e.tail)
    if page: pages[page][1]=pos
walk(body)
G=json.load(open('/tmp/gaps.json'))
for g,(p,ps) in zip(G,gaps):
    a,b,img=pages[p]; g['page']=p; g['frac']=round((ps-a)/max(1,b-a),2); assert img==g['img'],(img,g)
json.dump(G,open('/tmp/gaps.json','w'),ensure_ascii=False,indent=0)
for g in G: print(g['n'],g['img'],g['page'],g['frac'])
