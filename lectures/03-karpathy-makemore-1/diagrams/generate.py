"""makemore Part 1 다이어그램 2장 (diagram-design 스킬, 프로젝트 monochrome 스킨).
실행: python3 generate.py  (같은 폴더에 *.html 생성. PNG export는 headless Chrome으로 별도 수행)
1. two-roads.html   — Architecture: counting 경로와 gradient 경로가 같은 bigram 모델에 도달
2. broadcasting.html — tensor-shape view: keepdim 유무에 따라 행 정규화가 열 정규화로 바뀌는 버그
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

# ---------------------------------------------------------------- 1. two roads
def two_roads():
    W, H = 1080, 470
    b = ''
    # zones (painted first)
    for (zy, zh, name) in [(78, 108, 'COUNTING · 세고 나눈다'), (236, 160, 'GRADIENT · 예측하고 고친다')]:
        b += f'      <rect x="230" y="{zy}" width="826" height="{zh}" rx="8" fill="rgba(31,32,35,0.02)" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
        b += f'      <rect x="244" y="{zy+4}" width="{len(name)*6.4+16:.0f}" height="12" rx="2" fill="{PAPER}"/>\n'
        b += f'      <text x="{252}" y="{zy+13}" fill="rgba(31,32,35,0.45)" font-size="7" font-family="{MONO}" letter-spacing="0.14em">{name}</text>\n'
    # geometry
    IN = (40, 166, 150, 48)                      # input node, center y=190
    N_ = (380, 110, 170, 48); P_ = (710, 110, 150, 48)
    OH = (250, 270, 100, 48); LG = (410, 270, 110, 48); CT = (580, 270, 90, 48); PR = (730, 270, 110, 48); LS = (900, 270, 140, 48)
    # arrows before nodes
    # input -> N (up), input -> one-hot (down): fanned attach points on the input's right edge
    mid1 = 285
    b += f'      <path d="M 190,178 H {mid1-8} Q {mid1},178 {mid1},170 V 142 Q {mid1},134 {mid1+8},134 H 380" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    mid2 = 220
    b += f'      <path d="M 190,202 H {mid2-8} Q {mid2},202 {mid2},210 V 286 Q {mid2},294 {mid2+8},294 H 250" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += label(mid1+52, 122, 'N[x, y] += 1')
    b += label(178, 250, 'F.one_hot', w=60)
    # counting row
    b += harrow(550, 710, 134)
    b += label(630, 122, '(N+1) / rowsum · keepdim')
    # gradient row
    b += harrow(350, 410, 294); b += label(380, 282, '@ W', w=34)
    b += harrow(520, 580, 294); b += label(550, 282, '.exp()', w=44)
    b += harrow(670, 730, 294); b += label(700, 282, '/ rowsum', w=52)
    b += harrow(840, 900, 294); b += label(870, 282, '−log p[y]', w=54)
    # return arrow loss -> W (logits node), below the row
    b += f'      <path d="M 970,318 V 344 Q 970,352 962,352 H 473 Q 465,352 465,344 V 318" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#arrow)"/>\n'
    b += label(707, 368, 'loss.backward() · W.data += −50 · W.grad · 100회 반복', w=270)
    # equivalence links (vertical, same x)
    b += f'      <line x1="465" y1="158" x2="465" y2="270" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4,3"/>\n'
    b += label(465, 214, 'W.exp()가 N의 역할', w=110)
    b += f'      <line x1="785" y1="158" x2="785" y2="270" stroke="{ACC}" stroke-width="1" stroke-dasharray="4,3"/>\n'
    b += label(785, 214, '거의 같은 확률표 · 데이터 NLL 2.454 vs 2.475', w=210, color=ACC)
    # nodes
    b += node(*IN, 'bigram (x, y) 쌍', '228,146개 · 32,033 이름', 'input', tag='names.txt')
    b += node(*N_, 'N: 27×27 counts', 'int32 · 행=앞 글자, 열=다음 글자', 'store')
    b += node(*P_, 'P: 27×27 probs', '각 행의 합 = 1', 'focal')
    b += node(*OH, 'one-hot', 'xenc (n, 27)', 'step')
    b += node(*LG, 'logits', 'xenc @ W = W[x]', 'step')
    b += node(*CT, 'counts', 'exp → 양수', 'step')
    b += node(*PR, 'probs', 'softmax', 'focal')
    b += node(*LS, 'loss', 'NLL + 0.01·mean(W²)', 'step')
    # legend
    ly = 420
    b += f'      <line x1="40" y1="{ly-10}" x2="{W-40}" y2="{ly-10}" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
    b += f'      <text x="40" y="{ly+6}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">LEGEND</text>\n'
    b += f'      <rect x="40" y="{ly+16}" width="14" height="10" rx="2" fill="{ACCT}" stroke="{ACC}" stroke-width="1"/><text x="60" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">두 경로의 결과 (다음 글자 확률표)</text>\n'
    b += f'      <rect x="270" y="{ly+16}" width="14" height="10" rx="2" fill="rgba(31,32,35,0.05)" stroke="{MUTED}" stroke-width="0.8"/><text x="290" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">저장된 표 (파라미터)</text>\n'
    b += f'      <line x1="430" y1="{ly+21}" x2="450" y2="{ly+21}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4,3"/><text x="456" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">동치 관계 · 학습 루프의 되돌아가는 화살표</text>\n'
    b += f'      <text x="{W-40}" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}" font-style="italic" text-anchor="end">softmax = exp 후 행 정규화. NLL = 정답 열 probs[arange, y]의 −log 평균.</text>\n'
    html = page('makemore 1 · 두 길, 같은 모델', 'Architecture · makemore 1', '두 길, 같은 모델: counting과 gradient', 'two-roads',
                'bigram 모델에 이르는 두 경로', 'names.txt의 bigram 쌍에서 출발해, 위 경로는 27×27 카운트 N을 세어 행 정규화한 확률표 P를 만들고, 아래 경로는 one-hot 입력을 W에 곱해 logits, exp, 행 정규화(softmax)로 확률을 만들고 NLL loss의 기울기로 W를 100회 갱신한다. 두 결과는 같은 모델이다.', b, W, H)
    open(os.path.join(HERE, 'two-roads.html'), 'w', encoding='utf-8').write(html)
    return H

# ---------------------------------------------------------------- 2. broadcasting
def grid(x, y, n, cell, fill='#ffffff', stroke=MUTED, hl_row=None, hl_col=None, hl_fill=None, hl_stroke=None, ghost=False, rows=None, cols=None):
    s = ''
    for i in range(rows or n):
        for j in range(cols or n):
            f = fill; st = stroke; d = ''
            if ghost: st = 'rgba(31,32,35,0.25)'; d = ' stroke-dasharray="2,2"'; f = 'transparent'
            if (hl_row is not None and i == hl_row) or (hl_col is not None and j == hl_col):
                f = hl_fill; st = hl_stroke
            s += f'      <rect x="{x+j*cell}" y="{y+i*cell}" width="{cell}" height="{cell}" fill="{f}" stroke="{st}" stroke-width="0.8"{d}/>\n'
    return s

def vec(x, y, n, cell, horizontal, fill='rgba(31,32,35,0.05)', stroke=INK):
    s = ''
    for k in range(n):
        xx, yy = (x + k*cell, y) if horizontal else (x, y + k*cell)
        s += f'      <rect x="{xx}" y="{yy}" width="{cell}" height="{cell}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>\n'
    return s

def caption(x, y, text, color=MUTED, size=9, anchor='middle', font=None):
    return f'      <text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-family="{font or MONO}" text-anchor="{anchor}">{text}</text>\n'

def broadcasting():
    W, H = 1080, 470
    n, c = 6, 16   # 27×27을 6×6 축소판으로 그린다
    b = ''
    panels = [
        (40,  'keepdim=True · 맞음',   'P.sum(1, keepdim=True) → (27, 1)', False),
        (560, 'keepdim=False · 버그',  'P.sum(1) → (27,) → 정렬하면 (1, 27)', True),
    ]
    for (px, title, sub, buggy) in panels:
        zx, zw = px, 480
        b += f'      <rect x="{zx}" y="60" width="{zw}" height="300" rx="8" fill="rgba(31,32,35,0.02)" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
        b += f'      <rect x="{zx+14}" y="64" width="{len(title)*6.6+16:.0f}" height="12" rx="2" fill="{PAPER}"/>\n'
        b += f'      <text x="{zx+22}" y="73" fill="{ACC if buggy else "rgba(31,32,35,0.45)"}" font-size="7" font-family="{MONO}" letter-spacing="0.14em">{title}</text>\n'
        gy = 110
        # operand A: 27×27
        ax = zx + 30
        b += grid(ax, gy, n, c)
        b += caption(ax + n*c/2, gy + n*c + 16, 'P: (27, 27)')
        # ÷
        b += caption(ax + n*c + 26, gy + n*c/2 + 5, '÷', INK, 16, font=SANS)
        # operand B: divisor
        bx = ax + n*c + 52
        if not buggy:
            b += vec(bx, gy, n, c, horizontal=False)
            b += grid(bx + c, gy, n, c, ghost=True, cols=n-1)   # copied to the right
            # ghost region only n-1 columns wide: cover the first (real) column by drawing ghost from bx+c
            b += caption(bx + n*c/2, gy + n*c + 16, '(27, 1) → 가로로 복사')
            b += caption(bx + n*c/2, gy + n*c + 30, '행마다 자기 행의 합', SOFT, 8)
        else:
            b += vec(bx, gy, n, c, horizontal=True, stroke=ACC, fill=ACCT)
            b += grid(bx, gy + c, n, c, ghost=True, rows=n-1)   # copied downward
            b += caption(bx + n*c/2, gy + n*c + 16, '(1, 27) → 세로로 복사', ACC)
            b += caption(bx + n*c/2, gy + n*c + 30, '한 벡터가 모든 행에 재사용', SOFT, 8)
        # =
        b += caption(bx + n*c + 26, gy + n*c/2 + 5, '=', INK, 16, font=SANS)
        # result
        rx = bx + n*c + 52
        if not buggy:
            b += grid(rx, gy, n, c, hl_row=0, hl_fill='rgba(31,32,35,0.08)', hl_stroke=INK)
            b += caption(rx + n*c/2, gy + n*c + 16, 'P[0].sum() = 1.0')
            b += caption(rx + n*c/2, gy + n*c + 30, '행이 확률 분포 (원했던 것)', SOFT, 8)
        else:
            b += grid(rx, gy, n, c, hl_col=0, hl_fill=ACCT, hl_stroke=ACC)
            b += caption(rx + n*c/2, gy + n*c + 16, 'P[:, 0].sum() = 1.0', ACC)
            b += caption(rx + n*c/2, gy + n*c + 30, 'P[0].sum() = 7.02', SOFT, 8)
        b += caption(zx + zw/2, 300, sub, INK, 9)
        b += caption(zx + zw/2, 318, 'shape가 맞으니 에러 없이 실행된다' if buggy else 'P[i, j] / rowsum[i]', SOFT, 8)
        b += caption(zx + zw/2, 340, '(27,)를 오른쪽 정렬하면 (1,27): 열 방향으로 복사되어 P[i, j] / rowsum[j]가 된다' if buggy else '27×27 ÷ 27×1: 오른쪽부터 27 vs 1(복사), 27 vs 27(같음) → 허용', SOFT, 8)
    # rule strip
    ry = 400
    b += f'      <line x1="40" y1="{ry-10}" x2="{W-40}" y2="{ry-10}" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
    b += f'      <text x="40" y="{ry+6}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">BROADCASTING RULE</text>\n'
    b += f'      <text x="40" y="{ry+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">shape를 오른쪽 끝부터 맞춰 보며, 각 자리가 같거나 · 한쪽이 1이거나 · 한쪽에 없으면 허용. 1이거나 없는 쪽은 그 방향으로 복사된다.</text>\n'
    b += f'      <text x="{W-40}" y="{ry+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}" font-style="italic" text-anchor="end">6×6은 27×27의 축소판. 결과의 진한 줄 = 합이 1이 되는 방향.</text>\n'
    html = page('makemore 1 · broadcasting과 keepdim', 'Tensor shapes · makemore 1', 'keepdim 하나로 행 정규화가 열 정규화가 된다', 'broadcasting',
                'keepdim 유무에 따른 broadcasting 방향', '왼쪽: 27×27 행렬을 (27,1) 열벡터로 나누면 열벡터가 가로로 복사되어 각 행이 정규화된다. 오른쪽: keepdim 없이 (27,) 벡터로 나누면 (1,27) 행벡터로 정렬되어 세로로 복사되고, 각 열이 정규화되어 P[0].sum()이 7.02가 된다.', b, W, H)
    open(os.path.join(HERE, 'broadcasting.html'), 'w', encoding='utf-8').write(html)
    return H

if __name__ == '__main__':
    print('two-roads H=', two_roads()); print('broadcasting H=', broadcasting())
