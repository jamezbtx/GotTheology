import re
from frame import page, esc, chipsrow, OUT
from sources_reg import SRC
from lib import chips as mkchips
NUMRE=re.compile(r'^((?:[IVXL]+|\d+)\.)\s+')
def para(t, cls='creed-para'):
    t=esc(t)
    if t.startswith('##'): return f'<p class="creed-subhead">{t[2:].strip()}</p>'
    t=NUMRE.sub(lambda m: f'<strong class="creed-num">{m.group(1)}</strong> ', t)
    return f'<p class="{cls}">{t}</p>'
def card(id,label,title=None,paras=(),chips=(),note='',q=None,raw=None):
    t=f'\n          <h3 class="creed-sec-title">{title}</h3>' if title else ''
    qq=f'\n          <p class="creed-q">{esc(q)}</p>' if q else ''
    body=raw if raw is not None else ''.join('\n          '+para(p) for p in paras)
    n=f'\n        <aside class="creed-note" role="note">{note}</aside>' if note else ''
    return f'''
      <article class="verse-card creed-card creed-card--long" id="{id}">
        <div class="verse-text-block">
          <p class="verse-ref">{label}</p>{t}{qq}{body}
        </div>{chipsrow(chips)}{n}
      </article>'''
def group(id,title,sub=''):
    s=f'<span class="creed-group-sub">{sub}</span>' if sub else ''
    return f'''
      <h3 class="creed-group" id="{id}">{title}{s}</h3>'''
def toc(entries, cols=True):
    li=''.join(f'\n          <li><a href="#{i}">{l}</a></li>' for i,l in entries)
    return f'''
      <nav class="creed-toc{' creed-toc--cols' if cols else ''}" aria-label="Contents" id="contents">
        <p class="creed-toc-title">Contents</p>
        <ol>{li}
        </ol>
      </nav>'''
def build(spec):
    order=[]
    def cite(m):
        k=m.group(1)
        assert k in SRC, k
        if k not in order: order.append(k)
        n=order.index(k)+1
        return f'<sup class="creed-cite"><a href="#src-{n}">{n}</a></sup>'
    bg=''.join(f'\n      <p>{p}</p>' for p in spec['background'])
    meta=''.join((f'\n          <span aria-hidden="true">·</span>' if i else '')+f'\n          <span>{m}</span>' for i,m in enumerate(spec['meta']))
    both=''
    if spec.get('both'):
        b=spec['both']
        both=f'''
      <h2 id="both-traditions">Where both traditions stand</h2>
      <p>{b['intro']}</p>
      <div class="dual-cols creed-dual">
        <div class="dual-col">
          <span class="dual-label label-arminian">Arminian</span>{''.join('<p>'+x+'</p>' for x in b['arminian'])}
        </div>
        <div class="dual-col">
          <span class="dual-label label-reformed">Reformed</span>{''.join('<p>'+x+'</p>' for x in b['reformed'])}
        </div>
      </div>'''
    textblock=''
    if spec.get('items') is not None:
        textblock=f'''
      <h2 id="text">{spec.get('text_heading','The text')}</h2>
      <p class="creed-version">{spec['version']}</p>{spec.get('toc','')}
      <div class="verse-list creed-list">{''.join(spec['items'])}
      </div>'''
    body=f'''  <main class="bible-index article-page creed-page">
    <div class="reader article">
      <p class="browse-crumbs"><a href="/">Home</a> <span aria-hidden="true">›</span> <a href="/creeds/">Creeds &amp; Confessions</a></p>
      <div class="page-intro">
        <p class="eyebrow">{spec['eyebrow']}</p>
        <h1>{spec['h1']}</h1>
        <p>{spec['sub']}</p>
        <div class="passage-meta creed-meta">{meta}
          <span class="pill">{spec['pill']}</span>
        </div>
      </div>

      <h2 id="background">Background</h2>{bg}{spec.get('after_bg','')}{textblock}{spec.get('after_text','')}{both}
      @@SOURCES@@
      <aside class="disclaimer" role="note"><strong>About these notes.</strong>
        Historical notes are educational and cite their sources. Where scholars disagree, we say so. Commentary links open our verse-by-verse pages, where Arminian and Reformed readings sit side by side.</aside>
    </div>
  </main>
'''
    def cites(m):
        keys=re.findall(r'\[\[(\w+)\]\]',m.group(0)); nums=[]
        for k in keys:
            assert k in SRC, k
            if k not in order: order.append(k)
            n=order.index(k)+1
            if n not in nums: nums.append(n)
        return '<sup class="creed-cite">'+','.join(f'<a href="#src-{n}">{n}</a>' for n in nums)+'</sup>'
    body=re.sub(r'\s*(?:\[\[\w+\]\]\s*)*\[\[\w+\]\]',cites,body)
    for k in spec.get('also',[]):
        if k not in order: order.append(k)
    src=''.join(f'\n        <li id="src-{i}">{SRC[k]}</li>' for i,k in enumerate(order,1))
    body=body.replace('@@SOURCES@@',f'''
      <h2 id="sources">Sources</h2>
      <ol class="creed-sources">{src}
      </ol>
''')
    open(OUT+spec['slug']+'.html','w').write(page(spec['title'],spec['desc'],'/creeds/'+spec['slug'],body))
    return order
