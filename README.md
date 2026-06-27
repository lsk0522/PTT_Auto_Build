# PPT Auto Build

**PPT Auto Build**는 디자인 가이드(`DESIGN.md`)와 원시 텍스트(문서, 발표 자료)를 기반으로 아름답고 일관된 형태의 파워포인트(`.pptx`) 파일을 자동으로 생성해주는 어플리케이션입니다.

LLM(Gemini)을 활용해 텍스트를 구조화된 슬라이드 형태로 자동으로 분리 및 요약하며, `python-pptx`를 이용해 테마 토큰 기반의 세련된 결과물을 도출합니다. 데스크톱 앱(Tauri)과 CLI 도구를 모두 지원합니다.

## 기능 (Features)
- **Design Token 파싱**: `DESIGN.md` 파일에서 색상, 폰트 등의 테마 추출.
- **LLM 기반 자동 요약**: 원시 텍스트를 AI가 분석하여 슬라이드 제목과 글머리 기호 형태의 마크다운(DSL)으로 분할.
- **PPTX 렌더링**: 추출된 테마와 내용을 `python-pptx` 엔진을 통해 실제 동작하는 파워포인트 파일로 생성.
- **크로스 플랫폼 UI**: Rust + Tauri + React를 기반으로 한 작고 가벼운 데스크톱 인터페이스.

## 빠르게 시작하기 (Quick Start)
자세한 사용법은 [MANUAL.md](MANUAL.md)를 참고하세요.

### 1. Python CLI 엔진 테스트
```bash
cd src/engine
pip install -r requirements.txt
```
이후 상위 디렉터리에서 자동화 스크립트를 실행합니다.
```cmd
scripts\run_test.bat
```

### 2. 데스크톱 앱 실행 (Rust 설치 필요)
Rust([rustup.rs](https://rustup.rs/))가 설치된 환경에서 다음 스크립트를 실행합니다.
```cmd
scripts\run_ui.bat
```
