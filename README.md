# Telegram Bot Dashboard

A full-stack dashboard application for managing Telegram bot products with integration to an external phone registry API service (checkapi.org).

## Features

### Product Management
- Full CRUD operations for Telegram bot products
- Dashboard with statistics cards (total, active, expired, expiring soon)
- Search, filter, and pagination
- Bulk operations (renew, delete)
- CSV export functionality
- Auto-status updates based on expiry dates

### Phone Registry API Integration
- Check phone number existence
- Register single phone numbers with full details
- Bulk register up to 1000 phone numbers
- List phones with pagination and filtering
- Analytics and statistics
- Cleanup old records
- Spam/account status analysis

### Health Monitoring
- Application health check endpoint
- External API connectivity monitoring
- Database connection status

## Tech Stack

### Backend
- **Django 5.0** - Web framework
- **Django REST Framework** - RESTful API
- **PostgreSQL/SQLite** - Database
- **drf-spectacular** - API documentation
- **django-cors-headers** - CORS support
- **requests** - HTTP client for external API

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Axios** - HTTP client
- **React Query** - Data fetching
- **React Router** - Routing
- **Lucide React** - Icons

## Project Structure

```
dashboard/
├── backend/
│   ├── apps/
│   │   ├── products/          # Product management app
│   │   ├── phone_registry/    # External API integration
│   │   └── core/              # Core functionality
│   ├── config/
│   │   ├── settings/          # Environment-based settings
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── logs/                  # Application logs
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── hooks/             # Custom hooks
│   │   ├── types/             # TypeScript types
│   │   ├── lib/               # Utilities
│   │   └── App.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.example
├── dashboard.sh               # Management script
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- npm 10+
- PostgreSQL (optional, SQLite works for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd dashboard
   ```

2. **Run setup**
   ```bash
   ./dashboard.sh setup
   ```

3. **Configure environment variables**
   
   Backend (`backend/.env`):
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your settings
   ```
   
   Frontend (`frontend/.env`):
   ```bash
   cp frontend/.env.example frontend/.env
   # Edit frontend/.env with your settings
   ```

4. **Start the application**
   ```bash
   ./dashboard.sh start
   ```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

## Management Commands

The `dashboard.sh` script provides the following commands:

```bash
./dashboard.sh setup          # Initial setup
./dashboard.sh start          # Start application
./dashboard.sh stop           # Stop application
./dashboard.sh restart        # Restart application
./dashboard.sh autostart      # Enable auto-start on boot
./dashboard.sh migrate        # Run database migrations
./dashboard.sh test           # Run tests
./dashboard.sh logs           # View application logs
./dashboard.sh backup         # Backup database
./dashboard.sh restore <file> # Restore database
./dashboard.sh check-health   # Check system health
```

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# External Phone Registry API
PHONE_REGISTRY_API_URL=http://checkapi.org
PHONE_REGISTRY_API_KEY=your-external-api-key
PHONE_REGISTRY_API_TIMEOUT=30

# Optional
REDIS_URL=redis://localhost:6379/0
```

### Frontend (.env)

```bash
VITE_API_BASE_URL=http://localhost:8000
```

## External API Integration

This application integrates with checkapi.org, an external phone registry API service.

### Obtaining API Credentials

1. Visit checkapi.org
2. Sign up for an account
3. Generate an API key from your dashboard
4. Add the API key to your backend `.env` file

### Supported Endpoints

- **Health Check**: `GET /health`
- **Check Phone**: `POST /api/phone/check`
- **Register Phone**: `POST /api/phone/register`
- **Bulk Register**: `POST /api/phone/bulk-register`
- **List Phones**: `GET /api/phone/list`
- **Analytics**: `GET /api/phone/analytics`
- **Cleanup**: `DELETE /api/phone/cleanup`
- **Spam Analysis**: `POST /api/analyze-spam`

See the [API documentation](http://localhost:8000/api/docs/) for detailed request/response formats.

## API Endpoints

### Products

- `GET /api/products/` - List products
- `POST /api/products/` - Create product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product
- `GET /api/products/stats/` - Get statistics
- `POST /api/products/{id}/renew/` - Renew product
- `POST /api/products/bulk_renew/` - Bulk renew
- `POST /api/products/bulk_delete/` - Bulk delete
- `GET /api/products/export_csv/` - Export to CSV

### Phone Registry

- `GET /api/phone-registry/health/` - Health check
- `POST /api/phone-registry/check/` - Check phone
- `POST /api/phone-registry/register/` - Register phone
- `POST /api/phone-registry/bulk-register/` - Bulk register
- `GET /api/phone-registry/list/` - List phones
- `GET /api/phone-registry/analytics/` - Get analytics
- `DELETE /api/phone-registry/cleanup/` - Cleanup records
- `POST /api/phone-registry/analyze-spam/` - Analyze spam

### System

- `GET /health/` - System health check

## Development

### Backend Development

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

# Run development server
python3 manage.py runserver
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Testing

### Backend Tests

```bash
cd backend
python3 manage.py test
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Production Deployment

1. **Set environment to production**
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings.production
   ```

2. **Configure PostgreSQL database**
   Update `DATABASE_URL` in backend/.env

3. **Collect static files**
   ```bash
   cd backend
   python3 manage.py collectstatic
   ```

4. **Build frontend**
   ```bash
   cd frontend
   npm run build
   ```

5. **Use production server (Gunicorn)**
   ```bash
   cd backend
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```

6. **Setup reverse proxy (Nginx/Apache)**

7. **Enable auto-start**
   ```bash
   ./dashboard.sh autostart
   ```

## Troubleshooting

### Backend Issues

**Database connection errors:**
- Check DATABASE_URL in backend/.env
- Ensure PostgreSQL is running
- Verify database credentials

**External API errors:**
- Check PHONE_REGISTRY_API_KEY is correct
- Verify API URL is accessible
- Check API rate limits

### Frontend Issues

**API connection errors:**
- Verify VITE_API_BASE_URL in frontend/.env
- Ensure backend is running
- Check CORS configuration

**Build errors:**
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear build cache: `rm -rf dist`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the [API documentation](http://localhost:8000/api/docs/)
- Review the external API documentation at checkapi.org

## Acknowledgments

- Django REST Framework for the robust API backend
- shadcn/ui for beautiful React components
- checkapi.org for the phone registry API service
