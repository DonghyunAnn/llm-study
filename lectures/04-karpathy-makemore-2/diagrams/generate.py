"""makemore Part 2 다이어그램 2장 (diagram-design 스킬, 프로젝트 monochrome 스킨).
실행: python3 generate.py  (같은 폴더에 *.html 생성. PNG export는 headless Chrome으로 별도 수행)
1. mlp.html     — Architecture: Bengio et al. 2003 Fig. 1을 이 강의의 크기(3글자, C 27×2, 은닉 100)로 다시 그린 것
2. view.html    — tensor-shape view: view는 storage를 공유하고 shape/stride만 바꾼다, cat은 새 storage를 만든다
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
PAPER='#f6f5f2'; PAPER2='#ebeae6'; INK='#1f2023'; MUTED='#55595f'; SOFT='#7d8188'; ACC='#b3402a'; ACCT='rgba(179,64,42,0.08)'
SANS="'Geist', 'Noto Sans KR', sans-serif"; MONO="'Geist Mono', monospace"
FONTS='<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&family=Noto+Serif:ital@0;1&family=Noto+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@400&display=swap" rel="stylesheet">'

def page(title, eyebrow, h1, svg_id, svg_title, svg_desc, body, W, H):
    return f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title}</title>{FONTS}
<style>*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}:root{{--color-paper:{PAPER};--color-ink:{INK};--color-muted:{MUTED};--color-accent:{ACC};--font-sans:'Geist','Noto Sans KR',system-ui,sans-serif;--font-serif:'Instrument Serif','Noto Serif KR',serif;--font-mono:'Geist Mono',ui-monospace,monospace}}
body{{font-family:var(--font-sans);background:var(--color-paper);color:var(--color-ink);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:3rem 2rem}}.frame{{max-width:1200px;width:100%}}.eyebrow{{font-family:var(--font-mono);font-size:.66rem;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--color-muted);margin-bottom:.5rem}}h1{{font-family:var(--font-serif);font-size:clamp(1.5rem,2.4vw + .75rem,2rem);font-weight:400;letter-spacing:-.02em;line-height:1.15;color:var(--color-ink);margin-bottom:1.5rem}}svg{{width:100%;min-width:900px;display:block}}</style></head>
<body><div class="frame"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1>
    <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{svg_id}-title {svg_id}-desc">
      <title id="{svg_id}-title">{svg_title}</title>
      <desc id="{svg_id}-desc">{svg_desc}</desc>
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{MUTED}"/></marker>
        <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{ACC}"/></marker>
        <marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#4a5a6e"/></marker>
      </defs>
      <rect width="100%" height="100%" fill="{PAPER}"/>
{body}    </svg></div></body></html>
'''

def node(x, y, w, h, name, sub, kind='step', tag=None):
    fill, stroke, sw = {'step': ('#ffffff', INK, 1), 'focal': (ACCT, ACC, 1), 'store': ('rgba(31,32,35,0.05)', MUTED, 0.8), 'input': ('rgba(85,89,95,0.10)', SOFT, 0.8)}[kind]
    s = f'      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>\n'
    s += f'      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
    cy = y + h/2
    s += f'      <text x="{x+w/2}" y="{cy-2 if sub else cy+4}" fill="{INK}" font-size="12" font-weight="600" font-family="{SANS}" text-anchor="middle">{name}</text>\n'
    if sub:
        s += f'      <text x="{x+w/2}" y="{cy+12}" fill="{MUTED}" font-size="9" font-family="{MONO}" text-anchor="middle">{sub}</text>\n'
    if tag:
        s += f'      <text x="{x+w/2}" y="{y-6}" fill="{SOFT}" font-size="7" font-family="{MONO}" text-anchor="middle" letter-spacing="0.14em">{tag}</text>\n'
    return s

def label(x, y, text, w=None, color=MUTED, size=8):
    w = w or (len(text) * 5.2 + 10)
    return (f'      <rect x="{x-w/2:.1f}" y="{y-8}" width="{w:.1f}" height="12" rx="2" fill="{PAPER}"/>\n'
            f'      <text x="{x}" y="{y+1}" fill="{color}" font-size="{size}" font-family="{MONO}" text-anchor="middle">{text}</text>\n')

def harrow(x1, x2, y, color=MUTED, dashed=False, marker='arrow'):
    d = ' stroke-dasharray="4,3"' if dashed else ''
    return f'      <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="1.2"{d} marker-end="url(#{marker})"/>\n'


# ---------------------------------------------------------------- 1. mlp
def mlp():
    W, H = 1080, 380
    b = ''
    # nodes: x=idx (input) -> C lookup (store) -> view (step) -> hidden tanh (step) -> logits (step) -> softmax/CE (focal)
    IN = (40, 100, 150, 48); CL = (250, 100, 150, 48); VW = (460, 100, 120, 48); HD = (640, 100, 150, 48); LG = (850, 100, 190, 48)
    # arrows
    b += harrow(190, 250, 124); b += label(220, 112, 'C[X]', w=34)
    b += harrow(400, 460, 124); b += label(430, 112, '(n,3,2)', w=48)
    b += harrow(580, 640, 124); b += label(610, 112, '(n,6)', w=40)
    b += harrow(790, 850, 124); b += label(820, 112, '(n,100)', w=50)
    # shared-C note: three sublabels under C node
    # second row: loss path from logits down to loss node
    LS = (850, 220, 190, 48)
    b += f'      <line x1="945" y1="148" x2="945" y2="220" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += label(855, 184, 'F.cross_entropy(logits, Y)', w=150)
    # backward dashed return from loss to C (under the row)
    b += f'      <path d="M 900,268 V 296 Q 900,304 892,304 H 333 Q 325,304 325,296 V 148" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4,3" marker-end="url(#arrow)"/>\n'
    b += label(612, 320, 'loss.backward() · 모든 파라미터 p.data += −lr · p.grad  (C, W1, b1, W2, b2 = 3,481개)', w=400)
    # nodes
    b += node(*IN, '앞 글자 3개', 'X: (n, 3) 정수 인덱스', 'input', tag='CONTEXT · block_size = 3')
    b += node(*CL, 'C: 27×2 lookup', '2-dim · 세 자리가 공유', 'store', tag='EMBEDDING')
    b += node(*VW, 'view(-1, 6)', '이어 붙이기 · 복사 없음', 'step')
    b += node(*HD, 'tanh(· @ W1 + b1)', '은닉 100 뉴런 · (6→100)', 'store', tag='HIDDEN')
    b += node(*LG, 'logits = h @ W2 + b2', '27개 · (100→27)', 'store', tag='OUTPUT')
    b += node(*LS, 'loss (NLL)', 'softmax → −log p[y] 평균', 'focal')
    # legend
    ly = 352
    b += f'      <line x1="40" y1="{ly-10}" x2="{W-40}" y2="{ly-10}" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
    b += f'      <text x="40" y="{ly+6}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">LEGEND</text>\n'
    b += f'      <rect x="40" y="{ly+16}" width="14" height="10" rx="2" fill="rgba(31,32,35,0.05)" stroke="{MUTED}" stroke-width="0.8"/><text x="60" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">학습되는 파라미터: C, W1, b1, W2, b2</text>\n'
    b += f'      <rect x="300" y="{ly+16}" width="14" height="10" rx="2" fill="{ACCT}" stroke="{ACC}" stroke-width="1"/><text x="320" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">최적화 대상</text>\n'
    b += f'      <rect x="420" y="{ly+16}" width="14" height="10" rx="2" fill="rgba(85,89,95,0.10)" stroke="{SOFT}" stroke-width="0.8"/><text x="440" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">입력 데이터 (학습 안 됨)</text>\n'
    b += f'      <text x="{W-40}" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}" font-style="italic" text-anchor="end">Adapted from Bengio et al. 2003, Figure 1 (y = b + U·tanh(d + Hx); 이 강의는 직접 연결 W를 쓰지 않는다). 단어 17,000개 → 글자 27개.</text>\n'
    html = page('makemore 2 · MLP 언어 모델', 'Architecture · makemore 2', 'MLP 언어 모델: 글자 3개 → 임베딩 → 은닉층 → 다음 글자', 'mlp',
                'Bengio 2003 MLP 언어 모델을 글자 단위로 옮긴 구조', '앞 글자 3개의 정수 인덱스가 공유 lookup 표 C에서 2차원 벡터로 바뀌고, view로 이어 붙여 6차원이 된 뒤 tanh 은닉층 100개를 거쳐 27개 logits가 되고 cross entropy loss로 학습된다. 역전파는 C까지 흐른다.', b, W, H)
    open(os.path.join(HERE, 'mlp.html'), 'w', encoding='utf-8').write(html)
    return H

# ---------------------------------------------------------------- 2. view vs cat
def view():
    W, H = 1080, 430
    c = 18
    b = ''
    # storage strip (18 cells) at top
    sx, sy = 60, 96
    b += f'      <text x="{sx}" y="{sy-14}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">STORAGE · 메모리 위의 1차원 수열 (arange(18))</text>\n'
    for k in range(18):
        b += f'      <rect x="{sx+k*c}" y="{sy}" width="{c}" height="{c}" fill="rgba(31,32,35,0.05)" stroke="{MUTED}" stroke-width="0.8"/>\n'
        b += f'      <text x="{sx+k*c+c/2}" y="{sy+12}" fill="{INK}" font-size="8" font-family="{MONO}" text-anchor="middle">{k}</text>\n'
    # three views below, each a grid with shape/stride tag, connected by dashed lines up to storage (same storage)
    vy = 200
    views = [(60, 2, 9, '.view(2, 9)', 'shape (2,9) · stride (9,1)'), (300, 9, 2, '.view(9, 2)', 'shape (9,2) · stride (2,1)'), (420, 3, 6, '.view(3, 3, 2)', 'shape (3,3,2) · stride (6,2,1) · 6칸을 3×2로 읽음')]
    for (vx, rows, cols, name, sub) in views:
        b += f'      <text x="{vx}" y="{vy-10}" fill="{INK}" font-size="11" font-weight="600" font-family="{SANS}">{name}</text>\n'
        for i in range(rows):
            for j in range(cols):
                k = i*cols + j
                b += f'      <rect x="{vx+j*c}" y="{vy+i*c}" width="{c}" height="{c}" fill="#ffffff" stroke="{INK}" stroke-width="0.8"/>\n'
                b += f'      <text x="{vx+j*c+c/2}" y="{vy+i*c+12}" fill="{INK}" font-size="8" font-family="{MONO}" text-anchor="middle">{k}</text>\n'
        b += f'      <text x="{vx}" y="{vy+rows*c+14}" fill="{SOFT}" font-size="8" font-family="{MONO}">{sub}</text>\n'
    # 3x3x2 group separators
    b += f'      <line x1="{420+2*c}" y1="{vy-4}" x2="{420+2*c}" y2="{vy+3*c+4}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3,2"/>\n'
    b += f'      <line x1="{420+4*c}" y1="{vy-4}" x2="{420+4*c}" y2="{vy+3*c+4}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3,2"/>\n'
    # dashed "same storage" links from storage to each view (vertical, distinct x)
    for x in (140, 318, 474):
        b += f'      <line x1="{x}" y1="{sy+c}" x2="{x}" y2="{vy-24}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4,3"/>\n'
    b += label(229, 158, 'data_ptr() 동일 · 복사 없음', w=150)
    # right panel: cat creates new storage
    zx = 640
    b += f'      <rect x="{zx}" y="60" width="400" height="290" rx="8" fill="rgba(31,32,35,0.02)" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
    b += f'      <rect x="{zx+14}" y="64" width="150" height="12" rx="2" fill="{PAPER}"/><text x="{zx+22}" y="73" fill="{ACC}" font-size="7" font-family="{MONO}" letter-spacing="0.14em">torch.cat · 새 storage</text>\n'
    # emb (32,3,2) -> three slices -> cat -> (32,6) new storage
    ex = zx + 30; ey = 110
    b += f'      <text x="{ex}" y="{ey-10}" fill="{INK}" font-size="11" font-weight="600" font-family="{SANS}">emb (n, 3, 2)</text>\n'
    for j in range(3):
        for i in range(2):
            b += f'      <rect x="{ex+(j*2+i)*c}" y="{ey}" width="{c}" height="{c}" fill="#ffffff" stroke="{INK}" stroke-width="0.8"/>\n'
        b += f'      <text x="{ex+j*2*c+c}" y="{ey+c+12}" fill="{SOFT}" font-size="8" font-family="{MONO}" text-anchor="middle">{j}</text>\n'
    b += f'      <text x="{ex}" y="{ey+c+28}" fill="{SOFT}" font-size="8" font-family="{MONO}">한 행 = emb[:, j, :] 세 조각 (j = 0, 1, 2), 각 2칸</text>\n'
    # cat result
    ry = 210
    b += f'      <text x="{ex}" y="{ry-10}" fill="{INK}" font-size="11" font-weight="600" font-family="{SANS}">torch.cat(torch.unbind(emb, 1), 1) → (n, 6)</text>\n'
    for k in range(6):
        b += f'      <rect x="{ex+k*c}" y="{ry}" width="{c}" height="{c}" fill="{ACCT}" stroke="{ACC}" stroke-width="0.8"/>\n'
    b += f'      <text x="{ex}" y="{ry+c+14}" fill="{SOFT}" font-size="8" font-family="{MONO}">값은 emb.view(-1, 6)과 같지만 메모리를 새로 잡는다</text>\n'
    b += f'      <text x="{ex}" y="{ry+c+40}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">emb 한 행의 storage는 이미 [x0 y0 x1 y1 x2 y2] 순서라</text>\n'
    b += f'      <text x="{ex}" y="{ry+c+54}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">view(-1, 6)만으로 "이어 붙이기"가 된다. 복사가 필요 없다.</text>\n'
    b += f'      <text x="{ex}" y="{ry+c+80}" fill="{SOFT}" font-size="8" font-family="{MONO}">(32,3,2) → (32,6) · 원소 수 같음 → view 허용</text>\n'
    # rule strip
    ly = 402
    b += f'      <line x1="40" y1="{ly-10}" x2="{W-40}" y2="{ly-10}" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
    b += f'      <text x="40" y="{ly+6}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">VIEW RULE</text>\n'
    b += f'      <text x="40" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">연속(contiguous) 텐서는 원소 수만 같으면 view할 수 있고 storage offset · shape · stride만 바뀐다. 전치 등으로 stride가 꼬이면 새 shape이 stride와 호환돼야 한다. -1은 추론.</text>\n'
    b += f'      <text x="{W-40}" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}" font-style="italic" text-anchor="end">Karpathy가 권한 참고: ezyang, PyTorch internals (2019)</text>\n'
    html = page('makemore 2 · view와 storage', 'Tensor internals · makemore 2', 'view는 같은 메모리를 다르게 읽는다', 'view',
                'torch.Tensor의 storage와 view', '18개 숫자가 든 1차원 storage 하나를 (2,9), (9,2), (3,3,2)로 다르게 읽는 view 세 개. 모두 같은 메모리를 가리키고 shape과 stride만 다르다. 오른쪽은 torch.cat이 새 storage를 만드는 대비.', b, W, H)
    open(os.path.join(HERE, 'view.html'), 'w', encoding='utf-8').write(html)
    return H

if __name__ == '__main__':
    print('mlp H=', mlp()); print('view H=', view())
