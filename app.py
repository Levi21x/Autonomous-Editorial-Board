"""Streamlit front-end for The Autonomous Editorial Board."""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

import streamlit as st

# ── Make the src package importable when running from the project root ──────
ROOT = Path(__file__).parent
SRC = ROOT / "src" / "newsroom"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from main import run_editorial_board  # noqa: E402  (after sys.path patch)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Autonomous Editorial Board",
    page_icon="📰",
    layout="wide",
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/news.png", width=72)
    st.title("Editorial Board")
    st.caption("4-agent AI writing pipeline")
    st.divider()

    st.markdown("**Pipeline stages**")
    st.markdown(
        """
        1. 🕵️ **Lead Researcher** — live web research via Tavily  
        2. ✍️ **Senior Writer** — narrative drafting (Groq LLM)  
        3. 📈 **SEO Strategist** — keyword & meta optimisation  
        4. 🧐 **Editor-in-Chief** — final Markdown polish
        """
    )
    st.divider()
    st.markdown("**Tech stack**")
    st.markdown("CrewAI · Groq llama-3.3-70b · Tavily · Streamlit")

# ── Main area ────────────────────────────────────────────────────────────────
st.title("📰 The Autonomous Editorial Board")
st.markdown(
    "Enter any topic below and the 4-agent crew will **research**, **write**, "
    "**SEO-optimise**, and **edit** a production-ready article for you."
)

topic = st.text_input(
    label="Article Topic",
    placeholder='e.g. "The future of AI in journalism"',
    max_chars=200,
)

run_btn = st.button("🚀 Generate Article", type="primary", disabled=not topic.strip())

# ── Session state ─────────────────────────────────────────────────────────────
if "article_md" not in st.session_state:
    st.session_state.article_md = None
if "article_path" not in st.session_state:
    st.session_state.article_path = None
if "error" not in st.session_state:
    st.session_state.error = None

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.session_state.article_md = None
    st.session_state.article_path = None
    st.session_state.error = None

    stages = [
        ("🕵️", "Lead Researcher", "Searching the live web for verified facts…"),
        ("✍️", "Senior Writer",   "Crafting the narrative draft…"),
        ("📈", "SEO Strategist",  "Analysing keywords and optimising metadata…"),
        ("🧐", "Editor-in-Chief", "Polishing and finalising the article…"),
    ]

    progress_bar = st.progress(0, text="Starting pipeline…")
    status_area  = st.empty()

    for i, (icon, name, msg) in enumerate(stages):
        pct = int((i / len(stages)) * 100)
        progress_bar.progress(pct, text=f"{icon} **{name}** — {msg}")
        status_area.info(f"**Stage {i + 1}/{len(stages)}** — {name}: {msg}")

    # Actual crew execution — runs inside a spinner so the progress bar stays visible
    with st.spinner("Agents are collaborating… this usually takes 30–90 seconds."):
        try:
            output_path: Path = run_editorial_board(topic.strip())
            st.session_state.article_path = output_path
            st.session_state.article_md   = output_path.read_text(encoding="utf-8")
        except Exception:
            st.session_state.error = traceback.format_exc()

    progress_bar.progress(100, text="✅ Pipeline complete!")
    status_area.empty()

# ── Display result ────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error("The pipeline encountered an error:")
    st.code(st.session_state.error, language="python")

elif st.session_state.article_md:
    path = st.session_state.article_path
    md   = st.session_state.article_md

    st.success(f"Article generated and saved to `{path.name}`")

    # Two tabs: rendered preview + raw markdown
    tab_preview, tab_raw = st.tabs(["📄 Rendered Article", "📋 Raw Markdown"])

    with tab_preview:
        st.markdown(md, unsafe_allow_html=False)

    with tab_raw:
        st.code(md, language="markdown")

    # Download button
    st.download_button(
        label="⬇️ Download .md file",
        data=md,
        file_name=path.name,
        mime="text/markdown",
    )

    st.caption(f"Saved to: `{path}`")
