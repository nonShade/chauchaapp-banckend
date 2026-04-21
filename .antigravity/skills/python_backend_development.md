# Python Backend Development Skill

## Description
Enables agents to develop Python backend code following project architecture, conventions, and best practices. This skill encompasses creating controllers, services, repositories, DTOs, and integrating with databases and external APIs.

## Capabilities

### 1. Project Structure Navigation
- Understand and navigate the modular project structure (`app/modules/{module}/`)
- Identify appropriate locations for new code based on layer (controller, service, repository, dto)
- Locate shared utilities in `app/shared/`

### 2. Code Generation
- Generate Python classes and functions with proper imports and type hints
- Follow PEP 8 and project-specific formatting rules
- Create DTOs using Pydantic with appropriate validation
- Implement CRUD operations with proper error handling

### 3. Architectural Patterns Implementation
- Implement layered architecture (Controller-Service-Repository)
- Apply dependency injection patterns
- Design RESTful API endpoints with proper HTTP methods and status codes
- Use dependency inversion for testability

### 4. Database Integration
- Design database models (SQLAlchemy or similar ORM)
- Create repository classes with CRUD methods
- Implement transaction management
- Handle database migrations (Alembic)

### 5. API Development
- Define route handlers with request/response validation
- Implement authentication/authorization middleware
- Add OpenAPI documentation via decorators or separate spec
- Handle file uploads, pagination, filtering as needed

### 6. Error Handling
- Create custom exception hierarchy
- Implement global exception handlers
- Return consistent error responses

### 7. Performance Optimization
- Implement caching strategies (Redis, in-memory)
- Use connection pooling for databases
- Optimize queries with indexing and eager/lazy loading

## Input/Output

### Input
- Requirements specification (user story, acceptance criteria)
- Existing codebase context
- API design constraints (endpoints, data models)

### Output
- Production-ready Python code
- Updated `pyproject.toml` dependencies if needed
- Database migration scripts (if applicable)
- Updated OpenAPI documentation

## Workflow Integration

1. **Receive task** from Orchestrator with clear specifications
2. **Analyze requirements** and design solution
3. **Follow TDD** (write failing test first or coordinate with QADeveloper)
4. **Implement code** in appropriate layers
5. **Verify** code passes tests and meets acceptance criteria
6. **Submit** for review via Orchestrator

## Example Usage

### Task: "Create endpoint to fetch user profile"
1. Identify existing user module structure
2. Check if User DTOs already exist; create if missing
3. Implement or update UserRepository.get_by_id
4. Implement UserService.get_profile
5. Implement UserController.get_profile endpoint (GET /users/{id})
6. Add OpenAPI documentation
7. Write unit tests (or coordinate with QADeveloper)

## Tools
- **Language**: Python 3.12+
- **Framework**: Reflex (or FastAPI/Flask patterns)
- **Validation**: Pydantic v2
- **Database**: SQLAlchemy, asyncpg
- **Testing**: pytest (via QADeveloper collaboration)
- **Formatting**: black, isort
- **Linting**: mypy, pylint

## Dependencies
- PythonBackendDeveloper agent uses this skill
- Requires coordination with QADeveloper for tests
- Requires coordination with DevOpsDeveloper for deployment configuration