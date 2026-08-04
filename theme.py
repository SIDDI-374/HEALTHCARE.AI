"""
HealthMonAI visual theme — "Vitals Monitor"

Design concept: the interface reads like the display on a bedside patient
monitor — deep monitor-screen background, a glowing ECG trace as the
signature motif, and mono-spaced "readout" numbers for every metric.
Status is always communicated the way a real monitor would: a colored
left-edge on each card (mint = steady, amber = watch, coral = attention),
never a generic badge.

Tokens
------
Color
  bg-deep     #0B1F1E  main screen
  bg-panel    #12302C  card surface
  bg-panel-2  #163832  raised / hovered surface
  line-mint   #6EE7B0  the trace color — steady / good
  amber       #F2A93B  watch / caution
  coral       #FF6B5B  attention / alert
  ink         #EAF2EF  primary text (warm off-white, not pure white)
  muted       #8FA8A3  secondary text / labels

Type
  Display : Space Grotesk  (headers — technical, geometric)
  Body    : Inter          (everything else)
  Data    : IBM Plex Mono  (vitals, numbers — reads like a readout)
"""

import html as _html

COLORS = {
    "bg_deep": "#0B1F1E",
    "bg_panel": "#12302C",
    "bg_panel_2": "#173A34",
    "mint": "#6EE7B0",
    "amber": "#F2A93B",
    "coral": "#FF6B5B",
    "ink": "#EAF2EF",
    "muted": "#8FA8A3",
    "border": "rgba(110, 231, 176, 0.16)",
}

STATUS_COLOR = {
    "steady": COLORS["mint"],
    "watch": COLORS["amber"],
    "attention": COLORS["coral"],
}

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

:root {{
    --bg-deep: {COLORS['bg_deep']};
    --bg-panel: {COLORS['bg_panel']};
    --bg-panel-2: {COLORS['bg_panel_2']};
    --mint: {COLORS['mint']};
    --amber: {COLORS['amber']};
    --coral: {COLORS['coral']};
    --ink: {COLORS['ink']};
    --muted: {COLORS['muted']};
    --border: {COLORS['border']};
}}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(ellipse 900px 500px at 15% -10%, rgba(110,231,176,0.07), transparent 60%),
        var(--bg-deep);
    color: var(--ink);
}}

h1, h2, h3 {{
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--ink) !important;
    letter-spacing: -0.01em;
}}

h1 {{ font-weight: 700 !important; }}
h2, h3 {{ font-weight: 600 !important; }}

p, span, label, div {{
    color: var(--ink);
}}

hr {{
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.4rem 0;
}}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, var(--bg-panel) 0%, var(--bg-deep) 100%);
    border-right: 1px solid var(--border);
}}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {{
    font-family: 'Space Grotesk', sans-serif !important;
}}

[data-testid="stSidebar"] div[role="radiogroup"] {{
    gap: 4px;
    display: flex;
    flex-direction: column;
}}

[data-testid="stSidebar"] div[role="radiogroup"] label {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 9px 12px !important;
    transition: all 0.15s ease;
    width: 100%;
}}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background: var(--bg-panel-2);
    border-color: var(--border);
}}

[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
    background: rgba(110, 231, 176, 0.12);
    border-color: var(--mint);
}}

[data-testid="stSidebar"] div[role="radiogroup"] label p {{
    font-size: 0.92rem;
    font-weight: 500;
}}

/* hide the native radio dot, the pill itself is the indicator */
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
    display: none;
}}

/* ---------- Buttons ---------- */
.stButton > button {{
    background: var(--mint) !important;
    color: #06211D !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.5rem 1.1rem !important;
    transition: transform 0.1s ease, box-shadow 0.15s ease !important;
    box-shadow: 0 0 0 rgba(110,231,176,0);
}}

.stButton > button:hover {{
    box-shadow: 0 0 18px rgba(110, 231, 176, 0.35) !important;
    transform: translateY(-1px);
}}

/* ---------- Inputs ---------- */
.stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox [data-baseweb="select"] > div, .stTimeInput input {{
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
}}

/* ---------- Tabs ---------- */
[data-testid="stTabs"] button {{
    font-family: 'Space Grotesk', sans-serif;
    color: var(--muted) !important;
    font-weight: 600;
}}

[data-testid="stTabs"] button[aria-selected="true"] {{
    color: var(--mint) !important;
    border-bottom-color: var(--mint) !important;
}}

/* ---------- Alerts (success/info/warning/error) ---------- */
[data-testid="stAlert"] {{
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}}

/* ---------- Metric (native) ---------- */
[data-testid="stMetric"] {{
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
}}
[data-testid="stMetricValue"] {{
    font-family: 'IBM Plex Mono', monospace !important;
    color: var(--mint) !important;
}}
[data-testid="stMetricLabel"] {{
    color: var(--muted) !important;
}}

/* ---------- Progress bar ---------- */
.stProgress > div > div {{
    background: linear-gradient(90deg, var(--mint), #4FD8A0) !important;
}}
.stProgress > div {{
    background: var(--bg-panel) !important;
}}

/* ---------- Tables / dataframes ---------- */
.stTable, [data-testid="stTable"] {{
    background: var(--bg-panel);
    border-radius: 10px;
}}

/* ---------- Custom component classes ---------- */
.vitals-wrap {{
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin: 4px 0 18px 0;
}}

.pulse-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.05rem;
    font-weight: 700;
    color: var(--ink);
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0;
}}

.pulse-caption {{
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 2px;
    margin-bottom: 10px;
    font-family: 'Inter', sans-serif;
}}

.vital-card {{
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-left: 3px solid {COLORS['mint']};
    border-radius: 12px;
    padding: 14px 16px;
    height: 100%;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease;
    cursor: default;
}}

.vital-card:hover {{
    transform: translateY(-4px);
    background: var(--bg-panel-2);
    border-color: var(--mint);
    box-shadow: 0 10px 28px rgba(0,0,0,0.35), 0 0 18px rgba(110,231,176,0.18);
}}

.vital-icon {{
    font-size: 1.1rem;
    opacity: 0.9;
}}

.vital-label {{
    color: var(--muted);
    font-size: 0.78rem;
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 6px;
}}

.vital-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--ink);
    margin-top: 2px;
}}

.vital-sub {{
    color: var(--muted);
    font-size: 0.78rem;
    margin-top: 3px;
}}

.section-eyebrow {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--mint);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.card {{
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    height: 100%;
}}

.timeline-item {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px dashed var(--border);
}}
.timeline-item:last-child {{ border-bottom: none; }}

.timeline-dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}}

.timeline-text b {{ color: var(--ink); }}
.timeline-text span {{ color: var(--muted); font-size: 0.85rem; }}

.score-ring-wrap {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.summary-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 2px;
    border-bottom: 1px solid var(--border);
    font-family: 'Inter', sans-serif;
}}
.summary-row:last-child {{ border-bottom: none; }}
.summary-tag {{
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace;
}}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes pulseGlow {{
    0%, 100% {{ box-shadow: 0 0 4px currentColor; opacity: 1; }}
    50% {{ box-shadow: 0 0 12px currentColor; opacity: 0.7; }}
}}

@keyframes dotBlink {{
    0%, 80%, 100% {{ opacity: 0.25; transform: scale(0.85); }}
    40% {{ opacity: 1; transform: scale(1.1); }}
}}

.card, .vital-card {{
    animation: fadeInUp 0.45s ease;
}}

.timeline-dot {{
    animation: pulseGlow 1.8s ease-in-out infinite;
}}

.chat-bubble {{
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 18px;
    margin: 8px 0;
    font-family: 'Inter', sans-serif;
    line-height: 1.55;
    animation: fadeInUp 0.4s ease;
}}
.chat-bubble.user {{
    border-left: 3px solid var(--muted);
}}
.chat-bubble.assistant {{
    border-left: 3px solid var(--mint);
}}
.chat-bubble .bubble-role {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
    display: block;
}}
.chat-bubble.assistant .bubble-role {{ color: var(--mint); }}

.thinking-pulse {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 4px;
    color: var(--muted);
    font-size: 0.88rem;
    font-family: 'Inter', sans-serif;
}}
.thinking-pulse .dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--mint);
    animation: dotBlink 1.2s infinite ease-in-out;
}}
.thinking-pulse .dot:nth-child(2) {{ animation-delay: 0.15s; }}
.thinking-pulse .dot:nth-child(3) {{ animation-delay: 0.3s; }}
</style>
"""


def inject():
    """Return the <style> block to be passed to st.markdown(..., unsafe_allow_html=True)."""
    return CSS


def pulse_header(title: str, subtitle: str) -> str:
    """Signature element: an animated ECG trace running under the app title."""
    return f"""
<div class="vitals-wrap">
  <div class="pulse-title">🫀 {title}</div>
  <div class="pulse-caption">{subtitle}</div>
  <svg viewBox="0 0 1000 60" width="100%" height="52" preserveAspectRatio="none"
       xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="{COLORS['mint']}" stop-opacity="0.05"/>
        <stop offset="50%" stop-color="{COLORS['mint']}" stop-opacity="0.9"/>
        <stop offset="100%" stop-color="{COLORS['mint']}" stop-opacity="0.05"/>
      </linearGradient>
    </defs>
    <path d="M0,30 L260,30 L285,30 L300,8 L316,52 L332,30 L360,30
             L620,30 L645,30 L660,8 L676,52 L692,30 L720,30 L1000,30"
          fill="none" stroke="url(#fade)" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round">
      <animate attributeName="stroke-dasharray" from="0,1400" to="1400,0" dur="2.6s" repeatCount="indefinite"/>
    </path>
  </svg>
</div>
"""


def vital_card(icon: str, label: str, value: str, sub: str, status: str = "steady") -> str:
    color = STATUS_COLOR.get(status, COLORS["mint"])
    return f"""
<div class="vital-card" style="border-left-color:{color};">
  <div class="vital-icon">{icon}</div>
  <div class="vital-label">{label}</div>
  <div class="vital-value">{value}</div>
  <div class="vital-sub">{sub}</div>
</div>
"""


def section_eyebrow(icon: str, text: str) -> str:
    return f'<div class="section-eyebrow">{icon} {text}</div>'


def timeline_item(time: str, text: str, status: str = "steady") -> str:
    color = STATUS_COLOR.get(status, COLORS["mint"])
    return f"""
<div class="timeline-item">
  <div class="timeline-dot" style="background:{color};box-shadow:0 0 8px {color};"></div>
  <div class="timeline-text"><b>{time}</b> &nbsp; <span>{text}</span></div>
</div>
"""


def card_open() -> str:
    return '<div class="card">'


def card_close() -> str:
    return "</div>"


def summary_row(label: str, value: str, status: str = "steady") -> str:
    color = STATUS_COLOR.get(status, COLORS["mint"])
    return f"""
<div class="summary-row">
  <span>{label}</span>
  <span class="summary-tag" style="color:{color};background:rgba(110,231,176,0.08);border:1px solid {color}55;">{value}</span>
</div>
"""


def chat_bubble(role: str, text: str) -> str:
    """role: 'user' or 'assistant'. Text is HTML-escaped and newlines preserved."""
    safe = _html.escape(text).replace("\n", "<br>")
    label = "You asked" if role == "user" else "HealthMonAI"
    return f"""
<div class="chat-bubble {role}">
  <span class="bubble-role">{label}</span>
  {safe}
</div>
"""


def thinking_pulse(text: str = "Thinking") -> str:
    return f"""
<div class="thinking-pulse">
  <span>{text}</span>
  <span class="dot"></span><span class="dot"></span><span class="dot"></span>
</div>
"""


def style_chart(fig, ax):
    """Apply the monitor theme to a matplotlib figure/axis in-place."""
    fig.patch.set_facecolor(COLORS["bg_panel"])
    ax.set_facecolor(COLORS["bg_panel"])
    ax.tick_params(colors=COLORS["muted"])
    ax.xaxis.label.set_color(COLORS["muted"])
    ax.yaxis.label.set_color(COLORS["muted"])
    ax.title.set_color(COLORS["ink"])
    for spine in ax.spines.values():
        spine.set_color(COLORS["border"] if "rgba" not in COLORS["border"] else "#1E4A43")
    ax.grid(True, color="#1E4A43", linewidth=0.6, alpha=0.6)
    return fig, ax
