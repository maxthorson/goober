"""Write a self-contained, labeled KiCad schematic from the pin contract."""
import json, uuid
from pathlib import Path
R=Path(__file__).resolve().parents[1]; H=R/'hardware'
data=json.loads((H/'circuit.json').read_text())
root_id='6cb52c0c-41b0-4b47-a840-17fc680b0b41'
def uid():return str(uuid.uuid4())
def q(s):return json.dumps(str(s),ensure_ascii=False)
def fx(size=1.0,justify=''):return f'(effects (font (size {size} {size})){(" (justify "+justify+")") if justify else ""})'
libs=[]; placed=[]; wires=[]

pos={'U1':(55,70),'J1':(145,55),'ENC1':(145,100),'U2':(410,62),'Q1':(245,55),'Q2':(315,55),
     'F1':(180,30),'C10':(460,48),'C11':(245,90),'R1':(245,115),'R2':(315,90),'R3':(315,115),
     'R4':(410,115),'R5':(100,265),'R6':(165,265),'R7':(100,295),'R8':(165,295),'R9':(100,325)}
for n in range(1,10):
    row,col=divmod(n-1,3)
    pos['SW'+str(n)]=(45+col*65,145+row*35)
    pos['D'+str(n)]=(260+col*95,165+row*60)
    pos['C'+str(n)]=(260+col*95,195+row*60)

for part in data['parts']:
    if not part['pins']:continue
    ref=part['ref'];name=ref;symbol_id='Goober:'+name
    pinlist=list(part['pins'])
    # Pins are ordered down one side, making module header names unambiguous.
    pitch=2.54;height=max(7.62,(len(pinlist)+1)*pitch); w=12.7
    pins=''
    for i,num in enumerate(pinlist):
        py=(len(pinlist)-1)*pitch/2-i*pitch
        ptype=part['pin_types'].get(num,'passive')
        # Q1's drain is the switched supply source in this module-level symbol.
        if ref=='Q1' and num=='3':ptype='power_out'
        if ref=='Q2' and num=='3':ptype='open_collector'
        label=part['pin_names'].get(num,num)
        pins+=f'(pin {ptype} line (at {-w-2.54} {py} 0)(length 2.54)(name {q(label)} {fx(.9)})(number {q(num)} {fx(.9)}))\n'
    libs.append(f'''(symbol {q(symbol_id)} (pin_names (offset 0.8)) (in_bom yes)(on_board yes)
      (property "Reference" {q(ref)} (at 0 {height/2+2} 0) {fx()})
      (property "Value" {q(part['value'])} (at 0 {-height/2-2} 0) {fx(.9)})
      (property "Footprint" {q(part['footprint'])} (at 0 0 0)(effects(font(size 1 1))(hide yes)))
      (symbol {q(name+'_0_1')} (rectangle(start {-w} {height/2})(end {w} {-height/2})(stroke(width 0.254)(type default))(fill(type background))))
      (symbol {q(name+'_1_1')} {pins}))''')
    x,y=pos[ref];x=round(x/1.27)*1.27;y=round(y/1.27)*1.27;pid=part['uuid']
    placed.append(f'''(symbol (lib_id {q(symbol_id)})(at {x} {y} 0)(unit 1)(in_bom yes)(on_board yes)(dnp no)(uuid {pid})
      (property "Reference" {q(ref)} (at {x} {y-height/2-2} 0) {fx()})
      (property "Value" {q(part['value'])} (at {x} {y+height/2+2} 0) {fx(.9)})
      (property "Footprint" {q(part['footprint'])} (at {x} {y} 0)(effects(font(size 1 1))(hide yes)))
      (instances (project "goober" (path "/{root_id}" (reference {q(ref)})(unit 1)))))''')
    for i,num in enumerate(pinlist):
        px=x-w-2.54;py=y-(len(pinlist)-1)*pitch/2+i*pitch
        net=part['pins'][num]
        if net:
            end=px-7.62
            wires.append(f'(wire (pts(xy {px} {py})(xy {end} {py}))(stroke(width 0)(type default))(uuid {uid()}))')
            wires.append(f'(label {q(net)} (at {end} {py} 0) {fx(.95,"left bottom")}(uuid {uid()}))')
        else:wires.append(f'(no_connect (at {px} {py})(uuid {uid()}))')

notes=[('GOOBER / REV A — USB-C MACRO PAD',35,15,2),
       ('Controller / display / encoder',30,30,1.4),('9 direct inputs: switch closes GPIO to ground',30,125,1.4),
       ('Switched RGB supply and 3.3V-to-5V data buffer',225,15,1.4),
       ('Nine SK6812MINI-E-012 LEDs: reading-order daisy chain',230,140,1.4),
       ('Sockets and LEDs mount on the underside; switches enter from the top.',30,355,1.2),
       ('U1: component side faces outward on PCB underside. OLED harness must follow SIGNAL NAMES.',30,362,1.2),
       ('USB hub / charging passthrough deferred. No external power may be applied to 5V_USB.',30,369,1.2),
       ('Prototype: verify physical fit, current, USB behavior and all controls on assembled hardware.',30,376,1.2)]
texts=[f'(text {q(t)}(at {x} {y} 0) {fx(s,"left")}(uuid {uid()}))' for t,x,y,s in notes]
sch=f'''(kicad_sch (version 20250114)(generator "eeschema")(uuid {root_id})(paper "A2")
(title_block (title "Goober Rev A — USB-C macro pad")(rev "A.1")(comment 1 "Module-level symbols show every connected pin; circuit.json is the shared pin contract."))
(lib_symbols {''.join(libs)})
{''.join(placed)}{''.join(wires)}{''.join(texts)}
(sheet_instances(path "/"(page "1")))
)'''
(H/'goober.kicad_sch').write_text(sch)
(H/'Goober.kicad_sym').write_text('(kicad_symbol_lib\n (version 20241209)\n (generator "kicad_symbol_editor")\n'+''.join(libs).replace('(symbol \"Goober:', '(symbol \"')+')')
(H/'sym-lib-table').write_text('(sym_lib_table\n (version 7)\n (lib (name "Goober") (type "KiCad") (uri "${KIPRJMOD}/Goober.kicad_sym") (options "") (descr "Goober module symbols")))')
print('Schematic written:',len(placed),'components')
