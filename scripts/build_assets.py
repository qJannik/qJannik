#!/usr/bin/env python3
"""Generates the SVG graphics for the profile README in a dark and a light variant.

Usage:
    python3 scripts/build_assets.py
"""

from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
ORANGE, ORANGE_LIGHT = "#D97757", "#F0A07A"

THEMES = {
    "dark": dict(
        bg=("#0B1220", "#111C33", "#1B2B4B"), glow=("#3B82F6", 0.45, "#06B6D4", 0.28),
        dot=("#FFFFFF", 0.07), title="#F8FAFC", sub="#CBD5E1", muted="#94A3B8",
        card=("#131D33", "#0E1628"), stroke="#24324F", value="#F1F5F9", label=ORANGE_LIGHT,
        win=("#111827", "#0B1220"), winbar="#151F35", txt="#E2E8F0", dim="#64748B", ok="#4ADE80",
        shadow=0.35, outro="#8B96A8", bubble="#F8FAFC", bubble_txt="#1F2937", line=ORANGE,
    ),
    "light": dict(
        bg=("#F8FAFC", "#EEF2F8", "#DDE6F3"), glow=("#93C5FD", 0.55, "#FDBA74", 0.35),
        dot=("#0F172A", 0.06), title="#0F172A", sub="#334155", muted="#64748B",
        card=("#FFFFFF", "#F8FAFC"), stroke="#E2E8F0", value="#0F172A", label=ORANGE,
        win=("#FFFFFF", "#F8FAFC"), winbar="#F1F5F9", txt="#0F172A", dim="#64748B", ok="#16A34A",
        shadow=0.12, outro="#64748B", bubble="#1F2937", bubble_txt="#F8FAFC", line=ORANGE,
    ),
}

CRAB = [
    "..XXXXXXXX..",
    "..XXXXXXXX..",
    "..XEXXXXEX..",
    "XXXEXXXXEXXX",
    "XXXXXXXXXXXX",
    "..XXXXXXXX..",
]
LEGS_A = ["..X.X..X.X..", "..X.X..X.X.."]
LEGS_B = ["..X.X..X.X..", ".X.X....X.X."]


def pixels(rows, unit, chars, y0=0):
    return "".join(
        f"M{x * unit} {(y + y0) * unit}h{unit}v{unit}h-{unit}z"
        for y, row in enumerate(rows) for x, c in enumerate(row) if c in chars
    )


def crab(unit, eye="#1A1A1A", walking=False):
    body = f'<path fill="{ORANGE}" shape-rendering="crispEdges" d="{pixels(CRAB, unit, "XE")}"/>'
    eyes = f'<path fill="{eye}" class="eyes" shape-rendering="crispEdges" d="{pixels(CRAB, unit, "E")}"/>'
    if not walking:
        legs = f'<path fill="{ORANGE}" shape-rendering="crispEdges" d="{pixels(LEGS_A, unit, "X", 6)}"/>'
        return body + legs + eyes
    a = f'<path class="leg-a" fill="{ORANGE}" shape-rendering="crispEdges" d="{pixels(LEGS_A, unit, "X", 6)}"/>'
    b = f'<path class="leg-b" fill="{ORANGE}" shape-rendering="crispEdges" d="{pixels(LEGS_B, unit, "X", 6)}"/>'
    return body + a + b + eyes


ACCENT = f"""<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE_LIGHT}"/>
    </linearGradient>"""

WALK_CSS = """
      .leg-a { animation: legA .36s steps(1) infinite; }
      .leg-b { animation: legB .36s steps(1) infinite; }
      @keyframes legA { 0% { opacity: 1; } 50% { opacity: 0; } }
      @keyframes legB { 0% { opacity: 0; } 50% { opacity: 1; } }"""


def header(t):
    g = t["glow"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg'][0]}"/><stop offset="0.55" stop-color="{t['bg'][1]}"/><stop offset="1" stop-color="{t['bg'][2]}"/>
    </linearGradient>
    <radialGradient id="glow1" cx="0.85" cy="0.15" r="0.55">
      <stop offset="0" stop-color="{g[0]}" stop-opacity="{g[1]}"/><stop offset="1" stop-color="{g[0]}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="0.08" cy="1" r="0.5">
      <stop offset="0" stop-color="{g[2]}" stop-opacity="{g[3]}"/><stop offset="1" stop-color="{g[2]}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="{t['dot'][0]}" fill-opacity="{t['dot'][1]}"/>
    </pattern>
    {ACCENT}
    <clipPath id="round"><rect width="1200" height="340" rx="22"/></clipPath>
    <style>
      .fade {{ opacity: 0; animation: fade 1s ease-out forwards; }}
      .d1 {{ animation-delay: .15s; }} .d2 {{ animation-delay: .4s; }} .d3 {{ animation-delay: .65s; }}
      @keyframes fade {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      .bob {{ animation: bob 2.4s ease-in-out infinite; }}
      @keyframes bob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-6px); }} }}
      .eyes {{ transform-origin: 0 48px; animation: eyes 4s infinite; }}
      @keyframes eyes {{ 0%, 92%, 100% {{ transform: scaleY(1); }} 95% {{ transform: scaleY(0.1); }} }}
      .tw {{ animation: tw 3s ease-in-out infinite; }}
      .t2 {{ animation-delay: 1s; }} .t3 {{ animation-delay: 2s; }}
      @keyframes tw {{ 0%, 100% {{ opacity: .15; }} 50% {{ opacity: .9; }} }}
      .bubble {{ opacity: 0; transform-origin: 890px 112px; animation: bubble 9s ease-in-out 1.5s infinite; }}
      @keyframes bubble {{
        0% {{ opacity: 0; transform: scale(.85); }} 6%, 55% {{ opacity: 1; transform: scale(1); }}
        61%, 100% {{ opacity: 0; transform: scale(.85); }}
      }}
    </style>
  </defs>

  <g clip-path="url(#round)">
    <rect width="1200" height="340" fill="url(#bg)"/>
    <rect width="1200" height="340" fill="url(#dots)"/>
    <rect width="1200" height="340" fill="url(#glow1)"/>
    <rect width="1200" height="340" fill="url(#glow2)"/>

    <ellipse cx="996" cy="262" rx="92" ry="9" fill="#000000" fill-opacity="{t['shadow']}"/>
    <g transform="translate(900,110)"><g class="bob">{crab(16)}</g></g>
    <g fill="{ORANGE_LIGHT}">
      <rect x="860" y="84" width="6" height="6" class="tw"/>
      <rect x="1120" y="70" width="5" height="5" class="tw t2"/>
      <rect x="1140" y="180" width="6" height="6" class="tw t3"/>
      <rect x="845" y="200" width="4" height="4" class="tw t2"/>
    </g>

    <g class="bubble">
      <rect x="640" y="46" width="250" height="48" rx="14" fill="{t['bubble']}"/>
      <path d="M856 93 l22 18 l-4 -18z" fill="{t['bubble']}"/>
      <text x="765" y="77" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="600" fill="{t['bubble_txt']}">Let's build something!</text>
    </g>

    <g class="fade d1">
      <text x="80" y="110" font-family="{MONO}" font-size="22" fill="{t['muted']}">~ $ claude<tspan class="cursor" fill="{ORANGE_LIGHT}"> _</tspan></text>
    </g>
    <g class="fade d2">
      <text x="76" y="196" font-family="{SANS}" font-size="84" font-weight="700" fill="{t['title']}" letter-spacing="-1.5">Jannik</text>
      <rect x="80" y="218" width="96" height="5" rx="2.5" fill="url(#accent)"/>
    </g>
    <g class="fade d3">
      <text x="80" y="268" font-family="{SANS}" font-size="28" font-weight="500" fill="{t['sub']}">Apprentice IT Specialist for System Integration</text>
    </g>
  </g>
</svg>
"""


def cards(t):
    items = [
        ("ROLE", "Apprentice", "System Integration", "🎓"),
        ("LOCATION", "Germany", "Central European Time", "🌍"),
        ("BUILDING", "Hobby Projects", "With Claude Code", "🦀"),
    ]
    body = ""
    for i, (label, value, sub, icon) in enumerate(items):
        body += f"""
    <g transform="translate({i * 410},10)">
      <rect width="380" height="210" rx="20" fill="url(#card)" stroke="{t['stroke']}" stroke-width="1.5"/>
      <rect x="34" y="36" width="52" height="5" rx="2.5" fill="url(#accent)"/>
      <text x="34" y="84" class="label">{label}</text>
      <text x="34" y="134" class="value">{value}</text>
      <text x="34" y="172" class="sub">{sub}</text>
      <text x="336" y="70" class="icon" text-anchor="middle">{icon}</text>
    </g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="230" viewBox="0 0 1200 230">
  <defs>
    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t['card'][0]}"/><stop offset="1" stop-color="{t['card'][1]}"/>
    </linearGradient>
    {ACCENT}
    <style>
      text {{ font-family: {SANS}; }}
      .label {{ font-size: 19px; font-weight: 700; letter-spacing: 2.5px; fill: {t['label']}; }}
      .value {{ font-size: 36px; font-weight: 700; fill: {t['value']}; }}
      .sub {{ font-size: 22px; fill: {t['muted']}; }}
      .icon {{ font-size: 34px; }}
    </style>
  </defs>{body}
</svg>
"""


def terminal(t):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="520" viewBox="0 0 1200 520">
  <defs>
    <linearGradient id="win" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t['win'][0]}"/><stop offset="1" stop-color="{t['win'][1]}"/>
    </linearGradient>
    <style>
      .mono {{ font-family: {MONO}; font-size: 25px; }}
      .dim {{ fill: {t['dim']}; }} .txt {{ fill: {t['txt']}; }} .ok {{ fill: {t['ok']}; }}
      .or {{ fill: {ORANGE}; }} .pr {{ fill: {ORANGE}; font-weight: 700; }}
      .l {{ opacity: 0; animation: show .35s ease-out forwards; }}
      .a1 {{ animation-delay: .4s; }} .a2 {{ animation-delay: 1.2s; }} .a3 {{ animation-delay: 2.2s; }} .a4 {{ animation-delay: 3.2s; }}
      .a5 {{ animation-delay: 4.0s; }} .a6 {{ animation-delay: 4.7s; }} .a7 {{ animation-delay: 5.4s; }} .a8 {{ animation-delay: 6.2s; }}
      @keyframes show {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
      .cur {{ animation: blink 1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
    </style>
  </defs>

  <rect x="1" y="1" width="1198" height="518" rx="20" fill="url(#win)" stroke="{t['stroke']}" stroke-width="1.5"/>
  <path d="M1 21 a20 20 0 0 1 20 -20 h1158 a20 20 0 0 1 20 20 v35 h-1198z" fill="{t['winbar']}"/>
  <circle cx="36" cy="29" r="8" fill="#FF5F57"/>
  <circle cx="62" cy="29" r="8" fill="#FEBC2E"/>
  <circle cx="88" cy="29" r="8" fill="#28C840"/>
  <text x="600" y="37" text-anchor="middle" font-family="{SANS}" font-size="19" fill="{t['muted']}">jannik@hobby: ~/projects</text>

  <g class="mono">
    <text x="44" y="112" class="l a1"><tspan class="ok">~/projects</tspan><tspan class="dim"> $ </tspan><tspan class="txt">claude</tspan></text>
    <g class="l a2">
      <rect x="44" y="134" width="560" height="62" rx="10" fill="none" stroke="{ORANGE}" stroke-width="2"/>
      <text x="68" y="174"><tspan class="or">✻</tspan><tspan class="txt"> Welcome to </tspan><tspan class="txt" font-weight="700">Claude Code</tspan><tspan class="txt">!</tspan></text>
    </g>
    <text x="44" y="250" class="l a3"><tspan class="pr">&gt; </tspan><tspan class="txt">Let's build a new hobby project today</tspan></text>
    <text x="44" y="298" class="l a4"><tspan class="or">● </tspan><tspan class="txt">Sure! Let's get started.</tspan></text>
    <text x="72" y="340" class="l a5"><tspan class="ok">✓ </tspan><tspan class="dim">Project structure created</tspan></text>
    <text x="72" y="380" class="l a6"><tspan class="ok">✓ </tspan><tspan class="dim">First feature implemented</tspan></text>
    <text x="72" y="420" class="l a7"><tspan class="ok">✓ </tspan><tspan class="dim">Tests passing</tspan></text>
    <text x="44" y="474" class="l a8"><tspan class="pr">&gt; </tspan><tspan class="or cur">▌</tspan></text>
  </g>
</svg>
"""


def walk(t):
    # A small crab walking along a dotted line, used as a section divider.
    dots = "".join(f'<circle cx="{x}" cy="78" r="2" fill="{t["stroke"]}"/>' for x in range(20, 1200, 24))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="90" viewBox="0 0 1200 90">
  <defs>
    <style>
      .walker {{ animation: walk 16s linear infinite; }}
      @keyframes walk {{ from {{ transform: translateX(-90px); }} to {{ transform: translateX(1200px); }} }}
      .eyes {{ transform-origin: 0 18px; animation: eyes 3s infinite; }}
      @keyframes eyes {{ 0%, 90%, 100% {{ transform: scaleY(1); }} 94% {{ transform: scaleY(0.1); }} }}{WALK_CSS}
    </style>
  </defs>
  {dots}
  <g class="walker"><g transform="translate(0,26)">{crab(6, walking=True)}</g></g>
</svg>
"""


def outro(t):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="110" viewBox="0 0 1200 110">
  <defs>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ORANGE}" stop-opacity="0"/><stop offset="0.5" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE_LIGHT}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="150" y="20" width="900" height="2" fill="url(#line)"/>
  <text x="600" y="80" text-anchor="middle" font-family="{SANS}" font-size="34" fill="{t['outro']}" letter-spacing="1">Thanks for visiting my profile 🦀</text>
</svg>
"""


def scene(t):
    # Pixel-art scene: the crab typing on a laptop at its desk.
    dark = t is THEMES["dark"]
    wood, wood_top = ("#3B2A20", "#5A3E2B") if dark else ("#B08860", "#C8A27A")
    bezel = "#374151" if dark else "#4B5563"
    sky = "#0F1A33" if dark else "#BFDBFE"
    frame = "#2A3A5C" if dark else "#CBD5E1"

    def r(x, y, w, h, fill, cls=""):
        c = f' class="{cls}"' if cls else ""
        return f'<rect{c} x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'

    # window with night sky (dark) or sunny sky (light)
    window = r(840, 50, 200, 140, frame) + r(848, 58, 184, 124, sky)
    if dark:
        moon = ["..XXX.", ".XXX..", "XXX...", "XXX...", ".XXX..", "..XXX."]
        window += f'<path transform="translate(978,72)" fill="#F1F5F9" d="{pixels(moon, 6, "X")}"/>'
        window += "".join(r(x, y, 4, 4, "#F8FAFC", f"star s{i % 3}") for i, (x, y) in enumerate([(870, 80), (910, 120), (950, 70), (1010, 140), (880, 160), (940, 150)]))
    else:
        window += r(976, 72, 32, 32, "#FBBF24") + r(968, 84, 48, 8, "#FBBF24") + r(988, 64, 8, 48, "#FBBF24")
        window += r(872, 120, 56, 16, "#FFFFFF") + r(884, 108, 32, 12, "#FFFFFF")
    window += r(936, 58, 8, 124, frame) + r(848, 116, 184, 8, frame)

    # desk lamp with a soft light cone towards the laptop
    lamp = (f'<polygon class="glow" points="262,142 300,142 470,268 330,268" fill="#FCD34D" shape-rendering="geometricPrecision"/>'
            + r(184, 260, 56, 10, bezel) + r(206, 150, 8, 110, bezel) + r(206, 142, 56, 8, bezel)
            + r(250, 126, 56, 16, ORANGE) + r(258, 118, 40, 8, ORANGE))

    # laptop with code being written
    laptop = r(400, 118, 240, 140, bezel) + r(408, 126, 224, 124, "#0B1220") + r(380, 258, 284, 12, bezel) + r(500, 262, 44, 4, "#6B7280")
    code = [(424, 64, ORANGE), (496, 88, "#94A3B8"), (440, 120, "#60A5FA"), (440, 72, "#94A3B8"), (424, 40, ORANGE), (472, 96, "#60A5FA")]
    for i, (x, w, color) in enumerate(code):
        laptop += r(x, 142 + i * 16, w, 8, color, f"code k{i}")
    check = "M592 222h8v8h-8zM600 230h8v8h-8zM608 222h8v8h-8zM616 214h8v8h-8zM624 206h8v8h-8z"
    laptop += f'<path class="check" d="{check}" fill="#4ADE80"/>'

    # the crab, standing next to the laptop and typing with its left claw
    u = 10
    body = pixels(CRAB, u, "XE")
    legs = pixels(LEGS_A, u, "X", 6)
    eyes = pixels(CRAB, u, "E")
    crab_svg = (f'<g transform="translate(690,190)">'
                f'<path fill="{ORANGE}" shape-rendering="crispEdges" d="{body}{legs}"/>'
                f'<g class="claw"><path fill="{ORANGE}" shape-rendering="crispEdges" d="M-10 40h10v10h-10zM-20 50h10v10h-10zM-30 56h10v10h-10z"/></g>'
                f'<g class="look"><path fill="#1A1A1A" shape-rendering="crispEdges" d="{eyes}"/></g></g>')

    # coffee mug with rising steam and a small plant
    cup = "#F1F5F9" if dark else "#60A5FA"
    mug = (r(900, 238, 36, 32, cup) + r(900, 238, 36, 6, ORANGE) + r(936, 246, 8, 16, cup)
           + "".join(r(x, 224, 6, 6, t["muted"], f"steam p{i}") for i, x in enumerate([906, 916, 926])))
    plant = (r(1000, 244, 48, 26, "#C2410C") + r(996, 240, 56, 8, "#EA580C")
             + r(1020, 200, 8, 40, "#16A34A") + r(1004, 212, 16, 8, "#22C55E") + r(1028, 204, 16, 8, "#22C55E") + r(1008, 224, 12, 8, "#16A34A") + r(1028, 222, 14, 8, "#16A34A"))

    desk = r(100, 270, 1000, 14, wood_top) + r(100, 284, 1000, 6, wood) + r(130, 290, 16, 50, wood) + r(1054, 290, 16, 50, wood)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" shape-rendering="crispEdges">
  <defs>
    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t['card'][0]}"/><stop offset="1" stop-color="{t['card'][1]}"/>
    </linearGradient>
    <clipPath id="round"><rect width="1200" height="360" rx="20"/></clipPath>
    <style>
      .code {{ transform-box: fill-box; transform-origin: left; animation-duration: 9s; animation-iteration-count: infinite; animation-timing-function: steps(6); }}
      .k0 {{ animation-name: k0; }} .k1 {{ animation-name: k1; }} .k2 {{ animation-name: k2; }}
      .k3 {{ animation-name: k3; }} .k4 {{ animation-name: k4; }} .k5 {{ animation-name: k5; }}
      {"".join(f"@keyframes k{i} {{ 0%, {i * 10}% {{ transform: scaleX(0); }} {i * 10 + 9}%, 92% {{ transform: scaleX(1); }} 96%, 100% {{ transform: scaleX(0); }} }} " for i in range(6))}
      .check {{ opacity: 0; animation: check 9s steps(1) infinite; }}
      @keyframes check {{ 0%, 64% {{ opacity: 0; }} 66%, 92% {{ opacity: 1; }} 94%, 100% {{ opacity: 0; }} }}
      .claw {{ animation: type 9s infinite; }}
      @keyframes type {{
        0%, 4%, 8%, 12%, 16%, 20%, 24%, 28%, 32%, 36%, 40%, 44%, 48%, 52%, 56%, 60%, 64%, 66%, 100% {{ transform: translateY(0); }}
        2%, 6%, 10%, 14%, 18%, 22%, 26%, 30%, 34%, 38%, 42%, 46%, 50%, 54%, 58%, 62% {{ transform: translateY(-6px); }}
      }}
      .look {{ animation: look 9s steps(1) infinite; }}
      @keyframes look {{ 0%, 65% {{ transform: translate(-5px, 4px); }} 66%, 92% {{ transform: translate(0, -4px); }} 93%, 100% {{ transform: translate(-5px, 4px); }} }}
      .steam {{ opacity: 0; animation: steam 3s ease-out infinite; }}
      .p1 {{ animation-delay: 1s; }} .p2 {{ animation-delay: 2s; }}
      @keyframes steam {{ 0% {{ opacity: 0; transform: translateY(0); }} 30% {{ opacity: .8; }} 100% {{ opacity: 0; transform: translateY(-34px); }} }}
      .glow {{ opacity: {.16 if dark else .35}; animation: glow 4s ease-in-out infinite; }}
      @keyframes glow {{ 50% {{ opacity: {.24 if dark else .5}; }} }}
      .star {{ animation: tw 3s ease-in-out infinite; }}
      .s1 {{ animation-delay: 1s; }} .s2 {{ animation-delay: 2s; }}
      @keyframes tw {{ 0%, 100% {{ opacity: .2; }} 50% {{ opacity: 1; }} }}
    </style>
  </defs>
  <g clip-path="url(#round)">
    <rect width="1200" height="360" fill="url(#card)"/>
    {window}
    {lamp}
    {laptop}
    {crab_svg}
    {mug}
    {plant}
    {desk}
  </g>
  <rect x="0.75" y="0.75" width="1198.5" height="358.5" rx="20" fill="none" stroke="{t['stroke']}" stroke-width="1.5"/>
</svg>
"""


def main():
    ASSETS.mkdir(exist_ok=True)
    builders = dict(header=header, cards=cards, walk=walk, terminal=terminal, scene=scene, outro=outro)
    for name, build in builders.items():
        for theme, colors in THEMES.items():
            (ASSETS / f"{name}-{theme}.svg").write_text(build(colors), encoding="utf-8")
            print(f"wrote assets/{name}-{theme}.svg")


if __name__ == "__main__":
    main()
