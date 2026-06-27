# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-06-27
### Added
- Core Python Engine for PPTX Generation (`engine/`)
- `DESIGN.md` Parser module for extracting theme colors and typography.
- LLM Integration (Gemini 2.5 Flash) for parsing raw text and structuring it into `@slide` DSL.
- Tauri Desktop Shell (`ui/`) initialization with React Frontend.
- IPC commands connecting React UI to the Python backend sidecar.
- `.bat` helper scripts for easy environment setup and execution.
