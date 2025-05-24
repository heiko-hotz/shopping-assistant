# ADK Shopping Assistant

This project demonstrates a shopping assistant built with the Google Agent Development Kit (ADK). The assistant aims to understand a user's shopping needs by analyzing the context of their request, asking clarifying questions if necessary, and then summarizing the requirements.

## How it Works

The application consists of a main `root_agent` (currently named `contextual_search_root_agent` but invoked as `root_agent` by the ADK) that acts as the primary interface.
When a user provides a shopping-related query, this `root_agent` utilizes a specialized `contextual_request_analyzer_agent` (configured as an `AgentTool`) to understand the user's request.

1.  **User Input**: The user sends a message (e.g., "I'm looking for sneakers for the gym and for going out").
2.  **Root Agent (`contextual_search_root_agent`) Processing**:
    *   Receives the user's input.
    *   If the input is a shopping request, it calls the `contextual_request_analyzer_agent` tool.
    *   It passes the user's full query text as input to the tool.
3.  **Contextual Request Analyzer Agent (`contextual_request_analyzer_agent`) Tool Execution**:
    *   Receives the user's query.
    *   Analyzes the text to understand the user's needs.
    *   Returns a JSON object (`ContextualAnalysisOutput`) containing:
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

*   Aims to understand user's shopping needs through contextual analysis.
*   Engages in a basic conversational flow to clarify requirements if the initial request is ambiguous.
*   Uses a modular design with a specialized agent (`contextual_request_analyzer_agent`) acting as a tool.
*   Demonstrates `AgentTool` for inter-agent communication.
*   Utilizes Pydantic for structured output (`ContextualAnalysisOutput`) from the analyzer agent.
*   Runnable with `adk web` for easy local testing and interaction.

## Project Structure
```
shopping-assistant/
├── src/
│   ├── image_search/       <-- Original ADK Agent Module for image-based intent
│   └── contextual_search/  <-- ADK Agent Module for contextual understanding
│       ├── __init__.py     # Makes 'contextual_search' a Python package
│       └── agent.py        # Contains agent definitions for contextual search
└── .env                    # For API key configuration (if needed)
```

## Development & Testing

*   Development and testing utilize `adk web`.
*   To run the contextual search assistant, ensure your ADK environment is configured to point to the `contextual_search` module (e.g., by running `adk web src.contextual_search` or ensuring the default points there).
