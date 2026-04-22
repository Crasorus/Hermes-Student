# Student References

A curated list of tools, extensions, and resources useful for the Hermes lab and general AI-assisted development work.

---

## Visual Studio Code — Install & Setup

### 1. Install VS Code
- Download from: https://code.visualstudio.com/
- Choose the installer for your OS (Windows / macOS / Linux)
- During install (Windows), tick:
  - "Add to PATH"
  - "Register Code as an editor for supported file types"
  - "Add 'Open with Code' action to Windows Explorer file/directory context menu"

### 2. First-Time Setup
- Sign in with a GitHub or Microsoft account to sync settings across machines (optional but recommended)
- Open the **Command Palette** with `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) — this is how you access most commands
- Open a folder as your workspace: **File → Open Folder…**
- Open the integrated terminal: `` Ctrl+` ``

### 3. Recommended Settings
- Enable **Auto Save**: *File → Auto Save*
- Set **Format on Save**: Settings (`Ctrl+,`) → search "format on save" → tick the box
- Set default terminal to **Git Bash** (Windows) or **zsh** (macOS) if preferred

---

## Claude Code — Install & Setup

Claude Code is Anthropic's official CLI for Claude. It can run standalone in a terminal or integrate with VS Code via the extension below.

### 1. Install Claude Code
- Official docs: https://docs.claude.com/en/docs/claude-code/overview
- Install via npm (requires Node.js 18+):
  ```
  npm install -g @anthropic-ai/claude-code
  ```
- Verify: `claude --version`

### 2. Authenticate
- Run `claude` in your terminal
- Follow the prompts to sign in with your Anthropic account (or paste an API key)
- A browser window will open to complete authentication

### 3. First Run
- `cd` into your project folder (e.g. `cd d:/Hermes`)
- Run `claude` — this starts an interactive session scoped to that folder
- Claude Code reads `CLAUDE.md` automatically for project-specific instructions

### 4. Useful Commands Inside Claude Code
- `/help` — list all available commands
- `/clear` — reset the conversation
- `/init` — generate a CLAUDE.md for the current project
- `/run-workflow` — Hermes-specific: run a workflow from chat

---

## VS Code Extensions

Install any of these via the Extensions panel (`Ctrl+Shift+X`) or Command Palette → *Extensions: Install Extensions*.

### Claude Code (Anthropic)
- **Extension ID**: `anthropic.claude-code`
- **What it does**: Embeds Claude Code directly in VS Code — chat panel, inline diffs, file-aware context
- **Why you want it**: Seamless AI pair-programming without leaving the editor
- Marketplace: https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code

### Live Server (Ritwick Dey)
- **Extension ID**: `ritwickdey.LiveServer`
- **What it does**: Launches a local dev server with live reload for HTML/CSS/JS files
- **Why you want it**: Right-click any `.html` file → *Open with Live Server* → see changes instantly in your browser. Useful for previewing the Hermes intro presentation and any report HTML outputs.
- Marketplace: https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer

### Prettier — Code Formatter (Prettier)
- **Extension ID**: `esbenp.prettier-vscode`
- **What it does**: Opinionated code formatter for JS, TS, JSON, Markdown, YAML, HTML, CSS, and more
- **Why you want it**: Consistent formatting across the team — pair with *Format on Save* and you never think about indentation again
- Marketplace: https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode

### TODO Highlight (Wayou Liu)
- **Extension ID**: `wayou.vscode-todo-highlight`
- **What it does**: Highlights `TODO`, `FIXME`, `NOTE`, etc. comments in your code
- **Why you want it**: Quickly spot outstanding work in any file — especially helpful when reviewing agent skills and workflow markdown
- Marketplace: https://marketplace.visualstudio.com/items?itemName=wayou.vscode-todo-highlight

### Print — Rendered Markdown (PD Consulting)
- **Extension ID**: `pdconsec.vscode-print`
- **What it does**: Prints source code *and* rendered Markdown (with formatting, headings, tables intact) directly from VS Code
- **Why you want it**: Markdown files in Hermes (agent prompts, skill definitions, lab guides) look great rendered — use this to hand out clean printouts or save polished PDFs
- Marketplace: https://marketplace.visualstudio.com/items?itemName=pdconsec.vscode-print

### Quick Install (Command Palette)
Open Command Palette (`Ctrl+Shift+P`), type *Extensions: Install Extensions*, then paste each ID:
```
anthropic.claude-code
ritwickdey.LiveServer
esbenp.prettier-vscode
wayou.vscode-todo-highlight
pdconsec.vscode-print
```

---

## Additional References

### Hermes Project
- Project root: [d:/Hermes](../../)
- Student guide: [student_guide.md](student_guide.md)
- Optimization agent brief: [optimization_agent_brief.md](optimization_agent_brief.md)
- Project instructions: [CLAUDE.md](../../CLAUDE.md)

### Claude & Anthropic
- Claude Code docs: https://docs.claude.com/en/docs/claude-code/overview
- Anthropic API docs: https://docs.claude.com/en/api/overview
- Claude model overview: https://docs.claude.com/en/docs/about-claude/models

### Markdown
- Markdown cheat sheet: https://www.markdownguide.org/cheat-sheet/
- CommonMark spec (what Claude Code renders): https://commonmark.org/
