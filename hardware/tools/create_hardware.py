"""Create editable Goober carrier board, circuit contract and schematic.
Run using the Python bundled with KiCad (pcbnew API).
"""
import json, math, shutil, uuid
from pathlib import Path
import pcbnew as k

ROOT=Path(__file__).resolve().parents[1]
HW=ROOT/'hardware'
LIB=Path.home()/'Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints'
LOCAL=HW/'Goober.pretty'; LOCAL.mkdir(exist_ok=True)
MAR=ROOT/'tools/marbastlib/footprints/marbastlib-mx.pretty'
mm=k.FromMM
def pt(x,y): return k.VECTOR2I(mm(x),mm(y))
def uid(): return str(uuid.uuid4())
board=k.BOARD(); board.SetCopperLayerCount(2)
board.GetDesignSettings().SetCopperLayerCount(2)
board.GetDesignSettings().m_TrackMinWidth=mm(.2)
board.GetDesignSettings().m_MinClearance=mm(.2)
board.GetDesignSettings().m_HoleClearance=mm(.25)
board.GetDesignSettings().m_CopperEdgeClearance=mm(.25)
board.GetDesignSettings().m_ViasMinSize=mm(.6)
board.GetDesignSettings().m_MinThroughDrill=mm(.3)
board.GetDesignSettings().SetBoardThickness(mm(1.6))
netnames={}
def net(name):
    if name not in netnames:
        n=k.NETINFO_ITEM(board,name); board.Add(n); netnames[name]=n
    return netnames[name]
parts=[]
def shape(start,end,layer,width=.15):
    s=k.PCB_SHAPE(); s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(pt(*start));s.SetEnd(pt(*end));s.SetLayer(layer);s.SetWidth(mm(width)); board.Add(s)
def rectfp(fp,x1,y1,x2,y2,layer):
    s=k.PCB_SHAPE();s.SetShape(k.SHAPE_T_RECT);s.SetStart(pt(x1,y1));s.SetEnd(pt(x2,y2));s.SetLayer(layer);s.SetWidth(mm(.12));fp.Add(s)
def label(txt,x,y,size=1,layer=k.F_SilkS):
    t=k.PCB_TEXT(board);t.SetText(txt);t.SetPosition(pt(x,y));t.SetTextSize(pt(size,size));t.SetTextThickness(mm(.14));t.SetLayer(layer)
    if layer==k.B_SilkS:t.SetMirrored(True)
    board.Add(t)

# Module through-hole geometry comes from the Waveshare dimension drawing,
# not the elongated castellated pads in third-party footprints.
fp=k.FOOTPRINT(None); fp.SetReference('REF**'); fp.SetValue('RP2040-Zero')
rp_positions={}
for i in range(9):rp_positions[str(i+1)]=(7.62,-10.16+2.54*i)
for i in range(5):rp_positions[str(10+i)]=(5.08-2.54*i,10.16)
for i in range(9):rp_positions[str(15+i)]=(-7.62,10.16-2.54*i)
for number,(x,y) in rp_positions.items():
    pad=k.PAD(fp);pad.SetNumber(number);pad.SetAttribute(k.PAD_ATTRIB_PTH);pad.SetShape(k.PAD_SHAPE_CIRCLE);pad.SetSize(pt(1.8,1.8));pad.SetDrillSize(pt(1,1));pad.SetPosition(pt(x,y));pad.SetLayerSet(k.PAD.PTHMask());fp.Add(pad)
rectfp(fp,-9,-11.75,9,11.75,k.F_Fab)
rectfp(fp,-9.5,-12.25,9.5,12.25,k.F_CrtYd)
rectfp(fp,-4.5,-13,4.5,-5.5,k.F_Fab)
shutil.copy2(MAR/'SW_MX_HS_CPG151101S11_1u.kicad_mod',LOCAL/'SW_MX_HS_CPG151101S11_1u.kicad_mod')
fp.SetFPID(k.LIB_ID('Goober','RP2040_Zero_Headers'))
k.FootprintSave(str(LOCAL),fp)
shutil.copy2(MAR/'SW_MX_HS_CPG151101S11_1u.kicad_mod',LOCAL/'SW_MX_HS_CPG151101S11_1u.kicad_mod')

def add(ref,value,lib,name,x,y,pins,flip=False,angle=0,pin_names=None,pin_types=None):
    source=LOCAL if lib=='Goober' else LIB/(lib+'.pretty')
    f=k.FootprintLoad(str(source),name)
    if not f:raise RuntimeError((lib,name))
    f.SetReference(ref);f.SetValue(value);f.SetFPID(k.LIB_ID('Goober',name))
    # Embed every used footprint in the project for portable editing.
    if lib!='Goober' and not (LOCAL/(name+'.kicad_mod')).exists():
        shutil.copy2(source/(name+'.kicad_mod'), LOCAL/(name+'.kicad_mod'))
    f.SetPosition(pt(x,y));f.SetOrientationDegrees(angle)
    board.Add(f)
    if flip:f.Flip(pt(x,y),k.FLIP_DIRECTION_LEFT_RIGHT)
    for pad in f.Pads():
        if value == 'SK6812MINI-E':
            sz=pad.GetSize();sz.x=mm(1.30);pad.SetSize(sz)
        n=pins.get(pad.GetNumber())
        if n:pad.SetNet(net(n))
    f.Value().SetVisible(False)
    if ref.startswith('H'):f.Reference().SetVisible(False)
    if ref.startswith('D'):f.Reference().SetPosition(pt(x,y+3))
    f.Reference().SetTextSize(pt(.8,.8));f.Reference().SetTextThickness(mm(.12))
    parts.append(dict(ref=ref,value=value,footprint='Goober:'+name,x=x,y=y,
                      side='B' if flip else 'F',pins=pins,
                      pin_names=pin_names or {},pin_types=pin_types or {},uuid=str(f.m_Uuid.AsString())))
    return f

rp_pins={str(i+1):'KEY'+str(i+1) for i in range(9)}
rp_pins.update({'10':'LED_EN','11':'ENC_A','12':'ENC_B','13':'ENC_SW','14':'RGB_DATA',
               '15':'OLED_SDA','16':'OLED_SCL','17':None,'18':None,'19':None,'20':None,
               '21':'+3V3','22':'GND','23':'+5V_USB'})
rp_names={str(i+1):'GP'+str(i) for i in range(16)}
rp_names.update({'17':'GP26','18':'GP27','19':'GP28','20':'GP29','21':'3V3_OUT','22':'GND','23':'5V_USB'})
rp_types={str(i):'bidirectional' for i in range(1,21)}
rp_types.update({'21':'power_out','22':'power_out','23':'power_out'})
add('U1','Waveshare RP2040-Zero','Goober','RP2040_Zero_Headers',28,11.75,rp_pins,True,pin_names=rp_names,pin_types=rp_types)

for row in range(3):
    for col in range(3):
        i=row*3+col+1;x=40+(col-1)*19.05;y=44+row*19.05
        add('SW'+str(i),'Kailh CPG151101S11','Goober','SW_MX_HS_CPG151101S11_1u',x,y,{'1':'GND','2':'KEY'+str(i)},True)
        add('D'+str(i),'SK6812MINI-E','LED_SMD','LED_SK6812MINI-E_3.2x2.8mm_P1.5mm_ReverseMount',x,y+5.08,
            {'1':'GND','2':'LED_DIN'+str(i),'3':'+5V_LED','4':'LED_DIN'+str(i+1) if i<9 else None},True,
            pin_names={'1':'VSS','2':'DIN','3':'VDD','4':'DOUT'},pin_types={'1':'power_in','2':'input','3':'power_in','4':'output'})
        add('C'+str(i),'100nF 16V X7R','Capacitor_SMD','C_0805_2012Metric',x+6,y+5.8,{'1':'+5V_LED','2':'GND'},True,90)

add('ENC1','ALPS EC11E15244G1','Rotary_Encoder','RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm',54.5,17.5,
    {'A':'ENC_A','B':'ENC_B','C':'GND','S1':'ENC_SW','S2':'GND','MP':'GND'})
# OLED is wired by signal name; this 2.54-mm header is not a claimed pin-for-pin PH connector.
add('J1','OLED: GND 3V3 SCL SDA','Connector_PinHeader_2.54mm','PinHeader_1x04_P2.54mm_Vertical',10,27,
    {'1':'GND','2':'+3V3','3':'OLED_SCL','4':'OLED_SDA'},angle=90,
    pin_names={'1':'GND','2':'VCC','3':'SCL','4':'SDA'})
add('U2','SN74AHCT125D','Package_SO','SOIC-14_3.9x8.7mm_P1.27mm',47,29,
    {'1':'LED_GATE_N','2':'RGB_DATA','3':'RGB_5V','4':'+5V_USB','5':'GND','6':None,'7':'GND',
     '8':None,'9':'GND','10':'+5V_USB','11':None,'12':'GND','13':'+5V_USB','14':'+5V_USB'},
    pin_names={'1':'~OE1','2':'A1','3':'Y1','4':'~OE2','5':'A2','6':'Y2','7':'GND','8':'Y3','9':'A3','10':'~OE3','11':'Y4','12':'A4','13':'~OE4','14':'VCC'},
    pin_types={'1':'input','2':'input','3':'tri_state','4':'input','5':'input','6':'tri_state','7':'power_in','8':'tri_state','9':'input','10':'input','11':'tri_state','12':'input','13':'input','14':'power_in'})
add('Q1','AO3401A P-MOSFET','Package_TO_SOT_SMD','SOT-23',35,29,{'1':'LED_GATE_N','2':'+5V_FUSED','3':'+5V_LED'},pin_names={'1':'G','2':'S','3':'D'})
add('Q2','MMBT3904 NPN','Package_TO_SOT_SMD','SOT-23',26,30,{'1':'LED_BASE','2':'GND','3':'LED_GATE_N'},pin_names={'1':'B','2':'E','3':'C'})
def res(ref,val,x,y,pins,angle=0):return add(ref,val,'Resistor_SMD','R_0805_2012Metric',x,y,pins,angle=angle)
res('R1','100k',35,33,{'1':'+5V_FUSED','2':'LED_GATE_N'})
res('R2','10k',22,30,{'1':'LED_EN','2':'LED_BASE'},90)
res('R3','100k',27,34,{'1':'LED_BASE','2':'GND'})
res('R4','330R',47,36,{'1':'RGB_5V','2':'LED_DIN1'})
res('R5','4.7k',10,31,{'1':'+3V3','2':'OLED_SDA'})
res('R6','4.7k',15,31,{'1':'+3V3','2':'OLED_SCL'})
res('R7','3.3k',55,10,{'1':'+3V3','2':'ENC_A'})
res('R8','3.3k',61,10,{'1':'+3V3','2':'ENC_B'})
res('R9','4.7k',68,10,{'1':'+3V3','2':'ENC_SW'})
add('C10','100nF 16V X7R','Capacitor_SMD','C_0805_2012Metric',42,23,{'1':'+5V_USB','2':'GND'})
add('C11','4.7uF 16V X5R','Capacitor_SMD','C_0805_2012Metric',40,29,{'1':'+5V_LED','2':'GND'},angle=90)
add('F1','1206L050YR 0.5A PTC','Fuse','Fuse_1206_3216Metric',42,7,{'1':'+5V_USB','2':'+5V_FUSED'})
for i,(x,y) in enumerate([(4,4),(76,4),(4,92),(76,92)],1):
    add('H'+str(i),'M2.5 mounting','MountingHole','MountingHole_2.7mm_M2.5',x,y,{})

# Rounded 80 x 96 mm outline, 3 mm corner radius.
W,H,R=80,96,3
for a,b in [((R,0),(W-R,0)),((W,R),(W,H-R)),((W-R,H),(R,H)),((0,H-R),(0,R))]:shape(a,b,k.Edge_Cuts,.05)
for cx,cy,a in [(W-R,R,-90),(W-R,H-R,0),(R,H-R,90),(R,R,180)]:
    s=k.PCB_SHAPE();s.SetShape(k.SHAPE_T_ARC)
    def pol(deg):return pt(cx+R*math.cos(math.radians(deg)),cy+R*math.sin(math.radians(deg)))
    s.SetArcGeometry(pol(a),pol(a+45),pol(a+90));s.SetWidth(mm(.05));s.SetLayer(k.Edge_Cuts);board.Add(s)
label('goober',40,93,2)
label('REV A / RP2040 / QMK',40,90.5,.85)
label('USB-C',28,3,.85)
label('OLED',12,24,.8)
label('RP2040-ZERO: COMPONENTS FACE OUT',40,24,.8,k.B_SilkS)
label('GP0',18.1,1.7,.8,k.B_SilkS)
label('5V',38,1.7,.8,k.B_SilkS)
label('SUPPORT SOCKETS WHEN INSERTING SWITCHES',40,93,.8,k.B_SilkS)

title=k.TITLE_BLOCK();title.SetTitle('Goober Rev A — 9-key USB-C macro pad');title.SetRevision('A.1');board.SetTitleBlock(title)
k.SaveBoard(str(HW/'goober.kicad_pcb'),board)
project={'meta':{'filename':'goober.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_clearance':.2,'min_track_width':.2,'min_via_diameter':.6,'min_through_hole_diameter':.3,'min_hole_clearance':.25,'min_copper_edge_clearance':.25},'defaults':{'board_outline_line_width':.05}}},
         'net_settings':{'classes':[{'name':'Default','clearance':.2,'track_width':.25,'via_diameter':.65,'via_drill':.3,'microvia_diameter':.3,'microvia_drill':.1,'diff_pair_width':.25,'diff_pair_gap':.2,'diff_pair_via_gap':.25}],'netclass_assignments':{},'netclass_patterns':[]}}
(HW/'goober.kicad_pro').write_text(json.dumps(project,indent=2))
(HW/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "Goober")(type "KiCad")(uri "${KIPRJMOD}/Goober.pretty")(options "")(descr "Project footprints")))\n')
contract={'pcb_mm':[W,H,1.6],'pitch_mm':19.05,'switch_centers':[[40+(c-1)*19.05,44+r*19.05] for r in range(3) for c in range(3)],'mounting_holes':[[4,4],[76,4],[4,92],[76,92]],'encoder_center':[62,20],'oled_center':[27,18],'oled_module_mm':[36,12.5],'module_center':[28,11.75],'module_mm':[18,23.5],'parts':parts}
(HW/'circuit.json').write_text(json.dumps(contract,indent=2)+'\n')
print('Board and circuit created:',len(parts),'parts',len(netnames),'nets')
if not k.ExportSpecctraDSN(board,str(HW/'goober.dsn')):raise RuntimeError('DSN export failed')
