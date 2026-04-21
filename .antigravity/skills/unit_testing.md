# Unit Testing Skill

## Description
Enables agents to write comprehensive unit tests for Python code, ensuring each component works correctly in isolation. Follows pytest framework and promotes test-driven development.

## Capabilities

### 1. Test Structure Creation
- Create test files mirroring source structure (`tests/unit/controllers/`, `tests/unit/services/`, etc.)
- Write test classes and functions following pytest conventions
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`

### 2. Test Data Management
- Create test fixtures using `@pytest.fixture`
- Generate mock data with `factory_boy` or manual creation
- Set up and tear down test environment cleanly

### 3. Mocking Dependencies
- Mock external services (databases, APIs, file system) using `unittest.mock` or `pytest-mock`
- Simulate different responses (success, errors, timeouts)
- Verify mock interactions (`assert_called_with`, `assert_called_once`)

### 4. Assertion Writing
- Use Python's `assert` statement with descriptive messages
- Leverage pytest's built-in assertions for containers, exceptions, etc.
- Use `pytest.raises` to test expected exceptions
- Assert on complex data structures with `pytest.approx` for floats

### 5. Parameterized Testing
- Use `@pytest.mark.parametrize` for multiple test cases
- Test edge cases and boundary values
- Generate combinatorial test scenarios

### 6. Coverage Analysis
- Use `pytest-cov` to measure test coverage
- Identify untested code paths
- Generate coverage reports (HTML, XML)

### 7. Test Optimization
- Write fast, independent tests (no I/O, network)
- Use `pytest-xdist` for parallel test execution
- Tag tests (`@pytest.mark.slow`, `@pytest.mark.integration`) for selective running

## Input/Output

### Input
- Source code to test (functions, classes, modules)
- Requirements and edge cases to cover
- Existing test suite (for extension)

### Output
- Test files with comprehensive test cases
- Updated `conftest.py` with shared fixtures
- Coverage reports
- Test results (pass/fail, duration)

## Workflow Integration

### TDD Mode
1. Write failing unit test based on requirements
2. Implement minimal code to pass test
3. Refactor code and tests together
4. Repeat for next requirement

### Test-After Mode
1. Analyze existing code for behavior
2. Write tests to verify current behavior (characterization tests)
3. Add tests for edge cases and error conditions
4. Refactor with confidence

## Example Usage

### Testing a Service Function
```python
# app/modules/users/service.py
def register_user(email: str, password: str) -> User:
    # ... implementation

# tests/unit/services/test_user_service.py
def test_register_user_success(mock_user_repo):
    # Arrange
    email = "test@example.com"
    password = "secure"
    mock_user_repo.create.return_value = User(id=1, email=email)
    
    # Act
    result = register_user(email, password)
    
    # Assert
    assert result.id == 1
    assert result.email == email
    mock_user_repo.create.assert_called_once_with(email=email, password=password)

def test_register_user_duplicate_email(mock_user_repo):
    # Arrange
    mock_user_repo.create.side_effect = DuplicateEmailError()
    
    # Act & Assert
    with pytest.raises(DuplicateEmailError):
        register_user("existing@example.com", "password")
```

## Best Practices

### 1. Test Isolation
- Each test must be independent
- Reset mocks between tests
- Use transaction rollback for database tests

### 2. Readability
- Follow AAA pattern (Arrange, Act, Assert)
- Use helper functions for complex setup
- Name tests clearly: `test_<method>_when_<condition>_then_<result>`

### 3. Maintainability
- Avoid magic numbers and strings; use constants
- Share fixtures via `conftest.py`
- Keep tests close to the code they test

### 4. Performance
- Mock slow dependencies (network, disk I/O)
- Use `pytest --durations` to identify slow tests
- Run unit tests frequently during development

## Tools
- **Framework**: pytest
- **Mocking**: pytest-mock, unittest.mock
- **Factories**: factory_boy, faker
- **Coverage**: pytest-cov
- **Parameterization**: pytest.mark.parametrize

## Dependencies
- QADeveloper agent primarily uses this skill
- PythonBackendDeveloper may use it during TDD
- Requires source code to test