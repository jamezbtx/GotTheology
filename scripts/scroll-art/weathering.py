"""Original procedural weathering overlay for the scroll sheet (stains, foxing, worn edges, creases).
Single non-repeating image stretched to the sheet size (100% 100%), so no tiling or seams."""
import numpy as np
from PIL import Image, ImageFilter
rng=np.random.default_rng(11)
W,H=900,2400
def blob(scale):
    a=rng.random((H//scale+2,W//scale+2)).astype('f4')
    im=Image.fromarray((a*255).astype('u1')).resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale/2))
    return np.asarray(im,'f4')/255
n=0.55*blob(160)+0.3*blob(60)+0.15*blob(20)
n=(n-n.min())/(n.max()-n.min())
stain=np.clip((n-0.55)/0.45,0,1)**1.6*0.20           # broad discoloration
# tide-line rings on a few stains
for _ in range(7):
    cx,cy,r=rng.uniform(80,W-80),rng.uniform(100,H-100),rng.uniform(40,120)
    y,x=np.ogrid[:H,:W]; d=np.sqrt((x-cx)**2+((y-cy)*1.1)**2)
    stain+=0.025*np.exp(-((d-r)/10)**2)+0.03*(d<r)*np.exp(-(d/r)**2)
# foxing specks
fox=np.zeros((H,W),'f4')
for _ in range(260):
    x,y=rng.integers(0,W),rng.integers(0,H)
    edge=min(x,W-x)/W
    if rng.random()<0.35+0.6*(edge<0.12): fox[y,x]=rng.uniform(0.5,1)
fox=np.asarray(Image.fromarray((fox*255).astype('u1')).filter(ImageFilter.GaussianBlur(2.2)),'f4')/255*6
# worn edges
x=np.linspace(0,1,W)[None,:]; y=np.linspace(0,1,H)[None].T
ex=np.minimum(x,1-x); edge=np.clip(1-ex/0.07,0,1)**2*(0.6+0.4*blob(40))*0.30
a=np.clip(stain+np.clip(fox,0,0.35)+edge,0,0.45)
rgb=np.zeros((H,W,3),'f4'); rgb[...]=(120,82,38)
# creases: faint dark line + light highlight, wobbly, across page
lite=np.zeros((H,W),'f4')
for cy in rng.uniform(0.12,0.9,4)*H:
    yy=cy+12*np.sin(np.linspace(0,rng.uniform(2,5),W)+rng.uniform(0,6))
    Y=np.arange(H)[:,None]; d=Y-yy[None,:]
    fade=np.clip(np.sin(np.linspace(0,np.pi,W))*1.4,0,1)[None]
    a+=0.08*np.exp(-(d/1.6)**2)*fade; lite+=0.5*np.exp(-((d-4)/3)**2)*fade
a=np.clip(a,0,0.5)
rgb=rgb*(1-lite[...,None])+255*lite[...,None]*0.96
a=np.maximum(a,lite*0.10)
out=np.dstack([rgb,a*255]).astype('u1')
Image.fromarray(out,'RGBA').save('public/assets/scroll-weathering.webp',quality=82)
