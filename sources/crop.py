import sys
from PIL import Image
# usage: crop.py img x0 y0 x1 y1 (fractions) out [scale]
im=Image.open('remhi/h-%03d.png'%int(sys.argv[1]));W,H=im.size
f=[float(a) for a in sys.argv[2:6]]
c=im.crop((int(f[0]*W),int(f[1]*H),int(f[2]*W),int(f[3]*H)))
s=float(sys.argv[7]) if len(sys.argv)>7 else 1
if s!=1: c=c.resize((int(c.size[0]*s),int(c.size[1]*s)),Image.LANCZOS)
c.save(sys.argv[6])
