from playwright.sync_api import sync_playwright
S='/workspace/gt-creeds-mock/screens/'
pages=[('/creeds/remonstrant-confession','remonstrant-confession',[('version','#text'),('ch1','#chapter1'),('sources','#sources')]),
 ('/creeds/canons-of-dort','canons-of-dort',[('version','#text'),('head1-rejection','#head1-rejection'),('head5-rejection','#head5-rejection'),('sources','#sources')]),
 ('/creeds/heidelberg-catechism','heidelberg-catechism',[('top',None),('version','#text'),('lordsdays','#lords-day-16')]),
 ('/creeds/nicene-creed','nicene-creed',[('both','.creed-dual')])]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--headless=new'])
    for w,h,name,mob in [(1280,900,'desktop-1280',False),(390,844,'mobile-390',True)]:
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1 if not mob else 2,is_mobile=mob,has_touch=mob)
        for url,slug,parts in pages:
            pg.goto('http://127.0.0.1:4199'+url,wait_until='networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(600)
            H=pg.evaluate('document.documentElement.scrollHeight'); ov=pg.evaluate('document.documentElement.scrollWidth>window.innerWidth')
            print(name,slug,'height',H,'hscroll',ov)
            for part,sel in parts:
                y=0
                if sel:
                    e=pg.evaluate(f"(()=>{{const e=document.querySelector('{sel}');return e?e.getBoundingClientRect().top+window.scrollY-20:null}})()")
                    if e is None: print('MISSING',sel); continue
                    y=e
                ch=min(1800 if not mob else 1500, H-y)
                pg.screenshot(path=f'{S}{slug}-{part}-{name}.png',full_page=True,clip={'x':0,'y':y,'width':w,'height':ch})
    b.close()
