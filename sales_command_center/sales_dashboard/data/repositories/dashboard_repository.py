"""
Dashboard Repository
Handles all dashboard data queries
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
import logging

logger = logging.getLogger(__name__)


class DashboardRepository:
    """Repository for dashboard metrics and data"""

    def __init__(self, db: Session):
        self.db = db

    def get_overview_metrics(self) -> Dict[str, Any]:
        """
        Get key metrics for dashboard overview

        Returns:
            Dict containing all overview metrics
        """
        try:
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)

            # Raw SQL queries for performance
            today_metrics = self.db.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE status = 'fulfilled') as orders_fulfilled,
                    COUNT(*) FILTER (WHERE status = 'pending') as orders_pending,
                    COUNT(*) as orders_received,
                    SUM(total_amount) FILTER (WHERE status = 'fulfilled') as revenue_fulfilled,
                    SUM(total_amount) FILTER (WHERE status = 'pending') as revenue_pending,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value
                FROM orders
                WHERE DATE(order_date) = :today
            """, {"today": today}).fetchone()

            yesterday_metrics = self.db.execute("""
                SELECT
                    COUNT(*) as orders_received,
                    SUM(total_amount) as total_revenue
                FROM orders
                WHERE DATE(order_date) = :yesterday
            """, {"yesterday": yesterday}).fetchone()

            # Pipeline metrics
            pipeline_metrics = self.db.execute("""
                SELECT
                    COUNT(*) as total_deals,
                    SUM(amount) as total_value,
                    AVG(probability) as avg_probability
                FROM pipeline
                WHERE is_won IS NULL OR is_won = TRUE
            """).fetchone()

            # Win rate (last 30 days)
            win_rate = self.db.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE is_won = TRUE) as won,
                    COUNT(*) FILTER (WHERE is_won = FALSE) as lost,
                    CASE
                        WHEN COUNT(*) FILTER (WHERE is_won IS NOT NULL) > 0
                        THEN ROUND(100.0 * COUNT(*) FILTER (WHERE is_won = TRUE) /
                             COUNT(*) FILTER (WHERE is_won IS NOT NULL), 2)
                        ELSE 0
                    END as win_rate
                FROM pipeline
                WHERE actual_close_date >= :thirty_days_ago
            """, {"thirty_days_ago": today - timedelta(days=30)}).fetchone()

            # Calculate percentage changes
            orders_change = 0
            if yesterday_metrics and yesterday_metrics[0] > 0:
                orders_change = round(((today_metrics[2] - yesterday_metrics[0]) / yesterday_metrics[0]) * 100, 1)

            return {
                "orders_fulfilled": today_metrics[0] or 0,
                "orders_fulfilled_change": orders_change,
                "orders_pending": today_metrics[1] or 0,
                "orders_pending_value": float(today_metrics[4] or 0),
                "orders_received": today_metrics[2] or 0,
                "orders_received_value": float(today_metrics[5] or 0),
                "pipeline_value": float(pipeline_metrics[1] or 0),
                "pipeline_deals": pipeline_metrics[0] or 0,
                "win_rate": float(win_rate[2] or 0),
                "win_rate_change": 0,  # Calculate vs previous month
                "today_revenue": float(today_metrics[3] or 0),
                "quarter_progress": 87  # Calculate from quarterly data
            }

        except Exception as e:
            logger.error(f"Error getting overview metrics: {str(e)}")
            raise

    def get_revenue_trend(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get revenue trend for the last N days

        Args:
            days: Number of days to include

        Returns:
            List of daily revenue data
        """
        try:
            start_date = datetime.now().date() - timedelta(days=days-1)

            results = self.db.execute("""
                SELECT
                    DATE(order_date) as date,
                    SUM(total_amount) as revenue,
                    COUNT(*) as order_count
                FROM orders
                WHERE DATE(order_date) >= :start_date
                  AND status = 'fulfilled'
                GROUP BY DATE(order_date)
                ORDER BY date
            """, {"start_date": start_date}).fetchall()

            return [
                {
                    "date": str(row[0]),
                    "revenue": float(row[1]),
                    "orders": row[2]
                }
                for row in results
            ]

        except Exception as e:
            logger.error(f"Error getting revenue trend: {str(e)}")
            raise

    def get_regional_performance(self) -> List[Dict[str, Any]]:
        """Get sales performance by region"""
        try:
            results = self.db.execute("""
                SELECT
                    r.name as region,
                    COUNT(DISTINCT o.id) as order_count,
                    SUM(o.total_amount) as total_revenue,
                    AVG(o.total_amount) as avg_order_value
                FROM orders o
                JOIN customers c ON o.customer_id = c.id
                JOIN regions r ON c.region_id = r.id
                WHERE DATE(o.order_date) >= :thirty_days_ago
                GROUP BY r.id, r.name
                ORDER BY total_revenue DESC
            """, {"thirty_days_ago": datetime.now().date() - timedelta(days=30)}).fetchall()

            return [
                {
                    "region": row[0],
                    "orders": row[1],
                    "revenue": float(row[2]),
                    "avg_value": float(row[3])
                }
                for row in results
            ]

        except Exception as e:
            logger.error(f"Error getting regional performance: {str(e)}")
            raise

    def get_top_performers(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing sales reps"""
        try:
            results = self.db.execute("""
                SELECT
                    u.id,
                    u.first_name || ' ' || u.last_name as name,
                    COUNT(DISTINCT o.id) as deals_closed,
                    SUM(o.total_amount) as total_revenue
                FROM users u
                LEFT JOIN orders o ON u.id = o.sales_rep_id
                WHERE o.order_date >= :thirty_days_ago
                  AND o.status = 'fulfilled'
                GROUP BY u.id, u.first_name, u.last_name
                ORDER BY total_revenue DESC
                LIMIT :limit
            """, {
                "thirty_days_ago": datetime.now().date() - timedelta(days=30),
                "limit": limit
            }).fetchall()

            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "deals": row[2],
                    "revenue": float(row[3])
                }
                for row in results
            ]

        except Exception as e:
            logger.error(f"Error getting top performers: {str(e)}")
            raise

    def get_critical_alerts(self) -> List[Dict[str, Any]]:
        """Get critical alerts and issues"""
        try:
            alerts = []

            # Large pending orders (> 3 days)
            pending_orders = self.db.execute("""
                SELECT
                    o.order_number,
                    c.company_name,
                    o.total_amount,
                    CURRENT_DATE - DATE(o.order_date) as days_pending
                FROM orders o
                JOIN customers c ON o.customer_id = c.id
                WHERE o.status = 'pending'
                  AND CURRENT_DATE - DATE(o.order_date) > 3
                  AND o.total_amount > 100000
                ORDER BY o.total_amount DESC
                LIMIT 3
            """).fetchall()

            for order in pending_orders:
                alerts.append({
                    "type": "order_at_risk",
                    "priority": "high",
                    "title": "Large Deal at Risk",
                    "description": f"{order[1]} order (${order[2]:,.0f}) pending for {order[3]} days",
                    "amount": float(order[2]),
                    "days": order[3]
                })

            # Stalled pipeline deals (> 45 days in stage)
            stalled_deals = self.db.execute("""
                SELECT
                    p.opportunity_name,
                    c.company_name,
                    p.amount,
                    p.days_in_stage
                FROM pipeline p
                JOIN customers c ON p.customer_id = c.id
                WHERE p.days_in_stage > 45
                  AND (p.is_won IS NULL)
                ORDER BY p.amount DESC
                LIMIT 2
            """).fetchall()

            for deal in stalled_deals:
                alerts.append({
                    "type": "deal_stalled",
                    "priority": "medium",
                    "title": "Pipeline Deal Stalled",
                    "description": f"{deal[1]} - {deal[0]} (${deal[2]:,.0f}) stalled for {deal[3]} days",
                    "amount": float(deal[2]),
                    "days": deal[3]
                })

            return alerts

        except Exception as e:
            logger.error(f"Error getting critical alerts: {str(e)}")
            raise

    def get_pipeline_summary(self) -> Dict[str, Any]:
        """Get pipeline summary by stage"""
        try:
            results = self.db.execute("""
                SELECT * FROM pipeline_by_stage
            """).fetchall()

            return {
                "stages": [
                    {
                        "stage": row[0],
                        "count": row[1],
                        "total_value": float(row[2]),
                        "avg_deal_size": float(row[3]),
                        "avg_days": float(row[4])
                    }
                    for row in results
                ]
            }

        except Exception as e:
            logger.error(f"Error getting pipeline summary: {str(e)}")
            raise

    def get_at_risk_deals(self, threshold_days: int = 30) -> List[Dict[str, Any]]:
        """Get deals at risk (stalled too long)"""
        try:
            results = self.db.execute("""
                SELECT
                    p.id,
                    p.opportunity_name,
                    c.company_name,
                    p.stage,
                    p.amount,
                    p.probability,
                    p.days_in_stage,
                    u.first_name || ' ' || u.last_name as owner
                FROM pipeline p
                JOIN customers c ON p.customer_id = c.id
                LEFT JOIN users u ON p.owner_id = u.id
                WHERE p.days_in_stage > :threshold
                  AND (p.is_won IS NULL)
                ORDER BY p.amount DESC
            """, {"threshold": threshold_days}).fetchall()

            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "customer": row[2],
                    "stage": row[3],
                    "amount": float(row[4]),
                    "probability": row[5],
                    "days_in_stage": row[6],
                    "owner": row[7]
                }
                for row in results
            ]

        except Exception as e:
            logger.error(f"Error getting at-risk deals: {str(e)}")
            raise
