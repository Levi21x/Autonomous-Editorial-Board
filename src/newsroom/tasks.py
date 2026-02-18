"""Segment 3: Define workflow tasks and deliverables."""

from crewai import Task


class EditorialBoardTasks:
	"""Factory for task instructions and deliverable formats."""

	def research_brief_task(self, agent, topic: str) -> Task:
		return Task(
			description=(
				f"Research the topic: {topic}. Use live web sources and produce only verified facts. "
				"Prioritize recent sources and primary references where possible. Ignore generic opinions "
				"and unsupported claims."
			),
			expected_output=(
				"A structured Research Brief in markdown with these sections: "
				"1) Key Facts (8-12 bullets), 2) Verified Statistics with source links, "
				"3) Notable Quotes with attribution, 4) Source List (at least 6 credible URLs). "
				"No narrative article writing."
			),
			agent=agent,
		)

	def draft_article_task(self, agent, topic: str, research_task: Task) -> Task:
		return Task(
			description=(
				f"Using the Research Brief, write a compelling long-form draft article about {topic}. "
				"Maintain a premium tech-journalism tone, strong narrative flow, and factual accuracy. "
				"Do not invent facts; rely on research context."
			),
			expected_output=(
				"A Draft Article in markdown with a clear headline, engaging introduction, "
				"well-structured body sections, and concise conclusion. Target 900-1400 words. "
				"Use short paragraphs and smooth transitions."
			),
			agent=agent,
			context=[research_task],
		)

	def seo_optimization_task(self, agent, topic: str, draft_task: Task) -> Task:
		return Task(
			description=(
				f"Analyze the Draft Article for SEO performance for the topic {topic}. "
				"Propose practical on-page improvements without changing factual meaning."
			),
			expected_output=(
				"An Optimization Report in markdown containing: "
				"1) Primary keyword, 2) 5 secondary keywords, 3) SEO-friendly meta description (140-160 chars), "
				"4) Suggested H1 and improved H2 structure, 5) Internal/external linking suggestions, "
				"6) Readability and search-intent recommendations."
			),
			agent=agent,
			context=[draft_task],
		)

	def final_editorial_task(self, agent, draft_task: Task, seo_task: Task) -> Task:
		return Task(
			description=(
				"Merge the Draft Article and Optimization Report into one production-ready markdown article. "
				"Apply SEO recommendations naturally, fix awkward phrasing, and enforce clean formatting."
			),
			expected_output=(
				"Final publish-ready markdown article with: "
				"- Exactly one H1 title\n"
				"- Logical H2/H3 hierarchy\n"
				"- A meta description block at the top\n"
				"- Polished grammar and consistent tone\n"
				"- No process notes, only final content"
			),
			agent=agent,
			context=[draft_task, seo_task],
		)
