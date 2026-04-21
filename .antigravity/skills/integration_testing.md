# Integration Testing Skill

## Description
Enables agents to write integration tests that verify components work together correctly. Tests interactions between layers (controller-service-repository), API endpoints, and external services.

## Capabilities

### 1. API Endpoint Testing
- Test HTTP endpoints with actual server running
- Send requests and validate responses (status codes, headers, body)
- Test authentication/authorization flows
- Test error responses and edge cases

### 2. Database Integration Testing
- Test repository layer with real database (in-memory SQLite, testcontainers)
- Verify CRUD operations, transactions, and constraints
- Test database migrations (Alembic)
- Ensure data consistency across operations

### 3. External Service Integration
- Mock external APIs with tools like `responses`, `httpx_mock`
- Test retry logic, timeouts, error handling
- Verify contract compliance (request/response formats)

### 4. Component Integration
- Test service + repository integration (without HTTP layer)
- Test controller + service integration (with mocked dependencies)
- Verify data flow across layers

### 5. End-to-End Workflow Testing
- Test complete user flows across multiple endpoints
- Maintain session state (cookies, tokens) across requests
- Verify side effects (emails sent, events published)

### 6. Test Environment Management
- Set up test databases with schema and seed data
- Start/stop test servers (FastAPI, Reflex)
- Manage test containers (Docker) for external services

## Input/Output

### Input
- API specification (endpoints, request/response formats)
- Database schema and seed data requirements
- External service contracts
- User workflows to test

### Output
- Integration test files
- Test environment configuration
- Test data fixtures
- Test results (pass/fail, performance metrics)

## Workflow Integration

### 1. Test Strategy
- Decide which integrations to test (API, database, external services)
- Determine test scope (happy path, error cases, performance)
- Set up test environment (database, server, mocks)

### 2. Test Implementation
- Write test that exercises integration point
- Verify both success and failure scenarios
- Clean up test data after each test

### 3. Test Execution
- Run integration tests in CI pipeline
- Isolate integration tests from unit tests (different markers)
- Monitor test duration and flakiness

## Example Usage

### Testing User Registration Endpoint
```python
# tests/integration/api/test_user_registration.py

def test_register_user_success(test_client):
    """Test POST /users creates user and returns 201."""
    # Arrange
    user_data = {"email": "new@example.com", "password": "secure"}
    
    # Act
    response = test_client.post("/users", json=user_data)
    
    # Assert
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["email"] == user_data["email"]

def test_register_user_duplicate_email(test_client, existing_user):
    """Test duplicate email returns 409 Conflict."""
    # Arrange
    user_data = {"email": existing_user.email, "password": "different"}
    
    # Act
    response = test_client.post("/users", json=user_data)
    
    # Assert
    assert response.status_code == 409
    assert "error" in response.json()
```

### Testing Database Repository
```python
# tests/integration/database/test_user_repository.py

def test_user_repository_create_real_db(db_session):
    """Test UserRepository.create with real database session."""
    # Arrange
    repo = UserRepository(db_session)
    
    # Act
    user = repo.create(email="test@example.com", password="hashed")
    
    # Assert
    assert user.id is not None
    assert user.email == "test@example.com"
    
    # Verify persistence
    persisted = repo.get_by_id(user.id)
    assert persisted.email == user.email
```

## Best Practices

### 1. Test Isolation
- Each test should leave the database in the same state it found it
- Use transactions that roll back after each test
- Clear caches between tests

### 2. Performance
- Reuse expensive resources (database connections, test containers)
- Run integration tests less frequently than unit tests
- Use test data factories instead of hardcoded fixtures

### 3. Reliability
- Handle transient failures (network issues, timeouts)
- Use retries with exponential backoff for flaky operations
- Mark flaky tests and investigate root cause

### 4. Maintainability
- Separate test data setup into fixtures
- Use shared test utilities (`conftest.py`)
- Document assumptions about test environment

## Tools
- **HTTP Testing**: `httpx`, `requests`, `pytest-asyncio` for async
- **Database Testing**: `testcontainers`, `pytest-postgresql`, `sqlite` in-memory
- **Mocking External Services**: `responses`, `httpx_mock`, `vcr.py`
- **Test Server**: `uvicorn` test client, FastAPI/Reflex test client
- **Environment Management**: `pytest-docker`, `docker-compose` for integration

## Dependencies
- QADeveloper agent primarily uses this skill
- Requires coordination with DevOpsDeveloper for test container setup
- May require database schema and seed data