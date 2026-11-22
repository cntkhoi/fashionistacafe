import os, glob, json, base64, io, re
from PIL import Image, ImageFilter, ImageChops, ImageEnhance
SRC='/tmp/fc3d/out/'; DST='/home/user/fashionistacafe/website-demo/img/'; os.makedirs(DST,exist_ok=True)
def bloom(im):
    im=im.convert('RGB'); w,h=im.size
    hi=im.point(lambda v: max(0,(v-175))*3.2)
    hi=hi.resize((w//4,h//4)).filter(ImageFilter.GaussianBlur(max(4,w/160))).resize((w,h),Image.BICUBIC)
    hi=ImageEnhance.Brightness(hi).enhance(.5)
    return ImageChops.screen(im,hi)
def save(im,name,q): im.save(DST+name,'WEBP',quality=q,method=6)
tot=0
for p in sorted(glob.glob(SRC+'*.png')):
    n=os.path.basename(p)[:-4]; out=DST+n+'.webp'
    if os.path.exists(out) and os.path.getmtime(out)>os.path.getmtime(p): continue
    im=bloom(Image.open(p)); w,h=im.size
    if n.startswith('f') or n.startswith('hero'):
        hq=n.startswith('hero')
        save(im,n+'.webp',80 if hq else 66)
        m=im.crop((int(w*280/1280),0,int(w*1000/1280),h))
        if hq: m=m.resize((900,1200),Image.LANCZOS)
        save(m,'m_'+n+'.webp',78 if hq else 64)
    else: save(im,n+'.webp',80)
# journal crops from film frames
for name,src,box in (('j1','f008',(.30,.05,.80,.888)),('j2','f030',(.18,.12,.62,.853)),('j3','f042',(.30,.10,.86,1.0))):
    p=SRC+src+'.png'
    if os.path.exists(p):
        im=bloom(Image.open(p)); w,h=im.size; bw=(box[2]-box[0])*w; bh=min(h*(box[3]-box[1]),bw*1.25); bw=bh/1.25
        c=im.crop((int(box[0]*w),int(box[1]*h),int(box[0]*w+bw),int(box[1]*h+bh))).resize((900,1125),Image.LANCZOS); save(c,name+'.webp',78)
# page: inject cfg + LQIP
H='/home/user/fashionistacafe/website-demo/homepage-demo.html'; s=open(H).read()
cfg=open('/tmp/fc3d/cfg.json').read().strip()
s=re.sub(r'/\*CFG\*/\{.*?\};','/*CFG*/'+cfg+';',s,count=1,flags=re.S)
if os.path.exists(SRC+'hero_on.png'):
    b=io.BytesIO(); Image.open(SRC+'hero_on.png').convert('RGB').resize((40,30)).filter(ImageFilter.GaussianBlur(1)).save(b,'WEBP',quality=40)
    uri='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    s=re.sub(r'background-image:url\([^)]*\)','background-image:url(%s)'%uri,s,count=1)
open(H,'w').write(s)
fs=glob.glob(DST+'*.webp'); print(len(fs),'files',round(sum(os.path.getsize(f) for f in fs)/1e6,2),'MB; desktop frames',round(sum(os.path.getsize(f) for f in fs if os.path.basename(f).startswith('f'))/1e6,2),'mobile',round(sum(os.path.getsize(f) for f in fs if os.path.basename(f).startswith('m_f'))/1e6,2))
