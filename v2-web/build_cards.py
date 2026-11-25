from pathlib import Path
import json, html

ROOT = Path(__file__).parent

def esc(text): return html.escape(text, quote=True)

def source(title, url, note):
    return {'title':title, 'url':url, 'note':note}

def scene(a,b,title,desc):
    return {'name': a,'en':b,'content':title,'meter':desc}

def render_card(key,effect,scenes,duration,caption,action=None):
    panes = []
    for scene in scenes:
        panes.append(f'''
        <section class="mv-pane">
          <div class="mv-label"><b>{esc(scene["name"])}</b><span lang="en">{esc(scene["en"])}</span></div>
          <div class="mv-stage">{scene["content"]}</div>
          <div class="mv-meter">{esc(scene["meter"])}</div>
        </section>''')
    action_button = f'<button type="button" class="mv-action">{esc(action)}</button>' if action else ''
    return f'''
    <div id="demo-v2-{esc(key)}" class="motion-v2" data-motion="{esc(effect)}" data-duration="{duration}" role="group" aria-label="{esc('效果对照，可控播放器')}">
      <p class="mv-kicker">同一进度 · 左右对照</p>
      <div class="mv-compare">{''.join(panes)}</div>
      <div class="mv-controls">
        <button type="button" data-mv-action="play">播放</button>
        <button type="button" data-mv-action="pause" disabled>暂停</button>
        <button type="button" data-mv-action="reset">回到起点</button>
        {action_button}
        <label class="mv-scrubber"><span>进度</span>
          <input class="mv-range" type="range" min="0" max="1000" value="350" aria-label="两种效果的同步进度">
          <output class="mv-output">35%</output>
        </label>
      </div>
      <p class="mv-caption">{esc(caption)}</p>
    </div>'''.strip()

vocabulary = lambda note: source('Emil Kowalski · Animation Vocabulary', 'https://animations.dev/vocabulary', note)
motion = lambda note: source('Motion · Transitions', 'https://motion.dev/docs/react-transitions', note)
cards = []

def add(key, name, english, look, use, distinction, scenario, prompt, sources, effect, scenes, duration, caption, action=None, replace=None):
    card = {
        'key':key,'category':'web','name':name,'english':english,'look':look,
        'use':use,'distinction':distinction,'scenario':scenario,'prompt':prompt,
        'sources':sources,'demoHtml':render_card(key,effect,scenes,duration,caption,action)
    }
    if replace: card['replaceKey']=replace
    cards.append(card)

reveal = '''<div class="mv-reveal-frame"><div class="mv-reveal-inner"><div class="mv-screen-art"></div><div class="mv-reveal-text">NORTH / 01</div></div><i class="mv-cut" aria-hidden="true"></i></div>'''
add('mask-vs-fade','遮罩揭示与淡入','Mask Reveal · Fade-in',
    '拖到中段，左边山景逐段露出，遮罩边缘不断向右推进，露出的内容仍然清晰。右边整张山景同时变亮。',
    '利用露出边缘引导阅读路径，建立进入画面的方向感。淡入可以柔和地显现整组元素，降低突然出现的刺激。',
    '本例用动画化裁剪边界实现 Reveal。Fade-in 改的是不透明度。两者可以组合，但最好明确主次。',
    '遮罩揭示适合作品集封面、章节标题、图片轮播开场。淡入适合辅助文字、详情状态和需要轻量出现的内容。',
    '同一张封面做两种1800ms对照，A用从左到右的裁剪遮罩逐段露出，露出的内容保持100%不透明度，B保持形状不变而整体淡入。两边共用一条时间轴，提供重播、暂停和拖动进度。减少动态偏好生效时保持清晰的最终状态。',
    [vocabulary('已读 Entrances & Exits，核对 Reveal 和 Fade in 的原定义。'),
     source('MDN · clip-path', 'https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/clip-path','已读属性正文、示例与可见区域定义。原作者示例可切换不同裁剪路径。')],
    'reveal',[scene('遮罩揭示','Mask reveal',reveal,'已露出面积'),scene('淡入','Fade-in',reveal,'整张素材透明度')],1800,
    '看中间帧的边界与亮度。首次播放从起点开始，暂停时拖动进度可逐帧观察。')

items=''.join(f'<div class="mv-list-item"><i>{i}</i><span>{label}<em>{en}</em></span></div>' for i,label,en in [
    ('01','输入状态','INPUT'),('02','逻辑判断','LOGIC'),('03','设备反馈','OUTPUT'),('04','运行记录','EVENT')])
stack='<div class="mv-list">'+items+'</div>'
add('stagger-vs-together','交错入场与同时入场','Stagger · Simultaneous',
    '中途暂停时，左边四条状态卡依阅读顺序逐条出现，右边四条在同一时刻启动并完成。',
    '在有明确顺序的信息组内制造阅读节奏，让用户从上到下追随变化。逐项时差也可以突出关键流程。',
    'Stagger 的差异来自启动时间偏移。本例两侧单项位移、单项时长和缓动完全一致，只有错峰改变。',
    '适合首页功能条目、分步骤教程、菜单首次打开等。紧急报警或高频操作列表要优先及时呈现。',
    '设置四张状态卡，每项从下移14px且透明度0进入到原位且100%不透明，时长480ms，缓出。A按顺序每项相差135ms启动，B四项同时启动，统一1000ms对照时间轴。在首次进入时执行一次，避免滚动往返重复触发。',
    [vocabulary('已读 Sequencing & Timing 中的 Stagger、Delay、Duration。'),motion('已读 Orchestration 和 transitions 章节，核对 stagger 参数作为子项启动偏移。')],
    'stagger',[scene('交错入场','Stagger',stack,'依序启动'),scene('同时入场','Together',stack,'同一时刻启动')],1000,
    '让进度停在 30–60%，对比哪些条目已经到位。');

track='<div class="mv-track"><div class="mv-goal"><span>目标线</span></div></div><span class="mv-ball"></span><div class="mv-track-label"><span>起点</span><span>移动轨迹</span></div>'
add('spring-vs-easeout','弹簧回弹与固定缓出','Spring · Ease-out Tween',
    '相同起终点，两者都先加速或快速前进再停下。示例的欠阻尼弹簧会越过目标线并来回收敛，三次缓出始终未越过终点。',
    '弹簧能让短小反馈产生重量与回弹感。确定性的缓出适合需要明确到位时间和稳定感觉的状态变换。',
    'Spring 可以由质量、刚度、阻尼控制，其结果不一定回弹。图中专门选择有轻微过冲的欠阻尼配置。Tween 则依据既定时长及时间曲线插值。',
    '弹簧适合低风险的点赞、收藏、可拖动卡片回位、趣味按钮。弹窗文字和工业状态变化一般更适合快速、少过冲的曲线。',
    '演示一个对象从12%移动到78%。A用欠阻尼弹簧响应，轻微越过目标线后衰减稳定，B用三次缓出单调到位。为同一终点增加目标线和位移百分比，能暂停观察过冲，并提供减少动态版本。',
    [source('Emil Kowalski · Great Animations','https://emilkowal.ski/ui/great-animations','已读自然动效与快速动效讲解。原页有可调 stiffness / damping / mass 的弹簧可视化、Replay 和缓出示例。'),motion('已读 Spring、Tween 等类型参数，对照弹簧的物理参数与固定时间插值。')],
    'spring',[scene('欠阻尼弹簧','Spring',track,'朝终点移动'),scene('固定缓出','Ease-out',track,'朝终点移动')],1650,
    '暂停在目标线附近，观察哪一个对象曾越过终点。这个演示特意慢放以便辨认。')

land='<div class="mv-scenery"><div class="mv-layer mv-far"></div><div class="mv-layer mv-mid"></div><div class="mv-layer mv-near"></div><i class="mv-horizon"></i><div class="mv-scroll-tick"><i></i></div></div>'
add('parallax-vs-uniform','多层视差与同速滚动','Parallax · Uniform Scroll',
    '滑杆模拟滚动位置。左边近处山脊移动得更多，中景其次，背景与月亮移动得最少。右边三层一起移动。',
    '不同深度图层产生相对位移，赋予二维页面空间感。轻微视差还可以引导用户由前景看向远景。',
    '滚动跟随是动画随滚动进度变化的关系。视差强调多个深度层的相对运动速度不同。同速滚动仍可由滚动驱动，但不会制造该相对位移。',
    '适合叙事网站、旅游或品牌首页、展厅景深、机械结构分层探索。要减小幅度并防止遮住文本，避免高频操作界面持续晃动。',
    '把画面前景、中景、远景拆成三个可见图层，滑杆0%到100%映射同一滚动位置。左侧分别上移62px、30px、12px，右侧统一上移34px。停止拖动时各层停在当前状态，回拖时逆向恢复。保持正文固定可读。',
    [source('Bramus · Scroll-driven Animations','https://scroll-driven-animations.style/','已读引言与公开演示目录，核对 parallax background images 和随滚动进度正向／逆向推进的关系。'),
     source('Bramus · Chrome for Developers · 滚动驱动的动画','https://developer.chrome.com/docs/css-ui/scroll-driven-animations?hl=zh-cn','已读滚动时间轴的说明与示例，适合从这里研究 scroll() 与 view()。')],
    'parallax',[scene('多层视差','Parallax',land,'远 / 中 / 近'),scene('同速滚动','Uniform',land,'远 / 中 / 近')],2400,
    '拖影像的进度滑杆向右再回拖，观察每层相对位置变化。这是滚动位置模拟，不抢占当前网页滚动。')

spot='''<div class="mv-pointer-zone" tabindex="0" aria-label="在区域移动指针或按方向键"><div class="mv-pointer-grid"></div><div class="mv-pointer-card"><span class="mv-pointer-glow"></span><span class="mv-icon" aria-hidden="true">✦</span><b>作品入口</b></div><i class="mv-pointer-dot"></i></div>'''
mag='''<div class="mv-pointer-zone" tabindex="0" aria-label="在区域移动指针或按方向键"><div class="mv-magnet-anchor"></div><div class="mv-magnet">作品入口</div><i class="mv-pointer-dot"></i></div>'''
add('spotlight-vs-magnet','鼠标追光与磁吸按钮','Pointer Spotlight · Magnetic Button',
    '白色小圆表示同步指针。左边亮斑追随它而卡片位置固定，右边的按钮实体沿指针方向偏移，虚线表示原位。',
    '追光在内容内部制造局部焦点和材质质感，保留界面结构。磁吸强调控件对靠近的指针有反应，给人轻微的物理拉力感觉。',
    'Spotlight 变的是光斑位置和明暗，Magnetic 改的是对象位置。两者在代码中常使用同一个鼠标坐标来源，却是不同的设计决策。',
    '适合作品集封面、低频品牌 CTA、精选功能卡片。主导航与频繁使用的输入表单宜保持目标稳定，触屏与键盘需要仍可正常操作。',
    '给两块等大的区域同步模拟指针位置。A仅更新光斑的 CSS radial-gradient 中心，卡片位置不变，B使按钮向指针偏移、X最多20px且Y最多17px，保留虚线原位。允许真实 pointermove、触屏点击和方向键，也提供轨迹播放及复位。',
    [source('Codrops · MagneticButtons 原作者示例仓库','https://github.com/codrops/MagneticButtons','已读公开仓库 README，作者说明是一组磁吸交互与 hover 动画按钮，包含在线 demo 入口。原文章入口本次返回403，故用原仓库学习机制。'),
     source('MDN · radial-gradient()','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/gradient/radial-gradient','已读径向渐变语法与可指定中心位置。图中的动态中心与按钮位移是本图鉴原创对照。')],
    'pointer',[scene('局部追光','Spotlight',spot,'按钮保持原位'),scene('磁吸按钮','Magnetic',mag,'按钮随指针偏移')],3200,
    '可把鼠标移入任意一侧同步比较。触屏点按区域，键盘聚焦后使用方向键也能移动白色指针。')

def layouts(fly):
    thumb = '' if fly else '<div class="mv-screen-art mv-layout-thumb"></div>'
    hero = '' if fly else '<div class="mv-screen-art mv-layout-hero"></div>'
    layer = '<div class="mv-screen-art mv-layout-fly"></div>' if fly else ''
    return f'''
      <div class="mv-layout">
        <div class="mv-layout-old"><div class="mv-mini-bar">精选作品</div><div class="mv-mini-search"></div>{thumb}<div class="mv-mini-lines mv-old-lines"><i></i><i></i><i></i></div></div>
        <div class="mv-layout-new"><div class="mv-mini-bar">‹ 作品详情</div><div class="mv-mini-search"></div>{hero}<div class="mv-mini-lines mv-new-lines"><i></i><i></i><i></i></div></div>
        {layer}
      </div>'''
add('shared-vs-crossfade','共享元素转场与交叉淡化','Shared Element · Crossfade',
    '暂停在画面中间时，左边只有一个连续移动、放大的山景封面。右边缩略图和详情图处于两个固定位置，透明度逐渐交接。',
    '用同一可追踪的视觉对象串联列表和详情，帮助用户理解空间关系。交叉淡化则提供轻量视图切换，适用于内容无共享位置或无需表达导航空间时。',
    '共享元素转场包含身份、位置或尺寸的连续性；Crossfade 通过旧的与新的两层不透明度交换完成切换。两种方法都可以搭配其他文字变化。',
    '列表到详情、作品集封面展开、设备模型预览进入详情适合共享元素。标签内容切换、无共同对象的页面切换适合交叉淡化。',
    '展示同一封面从列表缩略图进入详情页。A保持封面唯一且连续改变位置、尺寸和圆角，其余内容渐变切换。B把旧列表与新详情固定在各自位置，交叉淡化。共用同样的时长和进度控制；关闭时可反向回到原位置。',
    [vocabulary('已读 Transitions Between States：Shared element transition / Crossfade / Continuity transition。'),
     source('Chrome for Developers · Same-document view transitions','https://developer.chrome.com/docs/web-platform/view-transitions/same-document','已读 Transition multiple elements 和 Transitioning elements do not need to be the same DOM element；原页带缩略图进入主图的演示与源码。')],
    'shared',[scene('共享元素','Shared element',layouts(True),'同一元素位置/尺寸连续'),scene('交叉淡化','Crossfade',layouts(False),'旧图透明度↓，新图透明度↑')],1800,
    '点击“打开详情”从起点播放。请暂停在50%，再把进度回拖至原列表。','打开详情',replace='shared')

feedback='''<div class="mv-feedback-center"><div class="mv-fake-button"><i class="mv-ripple"></i><span>保存</span></div><span class="mv-status">等待操作</span><div class="mv-confirm-panel"><b>✓</b> 保存成功</div></div>'''
add('feedback-states','即时按压反馈与延迟反馈','Microinteraction · Press Feedback',
    '点击下方模拟保存。两边都在同一时刻收到成功结果，左边先缩小回位、扩散触点高光并显示处理中；右边在等待时按钮保持原样，直到完成才更新。',
    '将“系统收到操作”与“任务最终成功”用不同视觉状态表达，减少重复点击和不确定感。按压反馈应贴合当前操作。',
    '动作反馈表明点击已接收。处理状态表示任务未完成。成功提示必须等待真实结果，失败也应有明确路径。',
    '适合表单提交、保存、导出、快速操作确认。本例是纯演示；真实危险操作仍需遵守其确认机制与联锁，不能仅靠色彩或动画传达状态。',
    '为示例保存按钮设计空闲、已按压、处理中、成功/失败状态。点击后立即短暂缩放至94%，同时显示处理中；收到真实成功结果后切换为已保存。对照版等到相同完成时间才改变按钮。避免把触点反馈误写成结果已成功。',
    [source('Google · Material motion','https://m1.material.io/motion/material-motion.html','已读 Responsive 与 Why does motion matter，包含触点扩散、精确回应用户操作、状态层级与反馈。'), source('Emil Kowalski · Great Animations','https://emilkowal.ski/ui/great-animations','已读 Great animations are fast 和 Great animations have a purpose，核对响应速度与状态变化的用意。')],
    'feedback',[scene('即时动作反馈','Immediate',feedback,'按压、处理中与完成'),scene('延迟反馈','Delayed',feedback,'只在完成时显示结果')],2000,
    '先模拟保存，再暂停在 20–60%。两侧任务完成时间相同，比较等待期间你能知道什么。','模拟保存')

(root_json := ROOT/'cards.json').write_text(json.dumps(cards, ensure_ascii=False, indent=2),encoding='utf-8')
css=(ROOT/'demo.css').read_text(encoding='utf-8-sig')
js=(ROOT/'demo.js').read_text(encoding='utf-8-sig')
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font:16px system-ui;margin:18px auto;max-width:940px;padding:0 12px;background:#f5f2e9;color:#101a2c}section.card{margin-bottom:18px;max-width:480px;border:1px solid #b5b9ba;padding:10px}h1,h2{line-height:1.25;margin:5px 0 10px}'+css+'</style><h1>交互动效对照</h1><main>'+''.join('<section class="card"><h2>'+esc(c['name'])+'</h2>'+c['demoHtml']+'</section>' for c in cards)+'</main><script>'+js+'</script></html>'
(ROOT/'preview.html').write_text(page,encoding='utf-8')
print(f'{len(cards)} cards, {root_json.stat().st_size} bytes')
