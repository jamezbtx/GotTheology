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

# Rolls: see slice_rolls.py (generated image, v10).
print('done')
