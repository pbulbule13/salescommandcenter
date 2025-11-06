"""
Order Agent
Handles all queries related to sales orders, fulfillment, and order status
"""

from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class OrderAgent(BaseAgent):
    """
    Agent responsible for order-related queries and operations
    """

    def get_system_prompt(self) -> str:
        return """
        You are a Sales Orders expert assistant for the Sales Command Center.
        Your role is to help sales executives understand order status, fulfillment rates,
        and order-related metrics.

        When answering:
        - Be specific with numbers and percentages
        - Highlight trends (increases/decreases)
        - Identify issues that need attention
        - Provide actionable recommendations
        - Use professional but friendly tone

        Example response:
        "You received 52 orders today totaling $2.3M, which is 12% higher than yesterday.
        Of these, 47 are already fulfilled and 23 are pending. The Disney order for $500K
        has been pending for 3 days and may need attention."
        """

    def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process order-related queries

        Args:
            query: User's natural language query
            context: Additional context (date ranges, filters, etc.)

        Returns:
            Dict containing response and data
        """
        try:
            # Extract intent and entities
            intent = self.analyze_intent(query)
            entities = self.extract_entities(query)

            # Fetch order data based on query
            order_data = self.fetch_order_data(query, entities, context)

            if not order_data:
                return {
                    "success": False,
                    "message": "No order data found for your query."
                }

            # Generate natural language response
            response = self.generate_natural_language_response(query, order_data)

            # Log the interaction
            self.log_interaction(query, response, context)

            return {
                "success": True,
                "response": response,
                "data": order_data,
                "agent": "OrderAgent",
                "intent": intent
            }

        except Exception as e:
            return self.handle_error(e, query)

    def fetch_order_data(
        self,
        query: str,
        entities: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fetch order data from database/APIs based on query

        Args:
            query: User query
            entities: Extracted entities
            context: Additional context

        Returns:
            Dict containing order data
        """
        # This is a simplified mock implementation
        # In production, this would query PostgreSQL and/or Netsuite API

        query_lower = query.lower()

        # Handle different query types
        if "today" in query_lower:
            return self.get_todays_orders()
        elif "pending" in query_lower:
            return self.get_pending_orders()
        elif "fulfilled" in query_lower:
            return self.get_fulfilled_orders()
        elif "received" in query_lower:
            return self.get_received_orders()
        else:
            return self.get_order_summary()

    def get_todays_orders(self) -> Dict[str, Any]:
        """Get today's order statistics"""
        # Mock data - replace with actual database query
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "orders_received": 52,
            "orders_fulfilled": 47,
            "orders_pending": 23,
            "total_value": 2300000,
            "avg_order_value": 44230,
            "comparison_yesterday": {
                "orders_received": 46,
                "percent_change": 13.0
            }
        }

    def get_pending_orders(self) -> Dict[str, Any]:
        """Get pending orders information"""
        # Mock data - replace with actual database query
        return {
            "total_pending": 23,
            "total_value": 450000,
            "orders": [
                {
                    "order_id": "SO-12345",
                    "customer": "Disney",
                    "value": 500000,
                    "days_pending": 3,
                    "status": "pending"
                },
                {
                    "order_id": "SO-12346",
                    "customer": "ABC Corp",
                    "value": 280000,
                    "days_pending": 1,
                    "status": "pending"
                },
                {
                    "order_id": "SO-12347",
                    "customer": "XYZ Ltd",
                    "value": 150000,
                    "days_pending": 5,
                    "status": "pending"
                }
            ],
            "avg_days_pending": 3.2,
            "longest_pending_days": 5
        }

    def get_fulfilled_orders(self) -> Dict[str, Any]:
        """Get fulfilled orders information"""
        # Mock data
        return {
            "today_fulfilled": 47,
            "this_week_fulfilled": 234,
            "fulfillment_rate": 87.5,
            "avg_fulfillment_time_hours": 18.5
        }

    def get_received_orders(self) -> Dict[str, Any]:
        """Get received orders information"""
        # Mock data
        return {
            "today_received": 52,
            "this_week_received": 267,
            "total_value_today": 2300000,
            "total_value_week": 11500000
        }

    def get_order_summary(self) -> Dict[str, Any]:
        """Get overall order summary"""
        # Mock data
        return {
            "total_orders": 52,
            "fulfilled": 47,
            "pending": 23,
            "partial": 5,
            "cancelled": 2,
            "total_value": 2300000,
            "fulfillment_rate": 87.5
        }

    def get_orders_by_customer(self, customer_name: str) -> List[Dict[str, Any]]:
        """
        Get all orders for a specific customer

        Args:
            customer_name: Name of the customer

        Returns:
            List of order dictionaries
        """
        # Mock implementation
        return [
            {
                "order_id": "SO-12345",
                "customer": customer_name,
                "date": "2025-11-04",
                "value": 500000,
                "status": "pending"
            }
        ]

    def get_orders_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Get orders within a date range

        Args:
            start_date: Start of date range
            end_date: End of date range

        Returns:
            List of orders
        """
        # Mock implementation - would query database
        return []

    def get_orders_over_amount(self, amount: float) -> List[Dict[str, Any]]:
        """
        Get orders over a specific amount

        Args:
            amount: Minimum order value

        Returns:
            List of orders
        """
        # Mock implementation
        return [
            {
                "order_id": "SO-12345",
                "customer": "Disney",
                "value": 500000,
                "status": "pending"
            }
        ]

    def calculate_fulfillment_rate(self, orders: List[Dict[str, Any]]) -> float:
        """
        Calculate the fulfillment rate for a set of orders

        Args:
            orders: List of order dictionaries

        Returns:
            float: Fulfillment rate as percentage
        """
        if not orders:
            return 0.0

        fulfilled_count = sum(1 for order in orders if order.get("status") == "fulfilled")
        return (fulfilled_count / len(orders)) * 100

    def identify_at_risk_orders(
        self,
        orders: List[Dict[str, Any]],
        threshold_days: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Identify orders that have been pending too long

        Args:
            orders: List of orders
            threshold_days: Number of days to consider at-risk

        Returns:
            List of at-risk orders
        """
        at_risk = []
        for order in orders:
            if order.get("status") == "pending" and order.get("days_pending", 0) > threshold_days:
                at_risk.append(order)

        return at_risk
