# Markdown to PPTX Generator (Tauri + Python)

Build a Windows desktop application that automatically generates beautifully styled `.pptx` files. It takes a design system definition (`DESIGN.md`) for styling, and raw text/documents for content. The app will automatically structure the raw text into slides using an LLM and apply the design tokens.

## Proposed Architecture (4 Modules)

The project will use **Tauri (React/Vite)** for the frontend UI and a **Python CLI** as the core engine, exactly as you described.

### Module 1: Theme Engine (`DESIGN.md` → Slide Theme)
Parses `DESIGN.md` to extract color palettes, typography, and component layouts.
- Reads tokens like `colors.canvas-soft`, `typography.display-1`.
- Maps these to Python objects (`Theme` class) that define slide backgrounds, text colors, and font properties.

### Module 2: Content Structuring Engine (Raw Data → Slide Markdown DSL)
Converts raw text/documents into structured slide markdown.
- **Mode A (Manual)**: User writes the slide DSL directly (e.g., `@slide: title`, `- bullet`).
- **Mode B (Auto/LLM)**: User inputs raw text. An LLM parses the text, extracts key sections and bullet points, and automatically generates the slide DSL.

### Module 3: PPT Generation Engine (Slide Markdown → `.pptx`)
Uses `python-pptx` to render the slides.
- Takes the Slide Markdown from Module 2 and the Theme from Module 1.
- Implements templates for `title`, `bullets`, `cards`, etc.
- Applies the specific design tokens (colors, fonts) to the `python-pptx` text frames and shapes.

### Module 4: Windows App Shell (Tauri)
A lightweight desktop app wrapper.
- **Frontend**: React/Vite for a modern UI (Design file upload, material text area, "Generate" button).
- **Backend (Rust)**: Receives the UI request and spawns the Python CLI as a sidecar process.
- **Python CLI**: `python design2ppt.py --design DESIGN.md --input material.txt --out presentation.pptx`.

## Directory Structure

```text
PPT_Build/
├── src-tauri/             # Tauri Rust backend (invokes Python sidecar)
├── src/                   # React/Vite Frontend
├── engine/                # Python Core CLI
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── theme.py       # Module 1: DESIGN.md parser
│   │   ├── content.py     # Module 2: LLM structuring & DSL parser
│   │   └── generator.py   # Module 3: python-pptx builder
│   ├── requirements.txt
│   └── design2ppt.py      # CLI Entry point
└── package.json           # Node dependencies for Tauri/React
```

## MVP Implementation Plan

1. **Setup Python Engine (`engine/`)**:
   - Implement `theme.py` to parse a mock `DESIGN-notion.md`.
   - Implement `content.py` to parse basic `@slide` DSL.
   - Implement `generator.py` using `python-pptx` to create `title` and `bullets` slides mapping the theme.
2. **Implement CLI Interface**: Make `design2ppt.py` work from the terminal for local testing.
3. **Setup Tauri App (`src/` & `src-tauri/`)**:
   - Initialize a Tauri project with React.
   - Create a simple UI to select `DESIGN.md` and input raw text.
   - Configure Tauri Rust backend to execute the Python CLI as a child process.
4. **Integrate LLM (Phase 2)**: Add the LLM prompt logic in `content.py` to auto-generate DSL from raw text.
