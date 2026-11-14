import sys
from playwright.sync_api import sync_playwright
S='/workspace/gt-creeds-mock/screens/'
pages=[('/creeds/','creeds-index','full'),('/creeds/five-articles-of-remonstrance','five-articles-of-remonstrance','full'),('/creeds/canons-of-dort','canons-of-dort','parts')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--headless=new'])
    for w,h,name,mob in [(1280,900,'desktop-1280',False),(390,844,'mobile-390',True)]:
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1 if not mob else 2,is_mobile=mob,has_touch=mob)
        for url,slug,mode in pages:
            pg.goto('http://127.0.0.1:4199'+url,wait_until='networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(700)
            H=pg.evaluate('document.documentElement.scrollHeight'); ov=pg.evaluate('document.documentElement.scrollWidth>window.innerWidth')
            print(name,slug,'height',H,'hscroll',ov)
            if mode=='full': pg.screenshot(path=f'{S}{slug}-{name}.png',full_page=True)
            else:
                # top of page through TOC and first cards
                for part,sel in [('top',None),('table','#remonstrance-and-dort'),('text','#head1'),('both','#both-traditions')]:
                    if sel: y=pg.evaluate(f"document.querySelector('{sel}').getBoundingClientRect().top+window.scrollY-20")
                    else: y=0
                    ch=min(2400 if not mob else 2000, H-y)
                    pg.screenshot(path=f'{S}{slug}-{part}-{name}.png',full_page=True,clip={'x':0,'y':y,'width':w,'height':ch})
    b.close()
