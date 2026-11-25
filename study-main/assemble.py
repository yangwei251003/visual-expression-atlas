from pathlib import Path
from html import escape as h
import base64
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
GROUPS={'web':'网页与三维交互','story':'视频、漫画与演示','engineering':'电气、工控与硬件','data':'数据与知识可视化','workflow':'AI 协作与工程交付'}
cards=[]
def add(group,key,asset,name,english,look,use,distinction,prompt,sources,keywords=''):
    cards.append(dict(group=group,key=key,asset=asset,name=name,english=english,look=look,use=use,
                      distinction=distinction,prompt=prompt,sources=sources,keywords=keywords))

add('web','scroll','main/scroll','滚动驱动与滚动触发','Scroll-driven · Scroll-triggered',
    '停在同一位置时，上排保持 60%，下排已自行播完。回滚后上排回到 30%。图中下排采用一次触发并保留结果的设定。',
    '逐帧展示、阅读进度、工位拆解需要用户控制进度。章节标题入场可以在进入视口时播放一次。',
    '滚动驱动由滚动位置决定进度。滚动触发用位置决定何时启动，再由时间推进。',
    '把展示区的滚动位置 0–100% 对应到动画进度。停滚停帧，回滚倒放。对照版在进入视口后用 300 毫秒播完一次。提供一个静态代表状态。',
    [('Bramus / Chrome for Developers《CSS scroll-triggered animations are coming!》','https://developer.chrome.com/blog/scroll-triggered-animations','原页实读，核对驱动与阈值触发两种案例'),
     ('Bramus《Reading Progress Indicator》','https://scroll-driven-animations.style/demos/progress-bar/css/','实测滚到 50% 再回 25%，条长跟随回退'),
     ('bili_16723812570《一行代码没写：我指挥AI做了4个交互网页｜拆帧滚动/深度视差/鼠标追光/3D拖拽》','https://www.bilibili.com/video/BV1Du3x6HEc1/?t=32','原片抽看，00:32 起看拆帧滚动，00:56 起看深度视差')],
    '滚动逐帧 scrub scrolling 触发器 入场 视差 parallax')

add('web','easing','main/easing','缓动与缓出','Easing · Ease-out',
    '两版都在 220 毫秒到同一终点。110 毫秒时，匀速只走一半，示例的三次缓出已走约八成八。',
    '让面板显得响应快、到位稳。改曲线时保持距离和时长一致，能较容易看出节奏差异。',
    '缓动分配单个动作途中的速度。时长决定总用时，错峰决定多元素各自什么时候开始。',
    '同一张卡片上移 12 像素，A 匀速、B 先快后慢，总时长都为 220 毫秒。给重播并并排比较中点，两个版本都别越过终点。',
    [('Easings.net《缓动函数速查表》中文版','https://easings.net/zh-cn','悬停实测 easeInCubic、easeOutCubic、easeOutBack'),
     ('Emil Kowalski《Great Animations》','https://emilkowal.ski/ui/great-animations','原页实读，核对速度、目的与弹簧参数')],
    '缓入 过冲 linear ease-in spring stagger')

add('web','shared','main/shared','共享元素转场','Shared element transition',
    '盯住蓝色封面。它从列表里的小图移到详情页头部并放大，内容文字随后才出现。',
    '在卡片展开、章节封面进入内容页时保留空间线索，让读者知道新出现的内容来自哪里。',
    '交叉淡化通过两层透明度完成交接。共享元素转场让同一视觉对象的位置与尺寸连续变化。',
    '点击封面后让同一张图片从卡片位置连续移到详情页头部并放大。文字在封面接近到位时进入。关闭时回到原卡片，保留轻量淡化模式。',
    [('Chrome for Developers《Same-document view transitions for single-page applications》','https://developer.chrome.com/docs/web-platform/view-transitions/same-document','原页实读，核对 view-transition-name 与独立元素过渡'),
     ('Emil Kowalski《Animation Vocabulary》','https://animations.dev/vocabulary','实读 Transitions Between States 分类')],
    'crossfade 容器转换 layout continuity view-transition-name')

add('web','hotspot','main/hotspot','三维热点与标注','3D hotspot · Annotation',
    '选中 02 后，说明框与端子锚点关联。想象旋转模型时，标记仍指向这个端子。',
    '设备、机械和教学模型可按部件引导探索，从一个总览逐步展开名称、作用和可执行操作。',
    '热点是与部件位置对应的交互目标。标注是读者看到的名称或解释，可通过热点和同等可操作的列表进入。',
    '为模型的三处可操作部件各设一个绑定表面的锚点。选中时高亮对应部件并展开简短说明。旋转视图后仍对准同一部件，键盘可通过部件列表获得同一结果。',
    [('<model-viewer> 项目《Annotations》','https://modelviewer.dev/examples/annotations/','原页实读，核对热点定位、法向与标注示例')],
    'glb 标签 3d model viewer 锚点 产品展示 exploded view')

add('story','jcut','design/j-cut-l-cut','音画错位剪接','J-cut · L-cut',
    '对照画面轨和声音轨的切点。J-cut 先听到 B；L-cut 先看到 B，A 的声音还在继续。',
    'J-cut 提前引入下一个空间或话题。L-cut 保持一句旁白的连贯，并提前给观众下一画面。',
    '普通同步切换的音画切点重合。J 与 L 的判据是新声音和新画面谁先到。',
    '用两段录屏做音画对照。A 版下一段声音提前 0.4 秒进入，B 版上一段的声音延续 0.4 秒。标出音轨和画面的切点，听审每次转场的语言是否完整。',
    [('Adobe Premiere《Create J and L cuts in Premiere Pro》','https://helpx.adobe.com/premiere/desktop/edit-projects/trim-clips/perform-j-cuts-and-l-cuts.html','原页实读，核对声音先进入与声音延续的操作')],
    '剪辑 声音桥 audio editing L剪 J剪 剪映 音频')

add('story','panels','design/comic-panel-gutter','漫画分格与格间补全','Panel · Gutter · Closure',
    '两格省去了触点闭合，三格保留这一关键中间状态。对照你能否复述灯为什么亮。',
    '把概念拆成读者能相互连接的动作。讲原理时给因果转折留一格，重复动作可以由读者补全。',
    '格间是两格之间的间隙。补全是读者根据前后格推知省去动作的过程。',
    '把一个实验画成三格。第一格给动作或问题，第二格画出导致结果的中间状态，第三格给结果。每格都用一个动作或图元支撑理解，少用解释性长句。',
    [('Scott McCloud《Understanding Comics》','https://scottmccloud.com/2-print/1-uc/index.html','实读作者章节导览与 Closure 释义')],
    '知识漫画 分镜 序列 故事 storyboard 前因 后果')

add('story','hierarchy','design/slide-hierarchy','视觉层级与留白','Visual hierarchy · Whitespace',
    '页内信息相同。左边多处争抢视线，右边先给节省时长，再展示两项对比证据。',
    '让答辩观众先抓住结论，再检查它由什么支撑。也适合宣传海报和作品集页。',
    '层级安排先看什么。留白把信息分组，并给主要内容腾出阅读空间。',
    '将这一页重做为一个结论和两条证据。结论置于主阅读路径，证据共享字号、间距和对齐轴。展示三秒后请读者复述结论，检查视线是否被装饰分散。',
    [('Ryan Orcutt / Duarte《Techniques for using critique language for more powerful and effective presentations》','https://www.duarte.com/blog/techniques-for-using-critique-language-for-more-powerful-and-effective-presentations/','实读 Contrast、Whitespace、Hierarchy 与三秒检验')],
    'PPT 汇报 职业规划 路演 排版 网格 字号 版式 contrast')

add('engineering','hmi','engineering/hmi-overview-faceplate','工艺总览与设备面板','Overview · Faceplate',
    '先在工艺流程中定位有高温提示的泵，再到设备面板读取状态和 85 °C。',
    '总览负责工艺导航和异常定位。把设备状态、诊断和操作编成可复用面板，可让多台设备共用一致的结构。',
    '设备详情是某个实例的页面。Faceplate 的另一个关键是模板复用，通过绑定让多台设备显示各自数据。',
    '设计一张工艺总览和一块可复用的泵面板。总览只显示区段、设备名和关键状态。选中泵后读温度、单位、状态与允许的操作。异常用颜色和文字共同表达。',
    [('Siemens《HMI Template Suite (WinCC Unified)》','https://cache.industry.siemens.com/dl/files/767/91174767/att_1293894/v2/91174767_HMITemplateSuiteUnified_V5.0_DOC_en.pdf#page=27','实看第 27、40 页布局和趋势/仪表配图。示例属于 WinCC Unified'),
     ('Siemens《Basics of faceplates (RT Unified)》','https://docs.tia.siemens.cloud/r/en-us/v20/configuring-screens-rt-unified/configuring-faceplates-rt-unified/basics-rt-unified/basics-of-faceplates-rt-unified','原页实读，核对可复用模板')],
    'WinCC HMI Siemens 博途 工控 人机界面 泵 SCADA PID')

add('engineering','alarm','engineering/alarm-event-log','报警与事件记录','Alarm · Event log',
    '左边显示报警已被确认但数值仍超限。右边按时间记录发生、确认和操作。',
    '让操作者快速回答哪里异常、谁已处理、设备是否恢复。复盘时可回查相关操作。',
    '报警确认记录知悉。报警恢复反映过程条件回到设定范围。事件历史保留动作时序。',
    '为一个示例超温信号画当前报警和事件历史两栏，把发生、确认、恢复写成三个可辨状态。模拟确认后温度仍高的情形，保持异常可见并追加操作记录。',
    [('Siemens《Basics of alarm logging》','https://docs.tia.siemens.cloud/r/en-us/v21/configuring-alarms-rt-unified/logging-alarms-rt-unified/basics-of-alarm-logging-rt-unified','原页实读，核对报警记录'),
     ('Siemens《Audit》','https://docs.tia.siemens.cloud/r/en-us/v20/readme-wincc-unified/audit','原页实读，核对操作审计用途')],
    '报警记录 确认 acknowledge 历史 温度 HMI 趋势')

add('engineering','ladder','engineering/ladder-contact-coil','梯形图的梯级、触点与线圈','Ladder logic · Rung · Contact · Coil',
    '上下图只改变 Sensor。沿这一梯级查看条件路径和 Lamp 的位值怎样变化。',
    '把操作者看到的输入、内部条件和输出联系起来。训练时逐一切换输入，可以追到哪一步使输出停止。',
    '触点读条件，线圈写入或驱动对应的逻辑位。图里的绿色标识说明监视状态，具体配色与软件有关。',
    '用一个传感器位控制一个示例指示灯。并排画输入为 0 和 1 的梯形图监视状态，注明地址、输入位和输出位，图旁解释单一变量怎样改变输出。',
    [('Redouane Ait Ali Yahia / SolisPLC《An Introduction to Basic Ladder Logic Instructions in Siemens Tia Portal》','https://www.solisplc.com/tutorials/siemens-tia-portal-programming-example-basic-ladder-logic-instructions','实读原文和梯形图示例')],
    'PLC TIA Portal PLCSIM 博途 梯级 网络 常开 自锁 输入输出')

add('engineering','eda','engineering/eda-symbol-footprint-trace','符号、封装、网络与走线','Symbol · Footprint · Net · Trace',
    '在两张图里找同样的 R1 与 TP1。左侧显示电气关系，右侧可看到实际焊盘与铜走线。',
    '在逻辑图与板图间核对器件身份、连接和布局。检查封装时可继续核对引脚编号、间距和方向。',
    '网络是一组应相连的节点。走线是 PCB 上实现连接的铜路径。封装描述落在板上的焊盘与外形。',
    '取同一组电阻、测试点和网络做原理图与板图的对照。两侧共享器件位号和网络名。标出符号的引脚、封装的焊盘、铜走线和测试点，给出检查顺序。',
    [('嘉立创EDA《专业版快速入门》','https://prodocs.lceda.cn/cn/quick-start.html','原页实读，核对原理图到 PCB 的流程'),
     ('嘉立创EDA《PCB设计03-PCB走线》','https://www.bilibili.com/video/BV1eL4y1T7iq/?t=220','已看官方预览关键帧。02:00 看 USB1 封装焊盘，03:40 看红色铜走线引出。未验证连播与音轨')],
    'PCB Proteus Arduino 嘉立创 EDA 封装 焊盘 过孔 via DRC')


add('engineering','cad','engineering/cad-orthographic-isometric','三视图与等轴测视图','Principal orthographic views · Isometric view',
    '沿琥珀色的台阶边，对照左边的主视、俯视和右视，再去右边找同一条空间转折。图左采用第三角法布置。',
    '三视图便于沿投影方向对应轮廓和布置尺寸。等轴测图帮助对方快速看懂台阶、深度等空间形状。',
    '等轴测也属于广义的正投影。这里比较的是沿主轴看的三张视图与一张同时呈现三个方向的轴测图。',
    '用同一个带台阶的零件做主视、俯视、右视与等轴测图。前三个采用同一比例并按指定投影法对齐。用同一颜色标出对应的台阶边，标注尺寸时放在形状表达最清楚的一面。',
    [('Autodesk《About Projected Views》','https://help.autodesk.com/view/ACD/2026/ENU/?caas=caas%2Fdocumentation%2FCIV3D%2F2014%2FENU%2FfilesACD%2FGUID-1317AAB6-6A6D-4B11-8AAE-471C461FB8C5-htm.html','实读基准、投影视图和对齐关系'),
     ('Autodesk《To Create a Projected View》','https://help.autodesk.com/cloudhelp/2027/ENG/AutoCAD-Core/files/GUID-01FCFC23-D754-4070-879A-734CEEDEAA18.htm','原厂操作步骤')],
    'CAD AutoCAD FreeCAD 工程制图 正投影 正交投影 三视图 主视 俯视 右视 等轴测')

add('data','signaling','design/signaling','视觉提示与讲解同步','Signaling · Cueing',
    '右图把时间位置、曲线上的对应点和读数同时标亮。跟着这一时刻看图即可定位信息。',
    '适合解说曲线、公式、流程和仿真。让刚听到的解释和眼前的证据发生在同一时刻。',
    '装饰可以丰富画面。视觉提示有明确指向，观众看完应能指出它对应的变量、步骤或因果。',
    '讲到第 4 秒时，同时标亮横轴上的第 4 秒、曲线交点和对应位移。其余标注保留低对比，语句结束后恢复。让读者暂停后能从画面复述对应关系。',
    [('Grant Sanderson / 3Blue1Brown《The paradox of the derivative》','https://www.3blue1brown.com/lessons/derivatives/#car-moving','实读 Car Moving 图解，核对按时刻读距离与斜率'),
     ('3Blue1Brown《【官方双语】微积分的本质 - 02 - 导数的悖论》','https://www.bilibili.com/video/BV1Lx411m7Vj/?t=70','原片抽看 1:10、1:30、1:45，虚线把时间、曲线点与已跑路程联系起来')],
    '教学动画 对齐 引导注意 读图 语音 同步 曲线 可视化')

add('data','chart','main/charts','按问题选择图表','Bar chart · Line chart · Scatterplot',
    '同一种简洁画风可以回答三类问题。对照条的长度、随时间连接的线、没有强制顺序的点云。',
    '让读者按任务读数据。条形图用于横向比较，折线图用于时序趋势，散点图用于比较两项连续变量之间的关系。',
    '类别之间没有自然顺序时，连线容易暗示不存在的先后。散点相关性也需要结合数据和上下文解释。',
    '先写图表要回答的一句话，再选可视编码。对于温度随时间的变化用折线，对于不同设备的最高温比较用条形，对于功率与温升用散点。统一单位并标明异常点。',
    [('Financial Times《Visual Vocabulary》','https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md','实读排名、变化、相关三类'),
     ('Severino Ribecca《The Data Visualisation Catalogue》','https://datavizcatalogue.com/ZH/','实读中文版目录和散点图原页')],
    '图表 排名 趋势 连续变量 相关 scatterplot chart KPI data visualization')

add('workflow','review','main/review','改动差异与验收','Diff · Checks · Acceptance criteria',
    '左边是文案究竟变了什么。右边把输入保留、清空恢复、窄屏文字分成三项可复查的结果。',
    '用 AI 写网页、改脚本或交素材时，复核范围和实际效果，减少在下一轮才发现问题。',
    '差异解释改动内容。检查记录解释运行结果。验收条件先说清什么观察结果算完成。',
    '先定义三个用户可观察的通过条件。完成后给改动前后差异、真实入口的操作结果，以及仍未验证的条件。用同样的输入分别展示修改前后。',
    [('GitHub Docs《Reviewing your proposed changes》','https://docs.github.com/en/get-started/start-your-journey/reviewing-your-proposed-changes','实读 Files changed 和 review 工作流'),
     ('GitHub Docs《About pull requests》','https://docs.github.com/en/pull-requests/get-started/about-pull-requests','实读差异、审核与状态检查的入口')],
    'AI 编程 Agent 自动化 复核 PR 回归 Git GitHub Vibe Coding 测试')

PROFILE = '''
<p><strong>从你做过的作品出发。</strong> 11 月 18 日的电气可视化项目有交互代码、提交和多端验证记录。11 月 6 日的知识可视化样本里能看到成组漫画、讲解视频、旁白与时间码。另一批产出包括职业展示 PPT、宣传物料、PLC 测试工程与 Proteus 仿真项目。</p>
<p>最强的共性是把抽象过程做成能操作、能复述的体验。优先学网页交互、教学叙事、工业界面与图表，其次补电路表达、汇报排版和 AI 交付复核。素材库抽样约有 5.5 GB 的 MP4 和 1.4 GB 的 WAV，包含原料、不同版本和成品，因此数量只用来判断资料类型。</p>
<details><summary>这些判断来自哪些记录</summary><p>以选定项目的 README、提交日期、验证和渲染记录、导出文件为主，另核对本机安装项。Windows 最近文件目录未提供可用记录，这是一份近期项目画像。图中统一采用自绘例子和假设数据。</p>
<ul>
<li><strong>网页与数据表达。</strong> 电气工位支持操作热点、曲线和事件。知识平台和算法体验项目都使用改条件、看结果的设计。</li>
<li><strong>讲述与展示。</strong> 漫画有逐格阅读的编排，视频有旁白、时间轴和分轨产物。职业展示和宣传资料还留有 PPT 与印刷版。</li>
<li><strong>工程与交付。</strong> 电气方向有博途测试工程、Proteus 仿真、Arduino 源文件与 DWG、DXF、FCStd 制图样本。技能工具的交付样本有验证记录。</li>
<li><strong>软件能力背景。</strong> 剪映、Photoshop、Blender、OBS、KiCad 等可用。仅凭安装项无法推断使用频率。</li>
</ul></details>
'''

ROUTE = '''
<ol>
<li><strong>第一轮，网页与教学 · 25 分钟。</strong> 看滚动对照和缓动图。同一模块只改一个变量，写明哪种变化在帮助理解。将视觉提示用于一幅曲线或一张实验图。</li>
<li><strong>第二轮，工控与图表 · 30 分钟。</strong> 选一个虚拟设备，画「位置 → 条件 → 输出 → 报警」。请读者只看图回答设备怎样了、原因在哪、下一步看什么。</li>
<li><strong>第三轮，讲述与复核 · 30 分钟。</strong> 同一内容分别做三格漫画、一页展示和 15 秒音画剪接。每版请一位读者复述，再用截图或录屏记录哪处最容易误解。</li>
</ol>
<p><strong>下次遇到新效果。</strong> 收藏原链接与时间点，补一张对照图、一对中英文名、一句用途和一个验收动作。这样积累的卡片更容易迁移到下一次创作。</p>
<p>原片抽看记录了代表画面与建议时间点。原页实读记录了正文或图例。交互实测记录了触发后的可观察结果。</p>
'''


DEMOS = {
'scroll': '''<details class="atlas-demo"><summary>动手对照两种时间轴</summary>
<section aria-label="滚动对照">
<p>滑杆代替滚动位置。拖过 50%，停手再往回拖。</p>
<label for="scroll-position">模拟滚动位置</label><input id="scroll-position" type="range" min="0" max="100" value="0">
<div class="sample-row"><span>驱动</span><progress id="linked-progress" aria-label="滚动驱动进度" max="100" value="0"></progress><span id="linked-value">0%</span></div>
<div class="sample-row"><span>一次触发</span><progress id="triggered-progress" class="triggered" aria-label="触发动画进度" max="100" value="0"></progress><span id="triggered-value">0%</span></div>
<button id="demo-reset" type="button">重置对照</button></section></details>''',
'easing': '''<details class="atlas-demo"><summary>播放缓动对照</summary>
<section aria-label="缓动对照"><p>慢放至 800 毫秒。看两个点多久到达中间位置。</p>
<div class="sample-row"><span>匀速</span><div class="runway"><i class="mark alt" aria-hidden="true"></i></div></div>
<div class="sample-row"><span>缓出</span><div class="runway"><i class="mark" aria-hidden="true"></i></div></div>
<button id="demo-easing-play" type="button">播放一次</button></section></details>''',
}

def img_data(asset):
    category,file=asset.split('/')
    imagepath=ROOT/('study-'+category)/(file+'.png')
    with Image.open(imagepath) as image:
        width,height=image.size
        image.verify()
    payload=base64.b64encode(imagepath.read_bytes()).decode('ascii')
    return ('data:image/png;base64,'+payload,width,height)

def render_card(c,i):
    data,w,ht=img_data(c['asset'])
    sourceitems=''.join(f'<li><a href="{h(url,quote=True)}" target="_blank" rel="noopener noreferrer">{h(title)}</a><br><span>{h(note)}</span></li>' for title,url,note in c['sources'])
    keywords=' '.join([c['name'],c['english'],c['keywords'],GROUPS[c['group']]])
    return f"""<article id="term-{c['key']}" class="knowledge-card" data-category="{c['group']}" data-keywords="{h(keywords,quote=True)}" aria-labelledby="title-{c['key']}">
<div class="card-body card-heading"><span class="card-index">{i:02d} / {GROUPS[c['group']]}</span>
<h3 id="title-{c['key']}">{h(c['name'])}</h3><p class="english" lang="en">{h(c['english'])}</p></div>
<figure class="card-figure"><img src="{data}" alt="{h(c['look'],quote=True)}" width="{w}" height="{ht}" loading="lazy"><figcaption><span>{h(c['look'])}</span><button class="figure-zoom" type="button" data-figure-zoom>查看大图</button></figcaption></figure>
<div class="card-body">
<dl class="card-facts"><div><dt>作用</dt><dd>{h(c['use'])}</dd></div><div><dt>辨析</dt><dd>{h(c['distinction'])}</dd></div></dl>
{DEMOS.get(c['key'],'')}
<details class="prompt"><summary>中文提示词</summary><blockquote>{h(c['prompt'])}</blockquote></details>
<div class="card-sources" aria-label="原始资料"><strong>原始资料与学习记录</strong><ul>{sourceitems}</ul></div>
<button type="button" class="copy-prompt" data-prompt="{h(c['prompt'],quote=True)}">复制提示词</button>
</div></article>"""

EXTRA = '''
<style>
.card-body.card-heading {flex:0 0 auto;gap:.28rem;}
.card-heading h3 {margin:0;line-height:1.24}
.card-body .card-sources ul {margin:.35rem 0 0;padding-inline-start:1.2em;}
.card-sources li + li {margin-top:.34rem}
.card-sources a {color:#176353}
.card-body .prompt blockquote {margin-top:.42rem;}
.profile details summary {cursor:pointer}
@media (max-width: 520px) {.card-body.card-heading {min-height:0}}
</style>
'''
out=ROOT/'视觉与专业术语图鉴.html'
html=(ROOT/'study-shell'/'shell.html').read_text(encoding='utf-8-sig')
replacements={'PROFILE':PROFILE, 'CARDS':'\n'.join(render_card(c,i) for i,c in enumerate(cards,1)), 'ROUTE':ROUTE, 'TOTAL':str(len(cards))}
for key,val in replacements.items():
    marker=f'<!--{key}-->'
    assert html.count(marker)>=1, marker
    html=html.replace(marker,val)
html=html.replace('</head>',EXTRA+'</head>')
enhancements=''.join((ROOT/'study-main'/file).read_text(encoding='utf-8-sig') for file in ('demos.html','figure-zoom.html'))
import re
styles=''.join(re.findall(r'<style>.*?</style>',enhancements,flags=re.S))
html=html.replace('</head>',styles+'</head>')
html=html.replace('</body>',re.sub(r'<style>.*?</style>','',enhancements,flags=re.S)+'</body>')
out.write_text(html,encoding='utf-8')
print(f'Built {len(cards)} cards, {sum(len(c["sources"]) for c in cards)} source entries, {out.stat().st_size} bytes.')
