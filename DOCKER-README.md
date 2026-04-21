# Docker Setup for chauchaapp-backend

This project includes Docker configuration for development, QA, and production environments using Docker Compose profiles.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Make sure you have a `.env` file with required environment variables (copy from `.env.example`)

## Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
# Edit .env with your actual values
```

## Available Profiles

### Development
- **Profile**: `development`
- **Database**: PostgreSQL with persistent volume
- **Features**: Hot reload, debug mode, source code mounted
- **Container names**: `chauchaapp-backend-dev`, `chauchaapp-postgres`

### QA (Quality Assurance)
- **Profile**: `qa`
- **Database**: Separate database (`chauchaapp_db_qa`)
- **Features**: Production-like settings, different port (8001)
- **Container names**: `chauchaapp-backend-qa`, `chauchaapp-postgres`

### Production
- **Profile**: `production`
- **Database**: Separate database (`chauchaapp_db_prod`)
- **Features**: Production optimizations, different port (8002)
- **Container names**: `chauchaapp-backend-prod`, `chauchaapp-postgres`

## Usage

### Start Development Environment
```bash
# Start all services (app, postgres) with development profile
docker-compose --profile development up

# Or build and start
docker-compose --profile development up --build

# Start in detached mode
docker-compose --profile development up -d
```

### Start QA Environment
```bash
docker-compose --profile qa up --build
```

### Start Production Environment
```bash
docker-compose --profile production up --build
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific profile
docker-compose --profile development down
```

### View Logs
```bash
# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs app  # development profile
docker-compose logs app-qa
docker-compose logs app-prod

# Follow logs
docker-compose logs -f
```

### Execute Commands in Container
```bash
# Run command in development container
docker-compose exec app bash

# Run tests in development container
docker-compose exec app pytest

# Access database
docker-compose exec postgres psql -U postgres -d chauchaapp_db
```

### Build Images
```bash
# Build all images
docker-compose build

# Build specific profile
docker-compose --profile development build
```

## Dockerfile Stages

The Dockerfile uses multi-stage builds:

1. **base**: Common dependencies and setup
2. **development**: Includes development dependencies and hot reload
3. **production**: Optimized for production with minimal layers

## Database Initialization

The PostgreSQL container automatically runs `scripts/init-db.sql` on first start. You can modify this file to add initial data or schema.

## Redis

Redis is included as an optional cache service. It's configured with persistence (append-only file).

## Network

All services are connected to a custom bridge network `chauchaapp-network`.

## Volumes

- `postgres-data`: PostgreSQL database files

## Health Checks

All services include health checks:
- PostgreSQL: Checks if database is ready
- Application: Implicit through dependency health

## Ports

- **Application Development**: `8000:8000`
- **Application QA**: `8001:8000`
- **Application Production**: `8002:8000`
- **PostgreSQL**: `5432:5432`

## Troubleshooting

### Permission Issues
If you encounter permission issues with volumes, ensure your user has appropriate Docker permissions.

### Build Cache
Clear Docker build cache if dependencies aren't updating:
```bash
docker-compose build --no-cache
```

### Environment Variables
Ensure `.env` file exists and has all required variables.

### Port Conflicts
If ports are already in use, modify the port mappings in `docker-compose.yml`.

### Database Connection
If the app can't connect to PostgreSQL, check if PostgreSQL container is healthy:
```bash
docker-compose logs postgres
```