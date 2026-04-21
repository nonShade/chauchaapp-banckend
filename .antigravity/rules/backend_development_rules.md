# Backend Development Rules

## Purpose
Ensure consistent, maintainable, and high-quality backend code following industry best practices and project-specific conventions.

## Architectural Rules

### 1. Layered Architecture
- **Controller Layer**: Handles HTTP requests/responses, input validation, and delegation to services.
  - Must use DTOs for request/response validation.
  - Must not contain business logic.
- **Service Layer**: Contains business logic, orchestration, and transaction management.
  - Must be independent of web framework.
  - Must delegate data access to repositories.
- **Repository Layer**: Abstracts data access (database, external APIs).
  - Must use proper ORM patterns or raw SQL with parameterization.
  - Must not contain business logic.

### 2. Separation of Concerns
- Each module (`auth`, `users`, `transactions`, etc.) must follow the layered structure:
  ```
  app/modules/{module}/
  ├── controller.py
  ├── service.py
  ├── repository.py
  ├── dto.py
  └── models.py (database models if using ORM)
  ```
- Shared utilities go in `app/shared/`.

### 3. DTO (Data Transfer Object) Usage
- All API input and output must be validated with Pydantic DTOs.
- DTOs must be separate from database models.
- Use `UserCreateDTO`, `UserResponseDTO` pattern.
- No raw dictionaries or tuples in API responses.

### 4. Error Handling
- Use custom exception hierarchy (e.g., `AppException`, `NotFoundException`, `ValidationException`).
- Exceptions must be caught at controller level and mapped to appropriate HTTP status codes.
- Error responses must follow consistent schema: `{"error": {"code": "...", "message": "..."}}`.

### 5. Dependency Injection
- Use dependency injection for services and repositories to enable testing.
- Avoid global state and singletons where possible.

## Code Quality Rules

### 1. Code Style
- Follow PEP 8 with line length 100.
- Use `black` for formatting, `isort` for imports.
- Use type hints for all function signatures and public APIs.
- Run `mypy` for static type checking.

### 2. Documentation
- Public functions and classes must have docstrings (Google style).
- Complex business logic must have inline comments explaining "why", not "what".
- API endpoints must be documented with OpenAPI/Swagger.

### 3. Testing
- Follow Test-Driven Development (TDD) where applicable.
- Unit test coverage must exceed 90% for new code.
- Tests must be independent, fast, and without side effects.
- Use fixtures and factories for test data.

### 4. Security
- Validate all user input (DTO validation, SQL injection prevention).
- Use parameterized queries; never concatenate SQL strings.
- Implement proper authentication/authorization for protected endpoints.
- Sanitize logs to avoid leaking sensitive data.

## Development Process Rules

### 1. TDD Workflow
1. Write failing test (unit or integration)
2. Implement minimal code to pass test
3. Refactor while keeping tests green
4. Repeat

### 2. Code Review
- All code changes must be reviewed by another agent (via Orchestrator).
- Review checklist: architecture compliance, test coverage, security, performance.

### 3. Version Control
- Commit messages must follow Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`.
- Each feature/bugfix must be in a separate branch.
- No direct commits to `main` or `develop` branches.

## Technology Specifics

### 1. Python
- Use Python 3.12+ features where appropriate.
- Prefer `uv` for dependency management.
- Use `pytest` for testing.

### 2. Database
- Use SQLAlchemy as ORM (if applicable).
- Migrations must be versioned (Alembic).

### 3. API
- RESTful design with proper HTTP methods and status codes.
- Version APIs via URL path (`/api/v1/...`).
- Pagination, filtering, sorting for list endpoints.

## Enforcement
- PythonBackendDeveloper must adhere to these rules.
- QADeveloper validates compliance through tests.
- Orchestrator monitors rule adherence during task execution.