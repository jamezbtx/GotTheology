import os, re
BIBLE='/workspace/gt-creeds-mock/public/bible'
NAMES={'genesis':'Genesis','exodus':'Exodus','ruth':'Ruth','psalms':'Psalm','proverbs':'Proverbs','isaiah':'Isaiah','daniel':'Daniel','jonah':'Jonah',
'matthew':'Matthew','mark':'Mark','luke':'Luke','john':'John','acts':'Acts','romans':'Romans','1-corinthians':'1 Corinthians','2-corinthians':'2 Corinthians',
'galatians':'Galatians','ephesians':'Ephesians','philippians':'Philippians','colossians':'Colossians','1-thessalonians':'1 Thessalonians','2-thessalonians':'2 Thessalonians',
'1-timothy':'1 Timothy','2-timothy':'2 Timothy','titus':'Titus','philemon':'Philemon','hebrews':'Hebrews','james':'James','1-peter':'1 Peter','2-peter':'2 Peter',
'1-john':'1 John','2-john':'2 John','3-john':'3 John','jude':'Jude','revelation':'Revelation'}
CCEL={'Gen':'genesis','Exod':'exodus','Ruth':'ruth','Ps':'psalms','Prov':'proverbs','Isa':'isaiah','Dan':'daniel','Jonah':'jonah','Matt':'matthew','Mark':'mark','Luke':'luke','John':'john','Acts':'acts','Rom':'romans','iCor':'1-corinthians','iiCor':'2-corinthians','Gal':'galatians','Eph':'ephesians','Phil':'philippians','Col':'colossians','iThess':'1-thessalonians','iiThess':'2-thessalonians','iTim':'1-timothy','iiTim':'2-timothy','Titus':'titus','Phlm':'philemon','Heb':'hebrews','Jas':'james','iPet':'1-peter','iiPet':'2-peter','iJohn':'1-john','iiJohn':'2-john','iiiJohn':'3-john','Jude':'jude','Rev':'revelation'}
# string abbreviations (lowercase, no dot) -> slug ; numbered handled separately
ABBR={'gen':'genesis','genesis':'genesis','exod':'exodus','exo':'exodus','ex':'exodus','exodus':'exodus','ruth':'ruth','ps':'psalms','psa':'psalms','psal':'psalms','psalm':'psalms','psalms':'psalms',
'prov':'proverbs','pro':'proverbs','proverbs':'proverbs','isa':'isaiah','isai':'isaiah','isaiah':'isaiah','esa':'isaiah','dan':'daniel','daniel':'daniel','jon':'jonah','jonah':'jonah',
'mat':'matthew','matt':'matthew','matth':'matthew','matthew':'matthew','mar':'mark','mark':'mark','luk':'luke','luke':'luke','joh':'john','john':'john','act':'acts','acts':'acts','rom':'romans','romans':'romans','kom':'romans',
'gal':'galatians','eph':'ephesians','ephes':'ephesians','phil':'philippians','philip':'philippians','col':'colossians','coloss':'colossians','tit':'titus','titus':'titus','philem':'philemon','heb':'hebrews','hebr':'hebrews',
'jam':'james','jas':'james','james':'james','jud':'jude','jude':'jude','rev':'revelation','revel':'revelation','apoc':'revelation'}
NUM={'cor':'corinthians','thes':'thessalonians','thess':'thessalonians','tim':'timothy','pet':'peter','joh':'john','john':'john','co':'corinthians'}
_idx=None
def index():
    global _idx
    if _idx is None:
        _idx={}
        for b in os.listdir(BIBLE):
            p=os.path.join(BIBLE,b)
            if not os.path.isdir(p): continue
            for c in os.listdir(p):
                if not c.isdigit(): continue
                rs=[]
                for f in os.listdir(os.path.join(p,c)):
                    m=re.match(r'^(\d+)-(\d+)\.html$',f)
                    if m: rs.append((int(m.group(1)),int(m.group(2))))
                _idx[(b,int(c))]=sorted(rs)
    return _idx
def resolve(slug,ch,v,v2=None):
    if not v: return None
    for a,b in index().get((slug,ch),[]):
        if a<=v<=b:
            href='/bible/%s/%d/%d-%d#v%d'%(slug,ch,a,b,v)
            lab='%s %d:%d'%(NAMES[slug],ch,v)+('–%d'%v2 if v2 and v2>v else '')
            return href,lab
    return None
def ccel(c):
    code,ch,v,v2=c
    s=CCEL.get(code)
    return resolve(s,ch,v,v2) if s else None
ROMAN={'i':1,'v':5,'x':10,'l':50,'c':100}
def roman(s):
    s=s.lower(); t=0
    for i,ch in enumerate(s):
        v=ROMAN[ch]; t+= -v if i+1<len(s) and ROMAN[s[i+1]]>v else v
    return t
REF=re.compile(r"(?:(\b[123]|\bI{1,3})\s*)?\b([A-Z][a-z]{1,6})\.?\s+([ivxlc]+|\d+)[\.:,]?\s*(\d+)(?:\s*[-–]\s*(\d+))?")
def parse(s):
    out=[]
    for m in REF.finditer(s):
        num,bk,ch,v,v2=m.groups(); bk=bk.lower()
        if num:
            n={'i':'1','ii':'2','iii':'3'}.get(num.lower(),num)
            base=NUM.get(bk)
            if not base: continue
            slug='%s-%s'%(n,base)
        else:
            slug=ABBR.get(bk)
        if not slug or slug not in NAMES: continue
        chn=int(ch) if ch.isdigit() else roman(ch)
        out.append((slug,chn,int(v),int(v2) if v2 and int(v2)>int(v) else None))
    return out
def chips(refs,limit):
    seen=set(); out=[]
    for r in refs:
        res=resolve(*r) if isinstance(r,tuple) else None
        if not res: continue
        page=res[0].split('#')[0]
        if page in seen: continue
        seen.add(page); out.append(res)
        if len(out)>=limit: break
    return out
def R(s):
    """curated: 'john 3:16' or 'john 3:16-18' or '1-john 2:2'"""
    m=re.match(r'^([\w-]+) (\d+):(\d+)(?:-(\d+))?$',s)
    r=(m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4)) if m.group(4) else None)
    if not resolve(*r): raise SystemExit('UNRESOLVED curated ref '+s)
    return r
