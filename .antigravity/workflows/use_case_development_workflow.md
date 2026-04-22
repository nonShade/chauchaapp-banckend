# Use Case Development Workflow

## Purpose
Systematically develop a complete use case from specification to deployed feature, including all layers (controller, service, repository) and corresponding test cases.

## Participants
- **Orchestrator**: Oversees the entire workflow, ensures adherence to process
- **PythonBackendDeveloper**: Implements production code for each layer
- **QADeveloper**: Develops and executes test cases
- **DevOpsDeveloper**: Configures deployment and environment if needed
- **PostgreSQLDatabaseDeveloper**: Designs and implements database schema changes, migrations, and test data

## Workflow Overview

### Phase 0: Specification Intake
1. **Orchestrator** receives a use case specification (natural language or structured).
2. **Orchestrator** uses Specs Driven Development skill to create:
   - Use case narrative
   - Actor(s) and system interactions
   - Preconditions, postconditions, invariants
   - Main success scenario
   - Extension/alternative scenarios (error cases)
3. **Orchestrator** validates specification with user, clarifies ambiguities.

### Phase 1: Architecture Design
1. **Orchestrator** identifies affected modules and layers.
2. **Orchestrator** designs:
   - API endpoints (HTTP methods, URLs, request/response schemas)
   - Database schema changes (new tables, columns, indexes)
   - Service layer methods and business logic flow
   - Integration points with external systems
3. **Orchestrator** creates a task breakdown with dependencies.

### Phase 2: Test Case Development
1. **QADeveloper** creates test cases for each scenario:
   - **Main success scenario**: Happy path test
   - **Alternative scenarios**: Edge cases, validation errors
   - **Error scenarios**: System failures, external service errors
2. Test cases are documented as:
   - Gherkin-style scenarios (Given-When-Then)
   - Test data requirements
   - Expected outcomes
3. **Orchestrator** reviews test cases for completeness.

### Phase 3: Layered Implementation (TDD)
For each layer (Repository → Service → Controller), follow TDD workflow:

#### Step 3.0: Database Schema Implementation
1. **PostgreSQLDatabaseDeveloper** designs database schema based on architecture design.
2. **PostgreSQLDatabaseDeveloper** creates SQL DDL scripts or Alembic migrations.
3. **PostgreSQLDatabaseDeveloper** generates test data for QA environment if needed.
4. **PostgreSQLDatabaseDeveloper** coordinates with PythonBackendDeveloper on ORM model definitions.

#### Step 3.1: Repository Layer
1. **QADeveloper** writes failing unit tests for repository methods.
2. **PythonBackendDeveloper** implements repository to pass tests (using database schema from Step 3.0).
3. **QADeveloper** writes integration tests with real database.
4. **PythonBackendDeveloper** fixes any integration issues.

#### Step 3.2: Service Layer
1. **QADeveloper** writes failing unit tests for service methods (mocking repository).
2. **PythonBackendDeveloper** implements service logic to pass tests.
3. **QADeveloper** writes integration tests for service + repository.
4. **PythonBackendDeveloper** fixes integration issues.

#### Step 3.3: Controller Layer
1. **QADeveloper** writes failing unit tests for controller (mocking service).
2. **PythonBackendDeveloper** implements controller endpoints.
3. **QADeveloper** writes API integration tests (HTTP level).
4. **PythonBackendDeveloper** fixes API issues.

### Phase 4: End-to-End Testing
1. **QADeveloper** creates end-to-end test that exercises the full use case:
   - Simulates actor actions through API calls
   - Verifies system state changes
   - Validates side effects (emails, notifications, etc.)
2. **PythonBackendDeveloper** fixes any bugs discovered.

### Phase 5: Non-Functional Requirements
1. **QADeveloper** performs:
   - Performance testing (response time under load)
   - Security testing (input validation, SQL injection, auth checks)
   - Compatibility testing (different clients, data formats)
2. **DevOpsDeveloper** ensures:
   - Monitoring and logging are configured
   - Deployment configuration supports the new feature
   - Scaling considerations if needed

### Phase 6: Validation & Deployment
1. **Orchestrator** runs full test suite (unit, integration, e2e).
2. **Orchestrator** verifies all acceptance criteria are met.
3. **DevOpsDeveloper** creates or updates deployment configuration.
4. **Orchestrator** coordinates deployment to staging environment.
5. **QADeveloper** performs smoke tests in staging.
6. **Orchestrator** approves promotion to production.

## Artifacts

### 1. Use Case Specification Document
- Located in `docs/use_cases/{use_case_name}.md`
- Contains narrative, scenarios, actors, data models

### 2. Test Case Document
- Located in `tests/use_cases/{use_case_name}.md`
- Lists all test scenarios with Gherkin format
- Maps to actual test files

### 3. API Contract
- OpenAPI specification in `docs/api/{use_case_name}.yaml`
- Request/response examples

### 4. Task Board
- Tracked in `.antigravity/tasks/{use_case_name}.md`
- Shows progress across layers and test types

## Example: User Registration Use Case

### Specification
**Actor**: Anonymous User  
**Precondition**: User is not logged in, email not already registered  
**Main Success Scenario**:
1. User submits email and password via registration form
2. System validates email format and password strength
3. System checks email uniqueness
4. System hashes password and stores user record
5. System returns user ID and confirmation

**Alternative Scenarios**:
- Email already registered → error message
- Invalid email format → validation error
- Password too weak → validation error
- Database unavailable → system error

### Architecture Design
- **Endpoint**: POST /api/v1/users
- **DTOs**: UserCreateDTO (email, password), UserResponseDTO (id, email, created_at)
- **Repository**: UserRepository.create(), UserRepository.get_by_email()
- **Service**: UserService.register_user() (business logic, password hashing)
- **Controller**: UserController.register() (HTTP handling)

### Test Cases
1. **TC1**: Valid registration → 201 Created
2. **TC2**: Duplicate email → 409 Conflict
3. **TC3**: Invalid email → 400 Bad Request
4. **TC4**: Short password → 400 Bad Request
5. **TC5**: Database error → 500 Internal Server Error

### Implementation Order
1. Repository layer (UserRepository)
2. Service layer (UserService)
3. Controller layer (UserController)
4. Integration tests
5. End-to-end flow

## Quality Gates

### Gate 1: Specification Complete
- All scenarios defined and approved
- API contract finalized
- Test cases documented

### Gate 2: Layer Completion
- Each layer passes all unit tests
- Integration tests between layers pass
- Code review completed

### Gate 3: End-to-End Validation
- All test scenarios pass
- Performance requirements met
- Security review passed

### Gate 4: Deployment Ready
- Configuration updated
- Monitoring in place
- Rollback plan defined

## Tools
- **Specification**: Markdown, Mermaid diagrams
- **Testing**: pytest, pytest-bdd (for Gherkin), testcontainers
- **API Design**: OpenAPI, Swagger UI
- **Task Tracking**: Markdown task lists, GitHub Projects

## Exit Criteria
- Use case fully implemented and tested
- All acceptance criteria satisfied
- Deployed to production (or ready for deployment)
- Documentation updated
- Team knowledge transferred