import sys,re
from bs4 import BeautifulSoup
def load(fn):
    s=BeautifulSoup(open(fn).read(),'html.parser')
    for t in s.select('span.mnote, sup.Note, span.pb'): t.decompose()
    return s
def rows(fn, col=-1):
    s=load(fn); out=[]
    for tr in s.find_all('tr'):
        tds=tr.find_all('td',recursive=False)
        if len(tds)>=2:
            out.append(tds[col])
    return s,out
if __name__=='__main__':
    fn=sys.argv[1]
    s,r=rows(fn)
    print(fn,'rows',len(r))
    for td in r[:int(sys.argv[2]) if len(sys.argv)>2 else 6]:
        print('---',re.sub(r'\s+',' ',td.get_text(' '))[:300])
