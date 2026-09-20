"""Compare exported schematic connectivity, PCB pads and firmware pin map."""
import json,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as k
R=Path(__file__).resolve().parents[1]; parts=json.loads((R/'hardware/circuit.json').read_text())['parts']; b=k.LoadBoard(str(R/'hardware/goober.kicad_pcb'))
expected={(p['ref'],pin):net for p in parts for pin,net in p['pins'].items() if net}
schematic={}
for net in ET.parse(R/'validation/schematic-netlist.xml').getroot().find('nets'):
 name=net.get('name').lstrip('/')
 if name.startswith('unconnected-'):continue
 for n in net.findall('node'):schematic[(n.get('ref'),n.get('pin'))]=name
pcb={}
for f in b.GetFootprints():
 for p in f.Pads():
  if p.GetNetname() and not p.GetNetname().startswith('unconnected-'):pcb[(f.GetReference(),p.GetNumber())]=p.GetNetname().lstrip('/')
assert expected==schematic,('Schematic mismatch',expected.items()^schematic.items())
assert expected==pcb,('PCB mismatch',expected.items()^pcb.items())
f=json.loads((R/'firmware/goober/rev_a/keyboard.json').read_text()); rp=next(p for p in parts if p['ref']=='U1')
for i,pin in enumerate(sum(f['matrix_pins']['direct'][:3],[])):
 assert rp['pin_names'][str(i+1)]==pin and rp['pins'][str(i+1)]=='KEY'+str(i+1)
assert f['matrix_pins']['direct'][3][0]==rp['pin_names']['13']=='GP12'
assert f['encoder']['rotary'][0]['pin_a']==rp['pin_names']['11']=='GP10'
assert f['encoder']['rotary'][0]['pin_b']==rp['pin_names']['12']=='GP11'
assert f['ws2812']['pin']==rp['pin_names']['14']=='GP13'
config=(R/'firmware/goober/rev_a/config.h').read_text()
for line in ['#define I2C1_SDA_PIN GP14','#define I2C1_SCL_PIN GP15','#define GOOBER_LED_POWER GP9']:assert line in config
result={'status':'pass','connected_unique_pads':len(expected),'nets':len(set(expected.values())),'checks':['Schematic vs circuit contract','PCB vs circuit contract','Keys, encoder, LED, OLED firmware GPIO mapping'],'note':'Connectivity parity does not validate component behavior or physical prototype operation.'}
(R/'validation/connectivity.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
