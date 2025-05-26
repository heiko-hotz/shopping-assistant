from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel, Field
from typing import List, Optional
from .prompts import CONTEXTUAL_REQUEST_ANALYZER_INSTRUCTIONS, CONTEXTUAL_SEARCH_ROOT_AGENT_INSTRUCTIONS

class ContextualAnalysisOutput(BaseModel):
    summary_of_understanding: str = Field(description="A brief summary of what the agent has understood from the user's request so far.")
    is_request_clear_enough_for_recommendations: bool = Field(description="True if the agent believes it has enough information to make relevant recommendations, False otherwise.")

contextual_request_analyzer_agent = Agent(
    name="contextual_request_analyzer_agent",
    model="gemini-2.5-flash-preview-05-20",
    description="Analyzes a user's shopping request to understand the product, context, desire, and any specified filters. Identifies missing information.",
    instruction=CONTEXTUAL_REQUEST_ANALYZER_INSTRUCTIONS,
    output_schema=ContextualAnalysisOutput,
    output_key="contextual_analysis_result"
)
print(f"Agent '{contextual_request_analyzer_agent.name}' defined.")


contextual_analyzer_as_tool = AgentTool(agent=contextual_request_analyzer_agent)

root_agent = Agent(
    name="contextual_search_root_agent",
    model="gemini-2.5-flash-preview-05-20",
    description="A shopping assistant that understands context, asks clarifying questions, and then summarizes needs.",
    instruction=CONTEXTUAL_SEARCH_ROOT_AGENT_INSTRUCTIONS,
    tools=[
        contextual_analyzer_as_tool
    ]
)
print(f"Root Agent 'root_agent' (contextual_search_root_agent) defined with tool '{contextual_analyzer_as_tool.name}'.")
