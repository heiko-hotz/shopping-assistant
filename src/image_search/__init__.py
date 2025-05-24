# This tells ADK to look for the 'root_agent' variable
# in the 'shopping_coordinator.py' file within this package.
from .agent import root_agent

print(f"Package '{__name__}' initialized, root_agent imported from shopping_coordinator.")