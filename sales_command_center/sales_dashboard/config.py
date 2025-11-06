"""
Sales Command Center Configuration
Centralized configuration management for all environment variables and settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Main configuration class for Sales Command Center"""

    # Application Settings
    APP_NAME = "Sales Command Center"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False") == "True"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")

    # LLM Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai or anthropic
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/sales_command_center")
    DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))

    # Redis Cache Configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL_DASHBOARD = int(os.getenv("CACHE_TTL_DASHBOARD", "30"))  # seconds
    CACHE_TTL_ORDERS = int(os.getenv("CACHE_TTL_ORDERS", "300"))  # 5 minutes
    CACHE_TTL_PIPELINE = int(os.getenv("CACHE_TTL_PIPELINE", "300"))  # 5 minutes

    # Salesforce Integration
    SALESFORCE_CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
    SALESFORCE_CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")
    SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")
    SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD")
    SALESFORCE_SECURITY_TOKEN = os.getenv("SALESFORCE_SECURITY_TOKEN")
    SALESFORCE_DOMAIN = os.getenv("SALESFORCE_DOMAIN", "login")  # login or test
    SALESFORCE_API_VERSION = os.getenv("SALESFORCE_API_VERSION", "v58.0")

    # Netsuite Integration
    NETSUITE_ACCOUNT_ID = os.getenv("NETSUITE_ACCOUNT_ID")
    NETSUITE_CONSUMER_KEY = os.getenv("NETSUITE_CONSUMER_KEY")
    NETSUITE_CONSUMER_SECRET = os.getenv("NETSUITE_CONSUMER_SECRET")
    NETSUITE_TOKEN_ID = os.getenv("NETSUITE_TOKEN_ID")
    NETSUITE_TOKEN_SECRET = os.getenv("NETSUITE_TOKEN_SECRET")
    NETSUITE_API_URL = os.getenv("NETSUITE_API_URL")

    # Email Service Configuration
    EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "sendgrid")  # sendgrid or ses
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    AWS_SES_REGION = os.getenv("AWS_SES_REGION", "us-east-1")
    EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS", "noreply@salescommandcenter.com")
    EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Sales Command Center")

    # Authentication & Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key-change-in-production")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))

    # OAuth Configuration
    OAUTH_PROVIDER = os.getenv("OAUTH_PROVIDER", "okta")  # okta, azure, etc.
    OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")
    OAUTH_REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI")
    OAUTH_ISSUER = os.getenv("OAUTH_ISSUER")

    # CORS Configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "True") == "True"

    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True") == "True"
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    # WebSocket Configuration
    WEBSOCKET_PING_INTERVAL = int(os.getenv("WEBSOCKET_PING_INTERVAL", "25"))
    WEBSOCKET_PING_TIMEOUT = int(os.getenv("WEBSOCKET_PING_TIMEOUT", "20"))

    # Task Queue Configuration (Celery)
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "sales-command-center-documents")
    AWS_S3_REGION = os.getenv("AWS_S3_REGION", "us-east-1")

    # Monitoring & Logging
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")
    LOG_TO_FILE = os.getenv("LOG_TO_FILE", "False") == "True"
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app.log")

    # Agent Configuration
    AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "30"))  # seconds
    MAX_CONVERSATION_HISTORY = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))

    # Data Sync Configuration
    SYNC_INTERVAL_SALESFORCE = int(os.getenv("SYNC_INTERVAL_SALESFORCE", "300"))  # 5 minutes
    SYNC_INTERVAL_NETSUITE = int(os.getenv("SYNC_INTERVAL_NETSUITE", "900"))  # 15 minutes
    ENABLE_WEBHOOKS = os.getenv("ENABLE_WEBHOOKS", "True") == "True"

    # Feature Flags
    ENABLE_VOICE_COMMANDS = os.getenv("ENABLE_VOICE_COMMANDS", "True") == "True"
    ENABLE_TRANSACTION_CREATION = os.getenv("ENABLE_TRANSACTION_CREATION", "True") == "True"
    ENABLE_AI_INSIGHTS = os.getenv("ENABLE_AI_INSIGHTS", "True") == "True"
    ENABLE_EMAIL_GENERATION = os.getenv("ENABLE_EMAIL_GENERATION", "True") == "True"

    # Business Rules
    MAX_ORDER_VALUE_WITHOUT_APPROVAL = int(os.getenv("MAX_ORDER_VALUE_WITHOUT_APPROVAL", "100000"))
    MAX_DISCOUNT_PERCENTAGE = float(os.getenv("MAX_DISCOUNT_PERCENTAGE", "15.0"))
    STALE_DEAL_DAYS = int(os.getenv("STALE_DEAL_DAYS", "30"))

    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        required_vars = [
            ('OPENAI_API_KEY', cls.OPENAI_API_KEY),
            ('DATABASE_URL', cls.DATABASE_URL),
        ]

        missing_vars = [var_name for var_name, var_value in required_vars if not var_value]

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        return True

    @classmethod
    def get_database_url(cls) -> str:
        """Get the database URL for SQLAlchemy"""
        return cls.DATABASE_URL

    @classmethod
    def get_redis_url(cls) -> str:
        """Get the Redis URL"""
        return cls.REDIS_URL

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return os.getenv("ENVIRONMENT", "development") == "production"

    @classmethod
    def get_llm_config(cls) -> dict:
        """Get LLM configuration as dictionary"""
        return {
            "provider": cls.LLM_PROVIDER,
            "model": cls.MODEL_NAME,
            "temperature": cls.LLM_TEMPERATURE,
            "max_tokens": cls.LLM_MAX_TOKENS,
            "api_key": cls.OPENAI_API_KEY if cls.LLM_PROVIDER == "openai" else cls.ANTHROPIC_API_KEY
        }

    @classmethod
    def get_salesforce_config(cls) -> dict:
        """Get Salesforce configuration as dictionary"""
        return {
            "client_id": cls.SALESFORCE_CLIENT_ID,
            "client_secret": cls.SALESFORCE_CLIENT_SECRET,
            "username": cls.SALESFORCE_USERNAME,
            "password": cls.SALESFORCE_PASSWORD,
            "security_token": cls.SALESFORCE_SECURITY_TOKEN,
            "domain": cls.SALESFORCE_DOMAIN,
            "api_version": cls.SALESFORCE_API_VERSION
        }

    @classmethod
    def get_netsuite_config(cls) -> dict:
        """Get Netsuite configuration as dictionary"""
        return {
            "account_id": cls.NETSUITE_ACCOUNT_ID,
            "consumer_key": cls.NETSUITE_CONSUMER_KEY,
            "consumer_secret": cls.NETSUITE_CONSUMER_SECRET,
            "token_id": cls.NETSUITE_TOKEN_ID,
            "token_secret": cls.NETSUITE_TOKEN_SECRET,
            "api_url": cls.NETSUITE_API_URL
        }


# Create a global config instance
config = Config()

# Validate on import (optional, can be commented out for development)
# config.validate()
