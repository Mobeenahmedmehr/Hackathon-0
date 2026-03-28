"""
Base class for all agents in the AI Employee system.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseAgent(ABC):
    """
    Base class that all agents should inherit from.
    Provides common functionality for execution, logging, and error handling.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self, plan_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Execute the agent's primary function based on the provided plan data.

        Args:
            plan_data (dict): Data containing the plan to execute

        Returns:
            Result of the execution
        """
        pass

    def log_action(self, action: str, details: Optional[Dict[str, Any]] = None):
        """
        Log an action taken by the agent.

        Args:
            action (str): Description of the action taken
            details (dict, optional): Additional details about the action
        """
        log_msg = f"Action: {action}"
        if details:
            log_msg += f" | Details: {details}"
        self.logger.info(log_msg)

    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle an error that occurred during execution.

        Args:
            error (Exception): The error that occurred
            context (str): Context about when the error occurred

        Returns:
            Error handling result
        """
        error_msg = f"Error in {self.__class__.__name__} ({context}): {str(error)}"
        self.logger.error(error_msg)

        # Return error information instead of raising
        return {
            "success": False,
            "error": str(error),
            "context": context
        }