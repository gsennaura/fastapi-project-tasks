-- 🗄️ Database Initialization Script
-- This script runs when PostgreSQL container starts for the first time

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set timezone
SET timezone = 'UTC';

-- Create indexes after tables are created by Alembic
-- Note: Actual table creation is handled by Alembic migrations
-- This file is for additional database setup if needed

-- Grant permissions (if needed for production)
-- GRANT ALL PRIVILEGES ON DATABASE projectsdb TO postgres;
