# thumbs.py — makes small card images toys/s/*.webp (440px) from toys/*.webp
# run after adding a toy photo:  python3 dev/thumbs.py
import os,glob
from PIL import Image
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','toys')
os.makedirs(os.path.join(R,'s'),exist_ok=True)
for f in sorted(glob.glob(os.path.join(R,'*.webp'))):
    o=os.path.join(R,'s',os.path.basename(f))
    if os.path.exists(o) and os.path.getmtime(o)>=os.path.getmtime(f):continue
    im=Image.open(f);im.thumbnail((440,440),Image.LANCZOS);im.save(o,'WEBP',quality=78,method=6);print('thumb',os.path.basename(f))
