# Quick Start Guide

Get the Telegram Bot Dashboard up and running in 5 minutes!

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd dashboard
```

### 2. Run Setup

```bash
./dashboard.sh setup
```

This command will:
- ✅ Create Python virtual environment
- ✅ Install all backend dependencies
- ✅ Create PostgreSQL database
- ✅ Run database migrations
- ✅ Load sample data
- ✅ Install frontend dependencies
- ✅ Create environment files

### 3. Configure Environment

The setup creates `.env` files automatically. For basic usage, you can use the defaults.

**Optional:** Edit `backend/.env` to add your Phone Registry API key:
```bash
PHONE_REGISTRY_API_KEY=your-api-key-here
```

### 4. Start the Application

```bash
./dashboard.sh start
```

The application will start:
- 🌐 Frontend: http://localhost:5173
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/api/docs/

## First Steps

### 1. Explore the Dashboard

Visit http://localhost:5173 to see:
- Overview statistics
- System health status
- Quick actions

### 2. Manage Products

Click "Products" to:
- View all Telegram bot products
- Filter by status
- Search products
- Export to CSV

### 3. Test Phone Registry

Click "Phone Registry" to:
- Check if a phone number exists
- Register new phone numbers
- Bulk register multiple numbers
- Cleanup old records

## Sample Data

The setup automatically loads 5 sample products. You can:
- View them in the Products page
- Edit or delete them
- Create new ones

## API Exploration

Visit http://localhost:8000/api/docs/ to explore:
- All API endpoints
- Request/response formats
- Try API calls directly from the browser

## Common Commands

```bash
# Start the application
./dashboard.sh start

# Stop the application
./dashboard.sh stop

# View logs
./dashboard.sh logs

# Run migrations
./dashboard.sh migrate

# Run tests
./dashboard.sh test

# Check health
./dashboard.sh check-health

# Backup database
./dashboard.sh backup
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -ti:8000  # Backend
lsof -ti:5173  # Frontend

# Kill the process
kill -9 <PID>
```

### Database Connection Error

```bash
# Ensure PostgreSQL is running
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Frontend Not Loading

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [API.md](API.md) for API reference
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Review [TESTING.md](TESTING.md) for testing guide

## Getting Help

- Check application logs: `./dashboard.sh logs`
- Review health status: http://localhost:8000/health/
- Check API logs: http://localhost:8000/api/phone/logs/

## Tips

1. **Development Mode**: The application runs in development mode by default with hot-reload enabled
2. **Sample Data**: Use the provided fixtures to test features quickly
3. **API Testing**: Use the Swagger UI to test API endpoints interactively
4. **Dark Mode**: Toggle dark/light mode using the moon/sun icon in the navigation
5. **Mobile**: The interface is fully responsive - try it on your phone!

Enjoy using the Telegram Bot Dashboard! 🚀
