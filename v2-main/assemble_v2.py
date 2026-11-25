from pathlib import Path
from html import escape as h
import base64, io, json, re, mimetypes
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OLD=ROOT/'study-main'/'assemble.py'
old_scope={'__file__':str(OLD)}
exec(compile(OLD.read_text(encoding='utf-8-sig').split('\ndef img_data(asset):')[0],str(OLD),'exec'),old_scope)
GROUPS={**old_scope['GROUPS'],'story':'视频剪辑、镜头与叙事','art':'美术风格与美学设计'}
cards=[dict(c,category=c['group'],sources=[dict(title=a,url=b,note=d) for a,b,d in c['sources']]) for c in old_scope['cards']]
oldcards={c['key']:c for c in cards}
def data(path):
    mime=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
def read_json(path): return json.loads(path.read_text(encoding='utf-8-sig'))

def add_lab(kind, labels, panels, caption, duration=2400,start=.35):
    pair=''.join(f'<section class="live-pane"><div class="live-label">{label}</div>{body}<div class="live-num"></div></section>' for label,body in zip(labels,panels))
    return f'''<div class="study-live" data-lab="{kind}" data-duration="{duration}" data-start="{start}" role="group" aria-label="可播放的效果对照">
    <div class="live-pair">{pair}</div>
    <div class="live-controls"><button data-live="play" type="button">播放</button><button data-live="pause" type="button">暂停</button><button data-live="reset" type="button">复位</button>
    <label>进度<input type="range" min="0" max="1000" value="350" aria-label="对照进度"><output>35%</output></label></div>
    <p class="live-caption">{caption}</p></div>'''
axis='<div class="live-axis"><i class="live-bar"></i></div>'
ball='<div class="live-axis"><i class="live-ball"></i></div>'
scene='<div class="live-focus"><div class="scene"><div class="table"></div><div class="distant">B</div><div class="near">A</div></div></div>'
chart='<canvas class="live-signaling" width="240" height="120" aria-label="时间位移示例曲线"></canvas>'
def model(anchor):
    f=''.join(f'<div class="cube-face {side}">'+ ('<span>1</span>' if side=='front' and anchor else '') +'</div>' for side in ['front','back','right','left','top','bottom'])
    return f'<div class="hotspot-stage {"" if anchor else "hotspot-fixed"}"><div class="hotspot-model">{f}</div></div>'

oldcards['scroll']['demoHtml']=add_lab('scroll',['滚动驱动','一次触发'],[axis,axis],'把滑杆当成时间，滚动位置先增加、停留、再回退。比较停留与回退时两个进度。',4000)
oldcards['easing']['demoHtml']=add_lab('easing',['匀速 Linear','三次缓出 Ease-out'],[ball,ball],'同一距离同一时间。暂停在 50%，读取两种曲线已经走过的比例。为便于观察做了慢放。',1400)
oldcards['signaling']['demoHtml']=add_lab('signaling',['只有完整曲线','标亮当前时刻'],[chart,chart],'同一假设数据、同一播报进度，右侧虚线把时刻和曲线点对应起来。',8000)
oldcards['hotspot']['demoHtml']=add_lab('hotspot',['模型表面锚点','固定屏幕标记'],[model(True),model(False)],'拖动或播放使两个示例立方体同步旋转。观察标记是否与同一个表面一起变化。CSS 三维示意。',2800,.15)

def entry(key,category,name,english,look,use,distinction,scenario,practice,prompt,sources,**kwargs):
    return dict(key=key,category=category,name=name,english=english,look=look,use=use,distinction=distinction,scenario=scenario,practice=practice,prompt=prompt,sources=sources,**kwargs)

def src(title,url,note):return dict(title=title,url=url,note=note)

focus=entry('rack-focus','story','移焦与整体模糊','Rack focus · Defocus',
    '同一画面里的前景 A 和远景 B，左边清晰位置从 A 移到 B。右边两者一起由模糊变清晰。',
    '在不换机位和不跳剪的情况下，把观众的注意力从一个深度的物体引到另一个物体。',
    '移焦改变清晰的焦平面。整体模糊改变整帧清晰度。这里用不同图层的模糊模拟焦点变化；真实拍摄还受景深、光圈和焦点距离影响。',
    '人物发现关键物件、实验前景与读数之间转换、产品细节揭晓。',
    '固定机位、焦距与画幅，放一前一后两个物件。将对焦从前景平滑切换到后景，观察大小和构图保持不变。',
    '固定镜位和焦距，前景 A 与后景 B 同时在画面中。起初 A 清晰 B 虚化，随后焦点缓慢移向 B。结尾 B 清晰 A 虚化，主体位置和大小保持稳定。另做整体模糊到清晰的对照。',
    [src('StudioBinder · The Rack Focus: Creative Examples of Camera Movements & Angles','https://www.studiobinder.com/blog/rack-focus-shot-camera-movement-angles/','实读定义、焦平面变化与电影用法。')],
    demoHtml=add_lab('focus',['同一镜头移焦 Rack focus','全画面去模糊 Defocus'],[scene,scene],'暂停在前、中、后，观察哪个深度清晰。前景与背景是独立图层的光学概念示意。',2200,0.22))

truck_canvas='<canvas class="live-signaling" width="240" height="144" aria-label="近柱、主体和背景门的透视比较"></canvas>'
truck=entry('truck-pan','story','横移与摇镜','Truck · Pan',
    '青绿色近柱、琥珀色主体和远处门。两边以相同主体水平位置变化为参照，左边的近柱与远门相对主体产生更明显的位置变化，右边是机位不动时的转向。',
    '横移带来空间视差与新的遮挡关系，适合侧向揭示。摇镜在同一点扩展观看方向，适合跟随视线或扫过宽场景。',
    'Truck 是摄影机侧向移动；Pan 是绕自身轴水平旋转。示例用理想针孔透视计算同一场景，不是实拍。',
    '室内或三维产品横向揭示、知识短片导览、人物视线转向、展品巡视。',
    '布置一根近柱和一个远门，固定焦距横移半米，观察主体被遮挡的位置变化。再站在同一点转向，比较近远对象。',
    '固定一个有近柱、主体和远门的透视场景，A相机侧向平移，B相机位置固定且水平转向。匹配主体在画面中的初末位置，比较近柱和背景门的相对位移，提供暂停拖动和对照。',
    [src('StudioBinder · Types of Camera Movements in Film Explained: Definitive Guide','https://www.studiobinder.com/blog/different-types-of-camera-movements-in-film/','实读横移、水平摇镜的定义、机位差别与场景用法。')],
    demoHtml=add_lab('truck-pan',['横移 Truck','摇镜 Pan'],[truck_canvas,truck_canvas],'拖动进度，观察青柱、琥珀主体以及远门三者的位置关系。',2600,.15))

glass='<div class="study-static-ui"><div class="live-pair">'+''.join(f'<section class="live-pane"><div class="live-label">{name}</div><div class="style-screen"><div class="glass-sample {cls}"><b>现场总览</b><span>Overview</span></div></div></section>' for name,cls in [('普通透明',''),('背景模糊','glass-blur')])+'</div><label class="style-setting">右侧模糊强度<input data-style-param="blur" type="range" min="0" max="24" value="12"><output>12 px</output></label><p class="live-caption">拖动强度；背景图案变模糊，卡片文字保持清晰。</p></div>'
glass_card=entry('glass-surface','art','玻璃拟态与普通半透明','Glassmorphism · Backdrop blur',
    '两侧有相同透明底色，右侧后面的图案边缘被模糊，文字和边框仍清楚。拖动模糊强度比较。',
    '分出浮动信息层，同时保留下面环境的色彩和空间线索。',
    '透明度是底色让背景透出。背景模糊是改变卡片后面的像素。玻璃拟态还可有边框、高光和合理层次。',
    '悬浮工具栏、产品展示说明、轻量卡片。高频工业读数、复杂正文优先保证稳定对比。',
    '在同一条复杂背景上做透明层与背景模糊层，把右侧模糊从 0 调到 24px，比较文字和背景边缘，观察不模糊时是否仍能阅读。',
    '做同一内容的双栏玻璃卡片对照。左侧只有半透明底，右侧应用 background blur 12px、细亮边和轻阴影。两侧文字保持完全相同且清晰，用户能滑杆调节模糊强度。',
    [src('MDN · backdrop-filter','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter','实读属性、半透明背景与可试用 blur 示例。')],demoHtml=glass)
type_ui='<div class="study-static-ui"><div class="live-pair">'+''.join(f'<section class="live-pane"><div class="live-label">{label}</div><div class="type-card {cls}"><span class="type-small">STUDY  /  课堂实验</span><h4 class="type-head">读懂光影<br>Light &amp; Form</h4><p class="type-desc">观察光源大小、影子边缘，以及明暗层次。先定位形状，再描述关系。</p></div></section>' for label,cls in [('紧密无节奏','type-bad'),('留出阅读节奏','type-good')])+'</div><label class="style-setting">右侧行高<input data-style-param="leading" type="range" min="100" max="205" value="155"><output>1.55 倍</output></label><label class="style-setting">右侧字距<input data-style-param="tracking" type="range" min="0" max="15" value="3"><span data-tracking-value>0.03 em</span></label></div>'
type_card=entry('type-rhythm','art','字距、字偶距与行距','Tracking · Kerning · Leading',
    '同一段内容用两个排版。拖右侧行高和字距，观察行之间的分离与横向阅读节奏。标题展示衬线与无衬线选择。',
    '让信息有节奏、可快速扫读，也使作品的气质与阅读场景协调。',
    '字偶距 Kerning 是特定字符对的调整。Tracking 控制一串字符整体字距。Leading/Line-height 控制纵向行间空间。',
    '作品集、课程长页、PPT正文、海报标题、工程说明。先测试实际字号、每行长度和窄屏。',
    '先改行高看纵向分隔，再只改字距看横向节奏。缩到手机宽度，看能否在三秒内复述标题和第一句。',
    '同一段内容做两个对照版，保持文字完全相同。右侧标题采用有层级的中英衬线搭配，正文从1.55倍行高开始，用滑杆分别修改行间空间和字距。不用全大写或过度加宽来取代清楚的层级。检查窄屏。',
    [src('Sarah Gibbons、Therese Fessenden / NN/g · Typography Terms: Glossary','https://www.nngroup.com/articles/typography-terms-ux/','实读术语及基线、行距、字偶距图例。'),src('Adobe InDesign · About kerning and tracking','https://helpx.adobe.com/indesign/desktop/format-and-style-text/tabs-indents-and-spacing/about-kerning-and-tracking.html','核对特定字偶与整体字符间距的区别。')],demoHtml=type_ui)

# Merge with the original project cards while preserving stable public anchors and earlier sources.
for folder in ['v2-web','v2-video','v2-art']:
    for c in read_json(ROOT/folder/'cards.json'):
        c['folder']=folder
        replace=c.get('replaceKey')
        if replace:
            original=oldcards[replace]
            c['key']=replace
            c['asset']=original['asset']
            for s in original['sources']:
                if s['url'] not in {x['url'] for x in c['sources']}:c['sources'].append(s)
            cards[cards.index(original)]=c
        else:
            cards.append(c)
cards.extend([focus,truck,glass_card,type_card])
scenarios={
'scroll':'长页产品拆解、阅读指示器、知识实验的进度控制、展览型作品集。','easing':'面板进入、按钮反馈、轻量卡片切换、日常操作的停靠。','hotspot':'设备数字模型、产品部件教学、装配图预览。','panels':'知识漫画、脚本分镜、操作说明。','hierarchy':'竞赛答辩、PPT、课件封面、活动海报。','hmi':'设备总览、虚拟工位、生产流程中参数监视。','alarm':'实时监控、异常排查、操作复盘。','ladder':'PLC实验、控制逻辑课堂、离线仿真调试。','eda':'原理图阅读、PCB走线、封装与网络核对。','cad':'装配图、机械零件设计与工程制图作业。','signaling':'知识动画、数学或控制曲线解说、实验步骤演示。','chart':'测量记录、实验汇报、实时曲线、数据故事。','review':'AI辅助开发、自动化流程、交互验收与迭代复盘。'}
practices={
'scroll':'播放到滚动位置停留的一段，暂停，再拖到结尾。回答为什么一次触发仍完成，而滚动驱动回退。','easing':'同一半程暂停并读出两个位置百分比，换实际卡片重做。','hotspot':'停在不同角度，检查左边记号是否仍在原表面，右边记号是否漂移。','mask-vs-fade':'拖动到 50%，定位遮罩边界与淡入的透明区域。两者结束位置应该一致。','stagger-vs-together':'暂停在约 40%，数一数已出现与尚未出现的条目。','spring-vs-easeout':'暂停在目标线附近，找出过冲，再把同样动作做成单调缓出。','parallax-vs-uniform':'拖到 60% 再回退，比较三层的相对位置。','spotlight-vs-magnet':'用鼠标、触摸或方向键移动白点，观察光斑与按钮实体的位移。','shared':'打开详情后暂停，沿同一封面找连续轨迹，再将进度退回起点。','feedback-states':'模拟保存，暂停在 20–60%，分别指出两个用户能否知道系统已收到输入。','signaling':'播放再暂停，读出当前时刻及位移。在一条真实课程图上复现同步提示。','jcut':'跳至 3.2、4.2 和 5.2 秒，戴耳机先听左再听右。剪出新声音先来和旧声音保留两个版本。','match-action':'跳到 3.93 秒和 4.07 秒，观察手的位置与动作时间是否延续。','cut-dissolve':'在 4 秒暂停，观察右侧两个场景同时可见，分别用硬切与叠化做一个时间过渡。','dolly-zoom-comparison':'跳到 6.9 秒，比较近柱、主人公和远处背景的比例。用 Blender 或真实摄影完成一次移动机位与固定机位改焦距的对照。'}
for c in cards:
    c.setdefault('scenario',scenarios.get(c['key'],'在当前工作中先做同内容的两版对照，保持输入条件一致。'))
    if not c.get('practice'):
        c['practice']=practices.get(c['key'],c['prompt'])

# Whole-segment re-reading summaries are mapped to the correct learned term. The source footage is linked, not embedded.
segments=read_json(ROOT/'v2-rewatch'/'rewatch.json')
def link_key(s):
    k=s['key']
    if k=='camera':
        if s['start'].startswith('02:'):return 'rack-focus'
        if s['start'].startswith('03:'):return 'truck-pan'
        return 'dolly-zoom-comparison'
    return {'scroll-concepts':'scroll','parallax':'parallax-vs-uniform','spotlight':'spotlight-vs-magnet'}.get(k,k)
for i,s in enumerate(segments,1):
    s['id']='source-lesson-'+str(i)
    s['term']=link_key(s)
    assert {'url','start','end','observed','practice','status'}<=s.keys()
for c in cards:
    c['segments']=[s for s in segments if s['term']==c['key']]
    for s in c['sources']:
        matches=[seg for seg in segments if seg['url'].split('?')[0]==s['url'].split('?')[0]]
        if matches: s['note']='新版已复核相关区间，具体时间点、观察及练习见下方原片跟练。'
    c['media']=list(dict.fromkeys((['interactive'] if c.get('demoHtml') else [])+(['video'] if c.get('videoFiles') else [])+(['imagegen'] if c.get('board') else [])+(['image'] if c.get('asset') else [])))
    if not c['media']: raise RuntimeError(c['key']+' has no visual')
order={
'web':['scroll','easing','spring-vs-easeout','mask-vs-fade','stagger-vs-together','parallax-vs-uniform','spotlight-vs-magnet','shared','feedback-states','hotspot'],
'story':['jcut','match-action','cut-dissolve','dolly-zoom-comparison','truck-pan','rack-focus','panels','hierarchy'],
'art':['art-media','art-style-history','composition-balance','light-style','palette-harmony','glass-surface','type-rhythm'],
'engineering':['hmi','alarm','ladder','eda','cad'],'data':['signaling','chart'],'workflow':['review']}
reverse={k:(i,j) for i,ks in enumerate(order.values()) for j,k in enumerate(ks)}
cards.sort(key=lambda c:reverse.get(c['key'],(99,99)))
assert len({c['key'] for c in cards})==len(cards)

def asset_path(c):
    group,name=c['asset'].split('/')
    return ROOT/('study-'+group)/(name+'.png')

def fig(path,caption,alt=None):
    with Image.open(path) as im: w,ht=im.size
    return f'<figure class="card-figure"><img src="{data(path)}" alt="{h(alt or caption,quote=True)}" width="{w}" height="{ht}" loading="lazy"><figcaption><span>{h(caption)}</span><button type="button" class="figure-zoom" data-figure-zoom>查看大图</button></figcaption></figure>'

def art_grid(c):
    file=ROOT/'v2-art'/c['board']
    if not file.is_file():
        raise FileNotFoundError(file)
    # Preserve the generated master unchanged; isolate panels for comfortable mobile viewing.
    dest=ROOT/'v2-art'/'panels'
    dest.mkdir(exist_ok=True)
    figures=[]
    with Image.open(file) as big:
        w,ht=big.size
        margin=7 if c['board']=='history.png' else 3
        for i,(title,note) in enumerate(c['panels']):
            x=i%2;y=i//2
            left=x*w//2+margin;top=y*ht//2+margin;right=(x+1)*w//2-margin;bottom=(y+1)*ht//2-margin
            # Preserve pixel-art edges as PNG, compress the other photographic panels.
            out=dest/(c['key']+'-'+str(i+1)+('.png' if c['key']=='art-media' and i==2 else '.webp'))
            crop=big.crop((left,top,right,bottom)).convert('RGB')
            if out.suffix=='.png':crop.save(out,optimize=True)
            else:crop.save(out,quality=92,method=6)
            figures.append(fig(out,title+' · '+note,title))
    return '<div class="art-study"><button type="button" class="art-layout" aria-pressed="false">并排总览</button><div class="art-grid">'+''.join(figures)+'</div><p class="study-note">ImageGen 原创对照样张，供观察风格与形式特征。每一幅均可放大；历史风格的实际作品见馆藏原链接。</p></div>'

def videos(c):
    folder=ROOT/c.get('folder','v2-video')
    out=[]
    for i,video in enumerate(c['videoFiles']):
        vpath=folder/video['path']
        poster=data(folder/video['poster']) if video.get('poster') else ''
        marks=''.join(f'<button type="button" class="video-mark" data-time="{mark["time"]:.2f}">{mark["time"]:g}s · {h(mark["label"])}</button>' for mark in video.get('marks',[]))
        videomark=f'poster="{poster}"' if poster else ''
        out.append(f'''<figure class="study-video"><video controls playsinline preload="metadata" width="1280" height="720" {videomark} aria-label="{h(c['name'],quote=True)}" src="{data(vpath)}"></video><figcaption>{h(video['caption'])}</figcaption><div class="video-marks" aria-label="暂停到关键时间点">{marks}</div></figure>''')
    return ''.join(out)
def display(c,i):
    modes=' '.join(c['media'])
    media_names={'interactive':'可控对照','video':'视频微片','imagegen':'ImageGen 多图','image':'效果图'}
    modes_text=' · '.join(media_names[m] for m in c['media'] if m!='image' or len(c['media'])==1)
    visuals=''
    if c.get('demoHtml'): visuals+=c['demoHtml']
    if c.get('videoFiles'): visuals+=videos(c)
    if c.get('board'): visuals+=art_grid(c)
    if c.get('asset'):
        static=fig(asset_path(c),c['look'])
        if visuals: visuals+='<details class="static-reference"><summary>看原有静态图解</summary>'+static+'</details>'
        else:visuals+=static
    sources=''.join(f'<li><a href="{h(s["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{h(s["title"])}</a><br><span>{h(s["note"])}</span></li>' for s in c['sources'])
    linked=''.join(f'<li><a href="#{s["id"]}">{h(s["author"])} · {h(s["start"])}–{h(s["end"])}</a> <a class="start-link" href="{h(s["url"],quote=True)}" target="_blank" rel="noopener noreferrer">直接打开该时间点 ↗</a></li>' for s in c['segments'])
    lesson=f'<div class="mini-sources"><strong>原片跟练</strong><ul>{linked}</ul></div>' if linked else ''
    keywords=' '.join([c['name'],c['english'],c.get('keywords',''),GROUPS[c['category']],modes_text])
    return f'''<article id="term-{c['key']}" class="knowledge-card" data-category="{c['category']}" data-media="{modes}" data-keywords="{h(keywords,quote=True)}" aria-labelledby="title-{c['key']}">
    <div class="card-body card-heading">
      <span class="card-index">{i:02d} / {GROUPS[c['category']]}<span class="media-type">{modes_text}</span></span>
      <h3 id="title-{c['key']}">{h(c['name'])}</h3><p class="english" lang="en">{h(c['english'])}</p>
    </div>
    <div class="card-visuals">{visuals}</div>
    <div class="card-body">
      <dl class="card-facts"><div><dt>看哪里</dt><dd>{h(c['look'])}</dd></div>
      <div><dt>作用</dt><dd>{h(c['use'])}</dd></div><div><dt>怎么分</dt><dd>{h(c['distinction'])}</dd></div>
      <div><dt>适用</dt><dd>{h(c['scenario'])}</dd></div></dl>
      <div class="practice-call"><b>现在就练</b><p>{h(c['practice'])}</p></div>
      {lesson}
      <details class="prompt"><summary>中文提示词</summary><blockquote>{h(c['prompt'])}</blockquote></details>
      <div class="card-sources"><strong>原始资料与学习记录</strong><ul>{sources}</ul></div>
      <button type="button" class="copy-prompt" data-prompt="{h(c['prompt'],quote=True)}">复制提示词</button>
    </div></article>'''

def source_section():
    groups={}
    for s in segments:groups.setdefault((s['author'],s['title']),[]).append(s)
    acc=[]
    for (author,title),group in groups.items():
        lessons=[]
        for s in group:
            use=s.get('use','')
            lessons.append(f'''<article class="source-lesson" id="{s['id']}"><div class="source-time"><strong>{h(s['start'])}–{h(s['end'])}</strong><a class="start-link" href="{h(s['url'],quote=True)}" target="_blank" rel="noopener noreferrer">打开原片 ↗</a><a href="#term-{s['term']}">回到对应效果</a></div><h4>这段看什么</h4><p>{h(s['observed'])}</p>{'<h4>具体如何用</h4><p>'+h(use)+'</p>' if use else ''}<h4>跟着做一次</h4><p>{h(s['practice'])}</p><small>{h(s['status'])}</small></article>''')
        acc.append(f'<section class="source-group"><div class="source-group-heading"><span>{h(author)}</span><h3>{h(title)}</h3></div><div class="source-lessons">{"".join(lessons)}</div></section>')
    return '<section id="source-practice" class="source-section"><div class="frame"><div class="section-heading"><h2>原片跟练</h2><p>5 条原视频 / 14 个相关区间 / 8 分 20 秒</p></div><p class="source-method">已取得公开媒体并对指定区间执行全音轨自动转写及全段时序读图（0.5 秒或 1 秒一个图像样本）。每段标有实际画面、用途和可练习任务。视频原址打开在标记时点；未把时序抽样和 ASR 标成真人连续看听。</p>'+''.join(acc)+'</div></section>'

PROFILE='''<div class="version-summary"><p><strong>第二版 · 2026.11.20</strong> 先练网页交互动效，再练剪接、运镜和美术判断。可控演示共用时间轴，原创视频可暂停到关键剪点，ImageGen 样张按同一主题比较视觉变量。</p></div><details><summary>为什么这些领域值得你优先学</summary>'''+old_scope['PROFILE']+'</details>'
ROUTE='''<ol><li><strong>网页动效（35 分钟）。</strong> 先比较 <a href="#term-scroll">滚动驱动</a>、<a href="#term-mask-vs-fade">揭示与淡入</a>、<a href="#term-spring-vs-easeout">弹簧和缓出</a>。从 0%、50%、100% 拖到任意位置观察。接着按 <a href="#source-practice">原片时间码</a>复现其中一段。</li><li><strong>视频与镜头（30 分钟）。</strong> 用耳机听 <a href="#term-jcut">J/L 剪接</a>，逐点暂停 <a href="#term-match-action">动作匹配和跳切</a>，比较 <a href="#term-dolly-zoom-comparison">推镜与变焦</a>。给同一小故事分别作两个版本。</li><li><strong>美术与设计（35 分钟）。</strong> 从 <a href="#term-art-media">四种画风</a>、<a href="#term-light-style">光线和明暗</a>、<a href="#term-palette-harmony">色彩关系</a>、<a href="#term-composition-balance">构图</a>入手，为同一个真实作品做至少三种对照并复述差别。</li><li><strong>工程和知识表达（30 分钟）。</strong> 选真实虚拟工位练定位状态、条件、输出和报警。用 <a href="#term-signaling">视觉提示</a> 和 <a href="#term-chart">选图原则</a> 将观察结果讲清楚。</li></ol><p class="source-method">将同一段素材做可控的 A/B 比较。每次只改一个变量，记录第一眼看到什么、它叫什么、何时有用、怎么验收。这样还可以用于下次向 AI 描述需求。</p>'''
html=(ROOT/'study-shell'/'shell.html').read_text(encoding='utf-8-sig')
for tag,val in [('PROFILE',PROFILE),('CARDS','\n'.join(display(c,i) for i,c in enumerate(cards,1))),('ROUTE',ROUTE),('TOTAL',str(len(cards)))]:
    html=html.replace('<!--'+tag+'-->',val)
html=html.replace('<button type="button" class="filter" data-filter="story" aria-pressed="false">镜头与视觉表达</button>','<button type="button" class="filter" data-filter="story" aria-pressed="false">剪辑与镜头</button><button type="button" class="filter" data-filter="art" aria-pressed="false">美术与美学</button>')
html=html.replace('<div class="search-row">','<div class="media-filter" role="group" aria-label="按呈现方式筛选"><button type="button" data-media-filter="all" aria-pressed="true">全部呈现</button><button type="button" data-media-filter="interactive" aria-pressed="false">可控演示</button><button type="button" data-media-filter="video" aria-pressed="false">视频动画</button><button type="button" data-media-filter="imagegen" aria-pressed="false">ImageGen 多图</button><button type="button" data-media-filter="image" aria-pressed="false">静态图解</button></div><div class="search-row">')
html=html.replace('<a class="secondary" href="#practice">按路线练习</a>','<a class="secondary" href="#source-practice">原片跟练</a><a class="secondary" href="#practice">按路线练习</a>')
html=html.replace('<section class="section route" id="practice"',source_section()+'<section class="section route" id="practice"')
html=html.replace('const cards = [...grid.querySelectorAll','const mediaFilters = [...document.querySelectorAll("button[data-media-filter]")];\n  let media = "all";\n  const cards = [...grid.querySelectorAll')
html=html.replace('category: element.dataset.category,','category: element.dataset.category,\n      media: element.dataset.media.split(" "),')
html=html.replace('words.every(word => card.text.includes(word));','(media === "all" || card.media.includes(media)) && words.every(word => card.text.includes(word));')
html=html.replace("  search.addEventListener('input'",'''  for (const b of mediaFilters) b.addEventListener("click", () => {
    media=b.dataset.mediaFilter;mediaFilters.forEach(x=>x.setAttribute("aria-pressed",String(x===b)));matchCards()
  });
  search.addEventListener('input' ''').replace("search.addEventListener('input' ,","search.addEventListener('input',")
html=html.replace("    search.value = '';\n    setCategory('all');","    search.value = '';\n    media='all'; mediaFilters.forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.mediaFilter==='all')));\n    setCategory('all');")
html=html.replace("        card.element.hidden = !matches;","        card.element.hidden = !matches;") if False else html
html=html.replace("      card.element.hidden = !matches;", "      card.element.hidden = !matches;\n      if(!matches){card.element.querySelectorAll('video').forEach(v=>v.pause());card.element.querySelectorAll('.study-live').forEach(r=>r.dispatchEvent(new Event('atlas-pause')));const p=card.element.querySelector('[data-mv-action=pause]');if(p&&!p.disabled)p.click()}")
# Preserve anchor navigation when a current filter hides a target card.
EVENTS="""
<script>
(()=> {
  document.addEventListener('click',event=>{
    const layout=event.target.closest('.art-layout');
    if(layout){const grid=layout.closest('.art-study').querySelector('.art-grid');const on=grid.classList.toggle('is-compact');layout.setAttribute('aria-pressed',String(on));layout.textContent=on?'逐张细看':'并排总览';return}
    const mark=event.target.closest('.video-mark');
    if(mark){const v=mark.closest('figure').querySelector('video');if(v.readyState===0){v.addEventListener('loadedmetadata',()=>{v.currentTime=Number(mark.dataset.time);v.pause()},{once:true});v.load()}else{v.pause();v.currentTime=Number(mark.dataset.time)}return}
    const anchor=event.target.closest('a[href^="#term-"]');if(anchor){const target=document.getElementById(anchor.hash.slice(1));if(target&&target.hidden){document.querySelector('#clear-filters').click();requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}}
  });
  document.addEventListener('play',event=>{if(event.target.tagName==='VIDEO')document.querySelectorAll('video').forEach(v=>{if(v!==event.target)v.pause()})},true);
})();
</script>
"""
CSS="""
<style>
.card-body.card-heading{flex:0 0 auto;gap:.28rem}.card-heading h3{margin:0;line-height:1.25}
.card-index{width:100%;display:flex;gap:.5rem;justify-content:space-between;align-items:baseline;flex-wrap:wrap}
.media-type{font-size:.72rem;letter-spacing:0;color:#617266;font-weight:600}
.card-body .card-sources ul,.mini-sources ul{margin:.35rem 0 0;padding-inline-start:1.2em}
.card-sources li+li,.mini-sources li+li{margin-top:.4rem}
.card-sources a,.mini-sources a,.source-section a,.route a{color:#176353}
.card-visuals{display:grid;gap:.7rem;margin:0!important;padding:0 clamp(10px,1.5vw,18px);min-width:0}
.static-reference{padding:.35rem 0;color:#176353;font-size:.85rem}
.static-reference summary{cursor:pointer}
.static-reference .card-figure{margin-top:.5rem}
.card-body .prompt blockquote{margin-top:.42rem}.profile details summary{cursor:pointer}
.card-figure figcaption{display:flex;align-items:start;gap:.45rem;justify-content:space-between}
.card-figure img{display:block;width:100%;height:auto}
.figure-zoom{flex:none}
.art-grid{display:grid;grid-template-columns:1fr 1fr;gap:.45rem;min-width:0}
.art-grid .card-figure{border-radius:5px}
.art-grid .card-figure img{aspect-ratio:1.5;object-fit:cover}
.art-grid .card-figure figcaption{display:block;min-height:75px;padding:.55rem .6rem;font-size:.78rem}
.art-grid .figure-zoom{display:block;margin:.45rem 0 0}
.study-note{font-size:.76rem;color:#647068;margin:.5rem 0}
.study-video{margin:0;border-radius:9px;overflow:hidden;background:#101a2c;color:#eaf4fc;padding:.55rem}
.study-video video{display:block;width:100%;height:auto;aspect-ratio:16 / 9;background:#0a1221;border-radius:5px}
.study-video figcaption{padding:.5rem .25rem;font-size:.8rem;line-height:1.55;color:#cbdce8}
.video-marks{display:flex;flex-wrap:wrap;gap:.45rem;padding:.15rem .25rem .4rem}
.video-mark{background:#1f3e50;border:1px solid #52748b;color:#e8f6fb;border-radius:6px;padding:.35rem .5rem;font-size:.76rem;cursor:pointer}
.practice-call{border-left:3px solid #5ba88c;background:#e9f0e9;padding:.6rem .75rem;color:#244c41;font-size:.87rem}
.practice-call p{margin:.3rem 0 0;color:#37594e}
.mini-sources{font-size:.8rem;overflow-wrap:anywhere;background:#f1f4ef;padding:.55rem .7rem;border-radius:5px;color:#3e5a50}
.start-link{font-weight:720;text-decoration:underline}
.media-filter{display:flex;gap:.4rem;flex-wrap:wrap;margin:.8rem 0}
.media-filter button{font-size:.81rem;border:1px solid #bbc8b8;color:#3a5147;border-radius:6px;background:#f4f5eb;padding:.38rem .58rem;cursor:pointer}
.media-filter button[aria-pressed=true]{background:#176353;border-color:#176353;color:white}
.source-section{background:#e7e9dd;border-block:1px solid #bec8b8;padding:clamp(32px,6vw,80px) 0}
.art-layout{display:none;margin:.2rem 0 .5rem;background:#f3f5ee;color:#176353;border:1px solid #bacdbb;border-radius:5px;padding:.32rem .55rem;font-size:.8rem;cursor:pointer}
.source-lesson:only-child{grid-column:1/-1}.source-lesson p{max-width:94ch}
.source-method{max-width:92ch;color:#56675c;line-height:1.8;font-size:.9rem;margin:1rem 0 1.5rem}
.source-group{margin:1.3rem 0 2rem}.source-group-heading{border-bottom:2px solid #94ad9c;padding:.55rem 0;margin-bottom:.8rem}
.source-group-heading h3{font-size:1.08rem;margin:.3rem 0}.source-group-heading span{font-size:.8rem;color:#176353;font-weight:750}
.source-lessons{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem}
.source-lesson{background:#f9f9ef;border:1px solid #c6cdbd;border-radius:8px;padding:1rem;min-width:0;scroll-margin-top:12px}
.source-time{display:flex;align-items:center;flex-wrap:wrap;gap:.5rem;font-size:.8rem;color:#176353}
.source-time strong{background:#133b33;color:white;border-radius:5px;padding:.3rem .55rem;font-variant-numeric:tabular-nums}
.source-lesson h4{font-size:.87rem;color:#176353;margin:.8rem 0 .2rem}.source-lesson p{font-size:.86rem;margin:0;line-height:1.7}
.source-lesson small{display:block;font-size:.72rem;color:#677367;margin-top:.7rem;line-height:1.6}
.version-summary{display:block;color:#26493c}.version-summary strong{color:#135d4a}
@media(max-width:600px){.source-lessons,.art-grid{grid-template-columns:1fr}.art-layout{display:inline-block}.art-grid.is-compact{grid-template-columns:1fr 1fr}.art-grid.is-compact figcaption{font-size:.72rem}.art-grid .card-figure figcaption{min-height:0}.media-type{font-size:.72rem}}
@media print {.media-filter,.video-marks,.video-mark{display:none!important}.source-lessons{display:block}.source-lesson{break-inside:avoid;margin:.5em 0}.study-video video{max-height:150pt}}
</style>
"""
zoom=(ROOT/'study-main'/'figure-zoom.html').read_text(encoding='utf-8-sig')
styles=re.findall(r'<style>.*?</style>',zoom,flags=re.S)
body_zoom=re.sub(r'<style>.*?</style>','',zoom,flags=re.S)
css_sources=''.join('<style>'+file.read_text(encoding='utf-8-sig')+'</style>' for file in [ROOT/'v2-web'/'demo.css',HERE/'labs.css'])
scripts=''.join('<script>'+file.read_text(encoding='utf-8-sig')+'</script>' for file in [ROOT/'v2-web'/'demo.js',HERE/'labs.js'])
html=html.replace('</head>',CSS+''.join(styles)+css_sources+'</head>')
html=html.replace('</body>',body_zoom+scripts+EVENTS+'</body>')
html=html.replace('单文件离线图鉴','单文件离线图鉴 · 2026.11.20 更新')
out=HERE/'atlas-v2-preview.html'
out.write_text(html,encoding='utf-8')
print(f'Built {len(cards)} term cards, {len(segments)} source intervals, {sum("interactive" in c["media"] for c in cards)} interactive visuals, {sum("video" in c["media"] for c in cards)} videos, {sum("imagegen" in c["media"] for c in cards)} ImageGen boards, {out.stat().st_size:,} bytes.')
