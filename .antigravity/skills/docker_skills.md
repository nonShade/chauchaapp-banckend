# Docker & Docker Compose Skill

## Description
Enables agents to create, configure, and maintain Docker containers and Docker Compose setups for development, testing, and production environments.

## Capabilities

### 1. Dockerfile Creation
- Write efficient Dockerfiles for Python applications
- Implement multi-stage builds to minimize image size
- Set up proper layer caching for faster builds
- Configure non-root users for security
- Set environment variables, working directories, and entrypoints

### 2. Docker Compose Configuration
- Define multi-service applications (app, database, cache, etc.)
- Configure networks, volumes, and ports
- Set up environment variables and secrets
- Implement health checks and dependency ordering
- Configure development vs production profiles

### 3. Image Optimization
- Reduce image size through Alpine base images, layer minimization
- Security scanning with Trivy, Snyk
- Implement .dockerignore to exclude unnecessary files
- Use BuildKit features for advanced caching

### 4. Container Orchestration (Basic)
- Define service scaling, restart policies
- Configure logging and monitoring within containers
- Set resource limits (CPU, memory)

### 5. Development Workflow
- Enable hot-reload for development containers
- Bind-mount source code for real-time updates
- Set up debugging tools (debugpy, ptvsd)
- Configure development-specific environment variables

### 6. Production Deployment
- Create production-optimized Dockerfiles
- Implement secure secret management
- Configure logging aggregation
- Set up health checks and readiness probes

### 7. Testing with Containers
- Use testcontainers for integration testing
- Create isolated test environments with Docker Compose
- Run tests inside containers for consistency

## Input/Output

### Input
- Application requirements (dependencies, runtime, ports)
- Environment configuration (dev, test, prod)
- External service dependencies (database, cache, message queue)
- Security and compliance requirements

### Output
- Dockerfile(s)
- docker-compose.yml
- .dockerignore file
- Documentation for building and running containers
- CI/CD pipeline integration scripts

## Workflow Integration

### 1. Development Environment Setup
1. Analyze application dependencies and runtime requirements
2. Create Dockerfile for application image
3. Create docker-compose.yml with all required services
4. Configure development-specific features (hot-reload, debug)
5. Test locally with `docker-compose up`
6. Update README with usage instructions

### 2. CI/CD Pipeline Integration
1. Create build script that builds Docker image
2. Push image to container registry
3. Update deployment scripts to use new image
4. Implement rollback strategies

### 3. Production Configuration
1. Create production Dockerfile (separate from development)
2. Configure production environment variables and secrets
3. Set up logging and monitoring
4. Implement security best practices

## Example Usage

### Creating a Python Application Dockerfile
```dockerfile
# Development stage
FROM python:3.12-slim as dev
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install --system -r pyproject.toml
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM python:3.12-slim as prod
WORKDIR /app
RUN adduser --disabled-password --gecos "" appuser
COPY --from=dev /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dev /app .
USER appuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Creating docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      target: dev
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/appdb
      - DEBUG=true
    volumes:
      - .:/app
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: sync
          path: .
          target: /app
          ignore:
            - .git/
            - __pycache__/

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Best Practices

### 1. Security
- Use non-root users inside containers
- Regularly update base images for security patches
- Scan images for vulnerabilities
- Never embed secrets in Dockerfile or image layers

### 2. Performance
- Leverage layer caching by ordering commands properly
- Use multi-stage builds to reduce final image size
- Minimize the number of layers

### 3. Maintainability
- Use environment variables for configuration
- Document container usage and configuration options
- Keep Dockerfiles and compose files version-controlled

### 4. Reproducibility
- Pin base image tags (e.g., `python:3.12-slim`, not `python:slim`)
- Use specific version tags for service images
- Lock dependency versions in requirements files

## Tools
- **Docker**: Container runtime
- **Docker Compose**: Multi-container orchestration
- **BuildKit**: Advanced build features
- **Trivy/Snyk**: Security scanning
- **Docker Scout**: Image optimization
- **Testcontainers**: Testing with containers

## Dependencies
- DevOpsDeveloper agent primarily uses this skill
- PythonBackendDeveloper provides application requirements
- QADeveloper may use for test container configuration