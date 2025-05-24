# src/contextual_search/__init__.py

# The ADK uses this file to discover the Agent to run.
# The import path is src.contextual_search.contextual_search_root_agent
from .agent import root_agent

print(f"Package '{__name__}' initialized, root_agent imported from agent.")