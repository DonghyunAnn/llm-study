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
2. **독립 적대적 리뷰 2회**: (a) 컨텍스트 없는 Claude 서브에이전트, (b) `codex exec -s read-only` — 둘 다 같은 리뷰 브리프를 받는다. 브리프 템플릿은 `tools/review_brief_template.md`. 검사 항목: 사실 오류, 타임스탬프/페이지 오류, 코드 인용 검증, 누락, 표시되지 않은 추론, 내부 일관성, 확인 질문의 정답 여부. 모든 지적은 근거(자막 줄 번호/논문 페이지/코드 file:line)를 달아야 한다.
3. 지적 사항을 근거로 판정해 반영 (리뷰어도 틀릴 수 있다 — 근거 없는 지적은 기각하고 이유를 남긴다).
4. 퇴고 후 최종본 커밋. 커밋 메시지에 리뷰 반영 여부를 적는다.

## Public 저장소 원칙

- 강의 자막 원문, 데이터셋, 체크포인트는 커밋하지 않는다 (`.gitignore`).
- 논문 Figure는 출처(Figure 번호, 저자, 연도)를 표기하고, 다시 그린 도식은 "adapted from"으로 구분한다.
- 서버 경로, 회사 관련 정보, 키는 올리지 않는다.
- 강의 노트는 자막 번역이 아니라 재구성한 정리로 쓰고, 원본 링크와 강의자를 명시한다.

## 도구

- 자막: `python tools/fetch_transcript.py <youtube url>` → `transcripts/` (gitignore 대상). `youtube-transcript-api` 필요.
- 영상은 자막 + 강의 repo/슬라이드 기반으로 정리한다. 화면 내용을 확인하지 못한 부분은 노트에 그렇게 적는다.
