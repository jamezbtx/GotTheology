from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--headless=new'])
    for w,h,name,mob in [(1280,900,'desktop-1280',False),(390,844,'mobile-390',True)]:
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1 if not mob else 2,is_mobile=mob,has_touch=mob)
        for url,slug in [('/creeds/nicene-creed','nicene-creed'),('/creeds/','creeds-index')]:
            pg.goto('http://127.0.0.1:4199'+url,wait_until='networkidle')
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(800)
            fonts=pg.evaluate("[...document.fonts].filter(f=>f.status=='loaded').map(f=>f.family+' '+f.weight)")
            print(name,slug,sorted(set(fonts)))
            pg.screenshot(path=f'/workspace/gt-creeds-mock/screens/{slug}-{name}.png',full_page=True)
    b.close()
