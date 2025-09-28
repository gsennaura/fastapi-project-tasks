# FastAPI Project Tasks - Clean Architecture

A robust and scalable RESTful API for managing Projects and Tasks, built with FastAPI following Clean Architecture, Domain-Driven Design (DDD), and SOLID principles.

## Architecture Overview

This implementation follows **Clean Architecture** with 4 distinct layers, strictly respecting the **Dependency Rule** (dependencies flow inward only):

```
Domain ← Application ← Interfaces ← Infrastructure
  ↑         ↑            ↑            ↑
 Pure   Orchestration  Adaptation   Details
```

### Project Structure

```
fastapi-project-tasks/
├── app/
│   ├── domain/                    # Business rules and entities
│   │   ├── entities/             # Core business entities
│   │   │   ├── project.py        # Project entity with business rules
│   │   │   └── task.py           # Task entity with validations
│   │   ├── value_objects/        # Immutable value objects
│   │   │   ├── project_id.py     # Typed UUID for Project
│   │   │   ├── task_id.py        # Typed UUID for Task
│   │   │   └── priority.py       # Priority (1-10) with validation
│   │   ├── interfaces/           # Repository interfaces
│   │   │   ├── project_repository.py # Project repository interface
│   │   │   └── task_repository.py    # Task repository interface
│   │   └── exceptions/           # Domain-specific exceptions
│   │       ├── base.py           # Base domain exception
│   │       ├── project_exceptions.py # Project exceptions
│   │       └── task_exceptions.py    # Task exceptions
│   │
│   ├── application/              # Use cases and business logic
│   │   ├── use_cases/           # Application-specific business rules
│   │   │   ├── create_project.py # Create project use case
│   │   │   ├── get_project.py    # Get project use case
│   │   │   ├── update_project.py # Update project use case
│   │   │   ├── delete_project.py # Delete project use case
│   │   │   ├── list_projects.py  # List projects use case
│   │   │   └── create_task.py    # Create task use case
│   │   ├── dtos/                # Data transfer objects
│   │   │   ├── project_dtos.py   # Project DTOs
│   │   │   ├── task_dtos.py      # Task DTOs
│   │   │   └── pagination_dto.py # Pagination DTO
│   │
│   ├── interfaces/              # External interface adapters
│   │   └── api/                 # HTTP API layer
│   │       ├── controllers/     # HTTP request handlers
│   │       │   ├── project_controller.py # Project controller
│   │       │   └── task_controller.py    # Task controller
│   │       ├── schemas/         # Request/response schemas
│   │       │   ├── project_schemas.py # Project schemas
│   │       │   ├── task_schemas.py    # Task schemas
│   │       │   └── common_schemas.py  # Common schemas
│   │       ├── routers/         # FastAPI routers
│   │       │   ├── projects.py  # Project routes
│   │       │   └── tasks.py     # Task routes
│   │       └── middleware/      # HTTP middleware
│   │           └── __init__.py  # Authentication middleware
│   │
│   ├── infrastructure/          # External concerns
│   │   ├── database/           # Database configuration
│   │   │   ├── __init__.py     # AsyncSession setup
│   │   │   └── models.py       # SQLAlchemy models
│   │   ├── repositories/       # Repository implementations
│   │   │   ├── project_repository.py # Project repo implementation
│   │   │   └── task_repository.py    # Task repo implementation
│   │   └── config/             # Application settings
│   │       └── settings.py     # Settings with Pydantic
│   │
│   ├── main.py                 # Application entry point
│   ├── dependencies.py         # Dependency injection
│   └── exception_handlers.py   # Global exception handlers
│
├── migrations/                  # Database migrations
├── tests/                      # Test suite
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── docker-compose.yml         # Docker configuration
```

### Layer Responsibilities

#### 1. Domain Layer (Core Business Rules)
- **Entities**: Core business objects (Project, Task) with business rules and invariants
- **Value Objects**: Immutable objects with business meaning (Priority, IDs)
- **Interfaces**: Abstract repository contracts for dependency inversion
- **Exceptions**: Domain-specific error conditions

**Key Principles:**
- No dependencies on external frameworks
- Contains pure business logic
- Defines contracts for external dependencies

#### 2. Application Layer (Use Cases)
- **Use Cases**: Application-specific business rules and workflows
- **DTOs**: Data transfer objects for communication between layers
- Orchestrates domain entities without external dependencies

**Key Principles:**
- Depends only on Domain layer
- Implements business workflows
- Coordinates multiple domain entities

#### 3. Interfaces Layer (Adapters)
- **Controllers**: Convert HTTP requests to use case calls
- **Schemas**: Request/response validation with Pydantic
- **Routers**: FastAPI route definitions and HTTP concerns
- **Middleware**: Cross-cutting concerns (authentication, logging)

**Key Principles:**
- Adapts external protocols to internal use cases
- Handles HTTP-specific concerns
- Validates input/output data

#### 4. Infrastructure Layer (External Details)
- **Repositories**: Data persistence implementations
- **Database**: SQLAlchemy models and configuration
- **Config**: Application settings and environment variables

**Key Principles:**
- Implements interfaces defined in Domain layer
- Contains framework-specific code
- Handles external system integrations

## API Features

### Project Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/projects/` | Create new project | Yes |
| GET | `/projects/{project_id}` | Get project by ID | Yes |
| PUT | `/projects/{project_id}` | Update project | Yes |
| DELETE | `/projects/{project_id}` | Delete project | Yes |
| GET | `/projects/` | List projects (paginated) | Yes |

### Task Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/projects/{project_id}/tasks/` | Create task in project | Yes |
| GET | `/projects/{project_id}/tasks/` | List tasks (by priority) | Yes |
| GET | `/tasks/{task_id}` | Get task by ID | Yes |
| PUT | `/tasks/{task_id}` | Update task | Yes |
| DELETE | `/tasks/{task_id}` | Delete task | Yes |

### Core Features
- **Authentication**: API Key support (Bearer token or X-API-Key header)
- **Pagination**: Configurable page size with `?page=1&page_size=20`
- **Priority Ordering**: Tasks automatically sorted by priority (10→1)
- **Validation**: Comprehensive input validation with Pydantic
- **Error Handling**: Structured error responses (404, 400, 422, 500)
- **Documentation**: Auto-generated Swagger UI and ReDoc
- **Performance**: Optimized queries with async/await throughout
- **Type Safety**: Full type hints for better developer experience

## Technology Stack

### Core Framework
- **FastAPI**: Modern Python web framework with automatic OpenAPI documentation
- **Pydantic**: Data validation and settings management using Python type hints
- **SQLAlchemy 2.0**: Modern async ORM with declarative mapping
- **Alembic**: Database migration tool

### Database
- **PostgreSQL**: Robust relational database
- **AsyncPG**: High-performance async PostgreSQL driver

### Development & Testing
- **Pytest**: Testing framework with async support
- **Black**: Code formatting
- **Ruff**: Fast Python linter

## Architecture Benefits

### Clean Architecture Advantages
- **Testability**: Each layer can be tested in isolation
- **Maintainability**: Clear separation of concerns
- **Flexibility**: Easy to swap external dependencies
- **Independence**: Business logic is framework-agnostic

### Domain-Driven Design Benefits
- **Ubiquitous Language**: Code reflects business terminology
- **Business Focus**: Domain logic is clearly separated
- **Rich Domain Models**: Entities contain business behavior
- **Bounded Contexts**: Clear boundaries between different areas

### SOLID Principles Implementation
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Derived classes are substitutable for base classes
- **Interface Segregation**: Many client-specific interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

## Request/Response Flow

### Example: Creating a Project

```
1. HTTP Request (POST /projects/)
   ↓
2. FastAPI Router
   ↓
3. Project Controller
   ↓ (converts request to DTO)
4. Create Project Use Case
   ↓ (creates domain entity)
5. Project Entity (business validation)
   ↓ (persists via interface)
6. Project Repository Interface
   ↓ (concrete implementation)
7. PostgreSQL Project Repository
   ↓ (saves to database)
8. PostgreSQL Database
   ↓ (returns through layers)
9. HTTP Response (JSON)
```

### Dependency Injection Flow

```python
# Composition Root (dependencies.py)
def get_project_repository(db: AsyncSession = Depends(get_db)):
    return PostgreSQLProjectRepository(db)

def get_create_project_use_case(repo = Depends(get_project_repository)):
    return CreateProjectUseCase(repo)

def get_project_controller(use_case = Depends(get_create_project_use_case)):
    return ProjectController(use_case)
```

## Data Models

### Project Entity
```python
class Project:
    id: ProjectId
    name: str  # Required, max 255 chars
    description: Optional[str]
    created_at: datetime
    
    def validate_name(self, name: str) -> None:
        # Business validation logic
```

### Task Entity
```python
class Task:
    id: TaskId
    project_id: ProjectId
    title: str  # Required, max 255 chars
    priority: Priority  # 1-10, default 5
    completed: bool  # Default False
    due_date: Optional[date]
    created_at: datetime
    
    def mark_completed(self) -> None:
        # Business method
```

### Value Objects
```python
class Priority:
    def __init__(self, value: int):
        if not (1 <= value <= 10):
            raise ValueError("Priority must be between 1 and 10")
        self._value = value
```

## Testing Strategy

### Unit Tests
- Domain entities and value objects (no dependencies)
- Use cases with mocked repositories
- Controllers with mocked use cases

### Integration Tests
- Repository implementations with test database
- API endpoints with test client
- Database migrations

### Architecture Tests
- Dependency direction enforcement
- Layer isolation validation
- Interface compliance checks

## Development Principles

### Clean Code
- Meaningful names and clear intent
- Small functions with single responsibility
- Minimal comments (self-documenting code)
- Consistent formatting with Black

### Error Handling
- Domain exceptions for business rule violations
- HTTP exceptions for API-specific errors
- Structured error responses with clear messages
- Proper logging for debugging

### Performance
- Async/await throughout the application
- Database connection pooling
- Query optimization with proper indexes
- Pagination for large datasets

This architecture ensures maintainability, testability, and scalability while following industry best practices and clean code principles.
