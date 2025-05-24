# ADK Shopping Assistants

This project demonstrates two types of shopping assistants built with the Google Agent Development Kit (ADK):
1.  An **Image Search Assistant** that analyzes a user's intent for an exact product match or something similar, often based on an implicitly or explicitly referenced image.
2.  A **Contextual Search Assistant** that aims to understand a user's shopping needs by analyzing the broader context of their request, asking clarifying questions, and then summarizing the requirements.

## How it Works

The application consists of two distinct agent modules, each with its own `root_agent`.

### 1. Image Search Assistant (`src/image_search`)

This assistant (main agent named `image_search_agent`) focuses on determining the type of match a user desires when they make a shopping request, typically when an image might be involved or the request is about a specific item.

1.  **User Input**: The user sends a message (e.g., "I want these shoes," "Show me jackets like this one").
2.  **Root Agent (`image_search_agent`) Processing**:
    *   Receives the user's input.
    *   If the input is a direct shopping request, it calls the `intent_analyzer_agent` tool.
    *   It passes the user's original query as the `user_request_text` argument to the tool.
3.  **Intent Analyzer Agent (`intent_analyzer_agent`) Tool Execution**:
    *   Receives the `user_request_text`.
    *   Analyzes the text to determine if the user wants an "exact" match or a "similar" match.
    *   Returns a JSON object (`IntentAnalysisOutput`) containing `match_type`, `reasoning`, and `confidence_score`.
4.  **Root Agent Response**:
    *   Receives the JSON analysis from the tool.
    *   Formulates a response to the user based on the `match_type` (e.g., "Okay, I understand you're looking for an EXACT match...").
    *   If the user input is a general greeting or informational question, the root agent handles it directly without using the intent analyzer.

### 2. Contextual Search Assistant (`src/contextual_search`)

This assistant (main agent named `contextual_search_root_agent` but invoked as `root_agent` by ADK within its module) aims to understand the user's needs by analyzing their request more deeply, asking clarifying questions if necessary, and then summarizing their requirements.

1.  **User Input**: The user sends a message (e.g., "I'm looking for sneakers for the gym and for going out at night").
2.  **Root Agent (`contextual_search_root_agent`) Processing**:
    *   Receives the user's input.
    *   If the input is a shopping request, it calls the `contextual_request_analyzer_agent` tool.
    *   It passes the user's full query text as input to the tool.
3.  **Contextual Request Analyzer Agent (`contextual_request_analyzer_agent`) Tool Execution**:
    *   Receives the user's query.
    *   Analyzes the text to understand the user's needs.
    *   Returns a JSON object (`ContextualAnalysisOutput`) containing (currently simplified):
        *   `summary_of_understanding`: A brief summary of what the agent has understood.
        *   `is_request_clear_enough_for_recommendations`: A boolean indicating if more information is needed.
4.  **Root Agent Response Flow**:
    *   Receives the analysis from the tool.
    *   **If `is_request_clear_enough_for_recommendations` is `false`**:
        *   The agent responds with the current `summary_of_understanding`.
        *   It then asks the user for more details to clarify their needs (e.g., "I understand that: [summary]. Could you tell me more about what you're looking for?").
    *   **When the user provides more information (or if the initial request was clear)**:
        *   The `root_agent` calls the `contextual_request_analyzer_agent` tool again with the new (or original full) user input.
        *   It then provides a final summary of the understood requirements (e.g., "Great, so summing up: [updated_summary_of_understanding]").
    *   If the user input is a general greeting, the root agent handles it directly.

## Features

**General:**
*   Uses a modular design with specialized agents acting as tools.
*   Demonstrates `AgentTool` for inter-agent communication.
*   Utilizes Pydantic for structured output from analyzer agents.
*   Runnable with `adk web` for easy local testing and interaction.

**Image Search Assistant Specific:**
*   Distinguishes between user intents for "exact" vs. "similar" product searches.
*   Handles general greetings and informational questions appropriately for its scope.

**Contextual Search Assistant Specific:**
*   Aims to understand user's broader shopping needs through contextual analysis.
*   Engages in a basic conversational flow to clarify requirements if the initial request is ambiguous.

## Project Structure
```
shopping-assistant/
├── src/
│   ├── image_search/       <-- ADK Agent Module for image-based intent
│   │   ├── __init__.py     # Makes 'image_search' a Python package
│   │   └── agent.py        # Contains agent definitions for image search
│   └── contextual_search/  <-- ADK Agent Module for contextual understanding
│       ├── __init__.py     # Makes 'contextual_search' a Python package
│       └── agent.py        # Contains agent definitions for contextual search
```

## Development & Testing

*   Development and testing utilize `adk web src`.
