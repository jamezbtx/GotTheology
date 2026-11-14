import re,os,glob
from bs4 import BeautifulSoup
PUB='/workspace/gt-creeds-mock/public'
bible=set(); problems=[]
for f in sorted(glob.glob(PUB+'/creeds/*.html')):
    h=open(f).read(); s=BeautifulSoup(h,'html.parser')
    ids={x.get('id') for x in s.find_all(id=True)}
    if 'noindex' not in h: problems.append((f,'no noindex'))
    if re.search(r'adsbygoogle|googlesyndication|made_with_ai',h,re.I): problems.append((f,'ad/ai'))
    if '[[' in h: problems.append((f,'marker left'))
    for a in s.find_all('a',href=True):
        u=a['href']
        if u.startswith('#'):
            if u[1:] not in ids: problems.append((f,'bad anchor '+u))
        elif u.startswith('/'):
            path,_,frag=u.partition('#')
            cand=[PUB+path, PUB+path+'.html', PUB+path.rstrip('/')+'/index.html']
            if not any(os.path.isfile(c) for c in cand): problems.append((f,'missing '+u))
            if path.startswith('/bible/'): bible.add(u)
            if frag and path.startswith('/creeds/'):
                tf=[c for c in cand if os.path.isfile(c)][0]
                if f'id="{frag}"' not in open(tf).read(): problems.append((f,'bad xanchor '+u))
            if frag and path.startswith('/bible/'):
                tf=[c for c in cand if os.path.isfile(c)][0]
                if f'id="{frag}"' not in open(tf).read(): problems.append((f,'bad bible anchor '+u))
    n=len(s.select('a.creed-ref')); print(os.path.basename(f), 'chips',n, 'sources', len(s.select('.creed-sources li')))
print('unique bible urls',len(bible)); print(problems[:30], len(problems))
open('/tmp/bible_urls.txt','w').write('\n'.join(sorted(bible)))
