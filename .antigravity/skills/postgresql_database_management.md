# PostgreSQL Database Management Skill

## Description
Enables agents to design, implement, and manage PostgreSQL databases, including schema design, SQL scripting, migrations, performance optimization, and test data generation. This skill ensures database solutions are scalable, secure, and aligned with project requirements.

## Capabilities

### 1. Database Schema Design
- Design normalized database schemas with proper table relationships (1:1, 1:N, N:M)
- Define appropriate data types (integer, varchar, text, boolean, timestamp, jsonb)
- Implement constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK)
- Create indexes (B-tree, GIN, GiST) for query optimization
- Design partitioning strategies for large tables
- Implement row-level security and column encryption where needed

### 2. SQL Script Development
- Write DDL scripts (CREATE, ALTER, DROP) with idempotent patterns
- Write DML scripts (INSERT, UPDATE, DELETE) for data manipulation
- Use transactions with proper COMMIT/ROLLBACK semantics
- Implement stored procedures, functions, and triggers when appropriate
- Use COPY command for bulk data loading

### 3. Migration Management
- Create versioned schema migrations using Alembic or raw SQL
- Ensure migrations are reversible (upgrade/downgrade)
- Handle data migrations (schema changes with data transformation)
- Manage migration dependencies and ordering
- Test migrations in isolated environments before deployment

### 4. Performance Optimization
- Analyze query performance using EXPLAIN ANALYZE
- Identify and create missing indexes
- Optimize query patterns (avoid N+1, use JOINs appropriately)
- Configure database parameters (work_mem, shared_buffers, maintenance_work_mem)
- Implement connection pooling (PgBouncer, SQLAlchemy pool)
- Monitor performance metrics (pg_stat_statements, pg_stat_user_tables)

### 5. Test Data Generation
- Generate realistic but fake test data for development and QA
- Maintain referential integrity across related tables
- Create data factories for different test scenarios (edge cases, load testing)
- Use tools like Faker or custom SQL scripts
- Ensure no real personal information in test data

### 6. Security Implementation
- Design role-based access control (CREATE ROLE, GRANT, REVOKE)
- Implement SSL connections for production
- Use parameterized queries to prevent SQL injection
- Encrypt sensitive columns (pgcrypto extension)
- Audit logging for sensitive operations

### 7. Backup and Recovery
- Design backup strategies (full, incremental, continuous archiving)
- Create backup scripts using pg_dump/pg_dumpall
- Implement point-in-time recovery (PITR) with WAL archiving
- Test restore procedures regularly

### 8. Monitoring and Maintenance
- Set up monitoring for database health (connections, locks, disk space)
- Implement vacuum and analyze maintenance jobs
- Monitor replication lag if using replication
- Set up alerts for critical issues

## Input/Output

### Input
- Requirements specification (entities, relationships, data volume)
- Performance requirements (query latency, throughput)
- Existing database schema (for modifications)
- Environment context (dev, QA, prod)

### Output
- SQL DDL scripts for schema creation
- Alembic migration files
- Test data generation scripts
- Performance optimization recommendations
- Database configuration recommendations
- Documentation (ER diagrams, data dictionary)

## Workflow Integration

1. **Receive task** from Orchestrator with database requirements
2. **Analyze requirements** and design database solution
3. **Create SQL scripts** or Alembic migrations
4. **Test changes** in isolated environment (if available)
5. **Coordinate** with PythonBackendDeveloper for ORM model updates
6. **Generate test data** if required for QA
7. **Document** changes and update schema documentation
8. **Submit** for review via Orchestrator

## Example Usage

### Task: "Create database schema for user authentication"
1. Design tables: `users`, `roles`, `user_roles`, `sessions`
2. Create relationships: users ↔ roles (many-to-many via user_roles)
3. Add columns: users.id (PK), users.email (UNIQUE), users.password_hash, users.created_at
4. Create indexes on users.email, sessions.user_id
5. Write SQL script in `scripts/schema/auth_tables.sql`
6. Create Alembic migration: `alembic revision --autogenerate -m "add auth tables"`
7. Generate test data: 100 users with realistic emails and passwords (hashed)
8. Update `app/shared/database/models.py` with SQLAlchemy models

### Task: "Optimize slow user query"
1. Analyze current query with `EXPLAIN ANALYZE`
2. Identify missing indexes on WHERE/JOIN columns
3. Create appropriate index: `CREATE INDEX idx_users_email ON users(email)`
4. Test query performance improvement
5. Create migration for index addition
6. Document index in schema documentation

## Tools
- **Database**: PostgreSQL 16+
- **CLI**: psql, pg_dump, pg_restore
- **Migration**: Alembic, Flyway (if applicable)
- **ORM**: SQLAlchemy 2.0+
- **Monitoring**: pg_stat_statements, pgAdmin, Grafana with PostgreSQL datasource
- **Testing**: pytest with testcontainers-postgresql
- **Data Generation**: Faker library, custom SQL scripts

## Dependencies
- PostgreSQLDatabaseDeveloper agent uses this skill
- Requires coordination with PythonBackendDeveloper for ORM integration
- Requires coordination with QADeveloper for test data and integration tests
- Requires coordination with DevOpsDeveloper for container configuration and backups

## Best Practices
- Always use parameterized queries to prevent SQL injection
- Test migrations on a copy of production data before applying to production
- Keep migrations small and focused on single logical changes
- Document schema changes and their business rationale
- Regularly vacuum and analyze tables to maintain performance
- Monitor long-running queries and connection counts
- Implement connection pooling to handle concurrent requests
- Use database-specific features (JSONB, full-text search) when appropriate