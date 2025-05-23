# src/shopping_app/agent.py
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel, Field

# --- Define the Match Analyzer Agent ---
class IntentAnalysisOutput(BaseModel):
    match_type: str = Field(description="The type of match identified: 'exact' or 'similar'.")
    reasoning: str = Field(description="A brief explanation for the classification.")
    confidence_score: float = Field(description="A confidence score between 0 and 1 indicating the certainty of the match type.")

intent_analyzer_agent = Agent(
    name="intent_analyzer_agent",
    model="gemini-2.0-flash",
    description="Analyzes a user's shopping request to determine if they want an exact match or a similar match. Returns 'exact' or 'similar'.",
    instruction="""You are a text analysis expert. Your task is to analyze the provided user's shopping request and determine if they are looking for an EXACT match or a SIMILAR match.

    Output your analysis as a JSON object with two keys: "match_type" and "reasoning".
    - "match_type" should be either "exact" or "similar".
    - "reasoning" should be a brief explanation of why you chose that type.
    - "confidence_score" should be a float between 0 and 1 indicating the certainty of the match type.
    Examples of EXACT match phrases:
    - "I want these specific sneakers, model X, size 9."
    - "Get me this exact dress."
    - "I need this particular laptop."
    - "Find these shoes."
    - "Show me this item."

    Examples of SIMILAR match phrases:
    - "I want sneakers like these."
    - "Show me something similar to this shirt."
    - "I'm looking for a laptop with these features."
    - "Can you find dresses in this style?"
    - "I like this, what else is like it?"

    """,
    output_schema=IntentAnalysisOutput,
)
print(f"Agent '{intent_analyzer_agent.name}' defined.")


# --- Define the Root Agent (Shopping Coordinator) ---

# Create an AgentTool instance from our match_analyzer_agent
intent_analyzer_as_tool = AgentTool(agent=intent_analyzer_agent)

# This is the main agent ADK will run.
# It must be named 'root_agent'.
root_agent = Agent(
    name="image_search_agent",
    model="gemini-2.0-flash",
    description="A shopping assistant that first analyzes the type of match a user wants.",
    instruction="""You are a helpful shopping assistant.
    A user will provide an input. Your primary goal is to help them with their shopping needs.

    First, carefully analyze the user's input to determine its nature:
    1.  **Direct Shopping Request**: The user explicitly states they want to find, buy, or look for an item (e.g., "I want to buy these shoes", "Find me a dress like this", "I'm looking for a new laptop").
    2.  **Informational Question about a Product**: The user asks a question about a product, possibly one that is currently visible or has been discussed (e.g., "What are these?", "Tell me more about this item", "What material is this?").
    3.  **General Greeting or Conversational Query**: The user offers a greeting, asks about your capabilities, or makes a general statement not directly related to a product or immediate shopping action (e.g., "Hello", "How are you?", "What can you do?").

    Your actions depend on this determination:

    -   **If it's a Direct Shopping Request (1):**
        Your next step is to understand if they want an EXACT item or something SIMILAR.
        To do this, you MUST use the 'intent_analyzer_agent' tool.
        Pass the user's original shopping request as the 'user_request_text' argument to the 'intent_analyzer_agent' tool.
        The 'intent_analyzer_agent' tool will return a JSON object indicating the 'intent_type' (either "exact" or "similar"), 'reasoning', and 'confidence_score'.
        Based on the tool's output:
        - If 'intent_type' is "exact", respond: "Okay, I understand you're looking for an EXACT match for their request. Let's find that specific item!"
        - If 'intent_type' is "similar", respond: "Got it! You're looking for items SIMILAR to their request. I can help you explore options!"
        - If the tool returns an error or an unexpected format, inform the user: "I had trouble understanding the specifics of your request."

    -   **If it's an Informational Question about a Product (2):**
        Respond to the question directly and informatively if you can. For example, if they ask "What are these?" and an image of shoes is visible, you might say, "These appear to be [brand/type] sneakers. Are you interested in finding these or something similar?"
        Do NOT use the 'intent_analyzer_agent' at this stage. Wait for the user to express a clearer shopping intent (e.g., "Yes, find these for me" or "Show me similar ones") before using the 'intent_analyzer_agent'.

    -   **If it's a General Greeting or Conversational Query (3):**
        Respond politely and appropriately. For example:
        - If "Hello", say: "Hello! How can I help you with your shopping today?"
        - If "What can you do?", explain your capabilities as a shopping assistant.
        Do NOT use the 'intent_analyzer_agent'.
    """,
    tools=[
        intent_analyzer_as_tool
    ]
)
print(f"Root Agent '{root_agent.name}' defined with tool '{intent_analyzer_as_tool.name}'.")