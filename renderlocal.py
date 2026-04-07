#!/usr/bin/env python3
import argparse
import html
import os
import pathlib
import sys
import tempfile
import webbrowser
import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename, TextLexer

# --- CONFIG ---
MAX_BYTES = 150 * 1024 
IGNORE = {".git", ".venv", "node_modules", "__pycache__", ".obsidian", "dist", "build"}
BINARIES = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".tar", ".exe", ".pyc"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    args = ap.parse_args()
    root = pathlib.Path(args.path).resolve()

    if not root.exists():
        print("Error: Path not found")
        return

    print("🔍 Scanning...")
    files = []
    for p in root.rglob("*"):
        if p.is_file() and not any(x in IGNORE for x in p.parts):
            if p.suffix.lower() not in BINARIES:
                try:
                    if p.stat().st_size <= MAX_BYTES:
                        files.append(p)
                except:
                    continue

    files.sort()
    print("📝 Processing " + str(len(files)) + " files...")

    fmt = HtmlFormatter(nowrap=False)
    sections = []
    toc = []
    cxml = ["<documents>"]

    for idx, p in enumerate(files, 1):
        rel = str(p.relative_to(root)).replace(os.sep, "/")
        sid = "f" + str(idx)
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
            cxml.append('<document index="' + str(idx) + '"><source>' + rel + '</source><document_content>' + txt + '</document_content></document>')
            
            if p.suffix.lower() in {".md", ".markdown"}:
                body_content = markdown.markdown(txt, extensions=["fenced_code", "tables"])
            else:
                try: lxr = get_lexer_for_filename(rel)
                except: lxr = TextLexer()
                body_content = '<div class="highlight">' + highlight(txt, lxr, fmt) + '</div>'
            
            # Formatting the section to match Karpathy's original UI
            sec = '<section class="file-section" id="' + sid + '">'
            sec += '<h2>' + html.escape(rel) + ' <span class="muted">(' + str(round(p.stat().st_size/1024, 1)) + ' KiB)</span></h2>'
            sec += '<div class="file-body">' + body_content + '</div>'
            sec += '<div class="back-top"><a href="#top">↑ Back to top</a></div></section>'
            
            sections.append(sec)
            toc.append('<li><a href="#' + sid + '">' + html.escape(rel) + '</a></li>')
        except:
            continue

    cxml.append("</documents>")
    
    # --- GitHub/Rendergit CSS Restoration ---
    gh_css = """
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; margin: 0; padding: 0; line-height: 1.45; }
    .page { display: grid; grid-template-columns: 320px minmax(0, 1fr); gap: 0; }
    #sidebar { position: sticky; top: 0; align-self: start; height: 100vh; overflow: auto; border-right: 1px solid #eee; background: #fafbfc; }
    #sidebar .inner { padding: 0.75rem; }
    #sidebar h2 { margin: 0 0 0.5rem 0; font-size: 1rem; }
    .toc { list-style: none; padding-left: 0; margin: 0; }
    .toc li { padding: 0.15rem 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 12px; }
    .toc a { text-decoration: none; color: #0366d6; }
    main { padding: 1rem; max-width: 1100px; margin: 0 auto; width: 100%; }
    .file-section { padding: 1rem; border-top: 1px solid #eee; margin-top: 1rem; }
    .file-section h2 { font-size: 1.1rem; margin-top: 0; }
    .muted { color: #6a737d; font-weight: normal; font-size: 0.8em; }
    pre { background: #f6f8fa; padding: 16px; overflow: auto; border-radius: 6px; font-size: 85%; line-height: 1.45; }
    .back-top { font-size: 0.8rem; margin-top: 0.5rem; }
    #llm-view { display: none; }
    textarea { width: 100%; height: 70vh; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 12px; padding: 10px; border: 1px solid #ddd; }
    .view-toggle { margin-bottom: 1rem; padding: 10px; border-bottom: 1px solid #eee; position: sticky; top: 0; background: white; z-index: 10; }
    button { padding: 5px 10px; border-radius: 6px; border: 1px solid #d1d9e0; background: #fff; cursor: pointer; }
    """ + fmt.get_style_defs('.highlight')

    # --- HTML ASSEMBLY ---
    html_out = []
    html_out.append('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">')
    html_out.append('<title>' + root.name + '</title><style>' + gh_css + '</style></head><body>')
    html_out.append('<div class="page" id="top">')
    html_out.append('<nav id="sidebar"><div class="inner"><h2>' + root.name + '</h2><ul class="toc">')
    html_out.extend(toc)
    html_out.append('</ul></div></nav>')
    html_out.append('<main><div class="view-toggle">')
    html_out.append('<button onclick="document.getElementById(\'h\').style.display=\'block\';document.getElementById(\'l\').style.display=\'none\'">👤 Human View</button> ')
    html_out.append('<button onclick="document.getElementById(\'h\').style.display=\'none\';document.getElementById(\'l\').style.display=\'block\'">🤖 LLM View</button>')
    html_out.append('</div><div id="h">')
    html_out.extend(sections)
    html_out.append('</div><div id="l"><textarea readonly>')
    html_out.append(html.escape("".join(cxml)))
    html_out.append('</textarea></div></main></div></body></html>')

    out_file = pathlib.Path(tempfile.gettempdir()) / (root.name + "_render.html")
    out_file.write_text("".join(html_out), encoding="utf-8")
    
    print("✨ Rendergit Style Success! Saved to: " + str(out_file))
    webbrowser.open("file://" + str(out_file.resolve()))

if __name__ == "__main__":
    main()