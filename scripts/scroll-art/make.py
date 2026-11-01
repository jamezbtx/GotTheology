"""Generate original matte scroll assets (rolls, sheet texture, gold-fleck strips). Run: python3 make.py"""
import numpy as np, base64, os, math
from PIL import Image, ImageFilter, ImageDraw
OUT=os.path.join(os.path.dirname(__file__),'..','..','public','assets')
rng=np.random.default_rng(42)
def pn(w,h,sx,sy,seed):
    r=np.random.default_rng(seed); f=np.fft.fft2(r.normal(size=(h,w)))
    fy=np.fft.fftfreq(h)[:,None]; fx=np.fft.fftfreq(w)[None,:]
    f*=np.exp(-((fx/sx)**2+(fy/sy)**2)/2); n=np.real(np.fft.ifft2(f)); return (n-n.mean())/n.std()
def save(a,name,**kw):
    Image.fromarray(np.clip(a,0,255).astype('uint8'),'RGBA').save(os.path.join(OUT,name),'WEBP',quality=88,**kw)

# ---- sheet fibre tile (seamless) ----
T=512
fib=0.7*pn(T,T,0.35,0.04,1)+0.5*pn(T,T,0.04,0.35,2)+0.6*pn(T,T,0.5,0.5,3)+0.25*pn(T,T,0.008,0.008,4)
base=np.array([238,229,209.0])
tile=base[None,None,:]*(1+0.014*fib[...,None])
save(np.dstack([tile,np.full((T,T),255)]),'scroll-sheet.webp')

# ---- gold fleck edge strips (seamless vertically) ----
SW,SH=180,900
def flecks(seed,left=True):
    im=Image.new('RGBA',(SW,SH),(0,0,0,0)); d=ImageDraw.Draw(im); r=np.random.default_rng(seed)
    for i in range(70):
        x=abs(r.normal(0,0.22))*SW; x=x if left else SW-x
        y=r.uniform(0,SH); s=r.uniform(0.4,1.6)*(1.7 if r.random()<.1 else 1)
        k=r.integers(4,8); g=r.uniform(.75,1.15)
        col=(int(212*g),int(176*g),int(92*g),int(r.uniform(80,160)))
        for dy in (-SH,0,SH):
            pts=[(x+s*r.uniform(.4,1.3)*math.cos(t),y+dy+s*r.uniform(.4,1.3)*math.sin(t)) for t in np.linspace(0,2*math.pi,k,endpoint=False)]
            r2=np.random.default_rng(i)  # keep shape identical for wrap copies
            d.polygon(pts,fill=col)
    return im.filter(ImageFilter.GaussianBlur(0.35))
flecks(7,True).save(os.path.join(OUT,'scroll-flecks-l.webp'),'WEBP',quality=90)
flecks(8,False).save(os.path.join(OUT,'scroll-flecks-r.webp'),'WEBP',quality=90)

# ---- rolls (2x): composite cap + N*mid + cap, then slice ----
H=88; CW=124; TW=512; N=3; W=2*CW+N*TW
y=np.linspace(-1,1,H)[:,None]
prof=0.86+0.10*np.exp(-((y+0.3)/0.5)**2)-0.14*np.clip(np.abs(y)-0.5,0,1)/0.5-0.08*np.clip(y,0,1)
ph=(np.arange(W)-CW)%TW
tex=(0.7*pn(TW,H,0.4,0.15,11)+0.6*pn(TW,H,0.02,0.2,12)+0.4*pn(TW,H,0.25,0.6,13))[:,ph]
wob=pn(TW,1,0.02,1,14)[0][ph]*0.6
rollc=np.array([222,201,162.0])
rgb=rollc*(prof*(1+0.035*tex))[...,None]
yy=np.arange(H)[:,None]
top=3+wob[None,:]; bot=H-4+wob[None,:]*0.8
alpha=np.clip(yy-top+1,0,1)*np.clip(bot-yy+1,0,1)
# gold flecks on roll
fl=np.zeros((H,W)); rr=np.random.default_rng(15)
for i in range(60):
    cx=rr.uniform(0,TW); cy=rr.uniform(10,H-10)
    for k in range(N+2):
        px=int(CW+cx+(k-1)*TW)
        if 0<=px<W: fl[int(cy),px]=rr.uniform(.4,1)
fl=np.asarray(Image.fromarray((fl*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(.6))).astype(float)/255
gold=np.array([200,163,80.0]); rgb=rgb*(1-fl[...,None]*.6)+gold*fl[...,None]*.6
# body only between the two end faces
cxl=CW*0.42; cxr=W-cxl; rx=H*0.22
xx=np.arange(W)[None,:]
body=(xx>=cxl)&(xx<=cxr)
alpha=alpha*body
# end faces with spiral
def face(cx,sign):
    global rgb,alpha
    ry=H/2-3.5; ex=(xx-cx)/rx; ey=(yy-H/2)/ry; rad=np.sqrt(ex**2+ey**2)
    inside=rad<=1
    ang=np.arctan2(ey,ex*sign)
    spiral=np.cos(2*math.pi*(rad*4.2 - ang/(2*math.pi)))
    sh=0.80+0.06*(1-rad)-0.04*ey
    col=np.array([205,184,148.0])*(sh*(1-0.10*np.clip(spiral,0,1)**3))[...,None]
    col=col*(1+0.03*tex[...,None])
    rim=np.clip((rad-0.86)/0.14,0,1)
    col=col*(1-0.15*rim[...,None])
    m=inside[...,None]
    rgb=np.where(m,col,rgb); alpha=np.where(inside,1.0,alpha)
face(cxl,1); face(cxr,-1)
img=np.dstack([rgb,alpha*255])
im=Image.fromarray(np.clip(img,0,255).astype('uint8'),'RGBA')
ch=im.split(); im=Image.merge('RGBA',[c.filter(ImageFilter.GaussianBlur(0.5)) for c in ch[:3]]+[ch[3].filter(ImageFilter.GaussianBlur(0.8))])
im.save('/workspace/parchment-fix/v9/roll-composite.png')
im.crop((0,0,CW,H)).save(os.path.join(OUT,'scroll-roll-l.webp'),'WEBP',quality=90)
im.crop((W-CW,0,W,H)).save(os.path.join(OUT,'scroll-roll-r.webp'),'WEBP',quality=90)
mid=im.crop((CW+TW,0,CW+2*TW,H)); mid.save('/tmp/_mid.webp','WEBP',quality=90)
d=base64.b64encode(open('/tmp/_mid.webp','rb').read()).decode()
for h,fn in [(44,'scroll-roll-mid.svg'),(24,'scroll-roll-mid-sm.svg')]:
    w=TW*h/H
    open(os.path.join(OUT,fn),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="{h}"><defs><pattern id="t" width="{w}" height="{h}" patternUnits="userSpaceOnUse"><image href="data:image/webp;base64,{d}" xlink:href="data:image/webp;base64,{d}" width="{w}" height="{h}" preserveAspectRatio="none"/></pattern></defs><rect width="100%" height="{h}" fill="url(#t)"/></svg>')
print('done')
