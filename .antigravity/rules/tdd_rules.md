# Test-Driven Development (TDD) Rules

## Purpose
Ensure high-quality, reliable code through rigorous test-first development practices.

## Core TDD Cycle (Red-Green-Refactor)

### 1. Red Phase
- Write a **failing test** that defines a desired improvement or new function.
- The test must fail for the expected reason (not compilation errors).
- Tests should be small and focused on a single behavior.

### 2. Green Phase
- Write the **minimum code** necessary to make the test pass.
- Do not add extra functionality; keep it simple.
- If the test passes, move to refactor phase.

### 3. Refactor Phase
- **Improve the code** while keeping tests green.
- Remove duplication, improve readability, apply design patterns.
- Ensure all tests still pass after refactoring.

## Rules for Developers

### 1. Test First
- No production code should be written without a failing test.
- Exception: scaffolding (file structure, empty classes) may be created but must be immediately followed by tests.

### 2. Test Isolation
- Each test must be independent and not rely on state from other tests.
- Use `setup`/`teardown` or fixtures to ensure clean state.
- Mock external dependencies (databases, APIs, filesystem).

### 3. Test Granularity
- Unit tests: test one function/method in isolation.
- Integration tests: test interaction between components (e.g., service + repository).
- End-to-end tests: test complete workflows (API endpoints).
- Write tests at the appropriate level; prefer unit tests for business logic.

### 4. Test Quality
- Tests must be readable and maintainable.
- Use descriptive test names: `test_<function>_<scenario>_<expected_behavior>`.
- Follow AAA pattern: Arrange, Act, Assert.
- Include edge cases, error conditions, and boundary values.

### 5. Coverage Requirements
- Aim for **90%+ line coverage** for new code.
- Critical paths must have 100% coverage.
- Use `pytest-cov` to measure coverage.

## Workflow Integration

### 1. Task Decomposition
- Orchestrator breaks features into testable units.
- Each subtask includes acceptance criteria expressed as test scenarios.

### 2. Collaboration between PythonBackendDeveloper and QADeveloper
- Option A: QADeveloper writes failing tests, PythonBackendDeveloper implements.
- Option B: PythonBackendDeveloper writes own tests (still following TDD).
- Both agents must ensure tests are comprehensive.

### 3. Continuous Testing
- Run unit tests on every change (via pre‑commit hooks or CI).
- Integration tests run at least before merging to `develop`.

## Example TDD Flow for User Registration

### Step 1: Define DTO validation (Red)
```python
# tests/unit/dto/test_user_dto.py
def test_user_create_dto_valid():
    data = {"email": "test@example.com", "password": "secure"}
    dto = UserCreateDTO(**data)
    assert dto.email == data["email"]
```

### Step 2: Implement DTO (Green)
```python
# app/modules/users/dto.py
class UserCreateDTO(BaseModel):
    email: EmailStr
    password: SecretStr
```

### Step 3: Refactor (if needed)
- Add more validation rules, reuse email validation logic.

### Step 4: Repeat for service layer, repository, controller.

## Tools
- `pytest`: test runner
- `pytest-mock`: mocking
- `pytest-cov`: coverage
- `factory_boy` or `pytest-factoryboy`: test data factories

## Enforcement
- QADeveloper monitors TDD adherence.
- CI pipeline fails if coverage drops below threshold.
- Orchestrator rejects tasks without adequate tests.