import json
from pathlib import Path
import pcbnew as k
R=Path(__file__).resolve().parents[1];b=k.LoadBoard(str(R/'hardware/goober.kicad_pcb'))
def xy(p):return [k.ToMM(p.x),k.ToMM(p.y)]
out={'pads':[], 'tracks':[], 'cuts':[]}
for f in b.GetFootprints():
 for p in f.Pads():
  for layer in [k.F_Cu,k.B_Cu]:
   if not p.IsOnLayer(layer):continue
   poly=p.GetEffectivePolygon(layer)
   for j in range(poly.OutlineCount()):
    line=poly.COutline(j)
    out['pads'].append({'ref':f.GetReference(),'pin':p.GetNumber(),'net':p.GetNetname(),'layer':0 if layer==k.F_Cu else 1,'points':[xy(line.CPoint(i)) for i in range(line.PointCount())]})
for t in b.GetTracks():
 layers=[0,1] if isinstance(t,k.PCB_VIA) else [0 if t.GetLayer()==k.F_Cu else 1]
 out['tracks'].append({'net':t.GetNetname(),'layers':layers,'start':xy(t.GetStart()),'end':xy(t.GetEnd()),'width':k.ToMM(t.GetWidth(k.F_Cu)) if isinstance(t,k.PCB_VIA) else k.ToMM(t.GetWidth())})
out['led_centers']=[xy(f.GetPosition())for f in b.GetFootprints()if f.GetReference().startswith('D')]
(R/'validation/route-geometry.json').write_text(json.dumps(out))
