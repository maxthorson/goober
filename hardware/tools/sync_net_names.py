"""Match KiCad sheet-qualified and no-connect names after routing."""
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as k
R=Path(__file__).resolve().parents[1];p=R/'hardware/goober.kicad_pcb';b=k.LoadBoard(str(p));mapping={}
for n in ET.parse(R/'validation/schematic-netlist.xml').getroot().find('nets'):
 for node in n.findall('node'):mapping[(node.get('ref'),node.get('pin'))]=n.get('name')
for net in list(b.GetNetsByNetcode().values()):
 name=net.GetNetname()
 if name and not name.startswith(('/','unconnected-')):net.SetNetname('/'+name)
for f in b.GetFootprints():
 if f.GetReference().startswith('H'):
  f.SetAttributes(f.GetAttributes()|k.FP_BOARD_ONLY|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES)
 for pad in f.Pads():
  name=mapping.get((f.GetReference(),pad.GetNumber()))
  if name and not pad.GetNetname():
   n=b.FindNet(name)
   if not n:n=k.NETINFO_ITEM(b,name);b.Add(n)
   pad.SetNet(n)
k.SaveBoard(str(p),b)
