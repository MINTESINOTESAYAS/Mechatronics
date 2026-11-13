#!/usr/bin/env python3
"""Draw original, not-to-scale schematics for the accompanying thesis draft.

Requires Pillow. The PNGs are intentionally self-contained so that both PDF and
Word versions can be edited without relying on external illustration software.
"""
from pathlib import Path
from math import atan2, cos, sin, pi
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / 'figures'
OUT.mkdir(exist_ok=True)
W, H = 1600, 840
NAVY = '#20364e'
TEAL = '#087f83'
COPPER = '#bd6635'
LIGHT = '#e8eff2'
PALE = '#e3f1f0'
INK = '#202932'
GRAY = '#66737c'
WHITE = '#ffffff'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F = ImageFont.truetype(FONT, 34)
FB = ImageFont.truetype(BOLD, 36)
SM = ImageFont.truetype(FONT, 28)
TITLE = ImageFont.truetype(BOLD, 40)


def canvas(title):
    im = Image.new('RGB', (W, H), WHITE)
    d = ImageDraw.Draw(im)
    d.text((55, 25), title, font=TITLE, fill=NAVY)
    d.line((55, 88, 1545, 88), fill='#ccd7dc', width=3)
    return im, d


def arrow(d, start, end, color=INK, width=6, head=19):
    d.line((start, end), fill=color, width=width)
    theta = atan2(end[1] - start[1], end[0] - start[0])
    pts = [end]
    for offset in (-0.55, 0.55):
        pts.append((end[0] - head * cos(theta + offset), end[1] - head * sin(theta + offset)))
    d.polygon(pts, fill=color)


def curved_arrow(d, box, start_deg, end_deg, color, width=7):
    d.arc(box, start_deg, end_deg, fill=color, width=width)
    x1, y1, x2, y2 = box
    cx, cy = (x1+x2)/2, (y1+y2)/2
    rx, ry = (x2-x1)/2, (y2-y1)/2
    def point(deg):
        a = deg*pi/180
        return (cx+rx*cos(a), cy+ry*sin(a))
    arrow(d, point(end_deg-10), point(end_deg), color, width, 18)


def label(d, xy, text, point, anchor='lt'):
    x, y = xy
    d.multiline_text((x, y), text, font=F, fill=INK, spacing=7)
    start = (x-15, y+20) if x > point[0] else (x+220, y+20)
    d.line((start, point), fill=GRAY, width=3)
    d.ellipse((point[0]-5, point[1]-5, point[0]+5, point[1]+5), fill=GRAY)


def frame(d):
    d.rounded_rectangle((145, 145, 1050, 715), radius=10, outline=NAVY, width=15)
    d.line((145, 205, 1050, 205), fill=NAVY, width=13)
    d.rectangle((158, 690, 1038, 715), fill=NAVY)


def concept1():
    im,d=canvas('Concept 1  |  Cartesian gantry + swivelling print head')
    frame(d)
    d.line((370, 205, 820, 205), fill=TEAL, width=18)
    d.rectangle((545, 178, 650, 233), fill=TEAL)
    d.line((597, 233, 597, 310), fill=NAVY, width=10)
    d.ellipse((564, 286, 630, 352), fill=WHITE, outline=COPPER, width=8)
    d.ellipse((584, 306, 610, 332), fill=COPPER)
    # Angular wrist and nozzle, exaggerated for legibility.
    d.polygon([(584,340),(621,325),(695,465),(655,483)], fill=LIGHT, outline=NAVY, width=7)
    d.polygon([(655,483),(695,465),(693,510),(678,522)], fill=COPPER, outline=NAVY)
    curved_arrow(d, (500,275,680,455), 200, 320, COPPER, 7)
    d.rectangle((350, 610, 860, 641), fill=NAVY)
    d.rectangle((500, 540, 730, 610), fill=PALE, outline=TEAL, width=6)
    d.line((495,575,730,575), fill=TEAL, width=3)
    arrow(d,(455,132),(725,132),TEAL,5)
    d.text((462,95),'X / Y travel (schematic)',font=SM,fill=TEAL)
    label(d,(1090,205),'XYZ gantry\npositions nozzle', (850,205))
    label(d,(1090,330),'A/B wrist tilts\nthe print head', (610,320))
    label(d,(1090,520),'Fixed build plate\nand workpiece', (755,620))
    d.text((260,755),'Tilted head increases moving mass; the bed stays stationary.',font=SM,fill=GRAY)
    im.save(OUT/'concept_1_tilting_head.png',optimize=True)


def concept2():
    im,d=canvas('Concept 2  |  Cartesian gantry + A/C rotary table')
    frame(d)
    d.line((370,205,820,205),fill=TEAL,width=18)
    d.rectangle((555,178,660,233),fill=TEAL)
    d.line((608,233,608,300),fill=NAVY,width=10)
    d.rounded_rectangle((565,300,650,390),radius=8,fill=LIGHT,outline=NAVY,width=6)
    d.polygon([(580,390),(635,390),(615,435),(600,435)],fill=COPPER,outline=NAVY)
    # Tilted bed as viewed along X. A pivot below plate; h exaggerated.
    d.polygon([(390,570),(835,450),(845,482),(399,602)],fill=PALE,outline=TEAL,width=7)
    d.polygon([(560,517),(696,480),(690,435),(574,464)],fill='#cfdded',outline=NAVY,width=5)
    d.line((644,622,618,526),fill=NAVY,width=8)
    d.ellipse((624,602,664,642),fill=WHITE,outline=COPPER,width=8)
    d.line((618,526,592,430),fill=COPPER,width=4)
    curved_arrow(d, (520,525,715,715), 200, 322, COPPER, 8)
    # C spin indicated as an ellipse around the table normal.
    curved_arrow(d, (475,480,775,570), 190, 345, TEAL, 6)
    arrow(d,(250,595),(250,465),NAVY,5)
    d.text((217,428),'Z',font=FB,fill=NAVY)
    arrow(d,(250,595),(350,595),NAVY,5)
    d.text((355,576),'Y',font=FB,fill=NAVY)
    d.text((230,615),'X: into page',font=SM,fill=NAVY)
    label(d,(1085,190),'XYZ gantry\n(nozzle vertical)',(820,205))
    label(d,(1085,325),'C: spin about\nbed normal',(680,515))
    label(d,(1085,475),'Heated bed\nand fixed part',(812,464))
    label(d,(1085,625),'A: tilt about\nfixed X axis',(644,622))
    d.text((260,755),'Side-view schematic; the pivot and bed offset are not to scale.',font=SM,fill=GRAY)
    im.save(OUT/'concept_2_tilting_table.png',optimize=True)


def concept3():
    im,d=canvas('Concept 3  |  Delta parallel gantry + A/C rotary table')
    for x in (205,580,955):
        d.rectangle((x,160,x+35,650),fill=LIGHT,outline=NAVY,width=7)
        d.rectangle((x-10,240 if x!=580 else 190,x+45,305 if x!=580 else 255),fill=TEAL,outline=NAVY,width=4)
    d.line((210,160,990,160),fill=NAVY,width=12)
    d.line((120,665,1060,665),fill=NAVY,width=16)
    # Three arm pairs converge on a travelling carriage.
    for sx,sy,ex in [(220,300,570),(590,250,590),(970,300,610)]:
        d.line((sx,sy,ex,415),fill=NAVY,width=9)
        d.ellipse((sx-9,sy-9,sx+9,sy+9),fill=COPPER)
        d.ellipse((ex-9,406,ex+9,424),fill=COPPER)
    d.rounded_rectangle((548,408,635,474),radius=8,fill=LIGHT,outline=NAVY,width=6)
    d.polygon([(565,474),(618,474),(600,510),(585,510)],fill=COPPER,outline=NAVY)
    d.polygon([(380,590),(770,540),(775,570),(385,620)],fill=PALE,outline=TEAL,width=7)
    d.ellipse((550,615,590,655),fill=WHITE,outline=COPPER,width=7)
    curved_arrow(d, (455,530,670,715), 200, 320, COPPER, 7)
    label(d,(1090,225),'Three coordinated\ntower carriages',(975,275))
    label(d,(1090,380),'Parallel links\nmove the nozzle',(830,347))
    label(d,(1090,565),'A/C rotary table\nunder the nozzle',(770,555))
    d.text((225,755),'Three tower actuators produce XYZ motion; A and C add two orientations.',font=SM,fill=GRAY)
    im.save(OUT/'concept_3_delta_table.png',optimize=True)


def centered(d, box, text, font=F, fill=INK):
    x1,y1,x2,y2=box
    lines=text.split('\n')
    heights=[]
    for line in lines:
        bb=d.textbbox((0,0),line,font=font)
        heights.append(bb[3]-bb[1])
    # uniform line height keeps labels vertically predictable.
    lh=font.size+7
    y=(y1+y2-lh*len(lines))/2
    for line in lines:
        width=d.textlength(line,font=font)
        d.text(((x1+x2-width)/2,y),line,font=font,fill=fill)
        y+=lh


def box(d,rect,text,fill=WHITE):
    d.rounded_rectangle(rect,radius=12,fill=fill,outline=NAVY,width=4)
    centered(d,rect,text)


def workflow():
    im,d=canvas('Control and safety architecture  |  proposed')
    # first row: digital preparation
    box(d,(45,130,300,245),'CAD model',LIGHT)
    box(d,(350,130,685,245),'5-axis path\n+ collision check',PALE)
    box(d,(735,130,1100,245),'Kinematics +\ntiming / extrusion',PALE)
    box(d,(1150,130,1540,245),'Coordinated motion\ncontroller',LIGHT)
    for a,b in [((300,188),(350,188)),((685,188),(735,188)),((1100,188),(1150,188))]:
        arrow(d,a,b,TEAL,6)
    # second row: electronics and actuators
    box(d,(1030,325,1540,440),'Six drive channels\nX, Y, Z, A, C and E',LIGHT)
    arrow(d,(1345,245),(1345,325),TEAL,6)
    box(d,(45,325,500,440),'Thermal controller\n+ temperature sensors',PALE)
    box(d,(535,325,955,440),'Nozzle + bed heaters',LIGHT)
    arrow(d,(500,382),(535,382),TEAL,6)
    # Temperature-ready and fault signals are routed back to the controller.
    d.line((270,440,270,480,1565,480,1565,215),fill=GRAY,width=4)
    arrow(d,(1565,215),(1540,215),GRAY,4,14)
    d.text((405,485),'Temperature-ready and fault signals to motion controller',font=SM,fill=GRAY)
    box(d,(1030,555,1540,680),'XYZ stage, A/C table,\nand filament feed',WHITE)
    arrow(d,(1285,440),(1285,555),TEAL,6)
    box(d,(45,555,955,680),'Hardwired E-stop + overtemperature cutoff\nCut heater / motor power; fail-safe brakes engage',WHITE)
    d.line((955,618,1030,618),fill=COPPER,width=6)
    arrow(d,(980,618),(1030,618),COPPER,6)
    d.text((70,755),'Closed-loop rotary encoders and home/limit switches are not shown individually.',font=SM,fill=GRAY)
    im.save(OUT/'control_architecture.png',optimize=True)

if __name__ == '__main__':
    concept1(); concept2(); concept3(); workflow()
    print('Wrote figures to', OUT)
