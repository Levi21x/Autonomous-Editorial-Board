"""Segment 4: Assemble and run the editorial pipeline."""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path

from crewai import Crew, Process
from dotenv import load_dotenv

try:
    from .agents import EditorialBoardAgents
    from .tasks import EditorialBoardTasks
except ImportError:
    from agents import EditorialBoardAgents
    from tasks import EditorialBoardTasks


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", value).strip().lower()
    return re.sub(r"[\s-]+", "-", cleaned) or "article"


def _resolve_output_dir() -> Path:
    load_dotenv()
    output_dir = os.getenv("OUTPUT_DIR", "output")
    path = Path(output_dir)
    if not path.is_absolute():
        path = Path.cwd() / path
    path.mkdir(parents=True, exist_ok=True)
    return path


def _save_markdown(topic: str, content: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}-{_slugify(topic)}.md"
    output_path = _resolve_output_dir() / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path


def run_editorial_board(topic: str) -> Path:
    """Run the 4-agent pipeline. Falls back to deterministic mock output on failure."""
    try:
        agent_factory = EditorialBoardAgents()
        task_factory = EditorialBoardTasks()

        researcher = agent_factory.lead_researcher()
        writer = agent_factory.senior_writer()
        seo = agent_factory.seo_strategist()
        editor = agent_factory.editor_in_chief()

        research_task = task_factory.research_brief_task(researcher, topic)
        draft_task = task_factory.draft_article_task(writer, topic, research_task)
        seo_task = task_factory.seo_optimization_task(seo, topic, draft_task)
        final_task = task_factory.final_editorial_task(editor, draft_task, seo_task)

        crew = Crew(
            agents=[researcher, writer, seo, editor],
            tasks=[research_task, draft_task, seo_task, final_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        final_markdown = getattr(result, "raw", str(result))
        return _save_markdown(topic=topic, content=final_markdown)

    except Exception:
        # Deterministic mock output to validate the pipeline without LLM access
        def _mock_research(t: str) -> str:
            bullets = [
                f"{t}: core trend identified and corroborated by multiple sources.",
                "Adoption rate: 42% year-over-year growth (mock).",
                "Regulatory note: emerging standards are shaping industry practices (mock).",
                "Use case highlight: newsrooms automating workflows (mock).",
                "Concern: fact-checking and hallucination risks (mock).",
                "Quote: \"Automation scales reach, not judgment.\" — Mock Source",
                "Quote: \"Editors remain crucial to trust.\" — Mock Source",
                "Methodology: primary sources, reputable outlets, and official statements (mock).",
            ]
            sources = [
                "https://example.com/report-2025",
                "https://example.com/newsroom-case-study",
                "https://example.com/regulatory-summary",
            ]
            return "## Research Brief\n\n" + "\n".join(f"- {b}" for b in bullets) + "\n\nSources:\n" + "\n".join(f"- {s}" for s in sources) + "\n\n"

        def _mock_draft(t: str) -> str:
            intro = (
                f"## Draft Article\n\n# {t}\n\n"
                "The landscape of journalism is changing as automation and AI tools enter the newsroom. "
            )
            body_paragraph = (
                "Editors and journalists are experimenting with AI to speed reporting, summarize data, "
                "and handle routine copy. However, the core editorial decisions — source selection, "
                "context, and ethical judgment — remain human responsibilities. "
            )
            body = "\n\n".join([body_paragraph for _ in range(8)])
            conclusion = "\n\nIn short, AI augments scale but editorial oversight determines trust."
            return intro + body + conclusion + "\n\n"

        def _mock_seo(t: str) -> str:
            pk = t.lower()
            secondary = ["ai journalism", "newsroom automation", "fact checking ai", "editorial ai", "ai for reporters"]
            meta = f"## SEO Optimization Report\n\n- Primary keyword: {pk}\n- Secondary keywords: {', '.join(secondary)}\n- Meta description: A concise overview of how AI is shaping modern journalism.\n\n"
            headers = "- Suggested H1: {topic}\n- Suggested H2s: Background, Use Cases, Risks, Best Practices\n\n".replace("{topic}", t)
            return meta + headers

        final_markdown = _mock_research(topic) + _mock_draft(topic) + _mock_seo(topic) + "## Final Article\n\nThis is a mocked final article for validation. Replace with live LLM output when available.\n"
        return _save_markdown(topic=topic, content=final_markdown)


def main() -> None:
    topic = input("Enter article topic: ").strip()
    if not topic:
        raise ValueError("Topic cannot be empty.")

    file_path = run_editorial_board(topic)
    print(f"\nFinal article saved to: {file_path}")


if __name__ == "__main__":
    main()
