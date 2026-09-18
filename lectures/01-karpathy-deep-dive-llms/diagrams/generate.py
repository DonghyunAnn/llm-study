"""Deep Dive 노트의 도식 3개를 diagram-design 스킬 규칙(흑백 스킨, 4px 그리드, Loop 기하)에 맞춰 생성한다.
실행: python3 generate.py  (같은 폴더에 *.html 생성. PNG export는 headless Chrome으로 별도 수행)"""
import math, os
HERE=os.path.dirname(os.path.abspath(__file__))
FONTS='<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&family=Noto+Serif:ital@0;1&family=Noto+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@400&display=swap" rel="stylesheet">'
PAPER='#f6f5f2'; INK='#1f2023'; MUTED='#55595f'; SOFT='#7d8188'; ACC='#b3402a'; ACCT='rgba(179,64,42,0.08)'
SANS="'Geist', 'Noto Sans KR', sans-serif"; MONO="'Geist Mono', monospace"
def page(slug,eyebrow,title,vb_w,vb_h,body,desc):
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  {FONTS}
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{ --color-paper: {PAPER}; --color-ink: {INK}; --color-muted: {MUTED}; --color-accent: {ACC};
      --font-sans: 'Geist', 'Noto Sans KR', system-ui, sans-serif; --font-serif: 'Instrument Serif', 'Noto Serif KR', serif; --font-mono: 'Geist Mono', ui-monospace, monospace; }}
    body {{ font-family: var(--font-sans); background: var(--color-paper); color: var(--color-ink); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 3rem 2rem; }}
    .frame {{ max-width: 1200px; width: 100%; }}
    .eyebrow {{ font-family: var(--font-mono); font-size: 0.66rem; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: var(--color-muted); margin-bottom: 0.5rem; }}
    h1 {{ font-family: var(--font-serif); font-size: clamp(1.5rem, 2.4vw + 0.75rem, 2rem); font-weight: 400; letter-spacing: -0.02em; line-height: 1.15; color: var(--color-ink); margin-bottom: 1.5rem; }}
    svg {{ width: 100%; min-width: 900px; display: block; }}
  </style>
</head>
<body>
  <div class="frame">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <svg viewBox="0 0 {vb_w} {vb_h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
      <title id="{slug}-title">{title}</title>
      <desc id="{slug}-desc">{desc}</desc>
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{MUTED}"/></marker>
        <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{ACC}"/></marker>
        <marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#4a5a6e"/></marker>
        <marker id="arrow-soft" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{SOFT}"/></marker>
      </defs>
      <rect width="100%" height="100%" fill="{PAPER}"/>
{body}
    </svg>
  </div>
</body>
</html>
'''
def node(x,y,w,h,name,sub,kind='step',tag=None):
    fill,stroke,sw={'step':('#ffffff',INK,1),'store':('rgba(31,32,35,0.05)',MUTED,0.8),'input':('rgba(85,89,95,0.10)',SOFT,0.8),'focal':(ACCT,ACC,1)}[kind]
    cx=x+w/2; s=f'      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>\n      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
    if tag:
        tw=8+len(tag)*5; tc=ACC if kind=='focal' else INK
        s+=f'      <rect x="{x+8}" y="{y+6}" width="{tw}" height="12" rx="2" fill="transparent" stroke="{tc}" stroke-opacity="0.4" stroke-width="0.8"/>\n      <text x="{x+8+tw/2}" y="{y+15}" fill="{tc}" font-size="7" font-family="{MONO}" text-anchor="middle" letter-spacing="0.08em">{tag}</text>\n'
        ny=y+h/2+7   # 태그가 있으면 이름을 아래로 내려 겹침 방지
    else:
        ny=y+h/2+(2 if not sub else -2)
    s+=f'      <text x="{cx}" y="{ny}" fill="{INK}" font-size="12" font-weight="600" font-family="{SANS}" text-anchor="middle">{name}</text>\n'
    if sub: s+=f'      <text x="{cx}" y="{ny+14}" fill="{MUTED}" font-size="9" font-family="{MONO}" text-anchor="middle">{sub}</text>\n'
    return s
def eyebrow(x,y,t): return f'      <text x="{x}" y="{y}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">{t}</text>\n'
def textw(t,size=8.5): return sum((size if ord(c)>0x2e7f else size*0.6) for c in t)
def legend(y,w,items,note=None):
    s=f'      <line x1="40" y1="{y-8}" x2="{w-40}" y2="{y-8}" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'+eyebrow(40,y+8,'LEGEND')
    x=40
    for fill,stroke,sw,label in items:
        s+=f'      <rect x="{x}" y="{y+18}" width="14" height="10" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n      <text x="{x+20}" y="{y+26}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">{label}</text>\n'
        x+=20+textw(label)+32
    if note: s+=f'      <text x="{w-40}" y="{y+26}" fill="{MUTED}" font-size="8.5" font-family="{SANS}" font-style="italic" text-anchor="end">{note}</text>\n'
    return s
LEG_STEP=('#ffffff',INK,1); LEG_STORE=('rgba(31,32,35,0.05)',MUTED,0.8); LEG_IN=('rgba(85,89,95,0.10)',SOFT,0.8); LEG_FOC=(ACCT,ACC,1)
def write(name,html): open(os.path.join(HERE,name),'w',encoding='utf-8').write(html)

# ---------- D1 pipeline ----------
b=''; cols=[200,500,800]; W=200; H=48
data=[('인터넷 문서','FineWeb · 15조 토큰'),('대화 데이터','라벨러 작성 · ~100만 개'),('연습문제 + 정답 / 선호 순서','검증 가능 · 검증 불가능')]
stage=[('Pretraining','next-token 예측 · 수개월','1'),('Supervised finetuning','같은 알고리즘, 데이터만 교체','2'),('Reinforcement learning','guess and check · RLHF 포함','3')]
model=[('Base model','인터넷 문서 시뮬레이터'),('SFT model','라벨러의 시뮬레이션'),('RL model','사고 전략이 창발')]
b+=eyebrow(40,92,'DATA')+eyebrow(40,212,'STAGE')+eyebrow(40,332,'ARTIFACT')
for cx in cols:
    b+=f'      <line x1="{cx}" y1="112" x2="{cx}" y2="182" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b+=f'      <line x1="{cx}" y1="232" x2="{cx}" y2="302" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
for x1,x2 in ((300,400),(600,700)):
    mid=(x1+x2)/2
    b+=f'      <path d="M {x1},328 H {mid-8} Q {mid},328 {mid},320 V 216 Q {mid},208 {mid+8},208 H {x2-2}" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
for i,cx in enumerate(cols):
    x=cx-W/2
    b+=node(x,64,W,H,*data[i],kind='input')
    b+=node(x,184,W,H,stage[i][0],stage[i][1],kind='focal' if i==2 else 'step',tag='STEP '+stage[i][2])
    b+=node(x,304,W,H,*model[i],kind='store')
b+=legend(392,1000,[(*LEG_IN,'데이터'),(*LEG_STEP,'학습 단계'),(*LEG_STORE,'결과물 (파라미터)'),(*LEG_FOC,'가장 새로운 단계')],'앞 단계의 결과물이 다음 단계의 출발점')
write('training-pipeline.html',page('training-pipeline','Architecture · Deep Dive into LLMs','LLM 학습 파이프라인: 세 단계와 세 결과물',1000,440,b,'인터넷 문서로 사전학습해 base 모델을 만들고, 대화 데이터로 SFT해 어시스턴트를 만들고, 연습문제로 RL해 사고 전략을 얻는 세 단계 흐름.'))

# ---------- D3 RLHF ----------
b=''; X=420; W=280; H=48; ys=[48,136,224,312,400]
items=[('1,000 프롬프트 × 5 롤아웃','"write a joke about pelicans"','input',None),
       ('사람이 순서를 매긴다','best → worst · 5,000회 판단','step','STEP 1'),
       ('Reward model 학습','(프롬프트, 응답) → 점수 · 순서와 일치하도록','focal','STEP 2'),
       ('Reward model을 상대로 RL','10억 회 채점을 시뮬레이터가 대신','step','STEP 3'),
       ('RL model','수백 스텝 뒤에는 reward hacking','store',None)]
for y in ys[:-1]:
    b+=f'      <line x1="{X+W/2}" y1="{y+H}" x2="{X+W/2}" y2="{y+88-2}" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
for (n,s,k,t),y in zip(items,ys): b+=node(X,y,W,H,n,s,kind=k,tag=t)
notes=[(48,'사람이 직접 채점하면 1,000 × 1,000 × 1,000 = 10억 회'),(136,'점수보다 순서가 사람에게 쉽다'),(224,'Transformer지만 언어를 생성하지 않는 채점 전용 모델'),(312,'시뮬레이터라 무한히 물어볼 수 있다'),(400,'"the the the the"가 점수 1.0을 받는 순간 멈춘다')]
for y,t in notes: b+=f'      <text x="{X+W+24}" y="{y+H/2+3}" fill="{SOFT}" font-size="9" font-family="{MONO}">{t}</text>\n'
b+=legend(488,1000,[(*LEG_IN,'입력'),(*LEG_STEP,'단계'),(*LEG_FOC,'간접화의 핵심'),(*LEG_STORE,'결과물')],'사람의 판단을 신경망으로 복제한 뒤 그 복제본을 상대로 최적화한다')
write('rlhf-indirection.html',page('rlhf-indirection','Architecture · Deep Dive into LLMs','RLHF: 사람 대신 사람의 시뮬레이터를 채점자로',1000,536,b,'1,000개 프롬프트의 5개 롤아웃을 사람이 순서 매기고, 그 순서에 맞는 reward model을 학습한 뒤, 그 모델을 상대로 RL을 돌려 RL 모델을 얻는 흐름.'))

# ---------- D2 RL loop (type-loop.md §2 기하) ----------
cx,cy,R=520,340,240; sw,sh=160,64; hw,hh=200,104
stations=[('문제 + 정답','"사과 값은?" · 답 3',None,False),('풀이를 여러 개 샘플링','수천~수백만 개 · 확률적',None,False),('정답과 대조','맞음 / 틀림 채점','CHECK',True),('좋은 풀이 선택','맞고 짧은 것',None,False),('그 풀이로 학습','확률을 높인다','UPDATE',False)]
N=len(stations)
def center(k):
    th=math.radians(-90+k*360/N); return cx+R*math.cos(th), cy+R*math.sin(th), th
def r4(v): return int(round(v/4)*4)
boxes=[]
for k in range(N):
    px,py,th=center(k); boxes.append((r4(px-sw/2),r4(py-sh/2)))
def inters(k):
    x,y=boxes[k]; pts=[]
    for xe in (x,x+sw):
        d=R*R-(xe-cx)**2
        if d>=0:
            for yy in (cy+math.sqrt(d),cy-math.sqrt(d)):
                if y<=yy<=y+sh: pts.append((xe,yy))
    for ye in (y,y+sh):
        d=R*R-(ye-cy)**2
        if d>=0:
            for xx in (cx+math.sqrt(d),cx-math.sqrt(d)):
                if x<=xx<=x+sw: pts.append((xx,ye))
    th=center(k)[2]
    def ang(p):
        a=math.atan2(p[1]-cy,p[0]-cx)-th
        return (a+math.pi)%(2*math.pi)-math.pi
    pts=sorted(set(pts),key=ang)
    entry=[p for p in pts if ang(p)<0][-1]; exit_=[p for p in pts if ang(p)>0][0]
    return entry,exit_
b=''
for k in range(N):
    j=(k+1)%N; _,qx=inters(k); qe,_=inters(j)
    phi=math.atan2(qe[1]-cy,qe[0]-cx)-1.2/R; qend=(cx+R*math.cos(phi),cy+R*math.sin(phi))
    b+=f'      <path d="M {qx[0]:.3f} {qx[1]:.3f} A {R} {R} 0 0 1 {qend[0]:.3f} {qend[1]:.3f}" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
k=4; px,py,th=center(k); ux,uy=math.cos(th),math.sin(th)
ds=min(sw/2/abs(ux) if ux else 1e9, sh/2/abs(uy) if uy else 1e9); dh=min(hw/2/abs(ux) if ux else 1e9, hh/2/abs(uy) if uy else 1e9)
s0=(px-ds*ux,py-ds*uy); s1=(cx+(dh+6)*ux,cy+(dh+6)*uy)
b+=f'      <line x1="{s0[0]:.1f}" y1="{s0[1]:.1f}" x2="{s1[0]:.1f}" y2="{s1[1]:.1f}" stroke="{SOFT}" stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arrow-soft)"/>\n'
mx,my=(s0[0]+s1[0])/2,(s0[1]+s1[1])/2
b+=f'      <rect x="{mx-46}" y="{my+10}" width="60" height="12" rx="2" fill="{PAPER}"/>\n      <text x="{mx-16}" y="{my+19}" fill="{SOFT}" font-size="8" font-family="{MONO}" text-anchor="middle" letter-spacing="0.06em">WEIGHTS</text>\n'
for k,(n,s,tag,foc) in enumerate(stations):
    x,y=boxes[k]; b+=node(x,y,sw,sh,n,s,kind='focal' if foc else 'step',tag=tag)
b+=f'      <rect x="{cx-hw/2}" y="{cy-hh/2}" width="{hw}" height="{hh}" rx="6" fill="{INK}"/>\n      <text x="{cx}" y="{cy-2}" fill="{PAPER}" font-size="12" font-weight="600" font-family="{SANS}" text-anchor="middle">모델 파라미터</text>\n      <text x="{cx}" y="{cy+14}" fill="{PAPER}" fill-opacity="0.75" font-size="9" font-family="{MONO}" text-anchor="middle">사고 전략이 쌓인다</text>\n'
b+=legend(640,1040,[(*LEG_STEP,'단계 (시계 방향)'),(*LEG_FOC,'정답 검사 · 사람이 없어도 된다'),(INK,INK,1,'축적되는 상태')],'점선은 파라미터로의 쓰기. 수만 개 문제에 대해 반복한다.')
write('rl-loop.html',page('rl-loop','Loop · Deep Dive into LLMs','RL: 풀이를 만들고, 채점하고, 잘 된 것으로 학습한다',1040,690,b,'문제와 정답에서 출발해 풀이를 여러 개 샘플링하고 정답과 대조한 뒤 좋은 풀이로 학습해 모델 파라미터를 갱신하는 반복 루프.'))
print('generated 3 diagrams')
