# llm-study

[minimind](https://github.com/jingyaogong/minimind)를 실습 기반으로 삼아 LLM을 처음부터 끝까지 공부하고, 그 과정을 학습 자료로 남기는 저장소.

## 읽기

웹북: https://donghyunann.github.io/llm-study/ (Quarto Book으로 빌드. PDF도 같은 원본에서 생성)

## 구성

| 폴더 | 내용 |
|---|---|
| `lectures/` | 강의 정리 노트. `NN-slug/notes.md` (자막 + 강의 repo 기반, 화면 내용은 미반영일 수 있음) |
| `papers/` | 논문 리뷰. `NN-slug/review.md` + `slides.pptx` |
| `readings/` | 블로그·기술 보고서 정리 (예: FineWeb) |
| `minimind-lab/` | minimind 실습 기록: 실험 로그, 직접 고쳐본 패치, 관찰 결과 |
| `tools/` | 자막 수집 등 보조 스크립트 |

원칙: 마크다운 노트가 원본, PPT는 그 결과물. 자막 원문·데이터셋·체크포인트는 커밋하지 않는다.

다이어그램: 모든 도식은 [diagram-design](https://github.com/cathrynlavery/diagram-design) 스킬(MIT, v2.6.27)의 디자인 시스템으로 통일한다. 원본은 각 자료 폴더의 `diagrams/*.html`(인라인 SVG), 슬라이드에는 거기서 export한 PNG를 넣는다.

## 로드맵

### 1. 큰 그림
- [ ] Karpathy — Deep Dive into LLMs like ChatGPT (3h31) — [정리 노트](lectures/01-karpathy-deep-dive-llms/notes.md)

### 2. 기초 (Karpathy Zero to Hero)
필수 (약 12시간)
- [ ] micrograd — 역전파 (2h25) — [정리 노트](lectures/02-karpathy-micrograd/notes.md)
- [ ] makemore 1 — bigram, 언어 모델링 프레임 (1h57) — [정리 노트](lectures/03-karpathy-makemore-1/notes.md)
- [ ] makemore 2 — MLP, 임베딩, 학습 루프 (1h15) — [정리 노트](lectures/04-karpathy-makemore-2/notes.md)
- [ ] Let's build GPT (1h56) — [정리 노트](lectures/05-karpathy-build-gpt/notes.md)
- [ ] Let's build the GPT Tokenizer (2h13)

보강 (minimind 실습 뒤에)
- [ ] Let's reproduce GPT-2 (124M) — 실전 사전학습, minimind `train_pretrain.py`와 직접 비교 (4h01)
- [ ] makemore 3 — 활성값·기울기, BatchNorm, 초기화 (1h55)

선택
- [ ] makemore 4 — 역전파 수동 구현 (1h55)
- [ ] makemore 5 — WaveNet (0h56). Transformer 경로와 무관, 건너뛰어도 됨
- [ ] How I use LLMs (2h11). 사용법 강의, 학습 로드맵과 무관
- [ ] [1hr Talk] Intro to LLMs (0h59). 2023년 강연, Deep Dive가 상위 호환

### 3. minimind 실습
- [ ] `model_minimind.py` 안 보고 직접 구현 → diff
- [ ] pretrain + SFT (mini 데이터, RTX 3080)
- [ ] SFT 라벨 마스킹 디버그 출력으로 확인
- [ ] DPO
- [ ] GRPO / CISPO
- [ ] 개선 과제: sequence packing, LR warmup, validation loss, LoRA alpha

### 4. 논문
- [ ] Attention Is All You Need
- [ ] LLaMA
- [ ] RoFormer (RoPE)
- [ ] GQA
- [ ] Chinchilla (scaling laws)
- [ ] InstructGPT
- [ ] DPO
- [ ] DeepSeekMath (GRPO)
- [ ] DeepSeek-R1
- [ ] LoRA

- [ ] FlashAttention
- [ ] PagedAttention (vLLM)

### 5. 보강 (Karpathy 강의가 다루지 않는 영역)
- [ ] Stanford CS336 — 시스템·스케일링·데이터·평가
- [ ] RLHF Book (Nathan Lambert) — post-training 이론
- [ ] HF Smol Training Playbook — 실제 학습 의사결정(ablation, 하이퍼파라미터, 데이터 믹스)
- [ ] HF Ultra-Scale Playbook — 분산 학습
- [ ] (선택) nanochat 코드 리딩

### 6. 선택 (관심사에 따라)
- [ ] 3Blue1Brown 신경망 시리즈 5~7장 — attention 시각적 직관 (기초가 흔들릴 때)
- [ ] The Illustrated Transformer / The Annotated Transformer — 자료 제작 시 도식 참고
- [ ] Mechanistic interpretability 입문 — A Mathematical Framework for Transformer Circuits
