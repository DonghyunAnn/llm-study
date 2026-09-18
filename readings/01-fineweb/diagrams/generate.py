"""FineWeb 처리 단계 깔때기(type-pyramid funnel). 폭은 토큰 수에 비례(정직한 폭 규칙)."""
import os
HERE=os.path.dirname(os.path.abspath(__file__))
PAPER='#f6f5f2'; PAPER2='#ebeae6'; INK='#1f2023'; MUTED='#55595f'; SOFT='#7d8188'; ACC='#b3402a'; ACCT='rgba(179,64,42,0.08)'
SANS="'Geist', 'Noto Sans KR', sans-serif"; MONO="'Geist Mono', monospace"
FONTS='<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&family=Noto+Serif:ital@0;1&family=Noto+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@400&display=swap" rel="stylesheet">'
layers=[  # (단계, 결과 토큰 수(T), 표시 문자열, 비고)
    ('기본 필터', 36, '36T', 'URL 차단 · 영어 ≥ 0.65 · MassiveText'),
    ('크롤별 독립 MinHash', 20, '20T', '−44% · 통합 dedup(4T)은 dedup 안 한 것과 차이 없음'),
    ('C4 필터 + 자체 필터 3개', 15, '15T', '−25% · 자체 필터 3개는 2019-18 실험에서 약 22%'),
    ('Edu 분류기 ≥ 3점', 1.3, '1.3T', '−92% · 2점 기준은 5.4T'),
]
W=1000; cx=400; maxw=560; LH=64; top=72
def width(t): return max(maxw*t/36, 16)
b=''
b+=f'      <text x="40" y="{top-16}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">DROP-OFF ↓ · 각 층의 아래 폭 = 그 단계 뒤 남는 토큰 수 (GPT-2 tokenizer)</text>\n'
prev=None
for i,(name,t,label,note) in enumerate(layers):
    y=top+i*LH; wb=width(t); wt=width(prev) if prev is not None else wb
    focal=(i==len(layers)-1)
    pts=f'{cx-wt/2:.1f},{y} {cx+wt/2:.1f},{y} {cx+wb/2:.1f},{y+LH} {cx-wb/2:.1f},{y+LH}'
    b+=f'      <polygon points="{pts}" fill="{ACCT if focal else PAPER2}" stroke="{ACC if focal else MUTED}" stroke-width="1"/>\n'
    wmid=(wt+wb)/2
    if wmid>160:
        b+=f'      <text x="{cx}" y="{y+LH/2-2}" fill="{INK}" font-size="12" font-weight="600" font-family="{SANS}" text-anchor="middle">{name}</text>\n'
        b+=f'      <text x="{cx}" y="{y+LH/2+13}" fill="{MUTED}" font-size="10" font-family="{MONO}" text-anchor="middle">→ {label}</text>\n'
        b+=f'      <text x="{cx+maxw/2+24}" y="{y+LH/2+4}" fill="{SOFT}" font-size="9" font-family="{MONO}">{note}</text>\n'
    else:
        b+=f'      <text x="{cx+maxw/2+24}" y="{y+LH/2-2}" fill="{ACC if focal else INK}" font-size="12" font-weight="600" font-family="{SANS}">{name} → {label}</text>\n'
        b+=f'      <text x="{cx+maxw/2+24}" y="{y+LH/2+13}" fill="{SOFT}" font-size="9" font-family="{MONO}">{note}</text>\n'
    prev=t
# source annotation
ly=top+len(layers)*LH+40
b+=f'      <line x1="40" y1="{ly-8}" x2="{W-40}" y2="{ly-8}" stroke="rgba(31,32,35,0.10)" stroke-width="0.8"/>\n      <text x="40" y="{ly+8}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">LEGEND</text>\n'
b+=f'      <rect x="40" y="{ly+18}" width="14" height="10" rx="2" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1"/><text x="60" y="{ly+26}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">FineWeb 단계 (결과 토큰 수)</text>\n'
b+=f'      <rect x="260" y="{ly+18}" width="14" height="10" rx="2" fill="{ACCT}" stroke="{ACC}" stroke-width="1"/><text x="280" y="{ly+26}" fill="{MUTED}" font-size="8.5" font-family="{SANS}">FineWeb-Edu · 최종 1.3T</text>\n'
b+=f'      <text x="{W-40}" y="{ly+26}" fill="{MUTED}" font-size="8.5" font-family="{SANS}" font-style="italic" text-anchor="end">입력: Common Crawl 96개 크롤(WARC → trafilatura). 기본 필터 전, 추출 직후, C4 직후의 토큰 수는 보고서에 없음</text>\n'
H=ly+48
html=f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>FineWeb 처리 단계 깔때기</title>{FONTS}
<style>*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}:root{{--color-paper:{PAPER};--color-ink:{INK};--color-muted:{MUTED};--color-accent:{ACC};--font-sans:'Geist','Noto Sans KR',system-ui,sans-serif;--font-serif:'Instrument Serif','Noto Serif KR',serif;--font-mono:'Geist Mono',ui-monospace,monospace}}
body{{font-family:var(--font-sans);background:var(--color-paper);color:var(--color-ink);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:3rem 2rem}}.frame{{max-width:1200px;width:100%}}.eyebrow{{font-family:var(--font-mono);font-size:.66rem;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--color-muted);margin-bottom:.5rem}}h1{{font-family:var(--font-serif);font-size:clamp(1.5rem,2.4vw + .75rem,2rem);font-weight:400;letter-spacing:-.02em;line-height:1.15;color:var(--color-ink);margin-bottom:1.5rem}}svg{{width:100%;min-width:900px;display:block}}</style></head>
<body><div class="frame"><p class="eyebrow">Funnel · FineWeb</p><h1>웹 36조 토큰이 1.3조가 되기까지</h1>
    <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="recipe-funnel-title recipe-funnel-desc">
      <title id="recipe-funnel-title">FineWeb 처리 단계와 남는 토큰 수</title>
      <desc id="recipe-funnel-desc">기본 필터 후 36조 토큰이 크롤별 MinHash로 20조, C4와 자체 필터로 15조, 교육 분류기로 1.3조 토큰이 되는 깔때기.</desc>
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{MUTED}"/></marker>
        <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{ACC}"/></marker>
        <marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#4a5a6e"/></marker>
      </defs>
      <rect width="100%" height="100%" fill="{PAPER}"/>
{b}    </svg></div></body></html>
'''
open(os.path.join(HERE,'recipe-funnel.html'),'w',encoding='utf-8').write(html); print('H=',H)
