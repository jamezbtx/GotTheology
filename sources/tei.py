import re
from lxml import etree
NS={'t':'http://www.tei-c.org/ns/1.0'}
def clean(el, keep_notes=False):
    el=etree.fromstring(etree.tostring(el,with_tail=False))
    if not keep_notes:
        for n in list(el.iter('{*}note')):
            tail=n.tail or ''; par=n.getparent(); prev=n.getprevious()
            if prev is not None: prev.tail=(prev.tail or '')+tail
            else: par.text=(par.text or '')+tail
            par.remove(n)
    # gaps
    for g in list(el.iter('{*}gap')):
        tail=g.tail or ''
        g.tail=None
        rep='•' if 'letter' in (g.get('extent') or '') else '[…]'
        par=g.getparent(); prev=g.getprevious()
        if prev is not None: prev.tail=(prev.tail or '')+rep+tail
        else: par.text=(par.text or '')+rep+tail
        par.remove(g)
    for g in list(el.iter('{*}g')):
        tail=g.tail or ''; par=g.getparent(); prev=g.getprevious()
        rep='' if g.get('ref')=='char:EOLhyphen' else (g.text or '')
        if prev is not None: prev.tail=(prev.tail or '')+rep+tail
        else: par.text=(par.text or '')+rep+tail
        par.remove(g)
    for pb in list(el.iter('{*}pb','{*}lb')):
        tail=pb.tail or ''; par=pb.getparent(); prev=pb.getprevious()
        if prev is not None: prev.tail=(prev.tail or '')+tail
        else: par.text=(par.text or '')+tail
        par.remove(pb)
    t=''.join(el.itertext())
    t=t.replace('ſ','s').replace('∣','').replace('­','')
    return re.sub(r'\s+',' ',t).strip()
def notes(el):
    return [re.sub(r'\s+',' ',''.join(n.itertext())).strip() for n in el.iter('{*}note')]
def load(fn):
    return etree.parse(fn).getroot()
