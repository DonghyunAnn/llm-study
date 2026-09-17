# llm-study

[minimind](https://github.com/jingyaogong/minimind)를 실습 기반으로 삼아 LLM을 처음부터 끝까지 공부하고, 그 과정을 학습 자료로 남기는 저장소.

## 구성

| 폴더 | 내용 |
|---|---|
| `lectures/` | 강의 정리 노트. `NN-slug/notes.md` (자막 + 강의 repo 기반, 화면 내용은 미반영일 수 있음) |
| `papers/` | 논문 리뷰. `NN-slug/review.md` + `slides.pptx` |
| `minimind-lab/` | minimind 실습 기록: 실험 로그, 직접 고쳐본 패치, 관찰 결과 |
| `tools/` | 자막 수집 등 보조 스크립트 |

원칙: 마크다운 노트가 원본, PPT는 그 결과물. 자막 원문·데이터셋·체크포인트는 커밋하지 않는다.

다이어그램: 모든 도식은 [diagram-design](https://github.com/cathrynlavery/diagram-design) 스킬(MIT, v2.6.27)의 디자인 시스템으로 통일한다. 원본은 각 자료 폴더의 `diagrams/*.html`(인라인 SVG), 슬라이드에는 거기서 export한 PNG를 넣는다.

## 로드맵

### 1. 큰 그림
- [ ] Karpathy — Deep Dive into LLMs like ChatGPT

### 2. 기초 (Zero to Hero)
- [ ] micrograd (autograd / backprop)
- [ ] makemore 시리즈
- [ ] Let's build GPT
- [ ] Let's build the GPT Tokenizer
- [ ] (선택) Let's reproduce GPT-2

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
