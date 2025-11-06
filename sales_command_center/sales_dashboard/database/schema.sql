-- Sales Command Center Database Schema
-- PostgreSQL 15+

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS conversation_history CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS pipeline CASCADE;
DROP TABLE IF EXISTS customer_contacts CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS regions CASCADE;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Regions Table
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Users Table (Sales Representatives)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'sales_rep', 'sales_manager', 'sales_exec', 'vp_sales'
    region_id INT REFERENCES regions(id),
    quota_monthly DECIMAL(12, 2),
    hire_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Products Table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    unit_price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2),
    inventory_qty INT DEFAULT 0,
    reorder_level INT DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Customers Table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    region_id INT REFERENCES regions(id),
    territory VARCHAR(100),
    account_manager_id INT REFERENCES users(id),
    revenue_ltv DECIMAL(12, 2) DEFAULT 0,
    customer_since DATE,
    credit_limit DECIMAL(12, 2),
    payment_terms VARCHAR(50), -- 'NET30', 'NET60', etc.
    is_active BOOLEAN DEFAULT TRUE,
    salesforce_id VARCHAR(50) UNIQUE,
    netsuite_id VARCHAR(50) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Customer Contacts Table
CREATE TABLE customer_contacts (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    title VARCHAR(100),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Pipeline/Opportunities Table
CREATE TABLE pipeline (
    id SERIAL PRIMARY KEY,
    opportunity_name VARCHAR(255) NOT NULL,
    customer_id INT NOT NULL REFERENCES customers(id),
    owner_id INT REFERENCES users(id),
    stage VARCHAR(50) NOT NULL, -- 'lead', 'qualified', 'proposal', 'negotiation', 'closed_won', 'closed_lost'
    amount DECIMAL(12, 2) NOT NULL,
    probability INT DEFAULT 50, -- 0-100
    expected_close_date DATE,
    actual_close_date DATE,
    lead_source VARCHAR(100),
    next_step TEXT,
    days_in_stage INT DEFAULT 0,
    is_won BOOLEAN,
    loss_reason TEXT,
    salesforce_id VARCHAR(50) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Orders Table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    customer_id INT NOT NULL REFERENCES customers(id),
    sales_rep_id INT REFERENCES users(id),
    order_date TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL, -- 'pending', 'processing', 'fulfilled', 'partial', 'cancelled'
    subtotal DECIMAL(12, 2) NOT NULL,
    tax DECIMAL(12, 2) DEFAULT 0,
    shipping DECIMAL(12, 2) DEFAULT 0,
    total_amount DECIMAL(12, 2) NOT NULL,
    fulfillment_percentage INT DEFAULT 0,
    payment_status VARCHAR(20), -- 'pending', 'paid', 'partial', 'overdue'
    shipping_address TEXT,
    billing_address TEXT,
    notes TEXT,
    netsuite_id VARCHAR(50) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    fulfilled_at TIMESTAMP,
    cancelled_at TIMESTAMP
);

-- Order Items Table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    line_total DECIMAL(12, 2) NOT NULL,
    quantity_fulfilled INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- AI Transactions Table (for voice-created orders)
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_uuid UUID DEFAULT uuid_generate_v4(),
    transaction_type VARCHAR(20) NOT NULL, -- 'sales_order', 'purchase_order'
    user_id INT REFERENCES users(id),
    voice_transcript TEXT,
    draft_data JSONB NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'draft', 'approved', 'submitted', 'failed'
    approved_by INT REFERENCES users(id),
    order_id INT REFERENCES orders(id),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    approved_at TIMESTAMP,
    submitted_at TIMESTAMP
);

-- Conversation History Table (AI Assistant)
CREATE TABLE conversation_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    session_id UUID DEFAULT uuid_generate_v4(),
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    intent VARCHAR(50),
    agents_used VARCHAR(255), -- comma-separated list
    response_time_ms INT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for Performance
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_pipeline_customer_id ON pipeline(customer_id);
CREATE INDEX idx_pipeline_stage ON pipeline(stage);
CREATE INDEX idx_pipeline_owner_id ON pipeline(owner_id);
CREATE INDEX idx_customers_region_id ON customers(region_id);
CREATE INDEX idx_customers_account_manager_id ON customers(account_manager_id);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_region_id ON users(region_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_conversation_history_user_id ON conversation_history(user_id);
CREATE INDEX idx_conversation_history_session_id ON conversation_history(session_id);

-- Views for Common Queries

-- Daily Orders Summary View
CREATE OR REPLACE VIEW daily_orders_summary AS
SELECT
    DATE(order_date) as order_date,
    COUNT(*) as total_orders,
    COUNT(*) FILTER (WHERE status = 'fulfilled') as fulfilled_orders,
    COUNT(*) FILTER (WHERE status = 'pending') as pending_orders,
    COUNT(*) FILTER (WHERE status = 'partial') as partial_orders,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM orders
GROUP BY DATE(order_date)
ORDER BY order_date DESC;

-- Pipeline Summary by Stage View
CREATE OR REPLACE VIEW pipeline_by_stage AS
SELECT
    stage,
    COUNT(*) as deal_count,
    SUM(amount) as total_value,
    AVG(amount) as avg_deal_size,
    AVG(days_in_stage) as avg_days_in_stage
FROM pipeline
WHERE is_won IS NULL OR is_won = TRUE
GROUP BY stage;

-- Top Customers by Revenue View
CREATE OR REPLACE VIEW top_customers_revenue AS
SELECT
    c.id,
    c.company_name,
    c.industry,
    r.name as region,
    COUNT(o.id) as order_count,
    SUM(o.total_amount) as total_revenue,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
LEFT JOIN regions r ON c.region_id = r.id
GROUP BY c.id, c.company_name, c.industry, r.name
ORDER BY total_revenue DESC;

-- Sales Rep Performance View
CREATE OR REPLACE VIEW sales_rep_performance AS
SELECT
    u.id,
    u.first_name || ' ' || u.last_name as rep_name,
    r.name as region,
    COUNT(DISTINCT o.id) as orders_count,
    SUM(o.total_amount) as total_revenue,
    COUNT(DISTINCT p.id) FILTER (WHERE p.is_won = TRUE) as deals_won,
    COUNT(DISTINCT p.id) FILTER (WHERE p.is_won = FALSE) as deals_lost,
    CASE
        WHEN COUNT(DISTINCT p.id) FILTER (WHERE p.is_won IS NOT NULL) > 0
        THEN ROUND(100.0 * COUNT(DISTINCT p.id) FILTER (WHERE p.is_won = TRUE) /
             COUNT(DISTINCT p.id) FILTER (WHERE p.is_won IS NOT NULL), 2)
        ELSE 0
    END as win_rate
FROM users u
LEFT JOIN orders o ON u.id = o.sales_rep_id
LEFT JOIN pipeline p ON u.id = p.owner_id
LEFT JOIN regions r ON u.region_id = r.id
WHERE u.role IN ('sales_rep', 'sales_manager')
GROUP BY u.id, u.first_name, u.last_name, r.name;

-- Comments for documentation
COMMENT ON TABLE orders IS 'Sales orders from customers';
COMMENT ON TABLE pipeline IS 'Sales opportunities and deals';
COMMENT ON TABLE customers IS 'Customer/account information';
COMMENT ON TABLE products IS 'Product catalog';
COMMENT ON TABLE users IS 'Sales representatives and managers';
COMMENT ON TABLE transactions IS 'AI-generated transactions from voice commands';
COMMENT ON TABLE conversation_history IS 'AI assistant conversation logs';
