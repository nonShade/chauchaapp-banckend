# PostgreSQL Development Rules

## Purpose
Ensure consistent, secure, and performant PostgreSQL database development across all environments. Establish standards for schema design, migrations, query optimization, and data management.

## Schema Design Rules

### 1. Naming Conventions
- **Tables**: Plural snake_case (e.g., `users`, `order_items`)
- **Columns**: Singular snake_case (e.g., `first_name`, `created_at`)
- **Primary Keys**: `id` column with `SERIAL`/`BIGSERIAL` or `UUID` (use `UUID` for distributed systems)
- **Foreign Keys**: `{referenced_table}_id` (e.g., `user_id` references `users.id`)
- **Indexes**: `idx_{table}_{columns}` (e.g., `idx_users_email`)
- **Constraints**: `ck_{table}_{constraint}` for check constraints

### 2. Data Types
- Use appropriate PostgreSQL native types:
  - `INTEGER`/`BIGINT` for counts, IDs
  - `VARCHAR(n)` with reasonable length limits (avoid `TEXT` for short strings unless unlimited)
  - `TEXT` for long, unbounded strings
  - `BOOLEAN` for true/false values
  - `TIMESTAMP WITH TIME ZONE` (`TIMESTAMPTZ`) for all timestamps
  - `NUMERIC(p,s)` for exact decimal numbers (money, measurements)
  - `JSONB` for semi-structured data (preferred over `JSON`)
- Avoid database-specific types that hinder portability unless necessary.

### 3. Constraints
- Always define `PRIMARY KEY` on every table
- Use `FOREIGN KEY` constraints with explicit `ON DELETE` and `ON UPDATE` actions:
  - `ON DELETE RESTRICT` for critical relations
  - `ON DELETE CASCADE` for dependent records (e.g., user comments)
  - `ON DELETE SET NULL` for optional relations
- Apply `NOT NULL` where column must always have a value
- Use `UNIQUE` constraints for business uniqueness (email, username)
- Implement `CHECK` constraints for domain validation (e.g., `price > 0`)

### 4. Default Values and Timestamps
- Use `DEFAULT CURRENT_TIMESTAMP` for `created_at` columns
- Update `updated_at` via trigger or application logic (never default)
- Consider `DEFAULT` values for non‑nullable columns with predictable initial values

### 5. Indexing Strategy
- Create indexes on all foreign key columns
- Add indexes for columns used in `WHERE`, `ORDER BY`, `JOIN`, and `GROUP BY`
- Use composite indexes for queries filtering multiple columns
- Consider `CREATE INDEX CONCURRENTLY` for production migrations
- Monitor index usage and remove unused indexes
- Use partial indexes for filtered queries (`WHERE status = 'active'`)
- Consider `UNIQUE` indexes for uniqueness constraints

## Migration Rules

### 1. Version Control
- All schema changes must be captured in versioned migration scripts
- Use Alembic for SQLAlchemy projects; raw SQL migrations must be idempotent
- Each migration should be a single logical change (avoid bundling unrelated changes)

### 2. Safety
- Never run `DROP TABLE`, `DROP COLUMN`, or `DROP INDEX` without a backup plan
- Provide `downgrade` steps for every migration (Alembic) or keep reversible SQL scripts
- Test migrations on a copy of production data before applying to production
- Use `IF EXISTS`/`IF NOT EXISTS` to make scripts idempotent

### 3. Data Migrations
- Separate schema migrations from data migrations when possible
- For large data changes, use batched updates to avoid locking
- Always verify data integrity after migration (counts, constraints)

### 4. Ordering
- Migrations must be applied in dependency order (create tables before foreign keys)
- Coordinate with application code deployment to avoid breaking changes

## Query and Performance Rules

### 1. SQL Writing
- Use parameterized queries exclusively to prevent SQL injection
- Prefer `JOIN` over multiple queries (N+1 problem)
- Use `EXPLAIN ANALYZE` to understand query plans
- Avoid `SELECT *`; explicitly list needed columns
- Use `LIMIT` for pagination; pair with `ORDER BY` for deterministic results

### 2. Transaction Management
- Keep transactions as short as possible
- Use appropriate isolation levels (default `READ COMMITTED` is usually sufficient)
- Handle transaction rollback on errors
- Avoid long-running transactions that hold locks

### 3. Connection Management
- Use connection pooling (SQLAlchemy pool, PgBouncer)
- Set reasonable timeouts (`statement_timeout`, `idle_in_transaction_timeout`)
- Monitor connection counts and prevent leaks

## Security Rules

### 1. Access Control
- Use principle of least privilege for database roles
- Create separate roles for application, migration, and admin tasks
- Grant only necessary permissions (`SELECT`, `INSERT`, `UPDATE`, `DELETE`)
- Never use superuser (`postgres`) for application connections

### 2. Data Protection
- Encrypt sensitive columns using `pgcrypto` (passwords, PII)
- Never store plain-text passwords; use strong hashing (bcrypt, argon2)
- Mask sensitive data in logs and error messages
- Implement row-level security (RLS) for multi-tenant applications

### 3. Network Security
- Use SSL/TLS for all production connections
- Restrict database access to trusted networks (VPC, firewall rules)
- Regularly rotate database credentials

## Environment-Specific Rules

### 1. Development
- May use simplified security settings for local development
- Populate with realistic but fake test data (no real PII)
- Automatically apply migrations on application start if safe

### 2. QA/Staging
- Mirror production schema and approximate data volume
- Use anonymized production data or generated test data
- Test all migrations before production deployment

### 3. Production
- All migrations must be reviewed and tested in staging first
- Perform backups before any schema change
- Have a rollback plan for every migration
- Monitor performance impact of changes

## Documentation Rules

### 1. Schema Documentation
- Maintain an up‑to‑date ER diagram (using `pg_dump --schema-only` or tools)
- Document business meaning of tables and columns in a data dictionary
- Note indexes and their purpose (which queries they optimize)

### 2. Migration Documentation
- Each migration script must include a comment describing the change and why
- Document any manual steps required alongside automated migrations
- Keep a changelog of database changes linked to application versions

## Collaboration Rules

### 1. With PythonBackendDeveloper
- Database schema changes must be reflected in SQLAlchemy models
- Repository layer queries should be reviewed for performance and correctness
- Coordinate on transaction boundaries and error handling

### 2. With QADeveloper
- Provide test data generation scripts for integration tests
- Help design database fixtures and factories
- Assist with performance testing of database queries

### 3. With DevOpsDeveloper
- Define backup and recovery procedures
- Set up monitoring and alerts for database metrics
- Configure database container resources and scaling

## Enforcement
- PostgreSQLDatabaseDeveloper must adhere to these rules
- PythonBackendDeveloper must follow rules when writing raw SQL
- Orchestrator validates rule compliance during task execution
- QADeveloper includes database rule checks in integration tests