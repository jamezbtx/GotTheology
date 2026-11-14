import re, json, sys, copy
sys.path.insert(0,'/workspace/gt-creeds-mock/sources')
from bs4 import BeautifulSoup
from tei import load as tload, clean as tclean, NS
SRC='/workspace/gt-creeds-mock/sources/'
OUT='/workspace/gt-creeds-mock/mock-src/data/'
def norm(t): return re.sub(r'\s+',' ',t.replace('\xad','')).replace(' ,',',').replace(' ;',';').replace(' .','.').replace(' :',':').strip()
def soup(fn):
    return BeautifulSoup(open(SRC+fn).read(),'html.parser')
def cites_of(el):
    out=[]
    for a in el.select('a.scripRef'):
        m=re.search(r"goBible\('\w+','(\w+)','(\d+)','(\d+)','(\d+)','(\d+)'\)",a.get('onclick') or '')
        if m: out.append([m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(5)) if m.group(4)==m.group(2) else int(m.group(3))])
    return out
def strip_notes(el):
    for t in el.select('span.mnote, sup.Note, span.pb'): t.decompose()
    return el
def txt(el): return norm(el.get_text())
ROMAN=r'(?:[IVXL]+)'
def save(name,obj):
    json.dump(obj,open(OUT+name+'.json','w'),indent=1,ensure_ascii=False); print(name,len(obj['sections']))

# ---------- Heidelberg (German | English)
def heidelberg():
    s=soup('c3-iv.vi.html'); frags=[]
    for tr in s.find_all('tr'):
        tds=tr.find_all('td',recursive=False)
        if len(tds)==2 and 'width' in (tds[1].get('style') or '') :
            td=tds[1]; c=cites_of(td); strip_notes(td); frags.append((txt(td),c))
    secs=[]; part=None; head=None; cur=None; mode=None
    def tc(x): return re.sub(r"'S\b","'s",x.title()).replace(' Of ',' of ').replace(' The ',' the ').replace(' And ',' and ')
    for t,c in frags:
        if not t or set(t)<=set('—- '): continue
        m=re.match(r'^\(?Question ?(\d+)\.$',t)
        if m:
            cur={'key':'q'+m.group(1),'label':'Question '+m.group(1),'q':'','a':[],'part':part,'head':head,'cites':[],'paren':t.startswith('(')}; secs.append(cur); mode='q'; continue
        if t=='Answer.': mode='a'; cur['a'].append(''); continue
        if re.match(r"^THE (FIRST|SECOND|THIRD) PART\.$",t): part=tc(t.rstrip('.')); head=None; mode='parthead'; continue
        if mode=='a' and re.match(r'^[A-Z]+ COMMANDMENT\.$',t):
            cur['a'].append('§'+tc(t.rstrip('.'))); cur['a'].append(''); continue
        if t.isupper() and len(t)<90 and mode in ('a','parthead',None):
            if mode=='parthead': part=part+': '+tc(t.rstrip('.')); mode=None
            else: head=tc(t.rstrip('.'))
            continue
        if cur is None: continue
        if mode=='q': cur['q']=(cur['q']+' '+t).strip()
        else: cur['a'][-1]=(cur['a'][-1]+' '+t).strip()
        cur['cites']+=c
    for x in secs: x['a']=[p for p in x['a'] if p]
    save('heidelberg',{'sections':secs})
# ---------- Belgic (French | English)
def belgic():
    s=soup('c3-iv.viii.html'); secs=[]; cur=None; expect_title=False
    for tr in s.find_all('tr'):
        tds=tr.find_all('td',recursive=False)
        if len(tds)!=2 or 'width' not in (tds[1].get('style') or ''): continue
        td=tds[1]; c=cites_of(td); strip_notes(td)
        paras=[norm(p.get_text()) for p in td.find_all('p')] or [txt(td)]
        paras=[p for p in paras if p]
        if not paras: continue
        m=re.match(r'^Art\. ?([IVXL]+)\.?$',paras[0])
        if m:
            cur={'key':'art'+m.group(1),'label':'Article '+m.group(1),'title':'','paras':[],'cites':[]}; secs.append(cur); expect_title=True; continue
        if cur is None: continue
        if expect_title: cur['title']=paras[0].rstrip('.'); expect_title=False; continue
        for i,p in enumerate(paras):
            if cur['paras'] and i==0 and not re.search(r'[.:;!?\'’”)\]]$',cur['paras'][-1]): cur['paras'][-1]+=' '+p
            elif cur['paras'] and i==0 and p[:1].islower(): cur['paras'][-1]+=' '+p
            else: cur['paras'].append(p)
        cur['cites']+=c
    save('belgic',{'sections':secs})
# ---------- Dort English (RCA text, positive articles + conclusion)
def dort():
    s=soup('c3-iv.xvi.html')
    start=[h for h in s.find_all('h4') if 'anons of the' in h.get_text() and 'ynod of' in h.get_text()]
    h=start[-1]; secs=[]; cur=None; head=None
    for el in h.find_all_next(['p','h4']):
        c=cites_of(el); strip_notes(el); t=txt(el)
        if not t or t.startswith('As held by') or t.startswith('[We append'): continue
        if re.match(r'^(FIRST|SECOND|THIRD AND FOURTH|FIFTH) HEADS? OF DOCTRINE\.?$',t): head=t.rstrip('.').title(); cur=None; continue
        if t.strip().rstrip('.').upper()=='CONCLUSION': head='Conclusion'; cur={'key':'conclusion','label':'Conclusion','head':head,'title':'','paras':[],'cites':[]}; secs.append(cur); continue
        if head and cur is None and not re.match(r'^A[re]t',t): 
            headtitle=t.rstrip('.'); secs.append({'key':'h'+str(len(secs)),'kind':'head','title':head,'sub':headtitle}); continue
        m=re.match(r'^A[re]t\s?\.\s*([IVXL]+)\.\s*(.*)$',t)
        if m:
            cur={'key':'%s-%s'%(len([x for x in secs if x.get('kind')=='head']),m.group(1)),'label':'Article '+m.group(1),'head':head,'paras':[m.group(2)],'cites':c}; secs.append(cur); continue
        if t.startswith('« Prev') : break
        if cur is not None: cur['paras'].append(t); cur['cites']+=c
    save('dort',{'sections':secs})
# ---------- WCF (English | Latin)
def wcf():
    s=soup('c3-iv.xvii.ii.html')
    content=s.find('h3')
    secs=[]; cur=None; n=0
    for el in content.find_all_next(['tr','p']):
        if el.name=='p' and el.find_parent('td') is None:
            t=norm(copy.copy(el).get_text())
            if cur and (t.startswith('[') or 'American revision' in t or 'changed in the American' in t or t.startswith('The above')):
                e2=copy.copy(el); strip_notes(e2); cur['notes'].append(norm(e2.get_text()))
            continue
        if el.name!='tr': continue
        tds=el.find_all('td',recursive=False)
        if len(tds)==4 and cur is not None:
            # canonical book list rows: two English columns
            for i in (0,1):
                b=norm(tds[i].get_text()).rstrip('.')
                if b: cur.setdefault('books',[[],[]])[i].append(b)
            continue
        if len(tds)!=2 or 'width' not in (tds[0].get('style') or ''): continue
        td=tds[0]; c=cites_of(td); strip_notes(td); t=txt(td)
        if not t: continue
        if re.match(r'^Of \w',t) and len(t)<90 and t.endswith('.'):
            n+=1; cur={'key':'ch%d'%n,'label':'Chapter %d'%n,'title':t.rstrip('.'),'paras':[],'cites':[],'notes':[]}; secs.append(cur); continue
        if cur is None: continue
        if re.match(r'^[IVX]+\. ',t) or not cur['paras']: cur['paras'].append(t)
        else: cur['paras'][-1]+=' '+t
        cur['cites']+=c
    save('wcf',{'sections':secs})
# ---------- Remonstrance (Dutch | Latin | English)
def remonstrance():
    s=soup('c3-iv.xv.html'); frags=[]
    for tr in s.find_all('tr'):
        tds=tr.find_all('td',recursive=False)
        if len(tds)==3:
            td=tds[2]; c=cites_of(td); strip_notes(td); frags.append((txt(td),c))
    save('remonstrance_raw',{'sections':[{'t':t,'cites':c} for t,c in frags]})
# ---------- simple paragraph docs (Methodist, FWB)
def paras(fn,name):
    s=soup(fn); h=s.find('h3'); out=[]
    for el in h.find_all_next('p'):
        strip_notes(el); t=txt(el)
        if t: out.append(t)
    save(name,{'sections':[{'t':t} for t in out]})
# ---------- TCP docs
# Remonstrant Confession: gaps read from the 1676 page images (SEA PDF of the
# UMI microfilm). Keys = order of body-text gaps outside margin notes (see gaps.py).
REMFILLS={1:'f',2:'un',3:'e',4:'r',9:'f',10:'h',11:'d',20:'f',31:'f',40:'λύτρον',41:'λύτρον',42:'e',57:'f'}
def fill_gaps(body,fills):
    k=0
    for g in list(body.iter('{*}gap')):
        if any(isinstance(a.tag,str) and a.tag.endswith('note') for a in g.iterancestors()): continue
        k+=1
        if k not in fills: continue
        par=g.getparent(); prev=g.getprevious(); txt=fills[k]+(g.tail or '')
        if prev is not None: prev.tail=(prev.tail or '')+txt
        else: par.text=(par.text or '')+txt
        par.remove(g)
    return k
def tcp(fn,name,types=('chapter',),fills=None):
    r=tload(SRC+fn); body=r.find('.//t:body',NS); secs=[]
    if fills: assert fill_gaps(body,fills)==58
    for d in body.iter('{*}div'):
        if d.get('type') in types:
            h=d.find('t:head',NS); cur={'key':d.get('type')+(d.get('n') or ''),'head':tclean(h) if h is not None else d.get('type'),'paras':[],'notes':[]}
            for el in d.iter('{*}p','{*}head'):
                if el is h: continue
                if any(isinstance(an.tag,str) and an.tag.endswith('note') for an in el.iterancestors()): continue
                if el.tag.endswith('head'): cur['paras'].append('##'+tclean(el)); continue
                cur['paras'].append(tclean(el))
                cur['notes']+=[tclean(n,keep_notes=True) for n in el.iter('{*}note')]
            secs.append(cur)
    save(name,{'sections':secs})
heidelberg(); belgic(); dort(); wcf(); remonstrance()
paras('c3-v.vi.html','methodist'); paras('c3-v.ii.iii.html','fwb')
tcp('A34255.xml','lbcf'); tcp('A64246.xml','remconf',('chapter','conclusion'),REMFILLS)
