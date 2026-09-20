"""Apply saved final connection to a board imported from goober.ses.
Re-running is idempotent: matching previously applied geometry is removed.
"""
import json
from pathlib import Path
import pcbnew as k
R=Path(__file__).resolve().parents[1]; p=R/'hardware/goober.kicad_pcb'
b=k.LoadBoard(str(p)); route=json.loads((R/'validation/manual-route.json').read_text());points=route['points']
old=route.get('previous_points',points)
def xy(t):return (round(k.ToMM(t.x),4),round(k.ToMM(t.y),4))
segments={frozenset([tuple(a[1:]),tuple(c[1:])])for a,c in zip(old,old[1:])}
segments|={frozenset([tuple(a[1:]),tuple(c[1:])])for a,c in zip(points,points[1:])}
for t in list(b.GetTracks()):
 if t.GetNetname()=='KEY7' and frozenset([xy(t.GetStart()),xy(t.GetEnd())]) in segments:b.Remove(t)
net=b.FindNet('KEY7');mm=k.FromMM
for a,c in zip(points,points[1:]):
 if a[0]==c[0]:
  t=k.PCB_TRACK(b); t.SetStart(k.VECTOR2I(mm(a[1]),mm(a[2])));t.SetEnd(k.VECTOR2I(mm(c[1]),mm(c[2])));t.SetWidth(mm(.2));t.SetLayer(k.F_Cu if a[0]==0 else k.B_Cu)
 else:
  t=k.PCB_VIA(b); t.SetPosition(k.VECTOR2I(mm(a[1]),mm(a[2])));t.SetWidth(mm(.6));t.SetDrill(mm(.3));t.SetLayerPair(k.F_Cu,k.B_Cu);t.SetViaType(k.VIATYPE_THROUGH)
 t.SetNet(net);b.Add(t)
k.SaveBoard(str(p),b)
