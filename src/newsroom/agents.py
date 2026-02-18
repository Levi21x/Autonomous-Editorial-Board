"""Segment 2: Define agent personalities and tools."""

import os

from crewai import Agent, LLM
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv


class EditorialBoardAgents:
	"""Factory for all autonomous editorial board agents."""

	def __init__(self) -> None:
		load_dotenv()

		self.model_name = os.getenv("MODEL_NAME", "groq/llama-3.3-70b-versatile")
		self.groq_api_key = os.getenv("GROQ_API_KEY", "")
		self.tavily_api_key = os.getenv("TAVILY_API_KEY", "")

		self.llm = self._build_llm()
		self.research_tool = TavilySearchTool(api_key=self.tavily_api_key)

	def _build_llm(self) -> LLM:
		return LLM(model=self.model_name, api_key=self.groq_api_key)

	def lead_researcher(self) -> Agent:
		return Agent(
			role="Lead Researcher",
			goal=(
				"Gather verified, recent, high-signal facts, quotes, and statistics "
				"about the assigned topic using live web research."
			),
			backstory=(
				"You are an investigative fact-checker in a top editorial newsroom. "
				"You ignore fluff, cross-check claims, prioritize primary sources, "
				"and deliver concise evidence-first research briefs."
			),
			tools=[self.research_tool],
			llm=self.llm,
			verbose=True,
			allow_delegation=False,
		)

	def senior_writer(self) -> Agent:
		return Agent(
			role="Senior Writer",
			goal=(
				"Transform raw research into a sharp, engaging, publication-grade "
				"narrative with strong flow and clarity."
			),
			backstory=(
				"You are a veteran tech journalist inspired by premium outlets like "
				"The Verge and TechCrunch. You craft compelling intros, smooth transitions, "
				"and clear explanations without sacrificing factual precision."
			),
			llm=self.llm,
			verbose=True,
			allow_delegation=False,
		)

	def seo_strategist(self) -> Agent:
		return Agent(
			role="SEO Strategist",
			goal=(
				"Optimize article discoverability by aligning topic coverage, keyword intent, "
				"metadata quality, and heading structure with search best practices."
			),
			backstory=(
				"You are a performance marketer focused on organic traffic growth. "
				"You diagnose ranking opportunities, identify high-value keyword angles, "
				"and turn good drafts into search-optimized content plans."
			),
			llm=self.llm,
			verbose=True,
			allow_delegation=False,
		)

	def editor_in_chief(self) -> Agent:
		return Agent(
			role="Editor-in-Chief",
			goal=(
				"Enforce final quality: merge editorial and SEO feedback into a polished, "
				"accurate, and cleanly formatted Markdown article ready for publishing."
			),
			backstory=(
				"You are the final decision-maker in the newsroom: strict on clarity, tone, "
				"and credibility. You remove awkward phrasing, ensure structural consistency, "
				"and approve only production-ready copy."
			),
			llm=self.llm,
			verbose=True,
			allow_delegation=False,
		)
