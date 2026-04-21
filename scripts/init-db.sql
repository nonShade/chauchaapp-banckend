-- Initial database setup for chauchaapp-backend
-- This script runs when PostgreSQL container starts for the first time

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create additional databases for QA and Production environments
-- Note: PostgreSQL only creates the main database from POSTGRES_DB environment variable
-- Additional databases are created here for different environments

-- Create QA database if it doesn't exist
CREATE DATABASE chauchaapp_db_qa;

-- Create production database if it doesn't exist
CREATE DATABASE chauchaapp_db_prod;

-- You can add initial data or schema migrations here
-- For example:
-- CREATE TABLE IF NOT EXISTS users (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Grant permissions (if using different users)
GRANT ALL PRIVILEGES ON DATABASE chauchaapp_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE chauchaapp_db_qa TO postgres;
GRANT ALL PRIVILEGES ON DATABASE chauchaapp_db_prod TO postgres;