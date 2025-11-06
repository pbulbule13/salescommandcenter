"""
Sales Command Center - FastAPI Application
Main application entry point for the Sales Command Center
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging

# Import configuration
from sales_dashboard.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    description="AI-Powered Sales Command Center with Voice Commands"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
frontend_path = Path(__file__).parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": config.APP_NAME,
        "version": config.VERSION
    }

# Root endpoint - serve the dashboard
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard HTML"""
    dashboard_path = frontend_path / "sales_dashboard.html"
    if dashboard_path.exists():
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Sales Command Center</h1><p>Dashboard not found</p>")

# API endpoints
@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics():
    """Get dashboard metrics"""
    # Mock data for now - will be replaced with real database queries
    return {
        "orders_fulfilled_today": 47,
        "orders_fulfilled_change": 12,
        "orders_pending": 23,
        "orders_pending_value": 450000,
        "orders_received_today": 52,
        "orders_received_value": 2300000,
        "pipeline_value": 12500000,
        "pipeline_deals": 145,
        "win_rate": 42,
        "win_rate_change": -3
    }

@app.get("/api/dashboard/revenue-trend")
async def get_revenue_trend():
    """Get revenue trend data"""
    return {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "data": [2.1, 2.3, 2.0, 2.5, 2.8, 1.9, 2.3]
    }

@app.get("/api/dashboard/regional-performance")
async def get_regional_performance():
    """Get regional performance data"""
    return {
        "labels": ["North America", "EMEA", "APAC", "LATAM"],
        "data": [5.8, 3.2, 2.9, 1.4]
    }

@app.get("/api/pipeline/funnel")
async def get_pipeline_funnel():
    """Get pipeline funnel data"""
    return {
        "stages": ["Lead", "Qualified", "Proposal", "Negotiation", "Closed Won"],
        "deal_counts": [145, 98, 67, 42, 28],
        "values": [18.5, 14.2, 10.8, 7.5, 5.2]
    }

@app.get("/api/products/performance")
async def get_product_performance():
    """Get product performance data"""
    return {
        "products": [
            "Enterprise Software License",
            "Professional Services",
            "Cloud Subscription",
            "Hardware - Tablets",
            "Support & Maintenance",
            "Training Services",
            "Custom Development",
            "Hardware - Servers"
        ],
        "revenue": [4.2, 3.8, 3.5, 2.9, 2.1, 1.8, 1.5, 1.2]
    }

@app.get("/api/orders")
async def get_orders():
    """Get recent orders"""
    return {
        "orders": [
            {
                "order_number": "SO-2025-1001",
                "customer": "Disney Corporation",
                "amount": 49100.00,
                "status": "fulfilled",
                "date": "2025-11-05"
            },
            {
                "order_number": "SO-2025-1002",
                "customer": "Tech Giants Inc",
                "amount": 67710.00,
                "status": "fulfilled",
                "date": "2025-11-05"
            },
            {
                "order_number": "SO-2025-1006",
                "customer": "Disney Corporation",
                "amount": 136200.00,
                "status": "pending",
                "date": "2025-11-05"
            }
        ]
    }

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if config.DEBUG else "An error occurred"
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {config.APP_NAME} v{config.VERSION}")
    logger.info(f"Debug mode: {config.DEBUG}")
    logger.info(f"Environment: {'production' if config.is_production() else 'development'}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info(f"Shutting down {config.APP_NAME}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
