from pathlib import Path
import subprocess, math, wave, sys, json
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
from shutil import which

FFMPEG = Path(which("ffmpeg") or "ffmpeg")
FPS, W, H, DURATION = 30, 1280, 720, 8
PANEL_W, PANEL_H = 596, 326
ORIGINS = (24,660)
INK = '#eff6f8'
DIM = '#9aafbc'
MINT = '#69e1bf'
AMBER = '#ffcf7a'
COBALT = '#8ecbfb'
BG = '#111a28'
FONT = r'C:/Windows/Fonts/msyh.ttc'
BOLD = r'C:/Windows/Fonts/msyhbd.ttc'
@lru_cache(maxsize=40)
def font(size, bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)
def text(d, x, y, s, size=24, color=INK, bold=False, anchor=None):
    d.text((x,y),s,font=font(size,bold),fill=color,anchor=anchor)
def rrect(d, b, fill, radius=9, outline=None, width=1):
    d.rounded_rectangle(tuple(int(v) for v in b),radius,fill=fill,outline=outline,width=width)
def line(d, p, color, width=2): d.line(p,fill=color,width=width,joint="curve")
def clock(x): return min(1,max(0,x))
def smooth(x): x=clock(x); return x*x*(3-2*x)
def shade(y, a, b): return tuple(int(x+(z-x)*y) for x,z in zip(a,b))
@lru_cache(maxsize=20)
def gradient(w,h,top,bottom):
    im=Image.new('RGB',(w,h))
    d=ImageDraw.Draw(im)
    for y in range(h): d.line((0,y,w,y),fill=shade(y/(h-1),top,bottom))
    return im
def canvas(title, subtitle, t, labels):
    im=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(im)
    text(d,24,16,title,38,INK,True)
    text(d,W-24,27,subtitle,20,DIM,False,'ra')
    line(d,[(24,82),(W-24,82)],'#30465a')
    for (x,label,ename,col) in zip(ORIGINS,labels[0],labels[1],(MINT,AMBER)):
        rrect(d,(x,100,x+7,140),col,3)
        text(d,x+18,99,label,29,col,True)
        text(d,x+PANEL_W,104,ename,20,DIM,False,'ra')
    text(d,24,680,'自制受控教学示意  ·  双栏使用同一时间基准',18,DIM)
    text(d,W-24,680,f'{t:04.1f} / {DURATION:.0f} 秒',20,INK,True,'ra')
    d.rectangle((24,712,1256,717),fill='#293a4b')
    d.rectangle((24,712,24+1232*t/DURATION,717),fill=MINT)
    return im,d
def scene_label(im, name, detail, color=INK):
    d=ImageDraw.Draw(im)
    rrect(d,(13,13,214,53),'#132536',8)
    text(d,25,20,name,24,color,True)
    text(d,16,290,detail,18,'#f5f5f2',True)
def timeline(d,x,y,t,rows,clipcuts,colors=('#367993','#b66e43')):
    # visual sound two lanes on a shared 0—8 second clock
    lx=x+62; rw=PANEL_W-78
    for idx,(lab,cut,tag_before,tag_after) in enumerate(rows):
        yy=y+idx*42
        text(d,x+2,yy+5,lab,19,DIM)
        u=rw*cut/DURATION
        rrect(d,(lx,yy,lx+u-2,yy+32),colors[0],4)
        rrect(d,(lx+u+2,yy,lx+rw,yy+32),colors[1],4)
        text(d,lx+u/2,yy+4,tag_before,18,'#f5f5f2',True,'ma')
        text(d,lx+u+(rw-u)/2,yy+4,tag_after,18,'#fff8ee',True,'ma')
    xx=lx+rw*t/DURATION
    for cut in sorted(set(clipcuts)):
        dd=lx+rw*cut/DURATION
        line(d,[(dd,y-1),(dd,y+len(rows)*42+2)],'#e2e8ec',1)
        text(d,dd,y+len(rows)*42+7,f'{cut:g}s',16,DIM,False,'ma')
    line(d,[(xx,y-8),(xx,y+len(rows)*42+5)],INK,3)
    d.polygon([(xx-6,y-8),(xx+6,y-8),(xx,y+1)],fill=INK)
def desk(t):
    im=gradient(PANEL_W,PANEL_H,(28,53,72),(18,29,48)).copy(); d=ImageDraw.Draw(im)
    # window, city and rain, monitor desk
    rrect(d,(25,32,231,198),'#204054',10,outline='#6b8396',width=2)
    for j in range(7):
        xx=34+j*28; hh=40+(j*37)%76
        d.rectangle((xx,188-hh,xx+21,188),fill='#38536a')
        for yy in range(198-hh,169,12):
            for x in range(xx+4,xx+20,7):
                if (x+yy+j)%3==0: d.rectangle((x,yy,x+3,yy+5),fill='#afc8cc')
    for i in range(24):
        xx=30+(i*39)%192; yy=34+int((i*47+85*t)%150)
        line(d,[(xx,yy),(xx-4,yy+11)],'#6495a9',1)
    line(d,[(128,35),(128,196)],'#8598a8',3)
    d.polygon([(0,240),(596,240),(596,326),(0,326)],fill='#455661')
    d.polygon([(0,262),(596,262),(596,326),(0,326)],fill='#2d3e48')
    # desk lamp
    d.ellipse((325,231,408,242),fill='#2a3344')
    line(d,[(362,232),(345,140),(393,106)],'#dfb374',8)
    d.polygon([(365,107),(431,107),(451,159),(345,159)],fill='#d9aa62')
    d.polygon([(348,160),(450,160),(527,238),(270,238)],fill='#66654a')
    d.ellipse((270,225,527,246),fill='#82704d')
    # computer
    rrect(d,(98,99,296,225),'#132332',13,outline='#557286',width=3)
    rrect(d,(109,110,285,211),'#3b6173',6)
    text(d,123,131,'正在工作',27,'#b8e2e1',True)
    for k in range(3):
        rrect(d,(124,173+k*11,124+130*(0.35+0.18*k),178+k*11),'#99c6cb',2)
    if int(t*2.6)%2: d.rectangle((248,170,252,193),fill='#e9efce')
    d.rectangle((183,225,207,237),fill='#4e7078')
    rrect(d,(144,233,251,241),'#6e8a8b',3)
    # keyboard and cup
    d.polygon([(115,247),(283,247),(313,270),(100,270)],fill='#a3b5bd')
    for ky in range(2):
        for kx in range(10):
            xx=117+kx*16; yy=252+ky*8
            rrect(d,(xx,yy,xx+12,yy+5),'#597c85' if (kx+ky)%4 else '#c0d6d7',1)
    d.ellipse((486,250,555,266),fill='#3d4b53')
    rrect(d,(500,220,538,260),'#bd8963',7)
    d.arc((525,226,550,248),-90,90,fill='#d6aa8b',width=4)
    scene_label(im,'A · 室内','画面内容：电脑、台灯',COBALT)
    return im
def station(t):
    im=gradient(PANEL_W,PANEL_H,(24,50,63),(23,34,50)).copy(); d=ImageDraw.Draw(im)
    # layered station architecture
    d.polygon([(0,0),(596,0),(596,52),(0,97)],fill='#243d4c')
    for i in range(7):
        xx=i*95
        line(d,[(xx,25),(xx,268)],'#4b6575',4)
    for i in range(5): line(d,[(0,82+i*39),(596,66+i*39)],'#324d58',2)
    d.rectangle((0,226,596,326),fill='#5d6870')
    d.polygon([(0,276),(596,258),(596,276),(0,315)],fill='#ddb263')
    for i in range(10):
        line(d,[(i*70,286),(i*70-15,300)],'#917f58',2)
    # moving train with glowing warm windows
    tx=-266+min(1.28,max(-.24,t/4.6))*480
    rrect(d,(tx,107,tx+602,252),'#d2d3c5',22,outline='#899c9d',width=2)
    d.rectangle((tx+2,161,tx+602,184),fill='#658987')
    for j in range(6):
        xx=tx+25+j*94
        rrect(d,(xx,124,xx+65,169),'#355a68',5)
        rrect(d,(xx+4,128,xx+61,164),'#dfcb9d',3)
        if j%2: d.rectangle((xx+30,142,xx+36,164),fill='#7f806d')
    d.rounded_rectangle((tx+327,171,tx+410,249),radius=4,outline='#7d9292',width=2)
    for j in (70,425,535): d.ellipse((tx+j,244,tx+j+44,268),fill='#26313b')
    # station sign
    rrect(d,(392,16,568,61),'#122b3a',7)
    text(d,480,22,'进站列车',24,'#ffda89',True,'ma')
    for i in range(3): d.ellipse((551+i%2*9,77+i*15,559+i%2*9,85+i*15),fill='#f7cf82')
    scene_label(im,'B · 站台','画面内容：列车进站',AMBER)
    return im
def jcut(t):
    im,d=canvas('J-cut / L-cut · 音画错位剪接','戴耳机听：左声道 J · 右声道 L',t, (('J-cut · 声音先到','L-cut · 声音延续'),('Audio lead','Audio carry-over')))
    for x,soundcut,c in zip(ORIGINS,(3,5),(MINT,AMBER)):
        im.paste(desk(t) if t<4 else station(t-4),(x,148))
        ss='A室内打字' if t<soundcut else 'B站台提示'
        rr=rrect(d,(x+345,158,x+PANEL_W-14,201),'#112b35',8)
        text(d,x+PANEL_W-28,166,'正在听：'+ss,18,c,True,'ra')
        timeline(d,x,496,t,[('画面',4,'A 室内','B 站台'),('声音',soundcut,'A 打字','B 提示')],[4,soundcut])
        msg='预告：下一场声音已经进入' if 3<=t<4 and soundcut==3 else ('延续：上一场声音尚未结束' if 4<=t<5 and soundcut==5 else ('00:03 声音 → 00:04 画面' if soundcut==3 else '00:04 画面 → 00:05 声音'))
        text(d,x,635,msg,23,c,True)
    return im
def workbench(t,close=False):
    # action continuity: one moving puck, camera scale around the cut state
    # montage is purpose-built; first view overhead, second a more oblique view.
    im=gradient(PANEL_W,PANEL_H,(42,67,80),(27,47,60)).copy(); d=ImageDraw.Draw(im)
    p=smooth((t-.6)/6.25)
    px=95+399*p
    scale=1.0 if not close else 1.22
    x0=385; y0=182
    def xy(x,y):
        # oblique closer framing, keep left-to-right axis
        if close: return (scale*(x-x0)+x0+0.17*(y-y0),0.78*(y-y0)+y0)
        return x,y
    def poly(coords,c, outline=None):
        d.polygon([xy(*p) for p in coords],fill=c)
        if outline: line(d,[xy(*p) for p in coords+[coords[0]]],outline,2)
    poly([(0,68),(596,68),(596,324),(0,324)],'#496775')
    for x in range(-30,700,52):
        line(d,[xy(x,69),xy(x,327)],'#385866',1)
    for y in range(72,327,48): line(d,[xy(0,y),xy(596,y)],'#5a7982',1)
    poly([(38,178),(555,178),(555,248),(38,248)],'#283e4c')
    poly([(43,182),(550,182),(550,244),(43,244)],'#233a48')
    # sensor rails and destination
    for x in range(63,553,47): line(d,[xy(x,212),xy(x+18,212)],'#6c9395',2)
    poly([(449,148),(560,148),(560,267),(449,267)],'#355c67','#91b2b5')
    poly([(458,158),(550,158),(550,258),(458,258)],'#537c80')
    # stylized open inspection gate
    poly([(460,120),(482,120),(482,160),(460,160)],'#c2a478')
    poly([(535,120),(557,120),(557,160),(535,160)],'#c2a478')
    for q in (458,553):
        for y in (165,253):
            c=xy(q,y)
            d.ellipse((c[0]-3,c[1]-3,c[0]+3,c[1]+3),fill=MINT)
    # moving inspection puck with readable tracking dot
    cx,cy=xy(px,212)
    shw=35*scale; shh=(24 if not close else 19)*scale
    d.ellipse((cx-shw-5,cy-shh+12,cx+shw+5,cy+shh+18),fill='#152c3a')
    d.ellipse((cx-shw,cy-shh,cx+shw,cy+shh),fill='#69c9ba',outline='#a8e4d0',width=3)
    d.ellipse((cx-shw*.76,cy-shh*.82,cx+shw*.76,cy+shh*.82),fill='#3b8f90',outline='#cbeacb',width=2)
    d.ellipse((cx-8,cy-8,cx+8,cy+8),fill='#fce2a1')
    text(d,295,272,'←  启点                       目标  →',19,INK,False,'ma')
    # tracking bracket
    for q,dir in [(cx-shw-12,1),(cx+shw+12,-1)]:
        if 8<q<PANEL_W-8:
            line(d,[(q+10*dir,cy-shh-10),(q,cy-shh-10),(q,cy-shh)],AMBER,2)
            line(d,[(q,cy+shh),(q,cy+shh+10),(q+10*dir,cy+shh+10)],AMBER,2)
    scene_label(im,'镜头 ② · 近景' if close else '镜头 ① · 中景','检测件向右运动 / 示意',MINT if close else COBALT)
    return im
def motion_cut(t):
    im,d=canvas('动作匹配剪接 / 跳切 · 连续运动','在 4s 暂停，追踪琥珀色定位点',t,(('Match on action · 动作对位','Jump cut · 跳过动作'),('切在动作进行中','同机位删除一段时间')))
    im.paste(workbench(t,t>=4),(ORIGINS[0],148))
    rt=min(8,t+1.35) if t>=4 else t
    im.paste(workbench(rt,False),(ORIGINS[1],148))
    for x,right in zip(ORIGINS,(False,True)):
        lx=x+18; rw=PANEL_W-34; yy=526
        c=AMBER if right else MINT
        text(d,x,488,'源动作时间',20,DIM)
        if right:
            end1=4/8*rw; start2=5.35/8*rw
            rrect(d,(lx,yy,lx+end1,yy+20),'#3f8f93',4)
            rrect(d,(lx+end1+3,yy,lx+start2-3,yy+20),'#6b4650',4)
            rrect(d,(lx+start2,yy,lx+rw,yy+20),'#bb8055',4)
            text(d,lx+(end1+start2)/2,yy+27,'删去 1.35s',17,AMBER,False,'ma')
            pos=rw*min(rt,8)/8
        else:
            rrect(d,(lx,yy,lx+rw/2,yy+20),'#3f8f93',4)
            rrect(d,(lx+rw/2,yy,lx+rw,yy+20),'#4c9d88',4)
            text(d,lx+rw/2,yy+27,'4s 同动作相位换镜头',18,MINT,False,'ma')
            pos=rw*t/8
        for z in (0,4,8):
            text(d,lx+rw*z/8,yy+55,f'{z}s',17,DIM,False,'ma')
        xx=lx+pos; line(d,[(xx,yy-8),(xx,yy+25)],INK,3)
        msg=('局部放大，运动方向与时间都连续' if not right else '省略中间，位置和时间出现断裂')
        text(d,x,635,msg,22,c,True)
    return im

def room(t,night):
    top,bottom=((34,44,72),(31,38,56)) if night else ((106,145,156),(209,195,164))
    im=gradient(PANEL_W,PANEL_H,top,bottom).copy(); d=ImageDraw.Draw(im)
    # window sky, drifting clouds, mountain, foreground
    rrect(d,(54,28,354,235),'#293c52' if night else '#e7d9bb',10,outline='#665c55',width=3)
    # sky occlusion rectangular inners
    win=Image.new('RGB',(284,191),'#20375c' if night else '#91bfcb')
    wd=ImageDraw.Draw(win)
    if night:
        for j in range(36):
            xx=(19+j*47)%282; yy=(11+j*53)%120
            wd.ellipse((xx,yy,xx+2+(j%3==0),yy+2+(j%3==0)),fill='#c5d7df')
        wd.ellipse((193,20,244,71),fill='#f8edc0')
        wd.ellipse((207,13,252,62),fill='#20375c')
    else:
        wd.ellipse((206,19,254,67),fill='#f6deb0')
        for j in range(3):
            xx=-46+j*100+t*8
            wd.ellipse((xx,37+j*11,xx+68,56+j*11),fill='#e0e6df')
            wd.ellipse((xx+22,25+j*11,xx+51,58+j*11),fill='#e0e6df')
    for ps,col in [([(0,139),(64,73),(108,117),(150,64),(219,137),(284,86),(284,191),(0,191)],'#344d70' if night else '#688f91'),
                   ([(0,156),(78,115),(130,149),(193,92),(284,142),(284,191),(0,191)],'#243950' if night else '#5c797b')]:
        wd.polygon(ps,fill=col)
    im.paste(win,(62,36))
    line(d,[(204,36),(204,227)],'#836f60',5); line(d,[(62,141),(346,141)],'#836f60',5)
    # desk and teacup
    d.polygon([(0,254),(596,239),(596,326),(0,326)],fill='#493a49' if night else '#ae8159')
    d.polygon([(0,269),(596,254),(596,326),(0,326)],fill='#343746' if night else '#89664f')
    # lamp
    d.ellipse((413,247,538,262),fill='#443f49' if night else '#554638')
    line(d,[(473,248),(466,140)],'#aaa17a',7)
    d.polygon([(430,116),(508,116),(540,172),(405,172)],fill='#ffc880' if night else '#c8c4a3')
    if night:
        # warm pool of light
        d.polygon([(405,173),(540,173),(596,240),(340,248)],fill='#675449')
        d.ellipse((342,241,596,272),fill='#947447')
    # cup
    d.ellipse((260,268,350,281),fill='#233448' if night else '#654d42')
    rrect(d,(278,225,329,274),'#e9debc',9)
    d.arc((319,235,347,263),-90,90,fill='#e6d2a9',width=6)
    for i in range(3):
        q=t*1.4+i*.73; xx=298+i*7+5*math.sin(q)
        d.arc((xx-12,199-5*i,xx+10,222-5*i),-85,65,fill='#8e9b9b' if night else '#c8c2b0',width=2)
    return im
def dcut(t):
    im,d=canvas('硬切 / 叠化 · 让时间如何跳转','00:04 对齐同一剪点',t,(('Hard cut · 硬切','Cross dissolve · 交叉叠化'),('瞬间改变图像','两个镜头逐渐交换权重')))
    A=room(t,False); B=room(t,True)
    alphas=(0 if t<4 else 1,clock((t-3.3)/1.4))
    for x,a,c in zip(ORIGINS,alphas,(MINT,AMBER)):
        im.paste(Image.blend(A,B,a),(x,148))
        lx=x+18; rw=PANEL_W-36; yy=516
        text(d,x,489,f'当前画面：日 {int((1-a)*100+.5)}% / 夜 {int(a*100+.5)}%',20,INK,True)
        # graph weighting, shared axes
        for j in (0,1): line(d,[(lx,yy+j*62),(lx+rw,yy+j*62)],'#405467',1)
        if x==ORIGINS[0]:
            ptsA=[(lx,yy),(lx+rw/2,yy),(lx+rw/2,yy+62),(lx+rw,yy+62)]
            ptsB=[(lx,yy+62),(lx+rw/2,yy+62),(lx+rw/2,yy),(lx+rw,yy)]
        else:
            ptsA=[(lx,yy),(lx+rw*3.3/8,yy),(lx+rw*4.7/8,yy+62),(lx+rw,yy+62)]
            ptsB=[(lx,yy+62),(lx+rw*3.3/8,yy+62),(lx+rw*4.7/8,yy),(lx+rw,yy)]
        line(d,ptsA,COBALT,3); line(d,ptsB,AMBER,3)
        xx=lx+rw*t/8; line(d,[(xx,yy-4),(xx,yy+67)],INK,2)
        text(d,lx,yy+73,'0s',17,DIM,False,'ma'); text(d,lx+rw/2,yy+73,'4s',17,DIM,False,'ma'); text(d,lx+rw,yy+73,'8s',17,DIM,False,'ma')
        text(d,x,635,'一帧从日到夜 · 节奏利落' if x==ORIGINS[0] else '1.4s 叠合 · 适合含蓄的时间推移',22,c,True)
    return im

def project(p,zcam,f):
    x,y,z=p
    q=f/(z-zcam)
    return PANEL_W/2+x*q, PANEL_H*.50-y*q
def spatial(t,dolly):
    # same final central size: f0/(subject-zcam) == fzoom/subject.
    delta=2.0*smooth((t-.65)/6.15)
    subject_z=7
    zcam=delta if dolly else 0
    f=340 if dolly else 340*subject_z/(subject_z-delta)
    im=gradient(PANEL_W,PANEL_H,(39,61,80),(32,43,58)).copy(); draw=ImageDraw.Draw(im)
    def poly(ps,color,outline=None):
        qs=[project(p,zcam,f) for p in ps]
        draw.polygon(qs,fill=color)
        if outline: line(draw,qs+[qs[0]],outline,2)
    def cube(x,y,z,w,h,depth,cols):
        # perspective center anchored. Draw sides and front.
        l,r=x-w/2,x+w/2; yf=y+h
        poly([(l,yf,z),(r,yf,z),(r,yf,z+depth),(l,yf,z+depth)],cols[1])
        if x>=0:
            poly([(l,y,z),(l,y,z+depth),(l,yf,z+depth),(l,yf,z)],cols[2])
        else:
            poly([(r,y,z),(r,y,z+depth),(r,yf,z+depth),(r,yf,z)],cols[2])
        poly([(l,y,z),(r,y,z),(r,yf,z),(l,yf,z)],cols[0],cols[2])
    poly([(-7,-1.5,16),(7,-1.5,16),(7,3.7,16),(-7,3.7,16)],'#556d7e','#7a8d98')
    poly([(-7,-1.5,3.0),(7,-1.5,3.0),(7,-1.5,16),(-7,-1.5,16)],'#344b5b')
    # floor grid convergence distinct from camera crop
    for x in range(-8,9):
        line(draw,[project((x*.64,-1.5,3.0),zcam,f),project((x*.64,-1.5,16),zcam,f)],'#526a78',1)
    for z in (3,3.7,4.6,5.8,7.4,10,13.5,16):
        line(draw,[project((-7,-1.5,z),zcam,f),project((7,-1.5,z),zcam,f)],'#536b77',1)
    # gallery opening and background object
    cube(0,-1.5,13.7,2.9,4.3,.5,('#7799a6','#a6bbc1','#435b6f'))
    poly([(-.95,-1.5,13.2),(.95,-1.5,13.2),(.95,1.92,13.2),(-.95,1.92,13.2)],'#1e4659')
    cube(-3.2,-1.5,13,0.48,3.4,1.3,('#7798a5','#a9bcc3','#455d6b'))
    cube(3.2,-1.5,13,0.48,3.4,1.3,('#7798a5','#a9bcc3','#455d6b'))
    # perspective target: model plinth and amber cylinder/sculpture
    cube(0,-1.5,subject_z,1.35,.48,.75,('#6a8086','#98b0ae','#455c6b'))
    # cube shape centered at same z exactly. Bounding corners give perspective.
    cube(0,-1.02,subject_z,1.38,1.95,.65,('#d59c64','#f1cc8f','#986f59'))
    xy=project((0,.04,subject_z-.01),zcam,f); size=f/(subject_z-zcam)
    draw.ellipse((xy[0]-size*.36,xy[1]-size*.36,xy[0]+size*.36,xy[1]+size*.36),fill='#efc88a',outline='#735c57',width=2)
    # foreground paired indicators (same geometry)
    cube(-1.88,-1.5,4.6,.38,3.65,.39,('#37595f','#86a9a6','#223b4c'))
    cube(1.88,-1.5,4.6,.38,3.65,.39,('#37595f','#86a9a6','#223b4c'))
    for x in (-1.88,1.88):
        q=project((x,2.17,4.58),zcam,f)
        if 0<q[0]<PANEL_W:
            draw.ellipse((q[0]-6,q[1]-6,q[0]+6,q[1]+6),fill=MINT)
    # outline target remains in center and annotation of background
    pos=project((0,.93,subject_z),zcam,f)
    left=project((-.69,-1.02,subject_z),zcam,f)
    right=project((.69,.93,subject_z),zcam,f)
    xs=(left[0]-8,right[0]+8); yh=right[1]-8; yl=left[1]+8
    for xx,dd in [(xs[0],1),(xs[1],-1)]:
        line(draw,[(xx+11*dd,yh),(xx,yh),(xx,yh+11)],AMBER,2)
        line(draw,[(xx,yl-11),(xx,yl),(xx+11*dd,yl)],AMBER,2)
    rrect(draw,(11,11,245,49),'#152738',7)
    text(draw,22,18,'机位移动' if dolly else '机位固定',23,MINT if dolly else AMBER,True)
    text(draw,582,302, f'主体倍率 {subject_z/(subject_z-delta):.2f}×',20,INK,True,'ra')
    return im,delta,f
def camera(t):
    im,d=canvas('推镜 / 变焦 · 透视关系的差别','同主体、同起终尺寸 · 比较前景与背景',t,(('Dolly in · 摄影机前移','Zoom in · 原地增加焦距'),('透视关系会变','视角收窄，透视不变')))
    for i,x in enumerate(ORIGINS):
        scene,delta,f=spatial(t,i==0); im.paste(scene,(x,148))
        dl='移动 '+f'{delta:0.2f}'+' 单位' if i==0 else '移动 0.00 单位'
        text(d,x,490,dl,23,MINT if i==0 else AMBER,True)
        text(d,x+PANEL_W,490,('模拟焦距固定：340 px' if i==0 else f'模拟焦距：{f:.0f} px'),20,DIM,False,'ra')
        # metric foreground/bg size relative to same subject size
        labels=(('前景倍率', (4.6/(4.6-delta) if i==0 else 7/(7-delta)),MINT),
                ('背景倍率', (13.2/(13.2-delta) if i==0 else 7/(7-delta)),COBALT))
        for j,(lbl,m,col) in enumerate(labels):
            yy=526+j*38
            text(d,x,yy,lbl,19,DIM)
            rrect(d,(x+108,yy+5,x+PANEL_W-84,yy+23),'#273a4a',4)
            w=PANEL_W-192; fill=w*min(1,m/2.0)
            rrect(d,(x+108,yy+5,x+108+fill,yy+23),col,4)
            text(d,x+PANEL_W-6,yy,f'{m:.2f}×',20,INK,True,'ra')
        text(d,x,635,'前景增长更快，空间层次重新分配' if i==0 else '每一深度的画面倍率相同',22,MINT if i==0 else AMBER,True)
    return im

RENDERERS={'j-l-cut':jcut,'match-action':motion_cut,'cut-dissolve':dcut,'dolly-zoom':camera}

# Original audio Foley, no music. Two J/L channels carry each independent timeline.
RATE=48000
N=RATE*DURATION
RNG=np.random.default_rng(91)
def tone(f,d,decay=1.9):
    tt=np.arange(int(RATE*d))/RATE
    env=np.minimum(1,tt/.006)*np.exp(-decay*tt/d)*np.minimum(1,(d-tt)/.025)
    return (np.sin(2*np.pi*f*tt)+.21*np.sin(2*np.pi*f*2.02*tt))*env
def add_at(track, sig, when, gain=1):
    i=int(RATE*when)
    if i<0: sig=sig[-i:]; i=0
    if i>=len(track): return
    l=min(len(sig),len(track)-i)
    track[i:i+l]+=gain*sig[:l]
def make_sound(key):
    if key=='j-l-cut':
        # room tone & gentle keyboard clicks; station chimes, constant time by scene
        tt=np.arange(N)/RATE
        A=.012*np.sin(2*np.pi*74*tt)
        for sec in np.arange(.25,7.8,.27):
            click=RNG.normal(0,1,int(.042*RATE))*np.exp(-np.arange(int(.042*RATE))/(.008*RATE))
            add_at(A,click,sec,.07)
        B=.018*np.sin(2*np.pi*125*tt)+.017*np.sin(2*np.pi*173*tt)
        for sec,f in ((0.15,523),(0.5,660),(0.85,784),(2.05,523),(2.4,660),(2.75,784),(4.0,523),(4.35,660),(4.7,784)):
            add_at(B,tone(f,.35),sec,.105)
        tracks=[]
        for cut in (3,5):
            c=int(cut*RATE)
            tr=np.zeros(N);tr[:c]=A[:c];tr[c:]=B[:N-c];tracks.append(tr)
        stereo=np.column_stack(tracks)
    elif key=='match-action':
        tracks=[]
        for right in (False,True):
            tr=np.zeros(N); noise=RNG.normal(0,.03,N)
            # soft guide rail friction then one contact pulse
            env=np.clip(np.sin(np.pi*np.clip((np.arange(N)/RATE-.6)/6.25,0,1)),0,1)
            tr+=noise*env
            add_at(tr,tone(145,.25),5.5 if right else 6.85,.055)
            tracks.append(tr)
        stereo=np.column_stack(tracks)
    else:
        # no effect-dependent sound on purely visual comparisons; allow comfortable silent playback
        stereo=np.zeros((N,2))
    # fades prevent output click without hiding an intentional visual timing
    edge=np.linspace(0,1,int(.035*RATE))
    stereo[:len(edge)]*=edge[:,None]
    stereo[-len(edge):]*=edge[::-1,None]
    p=ROOT/f'{key}-sfx.wav'
    with wave.open(str(p),'wb') as out:
        out.setnchannels(2);out.setsampwidth(2);out.setframerate(RATE)
        out.writeframes(np.clip(stereo*32767,-32767,32767).astype('<i2').tobytes())
    return p

def render(key):
    f=RENDERERS[key]; p=ROOT/f'{key}.mp4'; sfx=make_sound(key)
    cmd=[str(FFMPEG),'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(sfx),'-map','0:v:0','-map','1:a:0','-t',str(DURATION),'-c:v','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf','21','-g','30','-c:a','aac','-b:a','128k','-movflags','+faststart',str(p)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(DURATION*FPS):
            t=i/FPS; im=f(t); proc.stdin.write(im.tobytes())
            if i in (0,90,119,120,135,211):
                im.save(ROOT/f'{key}-frame-{i:03}.png')
    finally:
        proc.stdin.close(); ret=proc.wait()
        if ret: raise RuntimeError(f'ffmpeg {ret}')
    f(3.8 if key=='cut-dissolve' else 4.1 if key=='match-action' else 5.9 if key=='dolly-zoom' else 3.5).save(ROOT/f'{key}-poster.png')
    print(key, p.stat().st_size, flush=True)

if __name__=='__main__':
    for key in sys.argv[1:] or RENDERERS: render(key)





