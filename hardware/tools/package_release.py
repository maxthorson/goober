"""Package checked deliverables, excluding installed tools and work-in-progress files."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,re
R=Path(__file__).resolve().parents[1]
# Fabricator ZIP has files at its root.
fab=R/'hardware/Goober-Rev-A-Gerbers.zip'
with ZipFile(fab,'w',ZIP_DEFLATED)as z:
 for p in sorted((R/'hardware/gerbers').iterdir()):z.write(p,p.name)
assert ZipFile(fab).testzip() is None
selected=[]
for name in ['README.md','NOTICE.md']:
 selected.append(R/name)
for folder in ['docs','case','firmware','licenses']:
 selected.extend(p for p in (R/folder).rglob('*') if p.is_file())
for name in ['goober.kicad_pro','goober.kicad_pcb','goober.kicad_sch','Goober.kicad_sym','fp-lib-table','sym-lib-table','circuit.json','BOM.csv','schematic.pdf','Goober-Rev-A-Gerbers.zip','rp2040-zero-reference.pdf','rp2040-dimensions.jpg','sk6812mini-e.pdf','encoder-dimensions.gif','oled-photo.jpg']:
 selected.append(R/'hardware'/name)
selected.extend((R/'hardware/Goober.pretty').glob('*.kicad_mod'))
selected.extend(p for p in (R/'hardware/gerbers').iterdir() if p.is_file())
for name in ['goober-appearance.png','goober-cad.png','goober-exploded.png','pcb-top.svg','pcb-bottom.svg','gerber-top.svg','gerber-bottom.svg','gerber-top.png','gerber-bottom.png']:
 selected.append(R/'mockups'/name)
for name in ['pcb-final.json','schematic-erc.json','connectivity.json','firmware.json','gerber-parse.json','case-meshes.json','mechanical-clearances.json','firmware-build.log','release.json','schematic-netlist.xml']:
 selected.append(R/'validation'/name)
# Enforce clean digital checks before release.
drc=json.loads((R/'validation/pcb-final.json').read_text());assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
erc=json.loads((R/'validation/schematic-erc.json').read_text());assert all(not sh['violations'] for sh in erc['sheets'])
assert all(p.exists() for p in selected)
# Validate local Markdown links in the packaged documents.
relpaths={p.relative_to(R).as_posix() for p in selected}
for p in selected:
 if p.suffix!='.md':continue
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('http:','https:','#','mailto:')):continue
  dest=(p.parent/target.split('#')[0]).resolve()
  assert dest.exists(),(p,target)
checksums=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(R).as_posix()}\n' for p in sorted(selected))
(R/'CHECKSUMS.sha256').write_text(checksums);selected.append(R/'CHECKSUMS.sha256')
release=R/'releases/Goober-Rev-A-Prototype-Package.zip'
with ZipFile(release,'w',ZIP_DEFLATED,compresslevel=9)as z:
 for p in sorted(selected):z.write(p,'Goober-Rev-A/'+p.relative_to(R).as_posix())
with ZipFile(release)as z:assert z.testzip() is None
print(json.dumps({'release':str(release),'files':len(selected),'bytes':release.stat().st_size,'sha256':hashlib.sha256(release.read_bytes()).hexdigest(),'gerber_zip_bytes':fab.stat().st_size},indent=2))
