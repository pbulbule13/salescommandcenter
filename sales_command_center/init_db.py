"""
Database Initialization Script
Runs schema creation and seed data for Sales Command Center
"""

import os
import sys
from pathlib import Path
import psycopg2
from psycopg2 import sql
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_url():
    """Get database URL from environment"""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")

    # Render provides postgres:// but psycopg2 requires postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    return db_url


def run_sql_file(conn, filepath):
    """Execute SQL from a file"""
    logger.info(f"Running SQL file: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_content)
            conn.commit()
        logger.info(f"Successfully executed: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error executing {filepath}: {e}")
        conn.rollback()
        return False


def check_if_database_initialized(conn):
    """Check if database has already been initialized"""
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'regions'
                );
            """)
            exists = cursor.fetchone()[0]
            return exists
    except Exception as e:
        logger.error(f"Error checking database: {e}")
        return False


def init_database():
    """Initialize the database with schema and seed data"""
    try:
        # Get database URL
        db_url = get_database_url()
        logger.info("Connecting to database...")

        # Connect to database
        conn = psycopg2.connect(db_url)
        logger.info("Connected to database successfully")

        # Check if already initialized
        if check_if_database_initialized(conn):
            logger.info("Database already initialized, skipping...")
            conn.close()
            return True

        # Get SQL file paths
        base_path = Path(__file__).parent
        schema_path = base_path / "sales_dashboard" / "database" / "schema.sql"
        seed_path = base_path / "sales_dashboard" / "database" / "seed_data.sql"

        # Run schema
        if not schema_path.exists():
            logger.error(f"Schema file not found: {schema_path}")
            return False

        logger.info("Creating database schema...")
        if not run_sql_file(conn, schema_path):
            logger.error("Failed to create schema")
            conn.close()
            return False

        # Run seed data
        if seed_path.exists():
            logger.info("Loading seed data...")
            if not run_sql_file(conn, seed_path):
                logger.warning("Failed to load seed data (non-critical)")
        else:
            logger.warning(f"Seed data file not found: {seed_path}")

        conn.close()
        logger.info("Database initialization completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
