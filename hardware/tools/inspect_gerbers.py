from pathlib import Path
import json,math,warnings,xml.etree.ElementTree as ET
import pymupdf
from gerbonara import LayerStack
R=Path(__file__).resolve().parents[1]
with warnings.catch_warnings(record=True) as caught:
 warnings.simplefilter('always');s=LayerStack.open(R/'hardware/gerbers')
 result={'reader':'Gerbonara 1.6.3','layers':{str(key):len(v.objects) for key,v in s.graphic_layers.items()},'bounds_mm':s.bounding_box(),'plated_drill_objects':len(s.drill_pth.objects),'nonplated_drill_objects':len(s.drill_npth.objects)}
 assert len(s.graphic_layers)==7 and len(s.drill_pth.objects)==90 and len(s.drill_npth.objects)==31
 outline=s.graphic_layers[('mechanical','outline')];adj={}
 def point(x,y):return(round(x,4),round(y,4))
 for o in outline.objects:
  a=point(o.x1,o.y1);b=point(o.x2,o.y2);adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
 assert all(len(v)==2 for v in adj.values())
 remaining=set(adj);loops=0
 while remaining:
  loops+=1;stack=[remaining.pop()]
  while stack:
   for p in adj[stack.pop()]:
    if p in remaining:remaining.remove(p);stack.append(p)
 assert loops==10;result['closed_outline_contours']=loops
 for side in ['top','bottom']:
  colors={f'{side} copper':'#bd482e' if side=='top' else '#2467a3','mechanical outline':'#333333','drill pth':'white','drill npth':'#333333'}
  svg=str(s.to_svg(side_re=side+'|mechanical',margin=2,colors=colors))
  if side=='bottom':
   root=ET.fromstring(svg);g=ET.Element('{http://www.w3.org/2000/svg}g',{'transform':'translate(80 0) scale(-1 1)'})
   for c in list(root):root.remove(c);g.append(c)
   root.append(g);svg=ET.tostring(root,encoding='unicode')
  p=R/f'mockups/gerber-{side}.svg';p.write_text(svg);d=pymupdf.open('svg',svg.encode());pdf=pymupdf.open('pdf',d.convert_to_pdf());pdf[0].get_pixmap(matrix=pymupdf.Matrix(4,4)).save(str(p.with_suffix('.png')))
 result['reader_warnings']=sorted(set(str(w.message) for w in caught))
(R/'validation/gerber-parse.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
p=R/'validation/schematic/goober.svg';d=pymupdf.open('svg',p.read_bytes());pdf=pymupdf.open('pdf',d.convert_to_pdf());pdf.save(str(R/'hardware/schematic.pdf'));pdf[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(str(p.with_suffix('.png')))
