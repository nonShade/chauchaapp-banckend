# Antigravity Configuration

This directory contains configuration for Antigravity agents, rules, skills, and workflows tailored to the chauchaapp-backend project.

## Structure

```
.antigravity/
├── agents/               # Agent definitions
│   ├── orchestrator.md
│   ├── python_backend_developer.md
│   ├── qa_developer.md
│   └── devops_developer.md
├── rules/                # Behavioral rules and constraints
│   ├── project_boundaries.md
│   ├── backend_development_rules.md
│   └── tdd_rules.md
├── skills/               # Capabilities agents can use
│   ├── python_backend_development.md
│   ├── unit_testing.md
│   ├── integration_testing.md
│   ├── docker_skills.md
│   └── specs_driven_development.md
├── workflows/            # Process definitions
│   ├── tdd_workflow.md
│   └── use_case_development_workflow.md
└── README.md             # This file
```

## Agents

### Orchestrator
Central coordinator that decomposes tasks, delegates to specialized agents, and ensures adherence to workflows.

### Python Backend Developer
Specialized in implementing backend Python code following layered architecture (controller-service-repository), DTOs, and REST API design.

### QA Developer
Specialized in testing: unit tests, integration tests, end-to-end tests, and quality assurance.

### DevOps Developer
Specialized in containerization (Docker), CI/CD pipelines, deployment, and infrastructure.

## Rules

### Project Boundaries
Ensures agents operate only within project scope with least privilege, no side effects, and security best practices.

### Backend Development Rules
Defines architectural patterns (layered architecture, DTOs, error handling) and code quality standards (PEP 8, type hints, testing).

### TDD Rules
Enforces Test-Driven Development cycle (Red-Green-Refactor) and testing best practices.

## Skills

### Python Backend Development
Capability to develop Python backend code following project architecture and conventions.

### Unit Testing
Capability to write comprehensive unit tests using pytest and mocking.

### Integration Testing
Capability to write integration tests for APIs, databases, and external services.

### Docker Skills
Capability to create and maintain Docker containers and Docker Compose configurations.

### Specs Driven Development
Capability to interpret natural language specifications and convert them into structured implementation plans.

## Workflows

### TDD Workflow
Standardized Test-Driven Development process with collaboration patterns between PythonBackendDeveloper and QADeveloper.

### Use Case Development Workflow
End-to-end process for developing a complete use case from specification to deployment, including all layers and test cases.

## Usage

1. **Orchestrator** reads a user requirement.
2. **Orchestrator** applies **Specs Driven Development** skill to create a plan.
3. **Orchestrator** delegates tasks to specialized agents according to **workflows**.
4. Agents follow **rules** while using their **skills** to complete tasks.
5. **Orchestrator** validates completion against acceptance criteria.

## Customization

- Edit agent definitions to adjust permissions or responsibilities.
- Add new rules to enforce additional constraints.
- Create new skills for specialized capabilities.
- Define new workflows for different development processes.

## Integration with Project

This configuration is tailored to the chauchaapp-backend project structure:

- Python 3.12+, Reflex framework
- Layered architecture (controller-service-repository)
- DTOs with Pydantic
- pytest for testing
- Docker for containerization
- Modular organization under `app/modules/`