# llm-study

minimind 기반 LLM 독학 기록 + 학습 자료(강의 정리, 논문 리뷰 덱) 저장소. Public.

## 작업 규칙

- 이 저장소에서 세션을 시작한다. 스킬은 전역이 아니라 `.claude/skills/`(프로젝트 범위)에만 둔다.
- 마크다운이 원본, PPTX/DOCX는 산출물. 주제 하나 = 커밋 하나, README 로드맵 체크박스를 같이 갱신한다.
- 자료 본문은 한국어, 기술 용어는 영어 그대로. 슬라이드 제목·핵심 문장은 영어, 발표 대본은 한국어.
- 다이어그램은 전부 `diagram-design` 스킬로 만든다. 원본은 각 자료 폴더의 `diagrams/*.html`, 슬라이드에는 headless Chrome으로 export한 PNG를 넣는다 (PowerPoint는 이 스킬의 `rgba()` SVG fill을 검게 렌더링한다).
- 가능하면 자료마다 minimind의 해당 코드 위치를 연결한다 (예: DPO → `trainer/train_dpo.py`의 `dpo_loss`).

## Public 저장소 원칙

- 강의 자막 원문, 데이터셋, 체크포인트는 커밋하지 않는다 (`.gitignore`).
- 논문 Figure는 출처(Figure 번호, 저자, 연도)를 표기하고, 다시 그린 도식은 "adapted from"으로 구분한다.
- 서버 경로, 회사 관련 정보, 키는 올리지 않는다.
- 강의 노트는 자막 번역이 아니라 재구성한 정리로 쓰고, 원본 링크와 강의자를 명시한다.

## 도구

- 자막: `python tools/fetch_transcript.py <youtube url>` → `transcripts/` (gitignore 대상). `youtube-transcript-api` 필요.
- 영상은 자막 + 강의 repo/슬라이드 기반으로 정리한다. 화면 내용을 확인하지 못한 부분은 노트에 그렇게 적는다.
