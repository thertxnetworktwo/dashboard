#!/bin/bash

# Dashboard Management Script
# This script provides commands to manage the Telegram Bot Dashboard application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
BACKEND_DIR="backend"
FRONTEND_DIR="frontend"
DB_BACKUP_DIR="backups"

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Setup: Install dependencies and initialize
setup() {
    print_info "Setting up the application..."
    
    # Backend setup
    print_info "Installing backend dependencies..."
    cd $BACKEND_DIR
    pip3 install -r requirements.txt
    
    # Create database
    print_info "Running database migrations..."
    python3 manage.py migrate
    
    # Load sample data
    print_info "Loading sample data..."
    python3 manage.py populate_sample_data
    
    cd ..
    
    # Frontend setup
    print_info "Installing frontend dependencies..."
    cd $FRONTEND_DIR
    npm install
    cd ..
    
    # Create backup directory
    mkdir -p $DB_BACKUP_DIR
    
    print_success "Setup completed successfully!"
    print_info "Next steps:"
    print_info "  1. Copy backend/.env.example to backend/.env and configure"
    print_info "  2. Copy frontend/.env.example to frontend/.env and configure"
    print_info "  3. Run './dashboard.sh start' to start the application"
}

# Start: Start both backend and frontend servers
start() {
    print_info "Starting the application..."
    
    # Start backend
    print_info "Starting Django backend on port 8000..."
    cd $BACKEND_DIR
    python3 manage.py runserver 0.0.0.0:8000 &
    BACKEND_PID=$!
    echo $BACKEND_PID > /tmp/dashboard_backend.pid
    cd ..
    
    sleep 2
    
    # Start frontend
    print_info "Starting React frontend on port 5173..."
    cd $FRONTEND_DIR
    npm run dev -- --host &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > /tmp/dashboard_frontend.pid
    cd ..
    
    print_success "Application started successfully!"
    print_info "Backend running at: http://localhost:8000"
    print_info "Frontend running at: http://localhost:5173"
    print_info "API Docs running at: http://localhost:8000/api/docs/"
    print_info "Press Ctrl+C to stop or run './dashboard.sh stop'"
}

# Stop: Stop all running processes
stop() {
    print_info "Stopping the application..."
    
    if [ -f /tmp/dashboard_backend.pid ]; then
        BACKEND_PID=$(cat /tmp/dashboard_backend.pid)
        kill $BACKEND_PID 2>/dev/null || true
        rm /tmp/dashboard_backend.pid
        print_success "Backend stopped"
    fi
    
    if [ -f /tmp/dashboard_frontend.pid ]; then
        FRONTEND_PID=$(cat /tmp/dashboard_frontend.pid)
        kill $FRONTEND_PID 2>/dev/null || true
        rm /tmp/dashboard_frontend.pid
        print_success "Frontend stopped"
    fi
    
    # Kill any remaining processes
    pkill -f "manage.py runserver" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
    
    print_success "Application stopped"
}

# Restart: Stop and start
restart() {
    print_info "Restarting the application..."
    stop
    sleep 2
    start
}

# Autostart: Setup systemd service for auto-start on boot
autostart() {
    print_info "Setting up auto-start on boot..."
    
    # Create systemd service file
    SERVICE_FILE="/etc/systemd/system/dashboard.service"
    CURRENT_DIR=$(pwd)
    
    sudo cat > $SERVICE_FILE << EOF
[Unit]
Description=Telegram Bot Dashboard
After=network.target

[Service]
Type=forking
User=$USER
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/dashboard.sh start
ExecStop=$CURRENT_DIR/dashboard.sh stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable dashboard.service
    
    print_success "Auto-start configured successfully!"
    print_info "The application will start automatically on boot"
    print_info "Control with: sudo systemctl {start|stop|restart|status} dashboard"
}

# Migrate: Run database migrations
migrate() {
    print_info "Running database migrations..."
    cd $BACKEND_DIR
    python3 manage.py makemigrations
    python3 manage.py migrate
    cd ..
    print_success "Migrations completed"
}

# Test: Run tests
test() {
    print_info "Running tests..."
    
    # Backend tests
    print_info "Running backend tests..."
    cd $BACKEND_DIR
    python3 manage.py test
    cd ..
    
    # Frontend tests (if configured)
    # print_info "Running frontend tests..."
    # cd $FRONTEND_DIR
    # npm test
    # cd ..
    
    print_success "Tests completed"
}

# Logs: Show application logs
logs() {
    print_info "Showing application logs..."
    cd $BACKEND_DIR
    tail -f logs/app.log
}

# Backup: Backup database
backup() {
    print_info "Creating database backup..."
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$DB_BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3"
    
    cd $BACKEND_DIR
    cp db.sqlite3 ../$BACKUP_FILE
    cd ..
    
    print_success "Database backed up to: $BACKUP_FILE"
}

# Restore: Restore database from backup
restore() {
    if [ -z "$1" ]; then
        print_error "Usage: ./dashboard.sh restore <backup_file>"
        exit 1
    fi
    
    BACKUP_FILE=$1
    
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    
    print_info "Restoring database from: $BACKUP_FILE"
    
    # Stop application
    stop
    
    # Restore backup
    cp $BACKUP_FILE $BACKEND_DIR/db.sqlite3
    
    print_success "Database restored successfully"
    print_info "Run './dashboard.sh start' to start the application"
}

# Check health: Check health of app and external API
check_health() {
    print_info "Checking application health..."
    
    # Check backend health
    HEALTH_RESPONSE=$(curl -s http://localhost:8000/health/ || echo "failed")
    
    if [ "$HEALTH_RESPONSE" != "failed" ]; then
        print_success "Backend is healthy"
        echo "$HEALTH_RESPONSE" | python3 -m json.tool
    else
        print_error "Backend is not responding"
    fi
}

# Main command handler
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
    autostart)
        autostart
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
    *)
        echo "Usage: $0 {setup|start|stop|restart|autostart|migrate|test|logs|backup|restore|check-health}"
        echo ""
        echo "Commands:"
        echo "  setup         - Install dependencies, create DB, run migrations, setup frontend"
        echo "  start         - Start both frontend and backend servers"
        echo "  stop          - Stop all running processes"
        echo "  restart       - Stop and start"
        echo "  autostart     - Setup systemd service for auto-start on boot"
        echo "  migrate       - Run database migrations"
        echo "  test          - Run tests"
        echo "  logs          - Show application logs"
        echo "  backup        - Backup database"
        echo "  restore <file> - Restore database from backup"
        echo "  check-health  - Check health of app and external API"
        exit 1
        ;;
esac

exit 0
