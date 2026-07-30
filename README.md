# Sony Music — M&A Catalog Valuation Workbench (Streamlit host)

The actual application — all 8 screens, dark/light theme, custom SVG charts,
and the Excel export — is a single self-contained file, **`workbench.html`**
(pure HTML/CSS/JS, no frameworks, no Streamlit, no build step). It works on
its own if you just double-click it.

**`app.py`** is a thin Streamlit shell whose only job is to serve that file
full-bleed inside the page via `st.components.v1.html(...)`. This is what
lets the exact same app run inside **Streamlit in Snowflake (SiS)**, since
SiS requires a Streamlit entry point.

```
sony_ma_workbench_streamlit/
├── app.py              # Streamlit shell — embeds workbench.html in an iframe
├── workbench.html       # The real app: all 8 screens, self-contained
├── requirements.txt      # pip deps (local run)
├── environment.yml       # conda deps (Streamlit in Snowflake)
└── README.md
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Snowflake (Streamlit in Snowflake / SiS)

**Option A — Snowsight UI**
1. Snowsight → **Projects → Streamlit** → **+ Streamlit App**.
2. Upload `app.py`, `workbench.html`, and `environment.yml`, preserving the
   flat folder structure (`workbench.html` must sit next to `app.py`).
3. Set **Main file** to `app.py`. Save and run.

**Option B — SnowCLI**
```bash
snow streamlit deploy --replace \
  --database <your_db> --schema <your_schema> --name SONY_MA_WORKBENCH
```
Run from inside this folder — SnowCLI reads `environment.yml` and uploads
every file automatically.

## Notes

- All figures are illustrative dummy data, generated for UI review only.
- The embedded iframe is rendered at a fixed height (2400px) with its own
  scrollbar enabled, so nothing is clipped even on the longer screens
  (Metadata Review, New Release Forecasting). Adjust the `height=` argument
  in `app.py` if you want a taller or shorter initial viewport.
- To update the app itself, edit `workbench.html` directly — it's a normal
  static file, no Python changes needed.
