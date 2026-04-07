# 📂 renderlocal

> "Because my `node_modules` folder is a dark abyss and I just want to see my actual code."

Tired of clicking through 50 folders just to find that one function you wrote three weeks ago? Do you want to feed your entire local project to an LLM without your computer exploding? 

**renderlocal** is a specialized fork/tribute to [Andrej Karpathy's `rendergit`](https://github.com/karpathy/rendergit). While the original is amazing for GitHub repos, this version is built to sweep through your **local hard drive**, dodge the "junk" folders (looking at you, `.venv`), and flatten everything into one beautiful, searchable HTML page.

## ✨ Features

- **Local First**: No `git clone` needed. Point it at a folder, and it works.
- **The "Karpathy" UI**: Clean, sticky sidebar navigation and GitHub-style syntax highlighting.
- **LLM Ready**: One click to switch to **🤖 LLM View**. Copy the whole codebase in CXML format and watch Claude/ChatGPT actually understand your project.
- **Smart Filters**: Automatically ignores the heavy lifting stuff like `node_modules`, `.git`, `.venv`, and `__pycache__`.
- **Searchable**: Use `Ctrl+F` to find anything across the entire project instantly.

## 🚀 Usage

First, install the essentials:
```bash
pip install -r requirements.txt
```
Then, just point it at your project:
```bash
python renderlocal.py "C:\Users\You\Desktop\MyCoolProject"
```
The script will:
- Scan your files (even if there are 25,000 of them).
- Filter out the binaries and the bloat.
- Generate a single .html file in your temp folder.
- Pop it open in your browser automatically.

## 🛠 Why?

I was working on some local projects and realized I needed the rendergit experience without having to push every tiny change to GitHub first. This is for the builders who live in their local IDEs.

## 🤝 Credits & Thanks

Huge shoutout to Andrej Karpathy for the original rendergit. This script is a love letter to that utility—keeping the "vibe coding" spirit alive while making it work for those of us living in local directories.
