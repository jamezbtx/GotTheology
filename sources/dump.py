import sys,re
from ex import load
fn=sys.argv[1]
s=load(fn)
out=[]
for el in s.find_all(['p','h1','h2','h3','h4','h5','td']):
    if el.name=='td' : 
        if el.find(['p','h3','h4']): continue
    if el.find_parent('td') and el.name!='td' and False: pass
    t=re.sub(r'\s+',' ',el.get_text()).strip()
    if t: out.append(f'[{el.name}{"|L" if el.find_parent("td") and el.find_parent("td").find_previous_sibling("td") is None and el.find_parent("td").find_next_sibling("td") else ""}] {t}')
open(fn.replace('.html','.dump.txt'),'w').write('\n'.join(out))
print(fn,len(out))
