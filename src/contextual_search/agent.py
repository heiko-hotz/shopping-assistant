# src/contextual_search/agent.py
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Define the Contextual Analysis Agent ---
class ContextualAnalysisOutput(BaseModel):
    # Simplified to bare essentials
    summary_of_understanding: str = Field(description="A brief summary of what the agent has understood from the user's request so far.")
    is_request_clear_enough_for_recommendations: bool = Field(description="True if the agent believes it has enough information to make relevant recommendations, False otherwise.")
    # Removed identified_product_type, identified_context, identified_desire_or_intention, identified_filters, missing_information_questions

contextual_request_analyzer_agent = Agent(
    name="contextual_request_analyzer_agent",
    model="gemini-2.0-flash",
    description="Analyzes a user's shopping request to understand the product, context, desire, and any specified filters. Identifies missing information.",
    instruction="""You are an expert in understanding user shopping needs from natural language.
    Your task is to analyze the provided user's shopping request and extract key information.

    Based on the user's input, identify:
    1.  A summary of your understanding.
    2.  Whether the request is clear enough for recommendations.

    Output your analysis as a JSON object structured according to the 'ContextualAnalysisOutput' schema.

    Example User Request: "Lu, I'm looking for a sneaker that serves both for the gym and for going out at night"
    Potential Analysis:
    {
        "summary_of_understanding": "User is looking for sneakers for the gym and for going out.",
        "is_request_clear_enough_for_recommendations": false
    }
    """,
    output_schema=ContextualAnalysisOutput,
)
print(f"Agent '{contextual_request_analyzer_agent.name}' defined.")


# --- Define the Root Agent (Contextual Shopping Coordinator) ---

# Create an AgentTool instance from our contextual_request_analyzer_agent
contextual_analyzer_as_tool = AgentTool(agent=contextual_request_analyzer_agent)

# This is the main agent ADK will run.
# It must be named 'root_agent'.
root_agent = Agent(
    name="contextual_search_root_agent",
    model="gemini-2.0-flash",
    description="A shopping assistant that understands context, asks clarifying questions, and then summarizes needs.",
    instruction="""You are Lu, a helpful and friendly shopping assistant.
    Your goal is to understand the user's needs by analyzing their request, asking clarifying questions if necessary, and then summarizing their requirements before (hypothetically) proceeding to find products.

    Conversation Flow:
    1.  **Initial Request Analysis**:
        When the user provides an initial request, you MUST use the 'contextual_request_analyzer_agent' tool to understand it.
        Pass the user's full request text as input to the tool.

    2.  **Process Analyzer Output**:
        The 'contextual_request_analyzer_agent' tool will return a JSON object with 'summary_of_understanding' and 'is_request_clear_enough_for_recommendations'.

    3.  **Clarification (if needed - simplified)**:
        - If 'is_request_clear_enough_for_recommendations' is `false`:
            Respond with the 'summary_of_understanding' and a generic prompt for more details, for example: "I understand that: [summary_of_understanding]. Could you tell me more about what you're looking for?"
            Wait for the user's response.

    4.  **Request Clarified / Summarization (after user answers - simplified)**:
        - When the user provides more details, or if the initial request was already clear:
            Use the 'contextual_request_analyzer_agent' tool AGAIN with the new (or original) user input.
            Construct a summary message. Start with: "Great, so summing up:"
            Then, present the 'summary_of_understanding' from the LATEST tool output.

    5.  **General Interaction**:
        - If the user says "Hello", respond politely: "Hello! How can I help you with your shopping today?"

    **Important Notes**:
    - ALWAYS use the 'contextual_request_analyzer_agent' tool.
    """,
    tools=[
        contextual_analyzer_as_tool
    ]
)
print(f"Root Agent 'root_agent' (contextual_search_root_agent) defined with tool '{contextual_analyzer_as_tool.name}'.")

# Comments about multi-turn handling are less relevant with the simplified schema but kept for context
# To handle a potential second round of analysis if the first one needs clarification:
# The root agent's instruction needs to guide it to call the analyzer again
# with the combined initial query + answers.
# The current structure implies a state ("waiting for answers") but ADK agents are stateless per call.
# The root agent needs to be robust enough to understand if it's the first interaction or a follow-up.
# This can be managed by checking if its prior turn involved asking questions, or by analyzing user input for "answering" cues.
# For simplicity in this prompt, the instruction for step 4 assumes the agent can somehow know it's a follow-up
# or the user explicitly provides all info.
# A more robust solution might involve explicit state management or more complex prompt engineering
# for the root_agent to handle multi-turn conversations gracefully.