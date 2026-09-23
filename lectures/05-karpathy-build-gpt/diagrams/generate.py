"""Let's build GPT 다이어그램 2장 (diagram-design 스킬, 프로젝트 monochrome 스킨).
실행: python3 generate.py  (같은 폴더에 *.html 생성. PNG export는 headless Chrome으로 별도 수행)
1. decoder-block.html — Architecture: 강의의 decoder-only Transformer (pre-norm block × n_layer), adapted from Vaswani et al. 2017 Fig. 1
2. attention-head.html — Data flow: self-attention head 하나의 텐서 흐름 (q·kᵀ/√d → causal mask → softmax → @v)
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


# ---------------------------------------------------------------- 1. decoder block
def decoder():
    W, H = 1080, 560
    b = ''
    # left column: whole model (top to bottom); right: one block zoomed
    # model column nodes (x=60..300)
    MX, MW = 60, 240
    TOK = (30, 70, 150, 44); POS = (200, 70, 150, 44); BLK = (MX, 220, MW, 60); LNF = (MX, 320, MW, 44); HEAD = (MX, 380, MW, 44); LOSS = (MX, 440, MW, 44)
    # arrows down the column (vertical, same x)
    cx = MX + MW/2
    def varrow(y1, y2, color=MUTED, dashed=False, marker='arrow'):
        d = ' stroke-dasharray="4,3"' if dashed else ''
        return f'      <line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" stroke="{color}" stroke-width="1.2"{d} marker-end="url(#{marker})"/>\n'
    b += f'      <path d="M 105,114 V 146 Q 105,154 113,154 H {cx-14}" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += f'      <path d="M 275,114 V 146 Q 275,154 267,154 H {cx+14}" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += f'      <circle cx="{cx}" cy="154" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="1"/><text x="{cx}" y="158" fill="{INK}" font-size="12" font-family="{SANS}" text-anchor="middle">+</text>\n'
    b += varrow(163, 220); b += label(cx+62, 192, 'x (B,T,C)', w=60)
    b += varrow(280, 320); b += label(cx+70, 300, '× n_layer', w=60)
    b += varrow(364, 380); b += varrow(424, 440)
    # zoom link from BLK to right panel (dashed)
    b += f'      <path d="M {MX+MW},250 H 352 Q 360,250 360,242 V 78 Q 360,70 368,70 H 400" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4,3" marker-end="url(#arrow)"/>\n'
    b += label(322, 160, 'Block 하나', w=56)
    # right panel: zone for a block (x 400..1040)
    ZX, ZY, ZW, ZH = 400, 50, 640, 420
    b += f'      <rect x="{ZX}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="rgba(31,32,35,0.02)" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
    b += f'      <rect x="{ZX+14}" y="{ZY+4}" width="330" height="12" rx="2" fill="{PAPER}"/><text x="{ZX+22}" y="{ZY+13}" fill="rgba(31,32,35,0.45)" font-size="7" font-family="{MONO}" letter-spacing="0.14em">BLOCK · 통신(attention) 뒤 계산(feed-forward) · pre-norm</text>\n'
    # residual pathway: vertical line at rx from top to bottom of zone, with two "+" nodes
    RX = 480
    b += f'      <line x1="{RX}" y1="{ZY+40}" x2="{RX}" y2="{ZY+ZH-30}" stroke="{ACC}" stroke-width="1.6" marker-end="url(#arrow-accent)"/>\n'
    b += label(RX+72, ZY+52, 'residual pathway  x', w=110, color=ACC)
    # branch 1: ln1 -> MHA -> back to + at y=200
    L1 = (600, 100, 130, 40); SA = (600, 160, 200, 48); L2 = (600, 270, 130, 40); FF = (600, 330, 200, 48)
    # fork out from residual at y=120 to ln1 (horizontal), then down through SA, then back to residual at plus y=220
    b += f'      <line x1="{RX}" y1="{120}" x2="600" y2="120" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += f'      <line x1="665" y1="140" x2="665" y2="160" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += f'      <path d="M 665,208 V 232 Q 665,240 657,240 H {RX+14}" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += f'      <circle cx="{RX}" cy="240" r="9" fill="{PAPER}" stroke="{ACC}" stroke-width="1.2"/><text x="{RX}" y="244" fill="{ACC}" font-size="12" font-family="{SANS}" text-anchor="middle">+</text>\n'
    b += f'      <line x1="{RX}" y1="{290}" x2="600" y2="290" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += f'      <line x1="665" y1="310" x2="665" y2="330" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += f'      <path d="M 665,378 V 402 Q 665,410 657,410 H {RX+14}" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += f'      <circle cx="{RX}" cy="410" r="9" fill="{PAPER}" stroke="{ACC}" stroke-width="1.2"/><text x="{RX}" y="414" fill="{ACC}" font-size="12" font-family="{SANS}" text-anchor="middle">+</text>\n'
    b += label(720, 224, 'proj → dropout', w=90); b += label(720, 394, 'dropout', w=56)
    # nodes
    b += node(*TOK, 'token emb', 'idx → (B,T,C) · 65×384', 'store', tag='INPUT · 앞 글자 T개 (≤ 256)')
    b += node(*POS, 'position emb', 'arange(T) → (T,C) · 256×384'.replace('arange(T) → ',''), 'store', tag='POSITION')
    b += node(*BLK, 'Block × 6', '통신 + 계산 · 384-dim · 6 heads', 'step')
    b += node(*LNF, 'LayerNorm (ln_f)', '', 'step')
    b += node(*HEAD, 'lm_head', 'Linear 384 → 65 logits', 'store')
    b += node(*LOSS, 'cross_entropy', '(B·T, 65) vs targets', 'focal')
    b += node(*L1, 'LayerNorm ln1', '', 'step')
    b += node(*SA, 'MultiHeadAttention', '6 heads × head_size 64 · causal', 'focal')
    b += node(*L2, 'LayerNorm ln2', '', 'step')
    b += node(*FF, 'FeedForward', 'Linear 384→1536 · ReLU · →384', 'step')
    # side notes in the zone
    b += f'      <text x="840" y="110" fill="{SOFT}" font-size="8.5" font-family="{SANS}">토큰끼리 정보를 주고받는 유일한 곳.</text>\n'
    b += f'      <text x="840" y="124" fill="{SOFT}" font-size="8.5" font-family="{SANS}">과거만 본다(tril mask).</text>\n'
    b += f'      <text x="840" y="340" fill="{SOFT}" font-size="8.5" font-family="{SANS}">토큰마다 독립 계산.</text>\n'
    b += f'      <text x="840" y="354" fill="{SOFT}" font-size="8.5" font-family="{SANS}">안쪽 폭 4× (논문 512→2048).</text>\n'
    b += f'      <text x="{ZX+ZW-14}" y="{ZY+ZH-12}" fill="{SOFT}" font-size="8" font-family="{MONO}" text-anchor="end">x = x + sa(ln1(x)); x = x + ffwd(ln2(x))</text>\n'
    # legend
    ly = 512
    b += f'      <line x1="40" y1="{ly-10}" x2="{W-40}" y2="{ly-10}" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
    b += f'      <text x="40" y="{ly+6}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">LEGEND</text>\n'
    b += f'      <rect x="40" y="{ly+16}" width="14" height="10" rx="2" fill="{ACCT}" stroke="{ACC}" stroke-width="1"/><text x="60" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">이 강의의 핵심 (attention, loss)</text>\n'
    b += f'      <line x1="260" y1="{ly+21}" x2="280" y2="{ly+21}" stroke="{ACC}" stroke-width="1.6"/><text x="286" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">residual pathway · 기울기 고속도로</text>\n'
    b += f'      <text x="{W-40}" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}" font-style="italic" text-anchor="end">Adapted from Vaswani et al. 2017, Figure 1 (decoder 쪽만, cross-attention 없음, pre-norm). 크기는 gpt.py 최종값.</text>\n'
    html = page('Let\'s build GPT · decoder-only Transformer', 'Architecture · Let\'s build GPT', 'Decoder-only Transformer: 통신과 계산을 번갈아 6번', 'decoder-block',
                '강의의 GPT 구조', '왼쪽은 토큰 임베딩과 위치 임베딩을 더해 Block 6개, 최종 LayerNorm, lm_head, cross entropy로 가는 전체 흐름. 오른쪽은 Block 하나를 확대한 것으로, residual pathway에서 갈라져 LayerNorm → multi-head attention → 다시 더하고, LayerNorm → feed-forward → 다시 더한다.', b, W, H)
    open(os.path.join(HERE, 'decoder-block.html'), 'w', encoding='utf-8').write(html)
    return H

# ---------------------------------------------------------------- 2. attention head
def attention():
    W, H = 1080, 520
    b = ''
    X = (40, 190, 120, 48)
    Q = (230, 90, 130, 44); K = (230, 190, 130, 44); V = (230, 290, 130, 44)
    S = (430, 140, 150, 48); M = (650, 140, 130, 48); SM = (850, 140, 130, 48); O = (850, 290, 150, 48)
    # x -> q,k,v (fan out from right edge of X at three attach points)
    b += f'      <path d="M 160,202 H 187 Q 195,202 195,194 V 120 Q 195,112 203,112 H 230" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += harrow(160, 230, 214)
    b += f'      <path d="M 160,226 H 187 Q 195,226 195,234 V 304 Q 195,312 203,312 H 230" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    # q,k -> scores
    b += f'      <path d="M 360,112 H 387 Q 395,112 395,120 V 152 Q 395,160 403,160 H 430" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += f'      <path d="M 360,212 H 387 Q 395,212 395,204 V 176 Q 395,168 403,168 H 430" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>\n'
    b += harrow(580, 650, 164); b += label(615, 152, 'mask', w=36)
    b += harrow(780, 850, 164); b += label(815, 152, 'dim=-1', w=44)
    b += label(970, 262, 'dropout', w=50)
    # softmax -> out (down), v -> out (right)
    b += f'      <line x1="915" y1="188" x2="915" y2="290" stroke="{ACC}" stroke-width="1.2" marker-end="url(#arrow-accent)"/>\n'
    b += label(970, 240, 'wei (B,T,T)', w=76, color=ACC)
    b += harrow(360, 850, 314); b += label(605, 302, 'v (B,T,hs) · "관심 있으면 이걸 줄게"', w=200)
    # nodes
    b += node(*X, 'x', '(B,T,C) · 사적 정보', 'input')
    b += node(*Q, 'q = query(x)', '"내가 찾는 것" (B,T,hs)', 'step')
    b += node(*K, 'k = key(x)', '"내가 가진 것" (B,T,hs)', 'step')
    b += node(*V, 'v = value(x)', '"줄 것" (B,T,hs)', 'step')
    b += node(*S, 'q @ kᵀ · hs^-0.5', 'affinity (B,T,T)', 'step')
    b += node(*M, 'masked_fill', 'tril==0 → −inf', 'step')
    b += node(*SM, 'softmax', '행마다 합 1 · 과거 가중치', 'focal')
    b += node(*O, 'out = wei @ v', '(B,T,hs) · 가중 평균', 'focal')
    # mini matrix illustration of wei for T=4 below
    mx, my, c = 430, 344, 20
    vals = [[1,0,0,0],[.5,.5,0,0],[.33,.33,.33,0],[.25,.25,.25,.25]]
    b += f'      <text x="{mx}" y="{my-8}" fill="{SOFT}" font-size="7" font-family="{MONO}" letter-spacing="0.14em">WEI · T = 4 · 균등 affinity일 때 (v1–v3의 평균)</text>\n'
    for i in range(4):
        for j in range(4):
            fval = vals[i][j]; fill = f'rgba(179,64,42,{0.05+0.35*fval:.2f})' if fval>0 else '#ffffff'
            b += f'      <rect x="{mx+j*c}" y="{my+i*c}" width="{c}" height="{c}" fill="{fill}" stroke="{MUTED}" stroke-width="0.6"/>\n'
            txt = '0' if fval==0 else ('1' if fval==1 else f'{fval:.2f}'.lstrip('0'))
            b += f'      <text x="{mx+j*c+c/2}" y="{my+i*c+14}" fill="{INK}" font-size="7" font-family="{MONO}" text-anchor="middle">{txt}</text>\n'
    b += f'      <text x="{mx+4*c+10}" y="{my+14}" fill="{SOFT}" font-size="8" font-family="{MONO}">행 t = 토큰 t가 과거에서 얼마나</text>\n'
    b += f'      <text x="{mx+4*c+10}" y="{my+28}" fill="{SOFT}" font-size="8" font-family="{MONO}">위 삼각(미래) = 0 · 학습되면</text>\n'
    b += f'      <text x="{mx+4*c+10}" y="{my+42}" fill="{SOFT}" font-size="8" font-family="{MONO}">행마다 값이 달라진다</text>\n'
    # legend
    ly = 462
    b += f'      <line x1="40" y1="{ly-10}" x2="{W-40}" y2="{ly-10}" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n'
    b += f'      <text x="40" y="{ly+6}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">LEGEND</text>\n'
    b += f'      <rect x="40" y="{ly+16}" width="14" height="10" rx="2" fill="{ACCT}" stroke="{ACC}" stroke-width="1"/><text x="60" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">통신이 일어나는 곳 (가중치 계산, 가중 합)</text>\n'
    b += f'      <rect x="300" y="{ly+16}" width="14" height="10" rx="2" fill="#ffffff" stroke="{INK}" stroke-width="1"/><text x="320" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">토큰마다 독립인 선형 변환 (bias 없음)</text>\n'
    b += f'      <text x="{W-40}" y="{ly+24}" fill="{MUTED}" font-size="8.5" font-family="{SANS}" font-style="italic" text-anchor="end">gpt.py Head.forward · Attention(Q,K,V) = softmax(QKᵀ/√d_k)V (Vaswani et al. 2017, 식 1) + causal mask · hs = head_size</text>\n'
    html = page('Let\'s build GPT · self-attention head', 'Data flow · Let\'s build GPT', 'Self-attention head 하나: 무엇을 찾고, 무엇을 갖고, 무엇을 주나', 'attention-head',
                'self-attention head 하나의 텐서 흐름', '입력 x에서 query, key, value를 각각 선형 변환으로 만들고, q와 k의 내적을 head_size의 제곱근으로 나눠 affinity를 얻고, 미래 위치를 −inf로 가린 뒤 softmax로 행마다 합이 1인 가중치를 만들어 value의 가중 평균을 출력한다.', b, W, H)
    open(os.path.join(HERE, 'attention-head.html'), 'w', encoding='utf-8').write(html)
    return H

if __name__ == '__main__':
    print('decoder H=', decoder()); print('attention H=', attention())
