"""
Base Agent Class
Provides common functionality for all AI agents in the Sales Command Center
"""

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import logging
from openai import OpenAI
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all sales agents.
    Provides LLM integration, prompt management, and common utilities.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the base agent with configuration

        Args:
            config: Dictionary containing LLM and agent configuration
        """
        self.config = config
        self.provider = config.get("provider", "openai")
        self.model = config.get("model", "gpt-4-turbo-preview")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 2000)

        # Initialize LLM client based on provider
        if self.provider == "openai":
            self.llm_client = OpenAI(api_key=config.get("api_key"))
        elif self.provider == "anthropic":
            self.llm_client = Anthropic(api_key=config.get("api_key"))
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

        logger.info(f"Initialized {self.__class__.__name__} with provider: {self.provider}")

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent.
        Must be implemented by subclasses.

        Returns:
            str: The system prompt
        """
        pass

    @abstractmethod
    def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a user query and return a response.
        Must be implemented by subclasses.

        Args:
            query: The user's natural language query
            context: Additional context (user info, conversation history, etc.)

        Returns:
            Dict containing the response and any additional data
        """
        pass

    def call_llm(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        context_data: Optional[str] = None
    ) -> str:
        """
        Make a call to the LLM provider

        Args:
            user_message: The user's message/query
            system_prompt: Optional system prompt (uses default if not provided)
            context_data: Optional context data to include in the prompt

        Returns:
            str: The LLM's response
        """
        try:
            if system_prompt is None:
                system_prompt = self.get_system_prompt()

            # Construct the full prompt
            if context_data:
                full_user_message = f"Context:\n{context_data}\n\nQuery: {user_message}"
            else:
                full_user_message = user_message

            if self.provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_user_message}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content

            elif self.provider == "anthropic":
                response = self.llm_client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": full_user_message}
                    ]
                )
                return response.content[0].text

        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            raise

    def format_data_for_llm(self, data: Any) -> str:
        """
        Format data in a way that's easy for LLM to understand

        Args:
            data: Data to format (dict, list, etc.)

        Returns:
            str: Formatted data string
        """
        if isinstance(data, dict):
            return "\n".join([f"{k}: {v}" for k, v in data.items()])
        elif isinstance(data, list):
            return "\n".join([str(item) for item in data])
        else:
            return str(data)

    def extract_entities(self, query: str) -> Dict[str, Any]:
        """
        Extract entities from a user query using LLM

        Args:
            query: The user query

        Returns:
            Dict containing extracted entities
        """
        extraction_prompt = """
        Extract the following entities from the user query:
        - dates (e.g., "today", "this month", "Q1 2026")
        - customers (company names)
        - products (product names)
        - metrics (e.g., "revenue", "orders", "pipeline")
        - amounts (monetary values)
        - statuses (e.g., "pending", "fulfilled")

        Return as JSON.
        """

        try:
            response = self.call_llm(query, system_prompt=extraction_prompt)
            # Parse the JSON response (simplified - add proper JSON parsing)
            return {"raw": response}
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {}

    def analyze_intent(self, query: str) -> str:
        """
        Analyze the intent of a user query

        Args:
            query: The user query

        Returns:
            str: The detected intent (e.g., "order_status", "pipeline_query", "create_transaction")
        """
        intent_prompt = """
        Analyze the user query and determine the primary intent.
        Possible intents:
        - order_status: Asking about order fulfillment, pending orders, etc.
        - pipeline_query: Asking about deals, opportunities, pipeline
        - customer_query: Asking about customers, accounts
        - product_query: Asking about product performance
        - create_transaction: Wants to create a sales order or purchase order
        - comparison: Wants to compare time periods or regions
        - forecast: Asking about predictions or future trends

        Return only the intent name.
        """

        try:
            response = self.call_llm(query, system_prompt=intent_prompt)
            return response.strip().lower()
        except Exception as e:
            logger.error(f"Error analyzing intent: {str(e)}")
            return "unknown"

    def generate_natural_language_response(
        self,
        query: str,
        data: Dict[str, Any]
    ) -> str:
        """
        Generate a natural language response based on query and data

        Args:
            query: The original user query
            data: The data to include in the response

        Returns:
            str: Natural language response
        """
        formatted_data = self.format_data_for_llm(data)
        response_prompt = f"""
        Based on the following data, provide a clear, concise answer to the user's query.
        Be specific with numbers and provide actionable insights when relevant.

        User Query: {query}

        Data: {formatted_data}

        Provide a professional, helpful response.
        """

        try:
            return self.call_llm(response_prompt)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error processing your request."

    def validate_data(self, data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Validate that required fields are present in data

        Args:
            data: Data dictionary to validate
            required_fields: List of required field names

        Returns:
            bool: True if all required fields present
        """
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.warning(f"Missing required fields: {missing_fields}")
            return False
        return True

    def log_interaction(
        self,
        query: str,
        response: str,
        context: Dict[str, Any]
    ):
        """
        Log the interaction for analytics and debugging

        Args:
            query: User query
            response: Agent response
            context: Additional context
        """
        logger.info(f"Agent: {self.__class__.__name__}")
        logger.info(f"Query: {query}")
        logger.info(f"Response: {response[:100]}...")  # Truncate for logging

    def handle_error(self, error: Exception, query: str) -> Dict[str, Any]:
        """
        Handle errors gracefully and return user-friendly messages

        Args:
            error: The exception that occurred
            query: The original query

        Returns:
            Dict with error information
        """
        logger.error(f"Error in {self.__class__.__name__}: {str(error)}")

        return {
            "success": False,
            "error": str(error),
            "message": "I apologize, but I encountered an issue processing your request. Please try again or rephrase your query."
        }
