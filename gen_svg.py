import math, random, os
random.seed(7)
gd = lambda: [random.gauss(0, 1) for _ in range(3)]

def sh(x, y, z):
    n = math.sqrt(x*x + y*y + z*z); x, y, z = x/n, y/n, z/n
    r = 1 + .045*math.sin(7*x+1.3)*math.sin(8*y+.7)*math.sin(7*z+2.1) - .16*math.exp(-(x/.1)**2)*max(0, y)
    return (x*r*1.7, y*(.6 if y < 0 else .78)*r*1.7, z*1.3*r*1.7)

def cb(x, y, z):
    n = math.sqrt(x*x + y*y + z*z)
    return (x/n*.8, y/n*.45-1.2, z/n*.6-1.5)

def pr(p, ya=.55, pa=.12):
    x, y, z = p
    x, z = x*math.cos(ya) + z*math.sin(ya), -x*math.sin(ya) + z*math.cos(ya)
    y, z = y*math.cos(pa) - z*math.sin(pa), y*math.sin(pa) + z*math.cos(pa)
    s = 7.5/(7.5 - z)
    return (400 + x*s*125, 260 - y*s*125, z)

def hull(P):
    P = sorted(set(P))
    cr = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    out = []
    for seq in (P, P[::-1]):
        h = []
        for p in seq:
            while len(h) > 1 and cr(h[-2], h[-1], p) <= 0:
                h.pop()
            h.append(p)
        out += h[:-1]
    return out

def path(h):
    return 'M' + ' L'.join('%.1f %.1f' % p for p in h) + 'Z'

pts = [tuple(c*(.8 + .2*random.random()) for c in sh(*gd())) for _ in range(230)] + [cb(*gd()) for _ in range(36)]
Q = [pr(p) for p in pts]
E = set()
for i, a in enumerate(pts):
    for j in sorted(range(len(pts)), key=lambda j: sum((a[k]-pts[j][k])**2 for k in range(3)))[1:4]:
        E.add((min(i, j), max(i, j)))

B = {0: [], 1: [], 2: []}
for i, j in E:
    z = (Q[i][2] + Q[j][2]) / 2
    B[0 if z > .5 else 1 if z > -.5 else 2].append('M%.1f %.1fL%.1f %.1f' % (Q[i][0], Q[i][1], Q[j][0], Q[j][1]))
lines = ''.join('<path d="%s" stroke="url(#g)" stroke-width="%s" opacity="%s" fill="none"/>' % (''.join(B[k]), w, o)
                for k, w, o in ((2, .6, .2), (1, .7, .38), (0, .9, .6)))

cortex = hull([pr(sh(*gd()))[:2] for _ in range(1500)])
cere = hull([pr(cb(*gd()))[:2] for _ in range(400)])

maj = set(random.sample(range(len(pts)), 29))
dots = ''
for i, q in enumerate(Q):
    col = '#38bdf8' if q[0] < 400 else '#a78bfa'
    if i in maj:
        dots += '<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s" class="p p%d" filter="url(#b)"/>' % (q[0], q[1], col, i % 4)
    else:
        dots += '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" class="p p%d" opacity="%.2f"/>' % (
            q[0], q[1], 1.1 + .5*(q[2] > 0), col, i % 4, .5 + .1*(q[2] > 0))

E_list = list(E)
parts = ''
for _ in range(14):
    i, j = random.choice(E_list)
    parts += '<circle r="1.9" fill="#e0f7ff"><animateMotion dur="%.1fs" begin="-%.1fs" repeatCount="indefinite" path="M%.1f %.1fL%.1f %.1f"/></circle>' % (
        1.6 + 2*random.random(), 3*random.random(), Q[i][0], Q[i][1], Q[j][0], Q[j][1])

# ── Permanent skill labels ──────────────────────────────────────────────────
# Brain center ≈ (400, 260); brain spans x≈185–625, y≈95–435
# viewBox 800 × 560

def label(x, y, text, col, dot_x, dot_y, conn_x2, conn_y2, anchor='start'):
    """Render a skill label with dot + connector + text."""
    out = ''
    # connector line
    out += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.6" opacity="0.35"/>' % (
        dot_x, dot_y, conn_x2, conn_y2, col)
    # pulsing dot
    out += '<circle cx="%.1f" cy="%.1f" r="2.8" fill="%s" class="p" filter="url(#b)"/>' % (dot_x, dot_y, col)
    # text
    out += '<text x="%.1f" y="%.1f" fill="%s" font-family="ui-monospace,\'JetBrains Mono\',Consolas,monospace" font-size="9" font-weight="700" letter-spacing="0.09em" text-anchor="%s">%s</text>' % (
        x, y + 3.5, col, anchor, text)
    return out

L = ''

# ── TOP: AGENTIC (4) — #60a5fa ──
c = '#60a5fa'
# brain top approx y=98; labels at y=28, connector goes down to brain top
agentic = [('AI AGENTS', 155), ('MULTI-AGENT SYSTEMS', 295), ('TOOL CALLING', 480), ('MCP', 625)]
for txt, cx in agentic:
    bx = cx  # connector x on brain top (approx)
    by = 102
    L += label(cx, 20, txt, c, cx, 32, bx, by, 'middle')

# ── LEFT: MACHINE LEARNING (5) — #38bdf8 ──
c = '#38bdf8'
ml = ['MACHINE LEARNING', 'DEEP LEARNING', 'PYTORCH', 'TENSORFLOW', 'SCIKIT-LEARN']
for i, txt in enumerate(ml):
    dy = 148 + i * 30
    bx, by = 198, dy  # connector to brain left edge
    L += label(170, dy - 4, txt, c, 178, dy, bx, by, 'end')

# ── RIGHT: GENERATIVE AI (6) — #a78bfa ──
c = '#a78bfa'
gen = ['LARGE LANG. MODELS', 'GENERATIVE AI', 'RAG', 'LLM FINE-TUNING', 'HUGGING FACE', 'LANGCHAIN']
for i, txt in enumerate(gen):
    dy = 128 + i * 32
    bx, by = 622, dy
    L += label(630, dy - 4, txt, c, 622, dy, bx, by, 'start')

# ── BOTTOM-LEFT: PYTHON / BACKEND (4) — #c084fc ──
c = '#c084fc'
eng = ['PYTHON', 'FASTAPI', 'SQL', 'REST APIs']
for i, txt in enumerate(eng):
    dy = 460 + i * 20
    bx, by = 310, 435
    L += label(50, dy - 4, txt, c, 50, dy, bx, by, 'start')

# ── BOTTOM-RIGHT: COMPUTER VISION (4) — #22d3ee ──
c = '#22d3ee'
cv = ['YOLOV8', 'OPENCV', 'VISION TRANSFORMERS', 'OBJECT DETECTION']
for i, txt in enumerate(cv):
    dy = 460 + i * 20
    bx, by = 490, 435
    L += label(560, dy - 4, txt, c, 560, dy, bx, by, 'start')

# ── BOTTOM-CENTER: CLOUD / MLOPS (6) — #38bdf8 ──
c = '#38bdf8'
cloud = ['AWS', 'AWS BEDROCK', 'DOCKER', 'KUBERNETES', 'CI/CD', 'MLOPS']
cloud_xs = [60, 155, 258, 360, 455, 540]
for txt, cx in zip(cloud, cloud_xs):
    by = 435
    L += label(cx, 548, txt, c, cx, 550, cx, by, 'start')

# ── Divider lines ──
dividers = ''
dividers += '<line x1="40" y1="445" x2="310" y2="445" stroke="#1e293b" stroke-width="0.5"/>'
dividers += '<line x1="490" y1="445" x2="755" y2="445" stroke="#1e293b" stroke-width="0.5"/>'
dividers += '<line x1="40" y1="542" x2="620" y2="542" stroke="#1e293b" stroke-width="0.5"/>'

# Section tags (always visible)
tags = ''
tag_data = [
    (90, 435, 'ML', '#38bdf8'),
    (640, 435, 'GEN AI', '#a78bfa'),
    (90, 542, 'CLOUD / MLOPS', '#38bdf8'),
]
for tx, ty, ttxt, tc in tag_data:
    tags += '<text x="%d" y="%d" fill="%s" font-family="ui-monospace,Consolas,monospace" font-size="7.5" font-weight="600" letter-spacing="0.14em" opacity="0.45">%s</text>' % (tx, ty, tc, ttxt)

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" width="800" height="560" role="img" aria-label="Animated neural brain — Shabil Ahmed AI/ML skill map"><style>.fl{animation:fl 6s ease-in-out infinite}@keyframes fl{50%%{transform:translateY(-8px)}}.p{animation:pu 3s ease-in-out infinite}.p1{animation-delay:-.8s}.p2{animation-delay:-1.6s}.p3{animation-delay:-2.3s}@keyframes pu{50%%{opacity:.3}}@media(prefers-reduced-motion:reduce){.fl,.p{animation:none}}</style>
<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="200" y1="0" x2="600" y2="0"><stop offset="0" stop-color="#38bdf8"/><stop offset=".55" stop-color="#6d8cf8"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
<radialGradient id="r" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#38bdf8" stop-opacity=".02"/><stop offset=".8" stop-color="#38bdf8" stop-opacity=".07"/><stop offset="1" stop-color="#8b5cf6" stop-opacity=".2"/></radialGradient>
<filter id="b" x="-200%%" y="-200%%" width="500%%" height="500%%"><feGaussianBlur stdDeviation="2.6" result="s"/><feMerge><feMergeNode in="s"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g class="fl"><path d="%s" fill="url(#r)" stroke="url(#g)" stroke-width="1.2" opacity=".7" stroke-linejoin="round"/><path d="%s" fill="url(#r)" stroke="url(#g)" stroke-width="1.4" stroke-linejoin="round" filter="url(#b)" opacity=".85"/>%s%s%s</g>
%s%s%s</svg>''' % (path(cere), path(cortex), lines, dots, parts, L, dividers, tags)

os.makedirs('assets', exist_ok=True)
open('assets/ai-brain.svg', 'w').write(svg)
print('Wrote assets/ai-brain.svg', len(svg), 'bytes')
