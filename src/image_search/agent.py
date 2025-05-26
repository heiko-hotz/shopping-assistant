from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel, Field
from .prompts import INTENT_ANALYZER_INSTRUCTIONS, IMAGE_SEARCH_AGENT_INSTRUCTIONS

class IntentAnalysisOutput(BaseModel):
    match_type: str = Field(description="The type of match identified: 'exact' or 'similar'.")
    reasoning: str = Field(description="A brief explanation for the classification.")
    confidence_score: float = Field(description="A confidence score between 0 and 1 indicating the certainty of the match type.")

intent_analyzer_agent = Agent(
    name="intent_analyzer_agent",
    model="gemini-2.0-flash",
    description="Analyzes a user's shopping request to determine if they want an exact match or a similar match. Returns 'exact' or 'similar'.",
    instruction=INTENT_ANALYZER_INSTRUCTIONS,
    output_schema=IntentAnalysisOutput,
)
print(f"Agent '{intent_analyzer_agent.name}' defined.")


intent_analyzer_as_tool = AgentTool(agent=intent_analyzer_agent)

root_agent = Agent(
    name="image_search_agent",
    model="gemini-2.0-flash",
    description="A shopping assistant that first analyzes the type of match a user wants.",
    instruction=IMAGE_SEARCH_AGENT_INSTRUCTIONS,
    tools=[
        intent_analyzer_as_tool
    ]
)
print(f"Root Agent '{root_agent.name}' defined with tool '{intent_analyzer_as_tool.name}'.")