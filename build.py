"""Build the static atlas and its original timestamped notes."""
from html import escape
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def stamp(seconds):
    minutes, rest = divmod(round(seconds), 60)
    return f"{minutes:02d}:{rest:02d}"

def render_notes(groups):
    chunks = []
    for group in groups:
        title, author, link, lesson = (escape(group[k], quote=True) for k in ("title", "author", "url", "lesson"))
        chunks.append(f'<section><h2>{title}</h2><p>{author} · <a href="{link}">原视频</a></p><p>{lesson}</p>')
        for section in group["sections"]:
            chunks.append(f'<h3>{escape(section["title"])}</h3>')
            for note in section["notes"]:
                topic, term, seen, use, exercise = (escape(note[k]) for k in ("term","english","observation","use","exercise"))
                interval = stamp(note["start"]) + "–" + stamp(note["end"])
                chunks.append(f'<article><h4>{topic} <small>{term}</small></h4><p class="time">{interval}</p>'
                              f'<p>{seen}</p><p>{use}</p><p><strong>练习</strong>　{exercise}</p></article>')
        chunks.append('</section>')
    return "".join(chunks)

def main():
    subprocess.run([sys.executable, str(ROOT/"v2-main/assemble_v2.py")], check=True)
    html=(ROOT/"v2-main/atlas-v2-preview.html").read_text(encoding="utf-8")
    anchor='<a class="secondary" href="#source-practice">原片跟练</a>'
    if anchor not in html:
        raise ValueError("Source-learning navigation anchor was not found")
    html=html.replace(anchor, '<a class="secondary" href="./learning-notes.html">原片观察与练习</a>'+anchor, 1)
    (ROOT/"index.html").write_text(html,encoding="utf-8")
    notes=json.loads((ROOT/"notes.json").read_text(encoding="utf-8"))
    header=('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>原片观察与练习 · 视觉与专业术语图鉴</title><style>'
            'body{font:17px/1.65 system-ui,sans-serif;background:#eff1e7;color:#19322d;margin:0}'
            'main{max-width:58rem;margin:auto;padding:clamp(1rem,5vw,4rem)}a{color:#146859}section{margin:3rem 0}'
            'h1{font-size:clamp(2rem,7vw,4rem)}article{padding:1rem;background:#fbfbf3;margin:.5rem 0;border:1px solid #d1dacc;border-radius:.6rem}'
            'h4,.time{margin:0}.time,small{color:#40675a}p{margin:.5rem 0}</style><main>'
            '<a href="./index.html">← 返回图鉴</a><h1>原片观察与练习</h1>'
            '<p>按时间码回到创作者的原片。这里收录术语、画面观察和原创练习。</p>')
    (ROOT/"learning-notes.html").write_text(header+render_notes(notes)+"</main></html>",encoding="utf-8")

if __name__=="__main__":
    main()
