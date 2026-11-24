"""Crop the flyer screenshot and punch a transparent rounded-top hole where the photo goes."""
import json, sys
from PIL import Image, ImageDraw

src = sys.argv[1] if len(sys.argv) > 1 else "scripts/flyer-source.png"
im = Image.open(src).convert("RGBA")
CROP = (4, 4, 727, 807)          # strip grey screenshot border
HOLE = (125, 260, 607, 748)      # white box in source coords (x0,y0,x1,y1)
RADIUS = 22                      # top corner radius
im = im.crop(CROP)
hx0, hy0, hx1, hy1 = HOLE[0]-CROP[0], HOLE[1]-CROP[1], HOLE[2]-CROP[0], HOLE[3]-CROP[1]

S = 4  # supersample for smooth corners
m = Image.new("L", (im.width*S, im.height*S), 255)
d = ImageDraw.Draw(m)
d.rounded_rectangle((hx0*S, hy0*S, hx1*S, hy1*S + RADIUS*S*2), RADIUS*S, fill=0)
d.rectangle((hx0*S, hy1*S, hx1*S, im.height*S), fill=255)  # keep banner opaque
m = m.resize(im.size, Image.LANCZOS)
im.putalpha(m)
im.save("assets/template.png", optimize=True)
json.dump({"width": im.width, "height": im.height,
           "hole": {"x": hx0, "y": hy0, "w": hx1-hx0, "h": hy1-hy0, "r": RADIUS}},
          open("assets/template.json", "w"), indent=2)
print(im.size, hx0, hy0, hx1-hx0, hy1-hy0)
