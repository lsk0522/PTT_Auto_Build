# PPT Auto Build 사용 설명서 (Manual)

이 문서는 프로그램의 사용법과 내부 파일 규칙을 설명합니다.

## 1. DESIGN.md 작성 규칙
이 프로젝트는 테마를 정의할 때 YAML 프론트매터(Frontmatter) 형식을 사용합니다.

```yaml
---
colors:
  primary: "#0075de"
  canvas-soft: "#ffffff"
typography:
  display-1: "Inter"
---
```
이러한 토큰 값들을 엔진이 읽어들여 생성되는 PPTX의 색상과 폰트에 적용합니다. (현재 MVP 버전에서는 `primary_color` 위주로 매핑되어 있으며 향후 확장 가능합니다.)

## 2. 슬라이드 작성 방법
PPT의 내용을 작성하는 방법은 두 가지입니다.

### 방법 A: 수동 작성 (@slide DSL)
원하는 슬라이드 포맷을 직접 마크다운 형태로 지정할 수 있습니다.
```markdown
@slide: title
# 프로젝트 시작하기
부제목입니다.

---
@slide: bullets
## 프로젝트 구조
- 프론트엔드: React
- 백엔드: Python
```

### 방법 B: AI 자동 생성 (Raw Text 모드)
일반적인 글, 기획서, 회의록을 던지면 Gemini AI가 자동으로 방법 A의 형태로 변환해줍니다.
1. `run_test.bat` 혹은 UI에서 **Raw Data Mode**를 활성화.
2. 텍스트 파일을 업로드.
3. 자동으로 슬라이드가 나누어집니다.

## 3. 프로그램 실행
- **CLI 모드**: `python src/engine/design2ppt.py --design tests/test_design.md --input tests/test_input.txt --out result.pptx --raw`
- **UI 모드**: `scripts/run_ui.bat`을 실행해 웹 형태의 프로그램에서 파일을 클릭하여 업로드하고 Generate 버튼을 누르세요.
