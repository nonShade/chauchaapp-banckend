# Project Boundaries Rules

## Purpose
Ensure all agents operate strictly within the project scope and maintain security by following the principle of least privilege.

## Rules

### 1. Project Scope Limitation
- Agents must only read/write files within the project repository (`C:\Users\Ainsi\Desktop\proyectos\chauchaapp-backend` and subdirectories).
- No access to files outside the project directory unless explicitly authorized for specific tasks (e.g., reading global configuration files).
- All code modifications must be relevant to the project's goals.

### 2. Least Privilege
- Each agent has precisely defined permissions in its agent description.
- Agents must not request elevated permissions beyond their role.
- If an agent needs a capability outside its permissions, it must request delegation through the Orchestrator.
- No agent shall run arbitrary shell commands without explicit task justification.

### 3. No Side Effects
- Agents must not modify system configuration, install global packages, or alter environment variables outside the project.
- All dependencies must be declared in project configuration files (`pyproject.toml`, `requirements.txt`, `flake.nix`).
- Containerization must be used for external services (databases, caches) rather than installing them locally.

### 4. Security
- No hardcoded secrets in source code; use environment variables or secret management.
- Agents must not expose sensitive information in logs or outputs.
- All dependencies must be from trusted sources (PyPI, official Docker images).

### 5. Reproducibility
- All changes must be reproducible (e.g., via dependency lock files `uv.lock`, `flake.lock`).
- Docker images must be built from deterministic sources.

## Enforcement
- Orchestrator monitors agent activities for compliance.
- Violations result in task cancellation and notification to the user.
- Regular security audits by DevOpsDeveloper agent.