"""Check nominal component bounding shapes against printed solids."""
import trimesh,json,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];base=trimesh.load_mesh(R/'case/goober-base.stl');lid=trimesh.load_mesh(R/'case/goober-lid.stl');lid.apply_translation([0,0,13])
def box(a,z):
 m=trimesh.creation.box([b-c for b,c in zip(z,a)]);m.apply_translation([(b+c)/2 for b,c in zip(z,a)]);return m
verts=[[40,-48]]
for cx,cy,start in [(77,-3,0),(3,-3,90),(3,-93,180),(77,-93,270)]:
 for angle in np.linspace(start,start+90,33):
  a=np.radians(angle);verts.append([cx+3*np.cos(a),cy+3*np.sin(a)])
n=len(verts);faces=[[0,i,1 if i==n-1 else i+1]for i in range(1,n)];pcb=trimesh.creation.extrude_triangulation(np.array(verts),np.array(faces),1.6);pcb.apply_translation([0,0,11.4])
parts={'PCB (rounded outline)':pcb,'RP2040 board':box([19,-23.5,7.4],[37,0,8.4]),'USB connector':box([23.6,-6.3,4.2],[32.4,1.2,7.4]),'OLED PCB':box([9,-24.25,19.1],[45,-11.75,20.3]),'encoder body':box([55.8,-26.6,13],[68.2,-13.4,17.5])}
result={}
for n,m in parts.items():
 result[n]={}
 for cn,c in [('base',base),('lid',lid)]:
  inter=trimesh.boolean.intersection([m,c],engine='manifold');v=float(inter.volume) if len(inter.faces) else 0;result[n][cn]=v;assert v<1e-4,(n,cn,v)
result['note']='No positive-volume intersections for nominal bounding proxies. Excludes solder, wiring, switch clips and detailed component tolerances; physical fit test still required.'
(R/'validation/mechanical-clearances.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
