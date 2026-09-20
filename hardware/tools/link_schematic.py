import json
from pathlib import Path
import pcbnew as k
R=Path(__file__).resolve().parents[1];p=R/'hardware/goober.kicad_pcb';b=k.LoadBoard(str(p));parts={a['ref']:a for a in json.loads((R/'hardware/circuit.json').read_text())['parts']}
for f in b.GetFootprints():
 a=parts[f.GetReference()]
 if a['pins']:f.SetPath(k.KIID_PATH('/6cb52c0c-41b0-4b47-a840-17fc680b0b41/'+a['uuid']))
k.SaveBoard(str(p),b)
