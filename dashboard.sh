#!/bin/bash

# Telegram Bot Dashboard Management Script
# This script manages the Django-React dashboard application

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
VENV_DIR="$BACKEND_DIR/venv"
PYTHON="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"
MANAGE="$PYTHON $BACKEND_DIR/manage.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if PostgreSQL is installed
check_postgres() {
    if ! command -v psql &> /dev/null; then
        print_error "PostgreSQL is not installed. Please install PostgreSQL first."
        exit 1
    fi
}

# Check if Node.js is installed
check_node() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
}

# Setup function
setup() {
    print_info "Setting up Telegram Bot Dashboard..."
    
    # Check dependencies
    check_postgres
    check_node
    
    # Setup backend
    print_info "Setting up backend..."
    cd "$BACKEND_DIR"
    
    # Create virtual environment
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Install Python dependencies
    $PIP install --upgrade pip
    $PIP install -r requirements.txt
    print_success "Python dependencies installed"
    
    # Copy environment file if not exists
    if [ ! -f "$BACKEND_DIR/.env" ]; then
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        print_info "Created .env file. Please update it with your credentials."
    fi
    
    # Create database if not exists
    print_info "Creating database..."
    createdb dashboard_db 2>/dev/null || print_info "Database already exists"
    
    # Run migrations
    $MANAGE migrate
    print_success "Database migrations completed"
    
    # Create logs directory
    mkdir -p "$BACKEND_DIR/logs"
    
    # Load sample data
    print_info "Loading sample data..."
    $MANAGE loaddata apps/products/fixtures/sample_products.json || true
    print_success "Sample data loaded"
    
    # Setup frontend
    print_info "Setting up frontend..."
    cd "$FRONTEND_DIR"
    
    # Copy environment file if not exists
    if [ ! -f "$FRONTEND_DIR/.env" ]; then
        cp "$FRONTEND_DIR/.env.example" "$FRONTEND_DIR/.env"
    fi
    
    # Install Node dependencies
    npm install
    print_success "Node dependencies installed"
    
    print_success "Setup completed successfully!"
    print_info "Run './dashboard.sh start' to start the application"
}

# Start function
start() {
    print_info "Starting Telegram Bot Dashboard..."
    
    # Check if setup was run
    if [ ! -d "$VENV_DIR" ] || [ ! -d "$FRONTEND_DIR/node_modules" ]; then
        print_error "Please run './dashboard.sh setup' first"
        exit 1
    fi
    
    # Create log directory
    mkdir -p "$PROJECT_ROOT/logs"
    
    # Start backend
    print_info "Starting Django backend..."
    cd "$BACKEND_DIR"
    $MANAGE runserver 0.0.0.0:8000 > "$PROJECT_ROOT/logs/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$PROJECT_ROOT/.backend.pid"
    print_success "Backend started (PID: $BACKEND_PID)"
    
    # Wait a moment for backend to start
    sleep 2
    
    # Start frontend
    print_info "Starting React frontend..."
    cd "$FRONTEND_DIR"
    npm run dev > "$PROJECT_ROOT/logs/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$PROJECT_ROOT/.frontend.pid"
    print_success "Frontend started (PID: $FRONTEND_PID)"
    
    print_success "Dashboard is running!"
    print_info "Backend: http://localhost:8000"
    print_info "Frontend: http://localhost:5173"
    print_info "API Docs: http://localhost:8000/api/docs/"
}

# Stop function
stop() {
    print_info "Stopping Telegram Bot Dashboard..."
    
    # Stop backend
    if [ -f "$PROJECT_ROOT/.backend.pid" ]; then
        BACKEND_PID=$(cat "$PROJECT_ROOT/.backend.pid")
        kill $BACKEND_PID 2>/dev/null || true
        rm "$PROJECT_ROOT/.backend.pid"
        print_success "Backend stopped"
    fi
    
    # Stop frontend
    if [ -f "$PROJECT_ROOT/.frontend.pid" ]; then
        FRONTEND_PID=$(cat "$PROJECT_ROOT/.frontend.pid")
        kill $FRONTEND_PID 2>/dev/null || true
        rm "$PROJECT_ROOT/.frontend.pid"
        print_success "Frontend stopped"
    fi
    
    # Kill any remaining processes
    pkill -f "manage.py runserver" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
    
    print_success "Dashboard stopped"
}

# Restart function
restart() {
    stop
    sleep 2
    start
}

# Migrate function
migrate() {
    print_info "Running database migrations..."
    cd "$BACKEND_DIR"
    $MANAGE makemigrations
    $MANAGE migrate
    print_success "Migrations completed"
}

# Test function
test() {
    print_info "Running tests..."
    cd "$BACKEND_DIR"
    $MANAGE test
    print_success "Tests completed"
}

# Logs function
logs() {
    if [ -f "$PROJECT_ROOT/logs/backend.log" ] || [ -f "$PROJECT_ROOT/logs/frontend.log" ]; then
        echo "=== Backend Logs ==="
        tail -n 50 "$PROJECT_ROOT/logs/backend.log" 2>/dev/null || echo "No backend logs"
        echo ""
        echo "=== Frontend Logs ==="
        tail -n 50 "$PROJECT_ROOT/logs/frontend.log" 2>/dev/null || echo "No frontend logs"
    else
        print_info "No logs available. Start the application first."
    fi
}

# Backup function
backup() {
    BACKUP_DIR="$PROJECT_ROOT/backups"
    mkdir -p "$BACKUP_DIR"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/dashboard_backup_$TIMESTAMP.sql"
    
    print_info "Creating database backup..."
    pg_dump dashboard_db > "$BACKUP_FILE"
    print_success "Backup created: $BACKUP_FILE"
}

# Restore function
restore() {
    if [ -z "$1" ]; then
        print_error "Usage: ./dashboard.sh restore <backup_file>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "Backup file not found: $1"
        exit 1
    fi
    
    print_info "Restoring database from $1..."
    psql dashboard_db < "$1"
    print_success "Database restored"
}

# Check health function
check_health() {
    print_info "Checking application health..."
    
    # Check backend
    if curl -s http://localhost:8000/health/ > /dev/null; then
        print_success "Backend is healthy"
        curl -s http://localhost:8000/health/ | python3 -m json.tool
    else
        print_error "Backend is not responding"
    fi
    
    # Check frontend
    if curl -s http://localhost:5173 > /dev/null; then
        print_success "Frontend is accessible"
    else
        print_error "Frontend is not responding"
    fi
}

# Autostart function
autostart() {
    print_info "Setting up autostart with systemd..."
    
    SERVICE_FILE="/etc/systemd/system/dashboard.service"
    
    if [ ! -w "/etc/systemd/system/" ]; then
        print_error "Permission denied. Please run with sudo:"
        print_info "sudo ./dashboard.sh autostart"
        exit 1
    fi
    
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Telegram Bot Dashboard
After=network.target postgresql.service

[Service]
Type=forking
User=$USER
WorkingDirectory=$PROJECT_ROOT
ExecStart=$PROJECT_ROOT/dashboard.sh start
ExecStop=$PROJECT_ROOT/dashboard.sh stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable dashboard.service
    
    print_success "Autostart configured"
    print_info "Use 'sudo systemctl start dashboard' to start the service"
}

# Main script logic
case "$1" in
    setup)
        setup
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    migrate)
        migrate
        ;;
    test)
        test
        ;;
    logs)
        logs
        ;;
    backup)
        backup
        ;;
    restore)
        restore "$2"
        ;;
    check-health)
        check_health
        ;;
    autostart)
        autostart
        ;;
    *)
        echo "Telegram Bot Dashboard Management Script"
        echo ""
        echo "Usage: $0 {setup|start|stop|restart|migrate|test|logs|backup|restore|check-health|autostart}"
        echo ""
        echo "Commands:"
        echo "  setup         - Install dependencies and setup the application"
        echo "  start         - Start both frontend and backend servers"
        echo "  stop          - Stop all running processes"
        echo "  restart       - Stop and start the application"
        echo "  migrate       - Run database migrations"
        echo "  test          - Run tests"
        echo "  logs          - Show application logs"
        echo "  backup        - Backup database"
        echo "  restore FILE  - Restore database from backup"
        echo "  check-health  - Check health of app and external API"
        echo "  autostart     - Setup systemd service for auto-start on boot"
        exit 1
        ;;
esac

exit 0
