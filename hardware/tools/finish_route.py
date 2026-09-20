"""Find a conservative two-layer route for the remaining KEY7 connection."""
import json, heapq, math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt
R=Path(__file__).resolve().parents[1];g=json.loads((R/'validation/route-geometry.json').read_text())
step=.1; W,H=801,961
ims=[Image.new('1',(W,H))for _ in range(2)];ds=[ImageDraw.Draw(i)for i in ims]
targetims=[Image.new('1',(W,H))for _ in range(2)];ts=[ImageDraw.Draw(i)for i in targetims]
def pt(v):return tuple(round(a/step) for a in v)
for p in g['pads']:
 poly=[pt(v)for v in p['points']]
 if p['net']=='KEY7':
  if p['ref']!='U1':ts[p['layer']].polygon(poly,fill=1)
 else:ds[p['layer']].polygon(poly,fill=1)
for t in g['tracks']:
 for layer in t['layers']:
  draw=ts[layer] if t['net']=='KEY7' else ds[layer]
  draw.line([pt(t['start']),pt(t['end'])],fill=1,width=max(1,math.ceil(t['width']/step)))
for d in ds:
 d.rectangle((0,0,W-1,H-1),outline=1,width=4)
 for x,y in g['led_centers']:
  # Conservatively bound the complete milled opening, including corner reliefs.
  d.rectangle((*pt((x-1.7,y-1.5)),*pt((x+1.7,y+1.5))),fill=1)
dist=np.stack([distance_transform_edt(~np.asarray(im,dtype=bool))*step for im in ims])
clear=dist>.34;viaclear=(dist[0]>.56)&(dist[1]>.56)
targets=np.stack([np.asarray(im,dtype=bool) for im in targetims]);targets&=clear
heur=distance_transform_edt(~np.any(targets,axis=0))
sx,sy=pt((20.38,16.83))
startnodes=[(0,sy,sx),(1,sy,sx)]
cost={s:0 for s in startnodes};prev={};heap=[]
for s in startnodes:heapq.heappush(heap,(heur[sy,sx],0,s))
moves=[(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),(-1,1,math.sqrt(2)),(-1,-1,math.sqrt(2))]
end=None;count=0
while heap:
 _,c,n=heapq.heappop(heap)
 if c>cost[n]+1e-8:continue
 count+=1
 l,y,x=n
 if targets[l,y,x]:end=n;break
 nxt=[]
 for dx,dy,v in moves:
  xx,yy=x+dx,y+dy
  if 0<=xx<W and 0<=yy<H and clear[l,yy,xx]:
   if dx and dy and (not clear[l,y,xx] or not clear[l,yy,x]):continue
   nxt.append(((l,yy,xx),v))
 if viaclear[y,x]:nxt.append(((1-l,y,x),35))
 for a,v in nxt:
  nc=c+v
  if nc<cost.get(a,float('inf')):
   cost[a]=nc;prev[a]=n;heapq.heappush(heap,(nc+heur[a[1],a[2]],nc,a))
if end is None:raise RuntimeError('No route found')
path=[end]
while path[-1] in prev:path.append(prev[path[-1]])
path.reverse()
# Preserve each bend and every layer transition.
keep=[path[0]];last=None
for a,b in zip(path,path[1:]):
 direction=tuple(bb-aa for aa,bb in zip(a,b))
 if last is not None and direction!=last:keep.append(a)
 last=direction
keep.append(path[-1])
points=[[l,round(x*step,4),round(y*step,4)]for l,y,x in keep]
(R/'validation/manual-route.json').write_text(json.dumps({'net':'KEY7','points':points,'expanded':count},indent=2))
print('Route found:',len(points),'vertices;',count,'search nodes')
