# llm-study

minimind 기반 LLM 독학 기록 + 학습 자료(강의 정리, 논문 리뷰 덱) 저장소. Public.

## 작업 규칙

- 이 저장소에서 세션을 시작한다. 스킬은 전역이 아니라 `.claude/skills/`(프로젝트 범위)에만 둔다.
- 마크다운이 원본, PPTX/DOCX는 산출물. 주제 하나 = 커밋 하나, README 로드맵 체크박스를 같이 갱신한다.
- 자료 본문은 한국어, 기술 용어는 영어 그대로. 슬라이드 제목·핵심 문장은 영어, 발표 대본은 한국어.
- 다이어그램은 전부 `diagram-design` 스킬로 만든다. 원본은 각 자료 폴더의 `diagrams/*.html`, 슬라이드에는 headless Chrome으로 export한 PNG를 넣는다 (PowerPoint는 이 스킬의 `rgba()` SVG fill을 검게 렌더링한다).
- 가능하면 자료마다 minimind의 해당 코드 위치를 연결한다 (예: DPO → `trainer/train_dpo.py`의 `dpo_loss`).

## 자료 제작 절차 (강의 노트, 논문 리뷰 공통)

1. 초안 작성 (원본: 자막 + 강의 repo/공식 설명, 또는 논문 PDF).
2. **독립 적대적 리뷰 2회**: (a) 컨텍스트 없는 Claude 서브에이전트, (b) Codex — 설치된 `codex` 플러그인의 `/codex:rescue --background <브리프 경로와 지시>`(Codex 서브에이전트에 작업 위임) 또는 직접 `codex exec -s read-only -o <결과파일> "<브리프를 읽고 수행>"`. 둘 다 같은 리뷰 브리프를 받는다. `/codex:review`·`/codex:adversarial-review`는 git diff 기준 코드 리뷰라 자막·논문 대조에는 맞지 않는다. 브리프 템플릿은 `tools/review_brief_template.md`. 검사 항목: 사실 오류, 타임스탬프/페이지 오류, 코드 인용 검증, 누락, 표시되지 않은 추론, 내부 일관성, 확인 질문의 정답 여부. 모든 지적은 근거(자막 줄 번호/논문 페이지/코드 file:line)를 달아야 한다.
3. 지적 사항을 근거로 판정해 반영 (리뷰어도 틀릴 수 있다 — 근거 없는 지적은 기각하고 이유를 남긴다).
4. 퇴고 후 최종본 커밋. 커밋 메시지에 리뷰 반영 여부를 적는다.

## 코드베이스가 딸린 자료의 정리 방식

강의 repo(micrograd, makemore, ng-video-lecture, minbpe, build-nanogpt 등)나 논문 공식 구현이 있으면 "링크가 있다" 수준으로 끝내지 않는다.

- 해당 커밋을 clone해서 **코드를 노트 안에 그대로 가져오고**, 파일 → 클래스/함수 → 줄 단위로 분해한다.
- 각 블록마다 (1) 이 코드가 무엇을 하는지, (2) 왜 이렇게 짰는지(강의에서 설명한 이유), (3) minimind의 대응 코드 위치를 적는다.
- 코드 블록 안에는 한국어 각주(`# ...`)를 달아 각 줄의 역할을 설명한다. 원본 주석은 남기고 각주는 구분되게 쓴다.
- 강의 순서와 코드 순서가 다르면 강의 순서를 따르되, 파일 전체가 어디에 있는지 목차를 앞에 둔다.
- 라이선스(MIT 등)와 커밋 해시를 노트 머리말에 적는다. 코드를 실제로 실행해 본 결과(출력, 실패)도 기록한다.
- 리뷰 브리프에 "노트의 코드 블록이 원본 커밋과 일치하는지, 각주가 실제 동작을 맞게 설명하는지"를 검사 항목으로 추가한다.

## Public 저장소 원칙

- 강의 자막 원문, 데이터셋, 체크포인트는 커밋하지 않는다 (`.gitignore`).
- 논문 Figure는 출처(Figure 번호, 저자, 연도)를 표기하고, 다시 그린 도식은 "adapted from"으로 구분한다.
- 서버 경로, 회사 관련 정보, 키는 올리지 않는다.
- 강의 노트는 자막 번역이 아니라 재구성한 정리로 쓰고, 원본 링크와 강의자를 명시한다.

## 웹북 (Quarto Book)

- 모든 노트는 `_quarto.yml`의 chapters에 등록해야 책에 들어간다. 새 노트를 만들면 등록까지가 한 작업이다.
- 집필 규칙은 `STYLE.md`(책 부록으로도 렌더링됨). 제목에 수동 번호를 넣지 않고, 상호참조는 `{#sec-id}` + `@sec-id`, minimind 대응은 `::: {.callout-note title="minimind 대응"}` 콜아웃을 쓴다.
- 로컬 빌드: `.tools/quarto-1.10.18/bin/quarto render --to html` (결과 `_book/`), PDF는 `--to typst --output-dir _book_pdf`. 둘 다 gitignore. 커밋 전에 HTML을 한 번 렌더링해 깨진 곳이 없는지 본다.
- GitHub Pages 배포는 `.github/workflows/book.yml`이 main push마다 수행한다 (저장소 Settings → Pages → Source: GitHub Actions 필요).

## 도구

- 자막: `python tools/fetch_transcript.py <youtube url>` → `transcripts/` (gitignore 대상). `youtube-transcript-api` 필요.
- 영상은 자막 + 강의 repo/슬라이드 기반으로 정리한다. 화면 내용을 확인하지 못한 부분은 노트에 그렇게 적는다.
