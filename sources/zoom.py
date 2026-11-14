import sys
from PIL import Image
img,side,half=sys.argv[1:4]; d=[float(a) for a in sys.argv[4:8]]; out=sys.argv[8]
im=Image.open('remhi/h-%03d.png'%int(img));W,H=im.size
x0,x1=((0.0,0.53) if side=='L' else (0.45,1.0)); y0=(0.18 if half=='T' else 0.48)
s=(x1-x0)*W/1024
c=im.crop((int(x0*W+d[0]*s),int(y0*H+d[1]*s),int(x0*W+d[2]*s),int(y0*H+d[3]*s)))
c=c.resize((c.size[0]*2,c.size[1]*2),Image.LANCZOS); c.save(out)
