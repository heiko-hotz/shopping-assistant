# ADK Shopping Assistant

This project demonstrates a shopping assistant built with the Google Agent Development Kit (ADK). The assistant first analyzes the user's intent to determine if they are looking for an exact product match or something similar, and then responds accordingly.

## How it Works

The application consists of a main `root_agent` (named `image_search_agent`) that acts as the primary interface.
When a user provides a shopping-related query, the `image_search_agent` utilizes a specialized `intent_analyzer_agent` (configured as an `AgentTool`) to classify the user's request.

1.  **User Input**: The user sends a message (e.g., "I want these shoes," "Show me jackets like this one").
2.  **Root Agent (`image_search_agent`) Processing**:
    *   Receives the user's input.
    *   Based on its instructions, if the input is a direct shopping request, it calls the `intent_analyzer_agent` tool.
    *   It passes the user's original query as the `user_request_text` argument to the tool.
3.  **Intent Analyzer Agent (`intent_analyzer_agent`) Tool Execution**:
    *   Receives the `user_request_text`.
    *   Analyzes the text to determine if the user wants an "exact" match or a "similar" match.
    *   Returns a JSON object containing `match_type`, `reasoning`, and `confidence_score`.
4.  **Root Agent Response**:
    *   Receives the JSON analysis from the tool.
    *   Formulates a response to the user based on the `match_type` (e.g., "Okay, I understand you're looking for an EXACT match...").
    *   If the user input is a general greeting or informational question, the root agent handles it directly without using the intent analyzer.

## Features

*   Distinguishes between user intents for "exact" vs. "similar" product searches.
*   Handles general greetings and informational questions.
*   Uses a modular design with a specialized agent (`intent_analyzer_agent`) acting as a tool for the main agent.
*   Demonstrates `AgentTool` for inter-agent communication.
*   Utilizes Pydantic for structured output (`IntentAnalysisOutput`) from the analyzer agent.
*   Runnable with `adk web` for easy local testing and interaction.

## Project Structure
```
shopping-assistant/
├── src/
│   └── shopping_app/ <-- ADK Agent Module
│       ├── __init__.py # Makes 'shopping_app' a Python package
│       └── agent.py    # Contains all agent definitions
└── .env                # For API key configuration
```

## Development & Testing

*   Development and testing utilizes `adk web` for interactive sessions.
