# Sales Command Center - Database Setup Guide

## Quick Setup (5 Minutes)

### Prerequisites
- PostgreSQL 15+ installed
- Command line access (psql or pgAdmin)

### Step 1: Create Database

```bash
# Using psql command line
psql -U postgres

# Then run:
CREATE DATABASE sales_command_center;

# Or using createdb:
createdb sales_command_center
```

### Step 2: Run Schema Creation

```bash
# Navigate to database folder
cd sales_dashboard/database

# Run schema script
psql -U postgres -d sales_command_center -f schema.sql
```

### Step 3: Load Test Data

```bash
# Run seed data script
psql -U postgres -d sales_command_center -f seed_data.sql
```

### Step 4: Verify Installation

```bash
# Connect to database
psql -U postgres -d sales_command_center

# Check tables
\dt

# Check data
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM pipeline;
```

You should see:
- **Regions**: 10 records
- **Users**: 15 sales reps/managers
- **Products**: 14 products
- **Customers**: 20 companies
- **Pipeline**: 20 opportunities
- **Orders**: 25+ orders
- **Order Items**: 50+ line items

---

## Detailed Setup Instructions

### Windows Setup

#### 1. Install PostgreSQL

Download from: https://www.postgresql.org/download/windows/

During installation:
- Set password for `postgres` user (remember this!)
- Default port: 5432
- Include pgAdmin 4

#### 2. Open Command Prompt or PowerShell

```cmd
# Set PATH if needed (replace with your PostgreSQL path)
set PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin

# Verify installation
psql --version
```

#### 3. Create Database

```cmd
# Option 1: Using createdb
createdb -U postgres sales_command_center

# Option 2: Using psql
psql -U postgres
postgres=# CREATE DATABASE sales_command_center;
postgres=# \q
```

#### 4. Run Scripts

```cmd
# Navigate to project
cd C:\Users\pbkap\Documents\euron\Projects\salescommandcenter\sales_command_center\sales_dashboard\database

# Run schema
psql -U postgres -d sales_command_center -f schema.sql

# Run seed data
psql -U postgres -d sales_command_center -f seed_data.sql
```

---

### Mac/Linux Setup

#### 1. Install PostgreSQL

```bash
# Mac (using Homebrew)
brew install postgresql@15
brew services start postgresql@15

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql-15

# Start service
sudo systemctl start postgresql
```

#### 2. Create Database

```bash
# Create database
createdb sales_command_center

# Or using psql
sudo -u postgres psql
postgres=# CREATE DATABASE sales_command_center;
postgres=# \q
```

#### 3. Run Scripts

```bash
# Navigate to project
cd ~/Documents/salescommandcenter/sales_command_center/sales_dashboard/database

# Run schema
psql -d sales_command_center -f schema.sql

# Run seed data
psql -d sales_command_center -f seed_data.sql
```

---

## Using pgAdmin (GUI Method)

### 1. Open pgAdmin 4

Launch pgAdmin (installed with PostgreSQL)

### 2. Create Database

- Right-click "Databases"
- Select "Create" → "Database..."
- Name: `sales_command_center`
- Owner: `postgres`
- Click "Save"

### 3. Run Schema Script

- Right-click `sales_command_center` database
- Select "Query Tool"
- Open `schema.sql` file (File → Open)
- Click "Execute" (F5)

### 4. Run Seed Data Script

- In Query Tool, open `seed_data.sql`
- Click "Execute" (F5)

### 5. Verify Data

Run these queries in Query Tool:

```sql
-- Check all tables
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check record counts
SELECT
    'Regions' as table_name, COUNT(*) as count FROM regions
UNION ALL
SELECT 'Users', COUNT(*) FROM users
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Customers', COUNT(*) FROM customers
UNION ALL
SELECT 'Pipeline', COUNT(*) FROM pipeline
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items;
```

---

## Environment Configuration

### Update .env File

After database setup, update your `.env` file:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/sales_command_center
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

---

## Database Schema Overview

### Core Tables

**orders** (25+ records)
- Sales orders from customers
- Statuses: pending, fulfilled, partial
- Links to customers and sales reps

**customers** (20 records)
- Major companies (Disney, Tech Giants, etc.)
- Industry, region, account manager
- Lifetime revenue tracking

**pipeline** (20 records)
- Sales opportunities and deals
- Stages: lead → qualified → proposal → negotiation → closed
- Win/loss tracking

**products** (14 records)
- Software, services, hardware
- Pricing, inventory, categories

**users** (15 records)
- Sales team (reps, managers, executives)
- Quotas, regions, roles

### Supporting Tables

- **regions**: 10 geographic territories
- **customer_contacts**: Contact persons
- **order_items**: Line items for orders
- **transactions**: AI-generated voice orders
- **conversation_history**: AI assistant logs

### Views (Pre-built Analytics)

- `daily_orders_summary`: Daily aggregated order stats
- `pipeline_by_stage`: Pipeline value by stage
- `top_customers_revenue`: Top customers ranked
- `sales_rep_performance`: Rep performance metrics

---

## Sample Queries

### Today's Sales Summary

```sql
SELECT
    COUNT(*) FILTER (WHERE status = 'fulfilled') as fulfilled_orders,
    COUNT(*) FILTER (WHERE status = 'pending') as pending_orders,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM orders
WHERE DATE(order_date) = CURRENT_DATE;
```

### Pipeline by Stage

```sql
SELECT * FROM pipeline_by_stage;
```

### Top Customers

```sql
SELECT * FROM top_customers_revenue LIMIT 10;
```

### Sales Rep Rankings

```sql
SELECT * FROM sales_rep_performance
ORDER BY total_revenue DESC
LIMIT 10;
```

### Pending Large Orders

```sql
SELECT
    o.order_number,
    c.company_name,
    o.total_amount,
    o.order_date,
    CURRENT_DATE - DATE(o.order_date) as days_pending
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'pending'
  AND o.total_amount > 100000
ORDER BY o.total_amount DESC;
```

---

## Troubleshooting

### Issue: "psql: command not found"

**Solution**: Add PostgreSQL to PATH

```bash
# Windows
set PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin

# Mac (add to ~/.zshrc or ~/.bash_profile)
export PATH="/usr/local/opt/postgresql@15/bin:$PATH"

# Then reload
source ~/.zshrc
```

### Issue: "FATAL: password authentication failed"

**Solution**: Reset postgres password

```bash
# Windows (as Administrator)
psql -U postgres
ALTER USER postgres PASSWORD 'newpassword';

# Update .env with new password
```

### Issue: "Database already exists"

**Solution**: Drop and recreate

```sql
DROP DATABASE sales_command_center;
CREATE DATABASE sales_command_center;
```

### Issue: "Permission denied"

**Solution**: Run as postgres user

```bash
# Linux/Mac
sudo -u postgres psql

# Or grant permissions
GRANT ALL PRIVILEGES ON DATABASE sales_command_center TO your_user;
```

---

## Data Reset

To reset data (keep schema, reload fresh test data):

```sql
-- Connect to database
\c sales_command_center

-- Run seed data script again
\i seed_data.sql
```

To completely reset (drop everything):

```bash
# Drop database
dropdb sales_command_center

# Recreate
createdb sales_command_center

# Run both scripts
psql -d sales_command_center -f schema.sql
psql -d sales_command_center -f seed_data.sql
```

---

## Database Backup

### Create Backup

```bash
# Full database backup
pg_dump -U postgres sales_command_center > backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -U postgres sales_command_center | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Restore Backup

```bash
# From SQL file
psql -U postgres -d sales_command_center < backup_20251105.sql

# From compressed file
gunzip -c backup_20251105.sql.gz | psql -U postgres -d sales_command_center
```

---

## Production Considerations

### Security

1. **Change default password**
   ```sql
   ALTER USER postgres PASSWORD 'strong_random_password';
   ```

2. **Create dedicated user**
   ```sql
   CREATE USER salesapp WITH PASSWORD 'app_password';
   GRANT ALL PRIVILEGES ON DATABASE sales_command_center TO salesapp;
   GRANT ALL ON ALL TABLES IN SCHEMA public TO salesapp;
   ```

3. **Update .env**
   ```env
   DATABASE_URL=postgresql://salesapp:app_password@localhost:5432/sales_command_center
   ```

### Performance

1. **Enable query logging** (postgresql.conf)
   ```
   log_statement = 'all'
   log_duration = on
   ```

2. **Monitor slow queries**
   ```sql
   SELECT * FROM pg_stat_statements
   ORDER BY mean_exec_time DESC
   LIMIT 10;
   ```

3. **Regular maintenance**
   ```sql
   VACUUM ANALYZE;
   REINDEX DATABASE sales_command_center;
   ```

---

## Next Steps

After database setup:

1. ✅ Verify data with sample queries above
2. ✅ Update `.env` file with DATABASE_URL
3. ✅ Test Python connection: `python -c "import psycopg2; print('OK')"`
4. ✅ Run the FastAPI server: `python run_server.py`
5. ✅ Access API docs: http://localhost:8000/docs

---

## Need Help?

- PostgreSQL Docs: https://www.postgresql.org/docs/
- pgAdmin Guide: https://www.pgadmin.org/docs/
- Connection Issues: Check `pg_hba.conf` file
- Performance Tuning: Use `EXPLAIN ANALYZE` on slow queries

---

**Database is ready!** 🎉

You now have a fully populated database with realistic sales data for testing and demonstration.
