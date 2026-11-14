import re, html, os
D=os.path.dirname(__file__)
head=open(D+'/head.html').read(); foot=open(D+'/foot.html').read()
OUT='/workspace/gt-creeds-mock/public/creeds/'
def page(title, desc, path, body, footer_label='Creeds &amp; Confessions'):
    h=head.replace('<title>Articles — GotTheology</title>', f'<title>{title} — GotTheology</title>')
    h=re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1)+desc, h)
    h=re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1)+desc, h)
    h=h.replace('content="Articles — GotTheology"', f'content="{title} — GotTheology"')
    h=h.replace('https://got-theology.com/articles/', 'https://got-theology.com'+path)
    h=h.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0" />','<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  <meta name="robots" content="noindex,nofollow" />')
    h=h.replace('<link rel="stylesheet" href="/assets/gottheology.css" />','<link rel="stylesheet" href="/assets/gottheology.css" />\n  <link rel="stylesheet" href="/assets/creeds.css" />')
    h=h.replace('        <a href="/articles/">Articles</a>\n','        <a href="/articles/">Articles</a>\n        <a href="/creeds/">Creeds</a>\n',1)
    f=foot.replace('          <a href="/articles/">Articles</a>\n','          <a href="/articles/">Articles</a>\n          <a href="/creeds/">Creeds</a>\n',1)
    f=f.replace('<span>Articles</span>', f'<span>{footer_label}</span>')
    assert 'noindex' in h and 'adsbygoogle' not in h+body+f and 'made_with_ai' not in h+body+f
    return h+body+f
def esc(s): return html.escape(s, quote=False)
def chipsrow(chips):
    if not chips: return ''
    c=''.join(f'\n            <a class="topic-chip creed-ref" href="{h}">{l}</a>' for h,l in chips)
    return f'''
        <div class="creed-refs">
          <span class="topic-chips-label">Scripture</span>
          <div class="topic-chips-row">{c}
          </div>
        </div>'''
