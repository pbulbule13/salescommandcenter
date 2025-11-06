#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

echo "===== Starting Sales Command Center Build ====="

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r sales_command_center/requirements.txt

# Initialize database if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
    echo "Initializing database..."

    # Run database schema
    echo "Creating database schema..."
    python sales_command_center/init_db.py

    echo "Database initialized successfully!"
else
    echo "WARNING: DATABASE_URL not set, skipping database initialization"
fi

echo "===== Build completed successfully ====="
