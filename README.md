# Telegram Bot Dashboard

A full-stack dashboard application for managing Telegram bot products with integration to an external phone registry API service (checkapi.org).

## Tech Stack

### Backend
- **Django 5.0.8** with Django REST Framework
- **PostgreSQL** database with optimized indexes
- **Redis** for caching external API responses
- **drf-spectacular** for API documentation (Swagger/OpenAPI)

### Frontend
- **React 18+** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **shadcn/ui** components
- **React Query** for data fetching
- **React Hook Form + Zod** for form validation

### External Integration
- **Phone Registry API** (checkapi.org) integration with:
  - Health check monitoring
  - Retry logic with exponential backoff
  - Request/response logging
  - Circuit breaker pattern
  - Redis caching

## Features

### 1. Products Management Dashboard
- **CRUD Operations**: Create, read, update, delete products
- **Statistics Cards**:
  - Total products count
  - Active products
  - Expired products
  - Products expiring in next 7 days
- **Advanced Filtering**: By status, search term, expiring soon
- **Bulk Actions**: Bulk renew, bulk delete
- **Export**: Export products to CSV
- **Pagination**: Server-side pagination

### 2. Phone Registry API Integration
- **Health Check**: Monitor external API status
- **Check Phone**: Verify if a phone number exists
- **Register Phone**: Register single phone number
- **Bulk Register**: Register up to 1000 phone numbers at once
- **Cleanup**: Delete records older than retention period
- **API Logs**: View and filter external API call logs

### 3. Health Monitoring
- Internal health endpoint (`/health/`)
- Database connection status
- External API connection status
- Comprehensive error handling

## Project Structure

```
dashboard/
├── backend/
│   ├── manage.py
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── products/
│   │   │   ├── models.py          # Product model
│   │   │   ├── serializers.py     # DRF serializers
│   │   │   ├── views.py           # ViewSets and endpoints
│   │   │   ├── urls.py
│   │   │   └── fixtures/          # Sample data
│   │   ├── phone_registry/
│   │   │   ├── models.py          # APICallLog model
│   │   │   ├── services.py        # External API integration
│   │   │   ├── views.py           # Proxy endpoints
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── utils.py           # Retry logic, validation
│   │   └── core/
│   │       ├── views.py           # Health check logic
│   │       └── urls.py
│   ├── requirements.txt
│   ├── .env.example
│   └── logs/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                # shadcn components
│   │   │   ├── dashboard/         # Dashboard components
│   │   │   ├── products/          # Product components
│   │   │   └── phone-registry/    # Phone registry components
│   │   ├── pages/
│   │   ├── services/
│   │   │   ├── api.ts             # Base API client
│   │   │   ├── products.ts        # Product API calls
│   │   │   └── phone-registry.ts  # Phone registry API calls
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── .env.example
├── dashboard.sh                    # Management script
└── README.md
```

## Installation & Setup

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL 14+**
- **Redis** (optional, for caching)

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd dashboard
```

2. **Run setup**
```bash
./dashboard.sh setup
```

This will:
- Create Python virtual environment
- Install backend dependencies
- Create PostgreSQL database
- Run migrations
- Load sample data
- Install frontend dependencies
- Copy environment files

3. **Configure environment variables**

Edit `backend/.env`:
```bash
# Database
DATABASE_URL=postgresql://dashboard_user:dashboard_password@localhost:5432/dashboard_db

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# External Phone Registry API
PHONE_REGISTRY_API_URL=http://checkapi.org
PHONE_REGISTRY_API_KEY=your-api-key-here
PHONE_REGISTRY_API_TIMEOUT=30

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
```

Edit `frontend/.env`:
```bash
VITE_API_BASE_URL=http://localhost:8000
```

4. **Start the application**
```bash
./dashboard.sh start
```

Access the application:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs/

## Management Commands

The `dashboard.sh` script provides comprehensive management commands:

```bash
./dashboard.sh setup          # Install dependencies and setup
./dashboard.sh start          # Start both servers
./dashboard.sh stop           # Stop all processes
./dashboard.sh restart        # Restart application
./dashboard.sh migrate        # Run database migrations
./dashboard.sh test           # Run tests
./dashboard.sh logs           # View application logs
./dashboard.sh backup         # Backup database
./dashboard.sh restore FILE   # Restore database from backup
./dashboard.sh check-health   # Check health status
./dashboard.sh autostart      # Setup systemd auto-start
```

## API Documentation

### Products API

#### List Products
```
GET /api/products/
Query Parameters:
  - status: Filter by status (active, expired, renewed)
  - search: Search in name, description, customer_link
  - expiring_soon: Filter expiring in next 7 days (true/false)
  - page: Page number
```

#### Get Product Statistics
```
GET /api/products/statistics/
Response: {
  total: number,
  active: number,
  expired: number,
  renewed: number,
  expiring_soon: number
}
```

#### Create Product
```
POST /api/products/
Body: {
  name: string,
  description: string,
  bot_username_or_link: string,
  contract_months: number (1-12),
  customer_link: string
}
```

#### Renew Product
```
POST /api/products/{id}/renew/
Body: { months?: number }
```

#### Bulk Actions
```
POST /api/products/bulk_action/
Body: {
  product_ids: number[],
  action: "renew" | "delete",
  months?: number
}
```

#### Export Products
```
GET /api/products/export/
Returns: CSV file
```

### Phone Registry API

#### Health Check
```
GET /api/phone/health/
Response: {
  external_api: {...},
  status: "healthy" | "unhealthy"
}
```

#### Check Phone Number
```
POST /api/phone/check/
Body: { phone_number: "+1234567890" }
Response: {
  exists: boolean,
  registered_at?: string
}
```

#### Register Phone Number
```
POST /api/phone/register/
Body: { phone_number: "+1234567890" }
Response: {
  success: boolean,
  message: string,
  registered_at: string
}
```

#### Bulk Register
```
POST /api/phone/bulk-register/
Body: { phone_numbers: ["+1234567890", ...] }
Response: {
  success: boolean,
  total_submitted: number,
  newly_registered: number,
  already_exists: number,
  failed: number,
  message: string
}
```

#### Cleanup Old Records
```
POST /api/phone/cleanup/
Body: { retention_days: number }
Response: {
  success: boolean,
  deleted_count: number,
  retention_days: number,
  cutoff_date: string,
  message: string
}
```

#### API Call Logs
```
GET /api/phone/logs/
Query Parameters:
  - endpoint: Filter by endpoint
  - success: Filter by success status (true/false)
  - page: Page number
```

### Health Check
```
GET /health/
Response: {
  status: "healthy" | "unhealthy" | "degraded",
  timestamp: string,
  database: "connected" | "disconnected",
  external_api: "connected" | "disconnected" | "unhealthy"
}
```

## External API Configuration

### Obtaining API Credentials

1. Visit http://checkapi.org (or your phone registry provider)
2. Sign up for an account
3. Generate an API key from your dashboard
4. Add the API key to `backend/.env`:
   ```
   PHONE_REGISTRY_API_KEY=your-api-key-here
   ```

### API Rate Limits

The external API may have rate limits. The application handles this by:
- Implementing retry logic with exponential backoff (3 retries)
- Caching health check results (5 minutes)
- Logging all API calls for monitoring
- Graceful degradation when API is unavailable

## Database Schema

### Product Model
```python
- id: AutoField (Primary Key)
- name: CharField(255)
- description: TextField
- bot_username_or_link: CharField(500)
- contract_months: IntegerField (1-12)
- status: CharField (active, expired, renewed)
- customer_link: CharField(255)
- created_at: DateTimeField (auto)
- expiry_date: DateTimeField
- last_renewed: DateTimeField (nullable)

Indexes:
- status
- expiry_date
- created_at
```

### APICallLog Model
```python
- id: AutoField (Primary Key)
- endpoint: CharField(255)
- method: CharField(10)
- request_data: JSONField
- response_data: JSONField
- status_code: IntegerField
- success: BooleanField
- error_message: TextField
- response_time_ms: IntegerField
- created_at: DateTimeField (auto)

Indexes:
- endpoint
- success
- created_at
```

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
source venv/bin/activate
python manage.py test

# Or use the script
./dashboard.sh test
```

### Creating Migrations

```bash
cd backend
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate

# Or use the script
./dashboard.sh migrate
```

## Production Deployment

### Security Considerations

1. **Change SECRET_KEY** in production
2. **Set DEBUG=False**
3. **Configure ALLOWED_HOSTS** properly
4. **Use HTTPS** (enable SSL settings in production.py)
5. **Secure database credentials**
6. **Keep API keys in environment variables**

### Deployment Steps

1. Update environment variables for production
2. Use production settings:
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings.production
   ```
3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
4. Use a production server (Gunicorn, uWSGI)
5. Setup reverse proxy (Nginx, Apache)
6. Enable autostart:
   ```bash
   sudo ./dashboard.sh autostart
   ```

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Create database manually
createdb dashboard_db
```

### External API Not Responding
- Check if PHONE_REGISTRY_API_URL is correct
- Verify API key is valid
- Check network connectivity
- Review logs: `./dashboard.sh logs`

### Frontend Build Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

## Monitoring

### Application Logs
```bash
./dashboard.sh logs
```

### Health Check
```bash
./dashboard.sh check-health
# Or visit: http://localhost:8000/health/
```

### External API Monitoring
- View API call logs in the dashboard
- Check `/api/phone/logs/` endpoint
- Monitor success rate and response times

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at http://localhost:8000/api/docs/
- Check application logs with `./dashboard.sh logs`

## Acknowledgments

- Django REST Framework
- React and TypeScript community
- shadcn/ui for the component library
- Phone Registry API (checkapi.org)
