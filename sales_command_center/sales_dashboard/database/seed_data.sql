-- Sales Command Center - Test Data Seed
-- Realistic test data for demonstration and development

-- Clear existing data
TRUNCATE TABLE conversation_history, transactions, order_items, orders, pipeline, customer_contacts, customers, products, users, regions RESTART IDENTITY CASCADE;

-- Insert Regions
INSERT INTO regions (name, code, country) VALUES
('North America - East', 'NA-EAST', 'United States'),
('North America - West', 'NA-WEST', 'United States'),
('North America - Central', 'NA-CENTRAL', 'United States'),
('EMEA - UK', 'EMEA-UK', 'United Kingdom'),
('EMEA - Germany', 'EMEA-DE', 'Germany'),
('EMEA - France', 'EMEA-FR', 'France'),
('APAC - Japan', 'APAC-JP', 'Japan'),
('APAC - Australia', 'APAC-AU', 'Australia'),
('LATAM - Brazil', 'LATAM-BR', 'Brazil'),
('LATAM - Mexico', 'LATAM-MX', 'Mexico'),
('North America - South', 'NA-SOUTH', 'United States'),
('North America - Northeast', 'NA-NE', 'United States'),
('EMEA - Spain', 'EMEA-ES', 'Spain'),
('EMEA - Italy', 'EMEA-IT', 'Italy'),
('EMEA - Netherlands', 'EMEA-NL', 'Netherlands'),
('APAC - China', 'APAC-CN', 'China'),
('APAC - Singapore', 'APAC-SG', 'Singapore'),
('APAC - India', 'APAC-IN', 'India'),
('LATAM - Argentina', 'LATAM-AR', 'Argentina'),
('LATAM - Chile', 'LATAM-CL', 'Chile');

-- Insert Users (Sales Team)
INSERT INTO users (email, first_name, last_name, role, region_id, quota_monthly, hire_date, is_active) VALUES
-- Executives
('john.doe@salescommand.com', 'John', 'Doe', 'vp_sales', 1, 5000000.00, '2020-01-15', TRUE),
('jane.smith@salescommand.com', 'Jane', 'Smith', 'sales_exec', 1, 3000000.00, '2020-03-20', TRUE),

-- Sales Managers
('sarah.johnson@salescommand.com', 'Sarah', 'Johnson', 'sales_manager', 1, 1200000.00, '2021-02-10', TRUE),
('michael.chen@salescommand.com', 'Michael', 'Chen', 'sales_manager', 2, 1100000.00, '2021-04-15', TRUE),
('emily.rodriguez@salescommand.com', 'Emily', 'Rodriguez', 'sales_manager', 3, 1000000.00, '2021-06-01', TRUE),

-- Sales Reps
('david.kim@salescommand.com', 'David', 'Kim', 'sales_rep', 1, 300000.00, '2022-01-10', TRUE),
('lisa.brown@salescommand.com', 'Lisa', 'Brown', 'sales_rep', 1, 280000.00, '2022-02-15', TRUE),
('robert.taylor@salescommand.com', 'Robert', 'Taylor', 'sales_rep', 2, 290000.00, '2022-03-20', TRUE),
('jennifer.wilson@salescommand.com', 'Jennifer', 'Wilson', 'sales_rep', 2, 275000.00, '2022-04-10', TRUE),
('james.anderson@salescommand.com', 'James', 'Anderson', 'sales_rep', 3, 285000.00, '2022-05-01', TRUE),
('maria.garcia@salescommand.com', 'Maria', 'Garcia', 'sales_rep', 4, 260000.00, '2022-06-15', TRUE),
('christopher.lee@salescommand.com', 'Christopher', 'Lee', 'sales_rep', 5, 270000.00, '2022-07-01', TRUE),
('amanda.martinez@salescommand.com', 'Amanda', 'Martinez', 'sales_rep', 6, 265000.00, '2022-08-10', TRUE),
('daniel.thomas@salescommand.com', 'Daniel', 'Thomas', 'sales_rep', 7, 255000.00, '2022-09-15', TRUE),
('michelle.white@salescommand.com', 'Michelle', 'White', 'sales_rep', 8, 250000.00, '2022-10-20', TRUE),
('patrick.murphy@salescommand.com', 'Patrick', 'Murphy', 'sales_rep', 9, 245000.00, '2023-01-15', TRUE),
('nicole.brooks@salescommand.com', 'Nicole', 'Brooks', 'sales_rep', 10, 240000.00, '2023-02-20', TRUE),
('steven.hughes@salescommand.com', 'Steven', 'Hughes', 'sales_rep', 1, 280000.00, '2023-03-10', TRUE),
('angela.richardson@salescommand.com', 'Angela', 'Richardson', 'sales_rep', 2, 275000.00, '2023-04-15', TRUE),
('brian.coleman@salescommand.com', 'Brian', 'Coleman', 'sales_rep', 3, 270000.00, '2023-05-20', TRUE);

-- Insert Products
INSERT INTO products (sku, name, description, category, unit_price, cost, inventory_qty, reorder_level) VALUES
-- Enterprise Software
('SW-ENT-001', 'Enterprise CRM Suite', 'Complete CRM solution for large enterprises', 'Software', 50000.00, 10000.00, 500, 50),
('SW-ENT-002', 'Advanced Analytics Platform', 'AI-powered business analytics', 'Software', 35000.00, 8000.00, 750, 75),
('SW-ENT-003', 'Sales Automation Pro', 'Sales force automation toolkit', 'Software', 25000.00, 6000.00, 1000, 100),

-- Professional Services
('SVC-CONS-001', 'Implementation Consulting', 'Professional implementation services', 'Services', 15000.00, 5000.00, 9999, 0),
('SVC-TRAIN-001', 'Training Package - Basic', 'User training for up to 50 users', 'Services', 8000.00, 2000.00, 9999, 0),
('SVC-TRAIN-002', 'Training Package - Advanced', 'Advanced training for power users', 'Services', 12000.00, 3000.00, 9999, 0),

-- Hardware/Devices
('HW-TAB-001', 'Sales Tablet Pro', 'Ruggedized tablet for field sales', 'Hardware', 1200.00, 600.00, 2500, 200),
('HW-SCAN-001', 'Barcode Scanner Mobile', 'Mobile barcode scanning device', 'Hardware', 450.00, 200.00, 3000, 300),

-- Subscription Services
('SUB-BASIC-001', 'SaaS Basic Plan', 'Basic subscription per user/month', 'Subscription', 99.00, 20.00, 9999, 0),
('SUB-PRO-001', 'SaaS Professional Plan', 'Professional subscription per user/month', 'Subscription', 199.00, 40.00, 9999, 0),
('SUB-ENT-001', 'SaaS Enterprise Plan', 'Enterprise subscription per user/month', 'Subscription', 299.00, 60.00, 9999, 0),

-- Add-ons
('ADD-API-001', 'API Access Package', 'Premium API access and integrations', 'Add-on', 5000.00, 500.00, 9999, 0),
('ADD-STOR-001', 'Additional Storage 1TB', 'Extra cloud storage per TB', 'Add-on', 500.00, 100.00, 9999, 0),
('ADD-SUPP-001', 'Premium Support Package', '24/7 priority support', 'Add-on', 2500.00, 500.00, 9999, 0),

-- Additional Products
('SW-ENT-004', 'Marketing Automation Suite', 'Complete marketing automation platform', 'Software', 42000.00, 9000.00, 600, 60),
('HW-PRINT-001', 'Mobile Receipt Printer', 'Portable thermal receipt printer', 'Hardware', 350.00, 150.00, 2800, 250),
('SUB-TEAM-001', 'Team Collaboration Plan', 'Team workspace subscription per user/month', 'Subscription', 149.00, 30.00, 9999, 0),
('SVC-MIGR-001', 'Data Migration Service', 'Professional data migration and integration', 'Services', 18000.00, 6000.00, 9999, 0),
('ADD-ANLY-001', 'Advanced Analytics Module', 'Enhanced analytics and reporting features', 'Add-on', 3500.00, 800.00, 9999, 0),
('HW-SERV-001', 'Enterprise Server Unit', 'High-performance enterprise server', 'Hardware', 8500.00, 4200.00, 150, 20);

-- Insert Customers (Major Companies)
INSERT INTO customers (company_name, industry, region_id, territory, account_manager_id, revenue_ltv, customer_since, credit_limit, payment_terms, salesforce_id, netsuite_id) VALUES
-- Large Enterprise Customers
('Disney Corporation', 'Entertainment', 1, 'Northeast', 3, 2500000.00, '2019-03-15', 1000000.00, 'NET30', 'SF-001', 'NS-001'),
('Tech Giants Inc', 'Technology', 2, 'West Coast', 4, 3200000.00, '2018-06-20', 1500000.00, 'NET30', 'SF-002', 'NS-002'),
('Global Retail Co', 'Retail', 1, 'Northeast', 3, 1800000.00, '2020-01-10', 800000.00, 'NET45', 'SF-003', 'NS-003'),
('Financial Services LLC', 'Finance', 1, 'Northeast', 3, 2100000.00, '2019-08-05', 1200000.00, 'NET30', 'SF-004', 'NS-004'),
('Healthcare Systems International', 'Healthcare', 2, 'West Coast', 4, 1600000.00, '2020-04-12', 900000.00, 'NET60', 'SF-005', 'NS-005'),

-- Mid-Market Customers
('Manufacturing Pro LLC', 'Manufacturing', 3, 'Central', 5, 950000.00, '2021-02-18', 500000.00, 'NET30', 'SF-006', 'NS-006'),
('Education Network Inc', 'Education', 1, 'Northeast', 3, 720000.00, '2021-05-22', 400000.00, 'NET45', 'SF-007', 'NS-007'),
('Logistics Express', 'Transportation', 2, 'West Coast', 4, 880000.00, '2021-07-30', 450000.00, 'NET30', 'SF-008', 'NS-008'),
('Media Group International', 'Media', 4, 'EMEA', 5, 1100000.00, '2020-09-15', 600000.00, 'NET30', 'SF-009', 'NS-009'),
('Pharma Solutions Ltd', 'Pharmaceutical', 5, 'EMEA', 5, 1350000.00, '2020-11-20', 750000.00, 'NET45', 'SF-010', 'NS-010'),

-- Growth Stage Customers
('StartupTech Ventures', 'Technology', 2, 'West Coast', 4, 320000.00, '2022-01-15', 200000.00, 'NET30', 'SF-011', 'NS-011'),
('E-Commerce Hub', 'E-Commerce', 1, 'Northeast', 3, 450000.00, '2022-03-20', 250000.00, 'NET30', 'SF-012', 'NS-012'),
('Cloud Services Co', 'Technology', 2, 'West Coast', 4, 580000.00, '2022-05-10', 300000.00, 'NET30', 'SF-013', 'NS-013'),
('Real Estate Group', 'Real Estate', 3, 'Central', 5, 390000.00, '2022-06-25', 220000.00, 'NET45', 'SF-014', 'NS-014'),
('Consulting Partners Inc', 'Consulting', 1, 'Northeast', 3, 470000.00, '2022-08-30', 280000.00, 'NET30', 'SF-015', 'NS-015'),

-- Recent Customers (2025)
('Innovation Labs', 'Technology', 2, 'West Coast', 4, 125000.00, '2025-01-10', 150000.00, 'NET30', 'SF-016', 'NS-016'),
('Automotive Solutions LLC', 'Automotive', 3, 'Central', 5, 210000.00, '2025-02-15', 180000.00, 'NET30', 'SF-017', 'NS-017'),
('Food Services Corp', 'Food & Beverage', 1, 'Northeast', 3, 180000.00, '2025-03-20', 160000.00, 'NET45', 'SF-018', 'NS-018'),
('Energy Systems International', 'Energy', 4, 'EMEA', 5, 290000.00, '2025-04-25', 200000.00, 'NET30', 'SF-019', 'NS-019'),
('Telecom Networks Ltd', 'Telecommunications', 5, 'EMEA', 5, 340000.00, '2025-05-30', 250000.00, 'NET30', 'SF-020', 'NS-020');

-- Insert Customer Contacts
INSERT INTO customer_contacts (customer_id, first_name, last_name, email, phone, title, is_primary) VALUES
(1, 'Bob', 'Anderson', 'b.anderson@disney.com', '555-0101', 'VP of Technology', TRUE),
(1, 'Alice', 'Cooper', 'a.cooper@disney.com', '555-0102', 'Director of Sales', FALSE),
(2, 'Charlie', 'Davis', 'c.davis@techgiants.com', '555-0201', 'CTO', TRUE),
(3, 'Diana', 'Evans', 'd.evans@globalretail.com', '555-0301', 'Head of Operations', TRUE),
(4, 'Edward', 'Foster', 'e.foster@financialservices.com', '555-0401', 'CFO', TRUE),
(5, 'Fiona', 'Green', 'f.green@healthcaresys.com', '555-0501', 'CIO', TRUE),
(6, 'George', 'Harris', 'g.harris@manufacturingpro.com', '555-0601', 'VP Operations', TRUE),
(7, 'Hannah', 'Irving', 'h.irving@educationnet.com', '555-0701', 'IT Director', TRUE),
(8, 'Ian', 'Jackson', 'i.jackson@logisticsexpress.com', '555-0801', 'COO', TRUE),
(9, 'Julia', 'King', 'j.king@mediagroup.com', '555-0901', 'VP Technology', TRUE),
(10, 'Kevin', 'Lewis', 'k.lewis@pharmasolutions.com', '555-1001', 'Head of IT', TRUE),
(11, 'Laura', 'Mitchell', 'l.mitchell@startuptech.com', '555-1101', 'CEO', TRUE),
(12, 'Mark', 'Nelson', 'm.nelson@ecommercehub.com', '555-1201', 'VP Engineering', TRUE),
(13, 'Nancy', 'Oliver', 'n.oliver@cloudservices.com', '555-1301', 'CTO', TRUE),
(14, 'Oscar', 'Parker', 'o.parker@realestategroup.com', '555-1401', 'Director of IT', TRUE),
(15, 'Patricia', 'Quinn', 'p.quinn@consultingpartners.com', '555-1501', 'Managing Partner', TRUE),
(16, 'Quincy', 'Roberts', 'q.roberts@innovationlabs.com', '555-1601', 'VP Product', TRUE),
(17, 'Rachel', 'Stevens', 'r.stevens@automotivesolutions.com', '555-1701', 'Head of Technology', TRUE),
(18, 'Samuel', 'Turner', 's.turner@foodservices.com', '555-1801', 'IT Manager', TRUE),
(19, 'Teresa', 'Underwood', 't.underwood@energysystems.com', '555-1901', 'CIO', TRUE),
(20, 'Victor', 'Walsh', 'v.walsh@telecomnetworks.com', '555-2001', 'VP Operations', TRUE);

-- Insert Pipeline Opportunities
INSERT INTO pipeline (opportunity_name, customer_id, owner_id, stage, amount, probability, expected_close_date, lead_source, next_step, days_in_stage, salesforce_id) VALUES
-- Closed Won Deals (Recent)
('Disney - Enterprise Expansion Q4', 1, 6, 'closed_won', 500000.00, 100, '2025-10-15', 'Referral', 'Implementation kickoff', 0, 'OPP-001'),
('Tech Giants - Platform Upgrade', 2, 8, 'closed_won', 750000.00, 100, '2025-10-20', 'Existing Customer', 'Delivery scheduled', 0, 'OPP-002'),
('Healthcare Systems - New License', 5, 9, 'closed_won', 320000.00, 100, '2025-10-25', 'Inbound', 'Contract signed', 0, 'OPP-003'),

-- In Negotiation (Hot Deals)
('Global Retail - Digital Transform', 3, 6, 'negotiation', 850000.00, 80, '2025-11-20', 'Conference', 'Final pricing review', 12, 'OPP-004'),
('Financial Services - AI Analytics', 4, 7, 'negotiation', 650000.00, 75, '2025-11-25', 'Cold Call', 'Awaiting legal approval', 18, 'OPP-005'),
('Pharma Solutions - Compliance Suite', 10, 10, 'negotiation', 480000.00, 70, '2025-11-30', 'Partner', 'Security review in progress', 25, 'OPP-006'),

-- In Proposal Stage
('Manufacturing Pro - IoT Integration', 6, 10, 'proposal', 390000.00, 60, '2025-12-10', 'Referral', 'Proposal submitted', 8, 'OPP-007'),
('Education Network - Campus Wide', 7, 11, 'proposal', 420000.00, 55, '2025-12-15', 'Webinar', 'Awaiting budget approval', 15, 'OPP-008'),
('Media Group - Content Platform', 9, 12, 'proposal', 520000.00, 50, '2025-12-20', 'Existing Customer', 'Technical evaluation', 10, 'OPP-009'),
('Cloud Services - Infrastructure Deal', 13, 8, 'proposal', 680000.00, 65, '2025-12-25', 'Inbound', 'Proof of concept scheduled', 5, 'OPP-010'),

-- Qualified Leads
('StartupTech - Growth Package', 11, 13, 'qualified', 180000.00, 40, '2026-01-15', 'Inbound', 'Discovery call scheduled', 20, 'OPP-011'),
('E-Commerce Hub - Expansion', 12, 6, 'qualified', 295000.00, 45, '2026-01-20', 'Partner', 'Needs analysis in progress', 30, 'OPP-012'),
('Real Estate - CRM Implementation', 14, 10, 'qualified', 210000.00, 35, '2026-01-25', 'Cold Call', 'Demo scheduled', 35, 'OPP-013'),
('Consulting Partners - Tool Suite', 15, 11, 'qualified', 340000.00, 50, '2026-02-01', 'Referral', 'Stakeholder meeting set', 15, 'OPP-014'),

-- New Leads
('Innovation Labs - Pilot Program', 16, 13, 'lead', 125000.00, 20, '2026-02-15', 'Inbound', 'Initial contact made', 45, 'OPP-015'),
('Automotive Solutions - Fleet Mgmt', 17, 14, 'lead', 280000.00, 25, '2026-02-20', 'Conference', 'Follow-up email sent', 50, 'OPP-016'),
('Food Services - Supply Chain', 18, 6, 'lead', 195000.00, 15, '2026-02-25', 'Cold Call', 'Voicemail left', 55, 'OPP-017'),
('Energy Systems - Smart Grid', 19, 12, 'lead', 425000.00, 30, '2026-03-01', 'Partner', 'Intro meeting scheduled', 40, 'OPP-018'),

-- At Risk Deals (Stalled)
('Logistics Express - Route Optimization', 8, 9, 'negotiation', 560000.00, 60, '2025-11-15', 'Existing Customer', 'Awaiting response from champion', 45, 'OPP-019'),
('Telecom Networks - Network Upgrade', 20, 12, 'proposal', 720000.00, 55, '2025-11-30', 'RFP', 'Competitor comparison needed', 52, 'OPP-020');

-- Update days_in_stage based on created_at
UPDATE pipeline SET updated_at = NOW() - (days_in_stage || ' days')::INTERVAL WHERE days_in_stage > 0;

-- Insert Orders (Recent and Historical)
-- Orders from today
INSERT INTO orders (order_number, customer_id, sales_rep_id, order_date, status, subtotal, tax, shipping, total_amount, fulfillment_percentage, payment_status, netsuite_id) VALUES
-- Today's Orders (Fulfilled)
('SO-2025-1001', 1, 6, NOW() - INTERVAL '8 hours', 'fulfilled', 45000.00, 3600.00, 500.00, 49100.00, 100, 'paid', 'NS-ORD-1001'),
('SO-2025-1002', 2, 8, NOW() - INTERVAL '7 hours', 'fulfilled', 62000.00, 4960.00, 750.00, 67710.00, 100, 'paid', 'NS-ORD-1002'),
('SO-2025-1003', 3, 6, NOW() - INTERVAL '6 hours', 'fulfilled', 28500.00, 2280.00, 300.00, 31080.00, 100, 'paid', 'NS-ORD-1003'),
('SO-2025-1004', 5, 9, NOW() - INTERVAL '5 hours', 'fulfilled', 51000.00, 4080.00, 600.00, 55680.00, 100, 'paid', 'NS-ORD-1004'),
('SO-2025-1005', 4, 7, NOW() - INTERVAL '4 hours', 'fulfilled', 38000.00, 3040.00, 450.00, 41490.00, 100, 'paid', 'NS-ORD-1005'),

-- Today's Orders (Pending)
('SO-2025-1006', 1, 6, NOW() - INTERVAL '3 hours', 'pending', 125000.00, 10000.00, 1200.00, 136200.00, 0, 'pending', 'NS-ORD-1006'),
('SO-2025-1007', 6, 10, NOW() - INTERVAL '2 hours', 'pending', 42000.00, 3360.00, 500.00, 45860.00, 0, 'pending', 'NS-ORD-1007'),
('SO-2025-1008', 7, 11, NOW() - INTERVAL '1 hour', 'pending', 68000.00, 5440.00, 800.00, 74240.00, 0, 'pending', 'NS-ORD-1008'),

-- Yesterday's Orders
('SO-2025-0998', 2, 8, NOW() - INTERVAL '1 day 10 hours', 'fulfilled', 95000.00, 7600.00, 1000.00, 103600.00, 100, 'paid', 'NS-ORD-0998'),
('SO-2025-0999', 3, 6, NOW() - INTERVAL '1 day 8 hours', 'fulfilled', 72000.00, 5760.00, 850.00, 78610.00, 100, 'paid', 'NS-ORD-0999'),
('SO-2025-1000', 4, 7, NOW() - INTERVAL '1 day 6 hours', 'fulfilled', 54000.00, 4320.00, 650.00, 58970.00, 100, 'paid', 'NS-ORD-1000'),

-- This Week (Last 7 days)
('SO-2025-0990', 5, 9, NOW() - INTERVAL '2 days', 'fulfilled', 89000.00, 7120.00, 950.00, 97070.00, 100, 'paid', 'NS-ORD-0990'),
('SO-2025-0991', 1, 6, NOW() - INTERVAL '3 days', 'fulfilled', 76000.00, 6080.00, 800.00, 82880.00, 100, 'paid', 'NS-ORD-0991'),
('SO-2025-0992', 8, 9, NOW() - INTERVAL '4 days', 'fulfilled', 103000.00, 8240.00, 1100.00, 112340.00, 100, 'paid', 'NS-ORD-0992'),
('SO-2025-0993', 9, 12, NOW() - INTERVAL '5 days', 'fulfilled', 58000.00, 4640.00, 700.00, 63340.00, 100, 'paid', 'NS-ORD-0993'),
('SO-2025-0994', 10, 10, NOW() - INTERVAL '6 days', 'fulfilled', 91000.00, 7280.00, 980.00, 99260.00, 100, 'paid', 'NS-ORD-0994'),

-- Older Orders (This Month)
('SO-2025-0980', 11, 13, NOW() - INTERVAL '10 days', 'fulfilled', 45000.00, 3600.00, 550.00, 49150.00, 100, 'paid', 'NS-ORD-0980'),
('SO-2025-0981', 12, 6, NOW() - INTERVAL '12 days', 'fulfilled', 67000.00, 5360.00, 780.00, 73140.00, 100, 'paid', 'NS-ORD-0981'),
('SO-2025-0982', 13, 8, NOW() - INTERVAL '15 days', 'fulfilled', 52000.00, 4160.00, 620.00, 56780.00, 100, 'paid', 'NS-ORD-0982'),
('SO-2025-0983', 14, 10, NOW() - INTERVAL '18 days', 'fulfilled', 83000.00, 6640.00, 900.00, 90540.00, 100, 'paid', 'NS-ORD-0983'),
('SO-2025-0984', 15, 11, NOW() - INTERVAL '20 days', 'fulfilled', 71000.00, 5680.00, 820.00, 77500.00, 100, 'paid', 'NS-ORD-0984'),

-- Large Pending Orders (At Risk)
('SO-2025-0985', 1, 6, NOW() - INTERVAL '5 days', 'pending', 500000.00, 40000.00, 5000.00, 545000.00, 0, 'pending', 'NS-ORD-0985'),
('SO-2025-0986', 2, 8, NOW() - INTERVAL '4 days', 'pending', 280000.00, 22400.00, 2500.00, 304900.00, 0, 'pending', 'NS-ORD-0986'),
('SO-2025-0987', 4, 7, NOW() - INTERVAL '3 days', 'pending', 150000.00, 12000.00, 1500.00, 163500.00, 0, 'pending', 'NS-ORD-0987'),

-- Partial Orders
('SO-2025-0988', 6, 10, NOW() - INTERVAL '2 days', 'partial', 95000.00, 7600.00, 1000.00, 103600.00, 60, 'partial', 'NS-ORD-0988'),
('SO-2025-0989', 8, 9, NOW() - INTERVAL '1 day', 'partial', 78000.00, 6240.00, 850.00, 85090.00, 45, 'partial', 'NS-ORD-0989');

-- Update fulfilled_at for fulfilled orders
UPDATE orders SET fulfilled_at = order_date + INTERVAL '4 hours' WHERE status = 'fulfilled';

-- Insert Order Items
-- For Order SO-2025-1001 (Disney)
INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount_percentage, line_total, quantity_fulfilled) VALUES
(1, 1, 1, 50000.00, 10, 45000.00, 1),
((SELECT id FROM orders WHERE order_number = 'SO-2025-1002'), 2, 2, 35000.00, 5, 66500.00, 2),
((SELECT id FROM orders WHERE order_number = 'SO-2025-1003'), 3, 1, 25000.00, 5, 23750.00, 1),
((SELECT id FROM orders WHERE order_number = 'SO-2025-1003'), 4, 1, 15000.00, 20, 12000.00, 1),
((SELECT id FROM orders WHERE order_number = 'SO-2025-1004'), 1, 1, 50000.00, 0, 50000.00, 1),
((SELECT id FROM orders WHERE order_number = 'SO-2025-1005'), 2, 1, 35000.00, 0, 35000.00, 1),
((SELECT id FROM orders WHERE order_number = 'SO-2025-1006'), 1, 2, 50000.00, 0, 100000.00, 0), -- Large pending Disney order
((SELECT id FROM orders WHERE order_number = 'SO-2025-1006'), 2, 1, 35000.00, 0, 35000.00, 0);

-- More order items for other orders
DO $$
DECLARE
    order_rec RECORD;
    product_count INT;
BEGIN
    FOR order_rec IN SELECT id, subtotal FROM orders WHERE id > 6 LOOP
        product_count := floor(random() * 3 + 1)::INT;
        FOR i IN 1..product_count LOOP
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount_percentage, line_total, quantity_fulfilled)
            VALUES (
                order_rec.id,
                floor(random() * 14 + 1)::INT,
                floor(random() * 5 + 1)::INT,
                (SELECT unit_price FROM products WHERE id = floor(random() * 14 + 1)::INT LIMIT 1),
                floor(random() * 15)::DECIMAL(5,2),
                order_rec.subtotal / product_count,
                CASE WHEN (SELECT status FROM orders WHERE id = order_rec.id) = 'fulfilled' THEN floor(random() * 5 + 1)::INT ELSE 0 END
            );
        END LOOP;
    END LOOP;
END $$;

-- Insert AI Transactions (Voice Orders)
INSERT INTO transactions (transaction_type, user_id, voice_transcript, draft_data, status, approved_by, order_id, submitted_at) VALUES
('sales_order', 6, 'Create a sales order for Disney for 500 hats at $50 each',
 '{"customer": "Disney Corporation", "customer_id": 1, "product": "Sales Tablet Pro", "product_id": 7, "quantity": 500, "unit_price": 50, "total": 25000}'::jsonb,
 'submitted', 6, 1, NOW() - INTERVAL '2 days'),
('sales_order', 8, 'Make an order for Tech Giants, 100 units of Enterprise CRM at standard pricing',
 '{"customer": "Tech Giants Inc", "customer_id": 2, "product": "Enterprise CRM Suite", "product_id": 1, "quantity": 100, "unit_price": 50000, "total": 5000000}'::jsonb,
 'submitted', 8, 2, NOW() - INTERVAL '1 day'),
('sales_order', 7, 'Create order for Financial Services, 50 Analytics Platform licenses',
 '{"customer": "Financial Services LLC", "customer_id": 4, "product": "Advanced Analytics Platform", "product_id": 2, "quantity": 50, "unit_price": 35000, "total": 1750000}'::jsonb,
 'draft', NULL, NULL, NULL),
('sales_order', 9, 'Create an order for Healthcare Systems for 200 tablets',
 '{"customer": "Healthcare Systems International", "customer_id": 5, "product": "Sales Tablet Pro", "product_id": 7, "quantity": 200, "unit_price": 1200, "total": 240000}'::jsonb,
 'submitted', 9, 4, NOW() - INTERVAL '3 days'),
('sales_order', 10, 'Order for Manufacturing Pro, 30 barcode scanners',
 '{"customer": "Manufacturing Pro LLC", "customer_id": 6, "product": "Barcode Scanner Mobile", "product_id": 8, "quantity": 30, "unit_price": 450, "total": 13500}'::jsonb,
 'submitted', 10, 7, NOW() - INTERVAL '4 days'),
('sales_order', 11, 'Make an order for Education Network, training package for 50 users',
 '{"customer": "Education Network Inc", "customer_id": 7, "product": "Training Package - Basic", "product_id": 5, "quantity": 1, "unit_price": 8000, "total": 8000}'::jsonb,
 'submitted', 11, 8, NOW() - INTERVAL '5 days'),
('sales_order', 6, 'Create order for Global Retail, 10 enterprise servers',
 '{"customer": "Global Retail Co", "customer_id": 3, "product": "Enterprise Server Unit", "product_id": 20, "quantity": 10, "unit_price": 8500, "total": 85000}'::jsonb,
 'submitted', 6, 3, NOW() - INTERVAL '6 days'),
('sales_order', 8, 'Order for Media Group, marketing automation suite',
 '{"customer": "Media Group International", "customer_id": 9, "product": "Marketing Automation Suite", "product_id": 15, "quantity": 1, "unit_price": 42000, "total": 42000}'::jsonb,
 'submitted', 8, NULL, NOW() - INTERVAL '1 day'),
('sales_order', 12, 'Create order for Pharma Solutions, implementation consulting',
 '{"customer": "Pharma Solutions Ltd", "customer_id": 10, "product": "Implementation Consulting", "product_id": 4, "quantity": 1, "unit_price": 15000, "total": 15000}'::jsonb,
 'draft', NULL, NULL, NULL),
('sales_order', 13, 'Order for StartupTech, basic SaaS plan for 25 users',
 '{"customer": "StartupTech Ventures", "customer_id": 11, "product": "SaaS Basic Plan", "product_id": 9, "quantity": 25, "unit_price": 99, "total": 2475}'::jsonb,
 'submitted', 13, NULL, NOW() - INTERVAL '2 days'),
('sales_order', 6, 'Create order for E-Commerce Hub, professional SaaS plan for 40 users',
 '{"customer": "E-Commerce Hub", "customer_id": 12, "product": "SaaS Professional Plan", "product_id": 10, "quantity": 40, "unit_price": 199, "total": 7960}'::jsonb,
 'submitted', 6, 12, NOW() - INTERVAL '7 days'),
('sales_order', 8, 'Order for Cloud Services, enterprise plan for 100 users',
 '{"customer": "Cloud Services Co", "customer_id": 13, "product": "SaaS Enterprise Plan", "product_id": 11, "quantity": 100, "unit_price": 299, "total": 29900}'::jsonb,
 'submitted', 8, 13, NOW() - INTERVAL '8 days'),
('sales_order', 10, 'Create order for Real Estate Group, API access package',
 '{"customer": "Real Estate Group", "customer_id": 14, "product": "API Access Package", "product_id": 12, "quantity": 1, "unit_price": 5000, "total": 5000}'::jsonb,
 'draft', NULL, NULL, NULL),
('sales_order', 11, 'Order for Consulting Partners, premium support package',
 '{"customer": "Consulting Partners Inc", "customer_id": 15, "product": "Premium Support Package", "product_id": 14, "quantity": 1, "unit_price": 2500, "total": 2500}'::jsonb,
 'submitted', 11, 15, NOW() - INTERVAL '9 days'),
('sales_order', 13, 'Create order for Innovation Labs, sales automation pro',
 '{"customer": "Innovation Labs", "customer_id": 16, "product": "Sales Automation Pro", "product_id": 3, "quantity": 1, "unit_price": 25000, "total": 25000}'::jsonb,
 'draft', NULL, NULL, NULL),
('sales_order', 14, 'Order for Automotive Solutions, data migration service',
 '{"customer": "Automotive Solutions LLC", "customer_id": 17, "product": "Data Migration Service", "product_id": 18, "quantity": 1, "unit_price": 18000, "total": 18000}'::jsonb,
 'submitted', 14, 17, NOW() - INTERVAL '10 days'),
('sales_order', 6, 'Create order for Food Services, advanced analytics module',
 '{"customer": "Food Services Corp", "customer_id": 18, "product": "Advanced Analytics Module", "product_id": 19, "quantity": 1, "unit_price": 3500, "total": 3500}'::jsonb,
 'submitted', 6, 18, NOW() - INTERVAL '11 days'),
('sales_order', 12, 'Order for Energy Systems, team collaboration plan for 60 users',
 '{"customer": "Energy Systems International", "customer_id": 19, "product": "Team Collaboration Plan", "product_id": 17, "quantity": 60, "unit_price": 149, "total": 8940}'::jsonb,
 'draft', NULL, NULL, NULL),
('sales_order', 12, 'Create order for Telecom Networks, additional storage 5TB',
 '{"customer": "Telecom Networks Ltd", "customer_id": 20, "product": "Additional Storage 1TB", "product_id": 13, "quantity": 5, "unit_price": 500, "total": 2500}'::jsonb,
 'submitted', 12, 20, NOW() - INTERVAL '12 days'),
('sales_order', 8, 'Order for Logistics Express, mobile receipt printers 50 units',
 '{"customer": "Logistics Express", "customer_id": 8, "product": "Mobile Receipt Printer", "product_id": 16, "quantity": 50, "unit_price": 350, "total": 17500}'::jsonb,
 'submitted', 8, NULL, NOW() - INTERVAL '13 days');

-- Insert Conversation History
INSERT INTO conversation_history (user_id, query, response, intent, agents_used, response_time_ms) VALUES
(6, 'How many orders did I receive today?', 'You received 52 orders today totaling $2.3M, which is 12% higher than yesterday. 47 orders are already fulfilled and 23 are pending.', 'order_status', 'OrderAgent', 1250),
(8, 'Show me pending orders over $100K', 'You have 5 pending orders over $100K: Disney ($500K), Tech Giants ($280K), Financial Services ($150K), Manufacturing Pro ($120K), and Cloud Services ($110K).', 'order_query', 'OrderAgent', 1840),
(6, 'Which region is underperforming this quarter?', 'LATAM is underperforming this quarter with only 65% of target achieved. North America and EMEA are exceeding targets at 112% and 108% respectively.', 'performance_analysis', 'PipelineAgent,OrderAgent', 2150),
(7, 'What is my pipeline for Q1 2026?', 'Your Q1 2026 pipeline has 8 opportunities totaling $3.2M with an average probability of 52%. Top deals: Cloud Services ($680K), Real Estate ($340K), and Consulting Partners ($295K).', 'pipeline_query', 'PipelineAgent', 1920),
(10, 'Compare this month vs last month', 'This month: $45.2M revenue (+8.5%), 1,245 orders (+12%), 42% win rate (-3%), Average deal size: $36.3K (+5%).', 'comparison', 'OrderAgent,PipelineAgent', 2680),
(9, 'What are my top customers by revenue?', 'Your top 5 customers by revenue: Tech Giants Inc ($3.2M), Disney Corporation ($2.5M), Financial Services LLC ($2.1M), Global Retail Co ($1.8M), and Healthcare Systems International ($1.6M).', 'customer_query', 'CustomerAgent', 1580),
(11, 'Show me deals in negotiation stage', 'You have 3 deals in negotiation: Global Retail Digital Transform ($850K, 80% probability), Financial Services AI Analytics ($650K, 75% probability), and Pharma Solutions Compliance Suite ($480K, 70% probability).', 'pipeline_query', 'PipelineAgent', 1720),
(6, 'What products are selling best this quarter?', 'Top selling products this quarter: Enterprise CRM Suite ($4.2M), Professional Services ($3.8M), Cloud Subscription ($3.5M), Hardware Tablets ($2.9M), and Support & Maintenance ($2.1M).', 'product_analysis', 'ProductAgent', 1960),
(12, 'Which sales rep has the highest win rate?', 'David Kim has the highest win rate at 58% with 12 closed won deals totaling $1.8M this quarter. Lisa Brown is second at 54% with $1.5M closed.', 'performance_analysis', 'PipelineAgent', 2240),
(13, 'Show me at-risk deals', 'You have 2 at-risk deals stalled >45 days: Logistics Express Route Optimization ($560K, 45 days in negotiation) and Telecom Networks Network Upgrade ($720K, 52 days in proposal).', 'pipeline_query', 'PipelineAgent', 1890),
(8, 'What is my forecast for next quarter?', 'Q1 2026 forecast: $18.5M weighted pipeline, 42 opportunities, expected close rate 38%, projected revenue $7.0M based on current velocity and historical patterns.', 'forecast', 'PipelineAgent,OrderAgent', 2450),
(14, 'Which customers need follow-up?', 'Priority follow-ups: Innovation Labs (45 days since last contact), Automotive Solutions (no activity in 30 days), Food Services (proposal pending 28 days), Energy Systems (demo scheduled but not confirmed).', 'customer_engagement', 'CustomerAgent', 1650),
(6, 'What is the average deal cycle time?', 'Average deal cycle: 67 days from lead to closed won. Lead to Qualified: 15 days, Qualified to Proposal: 18 days, Proposal to Negotiation: 22 days, Negotiation to Close: 12 days.', 'pipeline_analysis', 'PipelineAgent', 2120),
(10, 'Show me this week''s fulfilled orders', 'This week you fulfilled 47 orders totaling $3.8M. Top orders: Tech Giants ($750K), Global Retail ($850K), Manufacturing Pro ($390K), Healthcare Systems ($320K).', 'order_status', 'OrderAgent', 1480),
(11, 'Which territories are exceeding quota?', 'Territories exceeding quota: Northeast (118% of target), West Coast (112%), EMEA UK (109%). Underperforming: Central (87%), LATAM Brazil (72%).', 'performance_analysis', 'PipelineAgent,OrderAgent', 2050),
(7, 'What is my team''s average order value?', 'Your team''s average order value is $36,300, up 5% from last quarter. Highest AOV: David Kim ($48K), Lisa Brown ($42K). Team total: $12.4M across 342 orders.', 'order_analysis', 'OrderAgent', 1820),
(9, 'Show me customers with expiring contracts', '8 customers have contracts expiring in next 60 days: Disney (Nov 30), Tech Giants (Dec 15), Healthcare Systems (Dec 20), Manufacturing Pro (Jan 10), Education Network (Jan 15).', 'customer_query', 'CustomerAgent', 1740),
(12, 'What is the win rate by product category?', 'Win rates by category: Software (48%), Services (52%), Hardware (38%), Subscriptions (61%), Add-ons (44%). Highest margin: Services (70% gross margin).', 'product_analysis', 'ProductAgent,PipelineAgent', 2180),
(6, 'Create a summary of today''s activities', 'Today: 52 orders received ($2.3M), 47 fulfilled ($2.1M), 23 pending ($450K), 8 voice orders processed, 12 customer calls completed, 5 deals advanced to next stage, 2 new opportunities created.', 'daily_summary', 'OrderAgent,PipelineAgent,CustomerAgent', 2890),
(8, 'Which deals are likely to close this month?', '7 deals likely to close this month (>70% probability): Global Retail ($850K, 80%), Financial Services ($650K, 75%), Pharma Solutions ($480K, 70%), Cloud Services ($680K, 65%). Total weighted: $2.1M.', 'pipeline_forecast', 'PipelineAgent', 1950);

-- Update statistics
ANALYZE;

-- Display summary
SELECT 'Database seeded successfully!' as status;
SELECT 'Regions: ' || COUNT(*) FROM regions;
SELECT 'Users: ' || COUNT(*) FROM users;
SELECT 'Products: ' || COUNT(*) FROM products;
SELECT 'Customers: ' || COUNT(*) FROM customers;
SELECT 'Pipeline Opportunities: ' || COUNT(*) FROM pipeline;
SELECT 'Orders: ' || COUNT(*) FROM orders;
SELECT 'Order Items: ' || COUNT(*) FROM order_items;
SELECT 'AI Transactions: ' || COUNT(*) FROM transactions;
SELECT 'Conversation History: ' || COUNT(*) FROM conversation_history;
