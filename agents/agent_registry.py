"""
Registry for all available agents in the AI Employee system.
"""

from .email_agent import EmailAgent
from .linkedin_agent import LinkedInAgent
from .automation_agent import AutomationAgent
from .research_agent import ResearchAgent

AGENT_REGISTRY = {
    "EmailAgent": EmailAgent,
    "LinkedInAgent": LinkedInAgent,
    "AutomationAgent": AutomationAgent,
    "ResearchAgent": ResearchAgent
}


def get_agent(agent_name):
    """
    Retrieve an agent instance by name.

    Args:
        agent_name (str): Name of the agent to retrieve

    Returns:
        An instance of the requested agent class
    """
    agent_class = AGENT_REGISTRY.get(agent_name)
    if agent_class is None:
        raise ValueError(f"Unknown agent: {agent_name}")
    return agent_class()