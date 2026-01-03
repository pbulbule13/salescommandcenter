"""
Sales Command Center - FastAPI Application
Main application entry point for the Sales Command Center
"""

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
import logging
import secrets
from pydantic import BaseModel
from typing import Optional

# Import configuration
from sales_dashboard.config import config

# Import LLM Fallback Service
try:
    from sales_dashboard.llm_service import get_llm_service, LLMProvider
    LLM_SERVICE_AVAILABLE = True
except ImportError:
    LLM_SERVICE_AVAILABLE = False

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

# Add session middleware for authentication
app.add_middleware(
    SessionMiddleware,
    secret_key=config.SECRET_KEY,
    session_cookie="session",
    max_age=3600 * 24,  # 24 hours
    same_site="lax",
    https_only=config.is_production()
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


# ============================================
# Authentication Helper Functions
# ============================================

def is_authenticated(request: Request) -> bool:
    """Check if user is authenticated"""
    return request.session.get("authenticated", False)


def auth_enabled() -> bool:
    """Check if authentication is enabled (credentials are set)"""
    return bool(config.APP_USERNAME and config.APP_PASSWORD)


# ============================================
# Authentication Endpoints
# ============================================

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Serve the login page"""
    # If already authenticated, redirect to dashboard
    if is_authenticated(request):
        return RedirectResponse(url="/", status_code=302)

    login_path = frontend_path / "login.html"
    if login_path.exists():
        with open(login_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Login page not found</h1>")


@app.post("/auth/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Handle login form submission"""
    # Check credentials
    if username == config.APP_USERNAME and password == config.APP_PASSWORD:
        request.session["authenticated"] = True
        request.session["username"] = username
        logger.info(f"User '{username}' logged in successfully")
        return {"success": True, "message": "Login successful"}

    logger.warning(f"Failed login attempt for user '{username}'")
    return JSONResponse(
        status_code=401,
        content={"success": False, "message": "Invalid username or password"}
    )


@app.get("/auth/logout")
async def logout(request: Request):
    """Handle logout"""
    username = request.session.get("username", "unknown")
    request.session.clear()
    logger.info(f"User '{username}' logged out")
    return RedirectResponse(url="/login", status_code=302)


@app.get("/auth/status")
async def auth_status(request: Request):
    """Check authentication status"""
    return {
        "authenticated": is_authenticated(request),
        "username": request.session.get("username"),
        "auth_enabled": auth_enabled()
    }


# Health check endpoint (no auth required)
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": config.APP_NAME,
        "version": config.VERSION
    }


# Root endpoint - serve the dashboard (requires auth if enabled)
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main dashboard HTML"""
    # Check authentication if enabled
    if auth_enabled() and not is_authenticated(request):
        return RedirectResponse(url="/login", status_code=302)

    dashboard_path = frontend_path / "sales_dashboard.html"
    if dashboard_path.exists():
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Sales Command Center</h1><p>Dashboard not found</p>")


# API endpoints
@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics(request: Request):
    """Get dashboard metrics"""
    if auth_enabled() and not is_authenticated(request):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

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
async def get_revenue_trend(request: Request):
    """Get revenue trend data"""
    if auth_enabled() and not is_authenticated(request):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    return {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "data": [2.1, 2.3, 2.0, 2.5, 2.8, 1.9, 2.3]
    }

@app.get("/api/dashboard/regional-performance")
async def get_regional_performance(request: Request):
    """Get regional performance data"""
    if auth_enabled() and not is_authenticated(request):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    return {
        "labels": ["North America", "EMEA", "APAC", "LATAM"],
        "data": [5.8, 3.2, 2.9, 1.4]
    }

@app.get("/api/pipeline/funnel")
async def get_pipeline_funnel(request: Request):
    """Get pipeline funnel data"""
    if auth_enabled() and not is_authenticated(request):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    return {
        "stages": ["Lead", "Qualified", "Proposal", "Negotiation", "Closed Won"],
        "deal_counts": [145, 98, 67, 42, 28],
        "values": [18.5, 14.2, 10.8, 7.5, 5.2]
    }

@app.get("/api/products/performance")
async def get_product_performance(request: Request):
    """Get product performance data"""
    if auth_enabled() and not is_authenticated(request):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

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
async def get_orders(request: Request):
    """Get recent orders"""
    if auth_enabled() and not is_authenticated(request):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

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


# ============================================
# LLM API Endpoints with Fallback Strategy
# ============================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    system_prompt: Optional[str] = None
    context: Optional[str] = None
    preferred_provider: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    content: str
    provider: str
    model: str
    success: bool
    error: Optional[str] = None
    latency_ms: Optional[float] = None


@app.get("/api/llm/status")
async def get_llm_status(request: Request):
    """
    Get status of all configured LLM providers.
    Shows which providers are available and their priority order.
    """
    if auth_enabled() and not is_authenticated(request):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    if not LLM_SERVICE_AVAILABLE:
        return {
            "available": False,
            "message": "LLM service not available",
            "providers": []
        }

    try:
        llm_service = get_llm_service()
        status = llm_service.get_provider_status()
        return {
            "available": True,
            "fallback_strategy": "Euri -> DeepSeek -> Google -> OpenAI -> Anthropic",
            **status
        }
    except Exception as e:
        logger.error(f"Error getting LLM status: {e}")
        return {
            "available": False,
            "message": str(e),
            "providers": []
        }


@app.post("/api/llm/chat", response_model=ChatResponse)
async def chat_with_llm(request: Request, chat_request: ChatRequest):
    """
    Send a message to the LLM with automatic fallback.

    The service will try providers in order:
    1. Euri AI (Primary)
    2. DeepSeek (Secondary)
    3. Google Gemini (Tertiary)
    4. OpenAI (Fallback)
    5. Anthropic (Fallback)

    If a provider fails, it automatically tries the next one.
    """
    if auth_enabled() and not is_authenticated(request):
        return ChatResponse(
            content="Unauthorized",
            provider="none",
            model="none",
            success=False,
            error="Authentication required"
        )

    if not LLM_SERVICE_AVAILABLE:
        return ChatResponse(
            content="LLM service is not available. Please configure API keys.",
            provider="none",
            model="none",
            success=False,
            error="LLM service not available"
        )

    try:
        llm_service = get_llm_service()

        # Convert preferred provider string to enum if provided
        preferred = None
        if chat_request.preferred_provider:
            try:
                preferred = LLMProvider(chat_request.preferred_provider.lower())
            except ValueError:
                pass

        response = llm_service.chat(
            user_message=chat_request.message,
            system_prompt=chat_request.system_prompt,
            context=chat_request.context,
            preferred_provider=preferred
        )

        return ChatResponse(
            content=response.content,
            provider=response.provider.value,
            model=response.model,
            success=response.success,
            error=response.error,
            latency_ms=response.latency_ms
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return ChatResponse(
            content="An error occurred while processing your request.",
            provider="none",
            model="none",
            success=False,
            error=str(e)
        )


@app.post("/api/query/ask")
async def ask_natural_language(request: Request, chat_request: ChatRequest):
    """
    Natural language query endpoint for the dashboard.
    Uses the LLM fallback service to answer questions about sales data.
    """
    if auth_enabled() and not is_authenticated(request):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    if not LLM_SERVICE_AVAILABLE:
        return {
            "success": False,
            "response": "AI features are not available. Please configure LLM API keys.",
            "provider": "none"
        }

    try:
        llm_service = get_llm_service()

        # System prompt for sales assistant
        system_prompt = chat_request.system_prompt or """
        You are a helpful sales assistant for the Sales Command Center.
        You help users understand their sales data, pipeline, orders, and business metrics.
        Be concise, professional, and provide actionable insights when relevant.
        If you don't have specific data, provide general guidance based on the question.
        """

        response = llm_service.chat(
            user_message=chat_request.message,
            system_prompt=system_prompt,
            context=chat_request.context
        )

        return {
            "success": response.success,
            "response": response.content,
            "provider": response.provider.value,
            "model": response.model,
            "latency_ms": response.latency_ms
        }

    except Exception as e:
        logger.error(f"Error in ask endpoint: {e}")
        return {
            "success": False,
            "response": "I apologize, but I encountered an error. Please try again.",
            "error": str(e)
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
    if auth_enabled():
        logger.info("Authentication is ENABLED")
    else:
        logger.info("Authentication is DISABLED (no credentials configured)")

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
