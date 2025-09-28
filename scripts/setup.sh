#!/bin/bash
# FastAPI Project Tasks - Setup Script

set -e

print_step() {
    echo "==> $1"
}

print_success() {
    echo "✓ $1"
}

print_warning() {
    echo "! $1"
}

print_error() {
    echo "✗ $1"
}

check_requirements() {
    print_step "Checking requirements"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    if ! command -v make &> /dev/null; then
        print_warning "Make is not installed. You can still use docker-compose commands directly"
    fi
    
    print_success "All requirements are met"
}

setup_environment() {
    print_step "Setting up environment"
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_success "Created .env file from .env.example"
    else
        print_warning ".env file already exists, skipping"
    fi
}

start_services() {
    print_step "Building and starting services"
    
    if command -v make &> /dev/null; then
        make setup
    else
        print_warning "Using docker-compose directly (make not available)"
        docker-compose build --no-cache
        docker-compose up -d
        sleep 10
        docker-compose exec fastapi-app alembic upgrade head
    fi
}

verify_setup() {
    print_step "Verifying setup"
    
    sleep 5
    
    if curl -s http://localhost:8000/health > /dev/null; then
        print_success "API is healthy"
    else
        print_error "API is not responding. Check logs with: make logs"
        exit 1
    fi
    
    if docker-compose exec -T fastapi-postgres pg_isready -U postgres > /dev/null; then
        print_success "Database is ready"
    else
        print_error "Database is not ready. Check logs with: make logs-db"
        exit 1
    fi
}

show_info() {
    echo
    echo "Setup completed successfully!"
    echo
    echo "Available Services:"
    echo "  API:           http://localhost:8000"
    echo "  Swagger Docs:  http://localhost:8000/docs"
    echo "  ReDoc:         http://localhost:8000/redoc"
    echo "  PostgreSQL:    localhost:5432"
    echo
    echo "Helpful Commands:"
    if command -v make &> /dev/null; then
        echo "  make dev       # Start with PgAdmin"
        echo "  make logs      # View application logs"
        echo "  make test      # Run tests"
        echo "  make help      # See all commands"
    else
        echo "  docker-compose logs fastapi-app        # View logs"
        echo "  docker-compose exec fastapi-app pytest # Run tests"
    fi
    echo
    echo "Tip: Install 'make' for easier development commands"
}

main() {
    echo
    echo "FastAPI Project Tasks - Setup"
    echo "============================="
    echo
    
    check_requirements
    setup_environment
    start_services
    verify_setup
    show_info
}

main "$@"
