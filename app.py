"""
Sony Music — M&A Catalog Valuation Workbench
Streamlit host shell.

The actual app (all 8 screens, theming, charts, Excel export) is a single
self-contained HTML/CSS/JS file (workbench.html) built with no external
frameworks. Streamlit's only job here is to serve that file full-bleed
inside an iframe via st.components.v1.html — this is what lets the app
run unmodified both locally and inside Streamlit in Snowflake (SiS).
"""

from pathlib import Path
import json

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Sony Music | M&A Catalog Valuation Workbench",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Strip Streamlit's own chrome (header/footer/padding) so the embedded
# HTML app reads as a full, native page rather than a widget-in-a-page.
st.markdown(
    """
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        div.block-container {padding: 0 !important; max-width: 100% !important;}
        iframe {display: block;}
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_PATH = Path(__file__).parent / "workbench.html"
html = HTML_PATH.read_text(encoding="utf-8")

data_dir = Path(__file__).parent / "data"
injected_data = {}
for json_file in data_dir.glob("*.json"):
    injected_data[json_file.stem] = json.loads(json_file.read_text(encoding="utf-8"))

html = html.replace("window.__INJECTED_DATA__ || {}", json.dumps(injected_data))

# Tall fixed height with internal scrolling looks/behaves oddly for a
# long, multi-section app like this one, so instead we render at a
# generous height and let the iframe's own content define page length —
# components.html sizes the iframe to `height`, so we pad well beyond
# the tallest screen (Screen 2 / Screen 7 tables) and disable the
# iframe's own scrollbar in favor of the outer Streamlit page scroll.
components.html(html, height=1000, scrolling=True)
