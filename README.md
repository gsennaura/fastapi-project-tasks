# FastAPI Project Tasks

![CI Pipeline](https://github.com/gsennaura/fastapi-project-tasks/workflows/CI%20Pipeline/badge.svg)
![Code Quality](https://github.com/gsennaura/fastapi-project-tasks/workflows/Code%20Quality/badge.svg)
![Security](https://github.com/gsennaura/fastapi-project-tasks/workflows/Security%20&%20Dependencies/badge.svg)

A RESTful API for managing Projects and Tasks built with FastAPI and Clean Architecture.

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Make (optional but recommended)

### Setup and Run

1. **Clone and enter the project**
```bash
git clone https://github.com/gsennaura/fastapi-project-tasks.git
cd fastapi-project-tasks
```

2. **One-command setup** ⚡
```bash
# This command does everything: copies .env, builds images, starts services, runs migrations
make first-run
```

🎉 **That's it!** Your API is now running at http://localhost:8000

3. **Daily development commands**
```bash
make up       # Start services
make down     # Stop services  
make logs     # View application logs
make test     # Run all tests (33 tests)
```

4. **Verify everything is working** ✅

Open these URLs in your browser:
- 🚀 **API Health**: http://localhost:8000/health
- 📚 **Swagger Documentation**: http://localhost:8000/docs  
- 📖 **ReDoc Documentation**: http://localhost:8000/redoc

**Quick Test:**
```bash
# Test the API
curl http://localhost:8000/health

# Run tests to make sure everything works
make test
```

## Available Services

| Service | URL | Description |
|---------|-----|-------------|
| **FastAPI** | http://localhost:8000 | Main API |
| **Swagger UI** | http://localhost:8000/docs | Interactive API documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative API documentation |
| **PostgreSQL** | localhost:5432 | Database |
| **PgAdmin** | http://localhost:5050 | Database management (dev mode only) |

## Development Commands

### Essential Commands
```bash
# First-time setup
make first-run     # Complete setup for new developers

# Daily operations  
make up           # Start all services
make down         # Stop all services
make restart      # Restart all services

# Development tools
make dev          # Start with PgAdmin and debugging tools
make logs         # Show application logs
make logs-all     # Show all container logs
```

### Database Operations
```bash
make migrate      # Run database migrations
make migration MESSAGE="description"  # Create new migration
make rollback     # Rollback last migration
```

### Code Quality
```bash
make test         # Run tests
make test-coverage # Run tests with coverage
make format       # Format code with Black
make lint         # Lint code with Ruff
make security     # Run security checks
```

### Utilities
```bash
make health       # Check API health
make status       # Show container status
make clean        # Clean containers and volumes
make help         # Show all available commands
```

## Manual Installation (Alternative)

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- pip or poetry

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database configuration

# Setup database
createdb projectsdb
alembic upgrade head

# Run application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Usage

### Authentication
All endpoints require API Key authentication. Include your API key in requests:

**Bearer Token:**
```bash
curl -H "Authorization: Bearer your-api-key" http://localhost:8000/projects/
```

**X-API-Key Header:**
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/projects/
```

**Default development API key:** `dev-secret-key`

### Quick Examples

**Using curl:**
```bash
# Create a project
curl -X POST http://localhost:8000/projects/ \
  -H "Authorization: Bearer dev-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "description": "A sample project"}'

# List all projects
curl -H "Authorization: Bearer dev-secret-key" \
  http://localhost:8000/projects/

# Create a task (replace {project_id} with actual ID)
curl -X POST http://localhost:8000/projects/{project_id}/tasks/ \
  -H "Authorization: Bearer dev-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"title": "Important Task", "description": "Task description", "priority": 8}'
```

**Using the interactive docs:**
1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Enter: `dev-secret-key`
4. Try any endpoint directly in the browser!

## API Endpoints

### Projects
- `POST /projects/` - Create new project
- `GET /projects/{project_id}` - Get project by ID
- `PUT /projects/{project_id}` - Update project
- `DELETE /projects/{project_id}` - Delete project
- `GET /projects/` - List projects (paginated)

### Tasks
- `POST /projects/{project_id}/tasks/` - Create task in project
- `GET /projects/{project_id}/tasks/` - List tasks (ordered by priority)
- `GET /tasks/{task_id}` - Get task by ID
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

## Features

- **Clean Architecture** with clear layer separation
- **API Key authentication** (Bearer token or X-API-Key header)
- **Automatic pagination** with configurable page size
- **Priority-based task ordering** (10→1)
- **Input validation** with Pydantic
- **Structured error responses** (404, 400, 422, 500)
- **Auto-generated documentation** (Swagger UI + ReDoc)
- **Async/await** throughout for performance
- **Type safety** with full type hints
- **Database migrations** with Alembic
- **Docker support** for easy deployment

## Environment Variables

Key environment variables (see `.env.example` for all options):

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/projectsdb

# Authentication
API_SECRET_KEY=dev-secret-key

# Application
DEBUG=true
LOG_LEVEL=info
```

## Testing

The project includes comprehensive unit and integration tests covering:
- **Domain entities** and value objects
- **Application use cases** with mocks
- **API endpoints** health checks
- **Database integrations**

```bash
# Run all tests (33 tests)
make test

# Run only unit tests
make test-unit

# Run only integration tests  
make test-integration

# Run with coverage report
make test-coverage

# Run specific test file
docker compose exec fastapi-app pytest tests/unit/domain/test_project_entity.py -v
```

**Test Structure:**
```
tests/
├── unit/                    # Fast, isolated tests
│   ├── domain/             # Entity and value object tests
│   └── application/        # Use case tests with mocks
├── integration/            # Database and API tests
├── test_simple.py          # Basic health checks
└── conftest.py            # Shared fixtures and config
```

## Troubleshooting

### Common Issues

**Database connection error:**
- Check if PostgreSQL is running: `docker-compose ps`
- Verify DATABASE_URL in `.env` file
- Run migrations: `make migrate`

**Port already in use:**
- Stop existing services: `make down`
- Check for other services on port 8000: `lsof -i :8000`

**Permission denied:**
- Make sure Docker is running and you have permissions
- Try with sudo if on Linux: `sudo make setup`

### Logs
```bash
# View application logs
make logs

# View database logs
make logs-db

# View all container logs
docker-compose logs -f
```

## Production Deployment

For production deployment, use the production Docker Compose configuration:

```bash
# Copy production environment file
cp .env.prod.example .env.prod

# Edit production settings
nano .env.prod

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## CI/CD Pipeline

The project includes comprehensive GitHub Actions workflows:

### 🔄 **Automated Workflows**

| **Workflow** | **Trigger** | **Purpose** |
|--------------|-------------|-------------|
| **CI Pipeline** | PR to `dev`/`main`, Push | Tests, linting, security, build |
| **Code Quality** | PR to `dev`/`main` | Coverage, complexity, metrics |
| **Security Scan** | Weekly, PR with deps | Vulnerability scanning |
| **Deploy** | Push to `main` | Production deployment |

### 📊 **Quality Gates**

**Pull Request Requirements:**
- ✅ All tests pass (33 tests)
- ✅ Code coverage > 80%
- ✅ Linting (Black, Ruff, MyPy)
- ✅ Security scan (Bandit, Safety)
- ✅ Docker build success

**Branch Protection:**
- `main`: Requires PR review + all checks ✅
- `dev`: Requires all CI checks ✅

### 🚀 **Development Workflow**

```bash
# 1. Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/your-feature

# 2. Develop with TDD
make test-unit  # Fast feedback loop
make test       # Full test suite

# 3. Quality checks (runs in CI)
make format     # Auto-format code
make lint       # Check code quality
make security   # Security analysis

# 4. Create PR to dev
# - GitHub Actions run automatically
# - Review required before merge

# 5. dev → main (release)
# - Full CI pipeline + deployment
```

## Contributing

1. Fork the repository
2. Create a feature branch from `dev` (`git checkout -b feature/amazing-feature`)
3. Follow TDD: write tests first, then implementation
4. Ensure all CI checks pass locally: `make test && make lint`
5. Commit with conventional commits (`feat:`, `fix:`, `docs:`, etc.)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request to `dev` branch

## Architecture

For detailed information about the project architecture, design patterns, and implementation details, see [ARCHITECTURE.md](ARCH.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
