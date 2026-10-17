"""Frobnicator SMD - John Hollis 3080 tremolo, updated for JLC SMD assembly.
Changes vs the Eagle build: SMD parts, TL431 (CJ431) 4.5 V bias in place of the two-LED reference, 3080 in a DIP-8 socket
with an alternative LM13700 footprint (fit ONE), extra series diode + jumper in the control path, MMBT3904 follower,
SS14, LED after the diode, ribbon header.  usage: build_frob_smd.py <out.kicad_sch>"""
from sch import *
import sys
OUT = sys.argv[1]
g = lambda n: round(n * 2.54, 3)
s = Sheet('Frobnicator', 'A3')
FR = 'Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder'
FC = 'Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder'
FC12 = 'Capacitor_SMD:C_1206_3216Metric_Pad1.33x1.80mm_HandSolder'
FPOT = 'UglyFace:Potentiometer_Alpha_16mm_Vertical'
FPAD = 'Connector_Wire:SolderWire-0.5sqmm_1x01_D0.9mm_OD2.1mm'
FLED = 'LED_THT:LED_D3.0mm'
RL = {'10M': 'C26108', '470k': 'C17709', '330k': 'C17629', '220k': 'C17556', '100k': 'C17407', '47k': 'C17713', '22k': 'C17560',
      '12k': 'C17444', '10k': 'C17414', '4k7': 'C17673', '2k2': 'C17520'}
CL = {'100n': 'C49678', '47n': 'C53134', '2n2': 'C28260', '1u': 'C28323', '22u': 'C12891'}
W = lambda *p: s.wire(*p)
P = s.P
def GND(p): s.power('GND', p)
def V9(p): s.power('+9V', p)
def lab(n, p, side='r'): s.label(n, p, side)
def Rh(ref, v, cx, y, desc=None): s.part(ref, 'Device', 'R', v, cx, y, 90, fp=FR, lcsc=RL[v], desc=desc or f'Resistor {v} 1% 0805', text='t')
def Rv(ref, v, x, cy, side='r', desc=None): s.part(ref, 'Device', 'R', v, x, cy, 0, fp=FR, lcsc=RL[v], desc=desc or f'Resistor {v} 1% 0805', text=side)
def fpc(v): return FC12 if v == '22u' else FC
def Ch(ref, v, cx, y, desc=None): s.part(ref, 'Device', 'C', v, cx, y, 90, fp=fpc(v), lcsc=CL[v], desc=desc or f'Ceramic {v}', text='t')
def Cv(ref, v, x, cy, side='r', desc=None): s.part(ref, 'Device', 'C', v, x, cy, 0, fp=fpc(v), lcsc=CL[v], desc=desc or f'Ceramic {v}', text=side)
def OPA(unit, x, y, mirror=None):
    s.part('U1', 'Amplifier_Operational', 'TL072', 'TL072', x, y, 0, unit=unit, mirror=mirror, fp='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
           lcsc='C6961', desc='Dual JFET op-amp (TL072CDT)', text='ic')
def PAD(ref, name, x, y, right=False):
    s.part(ref, 'Connector_Generic', 'Conn_01x01', name, x, y, 0 if right else 180, fp=FPAD, desc=f'Wire pad: {name}', bom=False,
           text=((x + 2.54, y - 1.27), (x + 2.54, y + 1.27), 'left') if right else ((x - 2.54, y - 1.27), (x - 2.54, y + 1.27), 'right'))
    return P(ref, '1')
def POT(ref, v, name, x, y, rot=0, mirror=None, text='r', trim=False):
    if text == 'r': text = ((x + 4.445, y - 1.27), (x + 4.445, y + 1.27), 'left')
    elif text == 'l': text = ((x - 4.445, y - 1.27), (x - 4.445, y + 1.27), 'right')
    s.part(ref, 'Device', 'R_Potentiometer_Trim' if trim else 'R_Potentiometer', v, x, y, rot, mirror=mirror,
           fp='Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical' if trim else FPOT,
           desc=f'{name} trimmer, Bourns 3296W, hand-soldered' if trim else f'{name} pot, 16mm, hand-soldered', text=text,
           extra=None if trim else {'Panel': name}, bom=False)
def LED(ref, x, y, rot, desc): s.part(ref, 'Device', 'LED', 'LED', x, y, rot, fp=FLED, desc=desc, text='t', bom=False)
def D4148(ref, x, y, rot, desc): s.part(ref, 'Diode', '1N4148W', '1N4148W', x, y, rot, fp='Diode_SMD:D_SOD-123', lcsc='C81598', desc=desc, text='t')

# ================================================================ LFO (unchanged values)
s.box('LFO: SCHMITT (U1A) + INTEGRATOR (U1B), RATE, RANGE switch', g(3), g(5), g(62), g(36))
OPA(1, g(20), g(22))
W(P('U1', '2'), (g(16), g(23)), (g(16), g(26))); lab('VB', (g(16), g(26)), 'l')
W(P('U1', '3'), (g(15), g(21)))
Rh('R11', '47k', g(10.5), g(21), desc='Schmitt input from the triangle'); W(P('R11', '2'), (g(15), g(21)))
W(P('R11', '1'), (g(6), g(21))); lab('TRI', (g(6), g(21)), 'l')
Rh('R10', '100k', g(20), g(16), desc='Schmitt hysteresis (triangle = +-0.47 x square)')
W((g(15), g(21)), (g(15), g(16)), P('R10', '1')); W(P('R10', '2'), (g(25), g(16)), (g(25), g(22)))
POT('RV1', 'A100k', 'RATE', g(29), g(22) + 3.81, mirror='x', text='r')
W(P('U1', '1'), (g(25), g(22)), P('RV1', '3'))
Rv('R9', '4k7', g(29), g(28.5), side='l', desc='RATE minimum'); W(P('RV1', '1'), P('R9', '1'))
W(P('R9', '2'), (g(29), g(31))); lab('VB', (g(29), g(31)), 'l')
yi = P('RV1', '2')[1]
Rh('R12', '220k', g(36), yi, desc='Integrator input'); W(P('RV1', '2'), P('R12', '1'))
OPA(2, g(47), yi + 2.54, mirror='x')
W(P('R12', '2'), (g(41), yi), P('U1', '6'))
W(P('U1', '5'), (g(43), yi + g(2)), (g(43), yi + g(4.5))); lab('VB', (g(43), yi + g(4.5)), 'l')
Ch('C6', '2n2', g(46.5), g(18), desc='Integrator cap (AUDIO range on its own)')
W((g(41), yi), (g(41), g(18)), (g(41), g(13)))
W((g(41), g(18)), P('C6', '1')); W(P('C6', '2'), (g(52), g(18)))
Ch('C7', '100n', g(44.5), g(13), desc='Range cap: RANGE switch adds it across C6 (LFO range)'); W((g(41), g(13)), P('C7', '1'))
s.part('SW1', 'Switch', 'SW_SPDT', 'RANGE', g(51), g(13), 0, fp='SuperFreq:SW_Taiway_100_SPDT_PC',
       desc='RANGE toggle (LFO / AUDIO), Taiway 100 SPDT, only pins 1-2 used, hand-soldered', text=((g(49), g(9)), (g(49), g(10.5)), 'left'),
       extra={'Panel': 'RANGE'}, bom=False)
W(P('C7', '2'), P('SW1', '2'))
s.noconnect(P('SW1', '3'))
yo = yi + g(1)
W(P('SW1', '1'), (g(55), P('SW1', '1')[1]), (g(55), yo))
W(P('U1', '7'), (g(52), yo), (g(55), yo), (g(58), yo)); W((g(52), g(18)), (g(52), yo)); lab('TRI', (g(58), yo))
s.text('LFO ~1-24 Hz with C7 switched in; ~50 Hz - 1.1 kHz on C6 alone (46x).', g(5), g(34))

# ================================================================ DEPTH / CONTROL CURRENT
s.box('DEPTH -> OTA CONTROL CURRENT (rate LED D4)', g(3), g(40), g(62), g(70))
yc = g(52)
lab('TRI', (g(6), yc - g(2)), 'l')
POT('RV2', 'B10k', 'DEPTH', g(12), yc, mirror='x', text=((g(14), yc + g(2)), (g(14), yc + g(3.5)), 'left'))
W((g(6), yc - g(2)), (g(12), yc - g(2)), P('RV2', '3'))
W(P('RV2', '1'), (g(12), yc + g(4))); lab('VB', (g(12), yc + g(4)), 'l')
yd = P('RV2', '2')[1]
Rh('R13', '12k', g(17), yd, desc='DEPTH to control current (was 10k; VB now 4.5 V)'); W(P('RV2', '2'), P('R13', '1'))
W(P('R13', '2'), (g(22), yd))
Cv('C5', '100n', g(22), yd + 3.81, side='l', desc='Control smoothing (~130 Hz with R13), as original'); GND(P('C5', '2'))
LED('D4', g(27.5), yd, 180, 'RATE LED: 3mm panel LED (flashes with the LFO), in the control path, hand-soldered')
W((g(22), yd), P('D4', '2'))
D4148('D1', g(34), yd, 180, 'Control-path diode (was 1N914)')
W(P('D4', '1'), P('D1', '2'))
D4148('D7', g(41), yd, 180, 'Extra drop for the 4.5 V VB: full cut-off at max DEPTH with a 3080')
W(P('D1', '1'), (g(38), yd), P('D7', '2')); W(P('D7', '1'), (g(44), yd), (g(48), yd)); lab('IABC', (g(48), yd))
s.part('JP1', 'Jumper', 'SolderJumper_2_Open', 'LM13700', g(41), yd + g(5), 0, fp='Jumper:SolderJumper-2_P1.3mm_Open_RoundedPad1.0x1.5mm',
       desc='Bridge ONLY when the LM13700 is fitted (its IABC pin sits ~0.6 V higher than the 3080)', text=((g(41), yd + g(7)), (g(41), yd + g(8.5)), None), bom=False)
W((g(38), yd), (g(38), yd + g(5)), P('JP1', '1')); W(P('JP1', '2'), (g(44), yd + g(5)), (g(44), yd))
s.text('I_ABC ~ (DEPTH wiper - 3.6 V) / 12k: 0 to ~200 uA at full DEPTH, ~80 uA at DEPTH minimum.', g(5), g(66))
s.text('3080: JP1 open.   LM13700: bridge JP1.', g(5), g(68))

# ================================================================ VCA: 3080 socket
s.box('VCA: 3080 OTA in DIP-8 SOCKET (U2)  +  Q1 OUTPUT FOLLOWER', g(66), g(5), g(160), g(70))
yv = g(26)
lab('IN', (g(69), yv), 'l'); W((g(69), yv), (g(72), yv))
Rv('R1', '10M', g(72), yv + 3.81, side='l', desc='Input pull-down'); GND(P('R1', '2'))
Ch('C4', '47n', g(76.5), yv, desc='Input coupling'); W((g(72), yv), P('C4', '1'))
Rh('R2', '330k', g(82.5), yv, desc='Input attenuator (with R3: /34)'); W(P('C4', '2'), P('R2', '1'))
s.part('U2', 'Amplifier_Operational', 'CA3080', '3080', g(98), yv - g(1), 0, fp='Package_DIP:DIP-8_W7.62mm_Socket',
       desc='3080 OTA in a DIP-8 socket (user stock), hand-soldered socket. Fit U2 OR U3, not both.', text='ic', bom=False)
W(P('R2', '2'), (g(86), yv), (g(90), yv), P('U2', '3'))
lab('OTA_P', (g(90), yv - g(2)), 'l'); W((g(90), yv - g(2)), (g(90), yv))
Rv('R3', '10k', g(86), yv + 3.81, side='l', desc='Input attenuator'); W(P('R3', '2'), (g(86), yv + g(3.5))); lab('VB', (g(86), yv + g(3.5)), 'l')
Rv('R6', '10M', g(90), yv + 3.81, side='r', desc='Bleed-through null feed')
POT('RV3', '100k', 'TRIM', g(90), yv + g(5.5), rot=90, trim=True, text=((g(93), yv + g(7.5)), (g(93), yv + g(9)), 'left'))
W(P('R6', '2'), P('RV3', '2'))
W(P('RV3', '1'), (P('RV3', '1')[0], yv + g(7))); GND((P('RV3', '1')[0], yv + g(7)))
V9(P('RV3', '3'))
W(P('U2', '2'), (g(93), P('U2', '2')[1]), (g(93), g(15)), (g(93), g(12)))
Rh('R5', '10k', g(89.5), g(15), desc='Feedback to VB'); W((g(93), g(15)), P('R5', '2')); W(P('R5', '1'), (g(86), g(15))); lab('VB', (g(86), g(15)), 'l')
W((g(93), g(12)), (g(93), g(9))); lab('OTA_N', (g(93), g(9)), 'l')
Rh('R4', '470k', g(98), g(12), desc='Output-to-inverting feedback'); W((g(93), g(12)), P('R4', '1'))
W(P('R4', '2'), (g(107), g(12)), (g(107), P('U2', '6')[1]))
V9(P('U2', '7')); GND(P('U2', '4'))
s.noconnect(P('U2', '1')); s.noconnect(P('U2', '8'))
W(P('U2', '5'), (P('U2', '5')[0], g(18))); lab('IABC', (P('U2', '5')[0], g(18)), 'r')
yq = P('U2', '6')[1]
s.part('Q1', 'Transistor_BJT', 'MMBT3904', 'MMBT3904', g(113), yq, 0, fp='Package_TO_SOT_SMD:SOT-23', lcsc='C20526',
       desc='Output emitter follower (was 2N5089)', text='r')
W(P('U2', '6'), (g(107), yq), (g(109), yq), P('Q1', '1'))
W((g(109), yq), (g(109), yq + g(6))); lab('OTA_OUT', (g(109), yq + g(6)), 'l')
V9(P('Q1', '3'))
ye = P('Q1', '2')[1] + g(1)
W(P('Q1', '2'), (P('Q1', '2')[0], ye), (g(116), ye))
Rv('R7', '22k', P('Q1', '2')[0], ye + g(2.5), side='l', desc='Emitter load'); W((P('Q1', '2')[0], ye), P('R7', '1')); GND(P('R7', '2'))
Ch('C3', '1u', g(117.5), ye, desc='Output coupling'); W((g(116), ye), P('C3', '1'))
W(P('C3', '2'), (g(122), ye), (g(126), ye)); lab('OUT', (g(126), ye))
Rv('R8', '100k', g(122), ye + 3.81, side='r', desc='Output pull-down'); GND(P('R8', '2'))
Cv('C9', '100n', g(140), g(20), desc='U2 decoupling - place at the socket'); V9(P('C9', '1')); GND(P('C9', '2'))
s.text('TRIM (through R6 10M) nulls the LFO bleed-through at the OTA input - most important in AUDIO range.', g(68), g(64))
s.text('U2 = 3080 (socket) OR U3 = LM13700 (SOIC-16, below): same pins via OTA_P / OTA_N / OTA_OUT / IABC.', g(68), g(66))

# ================================================================ ALTERNATIVE OTA: LM13700 (fit instead of the 3080)
s.box('ALTERNATIVE OTA: LM13700 half A (U3) - fit INSTEAD of U2, used as a plain 3080', g(66), g(74), g(116), g(112))
ya = g(88)
s.part('U3', 'Amplifier_Operational', 'LM13700', 'LM13700', g(88), ya, 0, unit=3, fp='Package_SO:SOIC-16_3.9x9.9mm_P1.27mm', lcsc='C174050',
       desc='LM13700MX (TI). NOT fitted by default (3080 in the socket); linearising diodes and buffers unused. Bridge JP1 when fitted.', text='ic', bom=False)
for pin, net, side in (('3', 'OTA_P', 'l'), ('4', 'OTA_N', 'l')):
    q = P('U3', pin); W(q, (q[0] - g(3), q[1])); lab(net, (q[0] - g(3), q[1]), side)
s.noconnect(P('U3', '2'))
q = P('U3', '5'); W(q, (q[0] + g(3), q[1])); lab('OTA_OUT', (q[0] + g(3), q[1]))
q = P('U3', '1'); W(q, (q[0] + g(3), q[1])); lab('IABC', (q[0] + g(3), q[1]))
s.part('U3', 'Amplifier_Operational', 'LM13700', 'LM13700', g(88), g(102), 0, unit=1, fp='Package_SO:SOIC-16_3.9x9.9mm_P1.27mm', lcsc='C174050', text='ic', bom=False)
for pin in ('13', '14'):
    q = P('U3', pin); W(q, (q[0] - g(2), q[1])); GND((q[0] - g(2), q[1]))
q = P('U3', '16'); W(q, (q[0] + g(2), q[1])); GND((q[0] + g(2), q[1]))
s.noconnect(P('U3', '15')); s.noconnect(P('U3', '12'))
for unit, pin_in, pin_out, x in ((4, '7', '8', g(104)), (2, '10', '9', g(104))):
    s.part('U3', 'Amplifier_Operational', 'LM13700', 'LM13700', x, g(86) if unit == 4 else g(100), 0, unit=unit, fp='Package_SO:SOIC-16_3.9x9.9mm_P1.27mm', lcsc='C174050', text='ic', bom=False)
    q = P('U3', pin_in); W(q, (q[0] - g(1), q[1]), (q[0] - g(1), q[1] + g(2))); GND((q[0] - g(1), q[1] + g(2)))
    s.noconnect(P('U3', pin_out))
s.text('Unused: half B inputs + I_ABC to GND, both buffers off, diode-bias pins open.', g(68), g(110))

# ================================================================ POWER, VB (TL431), LEDs, PADS
s.box('POWER, VB = 4.5 V (TL431), LEDs & PADS', g(3), g(74), g(62), g(112))
ry = g(80)
PAD('J3', '9V', g(8), ry)
s.part('D5', 'Diode', 'SS14', 'SS14', g(14), ry, 180, fp='Diode_SMD:D_SMA_Handsoldering', lcsc='C2480', desc='Series polarity protection', text='t')
W(P('J3', '1'), P('D5', '2'))
W(P('D5', '1'), (g(19), ry), (g(22), ry), (g(26), ry), (g(34), ry), (g(44), ry))
V9((g(19), ry)); s.power('PWR_FLAG', (g(22), ry))
Cv('C1', '22u', g(26), ry + 3.81, desc='+9V bulk'); GND(P('C1', '2'))
# LED after D1 (power / bypass LED via the header)
Rv('R15', '4k7', g(34), ry + 3.81, side='l', desc='Power LED current')
LED('D6', g(34), ry + g(7), 90, 'Power/bypass LED, 3mm panel, hand-soldered')
W(P('R15', '2'), P('D6', '2'))
W(P('D6', '1'), (g(34), ry + g(10.5))); lab('LED_K', (g(34), ry + g(10.5)), 'r')
# VB: 2k2 feed into a TL431 set to 2.495 x (1 + 10k/12k) = 4.57 V
Rv('R14', '2k2', g(44), ry + 3.81, side='l', desc='VB feed (~1.9 mA into the TL431)')
yb = ry + g(4)
W(P('R14', '2'), (g(44), yb), (g(49), yb), (g(53), yb), (g(57), yb)); lab('VB', (g(57), yb))
s.part('U4', 'Reference_Voltage', 'TL432DBZ', 'CJ431', g(49), yb + g(6), 90, fp='Package_TO_SOT_SMD:SOT-23', lcsc='C3113',
       desc='JSCJ CJ431 shunt reference, SOT-23 pins 1=REF 2=K 3=A (TL432 pinout). Replaces the two-LED VB.', text='r')
W((g(49), yb), P('U4', '2'))
GND(P('U4', '3'))
Rv('R16', '10k', g(53), yb + 3.81, side='r', desc='TL431 set: VB = 2.495 x (1 + R16/R17) = 4.57 V')
Rv('R17', '12k', g(53), yb + g(6) + 3.81, side='r', desc='TL431 set'); GND(P('R17', '2'))
W((g(53), yb), P('R16', '1')); W(P('R16', '2'), P('R17', '1'))
W(P('U4', '1'), (P('U4', '1')[0], P('R16', '2')[1]), P('R16', '2'))
Cv('C2', '22u', g(57), yb + 3.81, side='r', desc='VB filter (large C keeps the TL431 stable)'); GND(P('C2', '2'))
OPA(3, g(10), g(100)); V9(P('U1', '8')); GND(P('U1', '4'))
Cv('C8', '100n', g(13), g(100), desc='U1 decoupling - place at the chip'); V9(P('C8', '1')); GND(P('C8', '2'))
s.part('U3', 'Amplifier_Operational', 'LM13700', 'LM13700', g(22), g(100), 0, unit=5, fp='Package_SO:SOIC-16_3.9x9.9mm_P1.27mm', lcsc='C174050', text='ic', bom=False)
V9(P('U3', '11')); GND(P('U3', '6'))
Cv('C10', '100n', g(25), g(100), desc='U3 decoupling (only needed if the LM13700 is fitted)'); V9(P('C10', '1')); GND(P('C10', '2'))
s.part('J9', 'Connector_Generic', 'Conn_01x04', 'IN/LED/GND/OUT', g(125), g(80), 0, fp='Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical',
       desc='Ribbon header 0.1": IN, LED-, GND, OUT (hand-soldered)', text=((g(127), g(79)), (g(127), g(80.5)), 'left'), bom=False)
for pn, nm in (('1', 'IN'), ('2', 'LED_K'), ('4', 'OUT')):
    q = P('J9', pn); W(q, (q[0] - g(4), q[1])); lab(nm, (q[0] - g(4), q[1]), 'l')
q = P('J9', '3'); W(q, (q[0] - g(2), q[1]))
s.power('GND', (q[0] - g(2), q[1])); sym = s.syms[-1]; find1(sym, 'at')[3] = 270
for pr in find(sym, 'property'):
    if pr[1] == 'Value':
        find1(pr, 'at')[1:4] = [q[0] - g(2) - 2.6, q[1], 90]; find1(pr, 'effects').append([Sym('justify'), Sym('left')])
for i_, (ref, name) in enumerate((('J4', 'G'), ('J5', 'IG'), ('J6', 'OG'))):
    y = g(90) + i_ * g(3)
    j = PAD(ref, name, g(124), y); W(j, (g(128), y)); GND((g(128), y))
    if ref == 'J4': s.power('PWR_FLAG', (g(127), y))
s.box('OFF-BOARD WIRING', g(118), g(74), g(160), g(112))

s.write(OUT, {'title': 'Frobnicator SMD', 'date': '2026-09-29', 'rev': '1.0 draft',
              'company': 'Super-Freq',
              'comments': ['After John Hollis. 3080 in a socket OR LM13700 (fit one); TL431 4.5 V bias',
                           'TL072 LFO: RATE, DEPTH, RANGE (LFO / audio-rate pseudo ring mod), rate LED',
                           'DRAFT for review']})
print('ok', len(s.syms), 'symbols')
