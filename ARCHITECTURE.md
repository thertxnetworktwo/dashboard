# Architecture Documentation

## Overview

The Telegram Bot Dashboard is a full-stack web application built with Django (backend) and React (frontend), designed to manage Telegram bot products and integrate with an external Phone Registry API.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │  Browser   │  │    Mobile    │  │  API Clients     │    │
│  └────────────┘  └──────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  React Frontend (TypeScript + Vite)                   │  │
│  │  - Dashboard Page                                      │  │
│  │  - Products Management                                 │  │
│  │  - Phone Registry Interface                           │  │
│  │  - shadcn/ui Components + Tailwind CSS                │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Django REST Framework                                 │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  │  │
│  │  │  Products   │  │Phone Registry│  │    Core     │  │  │
│  │  │   ViewSet   │  │   Views      │  │  Health     │  │  │
│  │  └─────────────┘  └──────────────┘  └─────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Business Layer                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Services & Business Logic                            │  │
│  │  ┌─────────────────┐  ┌───────────────────────────┐  │  │
│  │  │ Product Service │  │ Phone Registry API Service│  │  │
│  │  │  - Renewal      │  │  - Check Phone            │  │  │
│  │  │  - Statistics   │  │  - Register Phone         │  │  │
│  │  │  - Bulk Actions │  │  - Bulk Register          │  │  │
│  │  └─────────────────┘  │  - Cleanup                │  │  │
│  │                       │  - Retry Logic            │  │  │
│  │                       │  - Circuit Breaker        │  │  │
│  │                       └───────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
┌─────────────────────────┐  ┌─────────────────────────────┐
│    Data Layer           │  │  External Services          │
│  ┌───────────────────┐  │  │  ┌───────────────────────┐ │
│  │   PostgreSQL      │  │  │  │ Phone Registry API    │ │
│  │   - Products      │  │  │  │ (checkapi.org)        │ │
│  │   - APICallLog    │  │  │  │ - Health Check        │ │
│  └───────────────────┘  │  │  │ - Phone Operations    │ │
│  ┌───────────────────┐  │  │  └───────────────────────┘ │
│  │   Redis Cache     │  │  └─────────────────────────────┘
│  │   - Health Status │  │
│  │   - API Responses │  │
│  └───────────────────┘  │
└─────────────────────────┘
```

## Component Breakdown

### Frontend Architecture

#### Technology Stack
- **React 18+**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS
- **shadcn/ui**: Component library
- **React Query**: Data fetching and caching
- **React Router**: Client-side routing
- **Axios**: HTTP client

#### Component Structure

```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   └── ...
│   ├── dashboard/       # Dashboard-specific components
│   ├── products/        # Product management components
│   └── phone-registry/  # Phone registry components
├── pages/               # Page-level components
│   ├── DashboardPage.tsx
│   ├── ProductsPage.tsx
│   └── PhoneRegistryPage.tsx
├── services/            # API client services
│   ├── api.ts          # Base Axios configuration
│   ├── products.ts     # Product API calls
│   └── phone-registry.ts
├── hooks/               # Custom React hooks
├── utils/               # Utility functions
├── types/               # TypeScript type definitions
└── App.tsx             # Main application component
```

#### State Management
- **React Query**: Server state (API data)
- **React Hooks**: Local component state
- **Context API**: Global UI state (theme, auth)

#### Data Flow
```
User Action → Component Event Handler → API Service → 
Backend API → Response → React Query Cache → Component Update
```

### Backend Architecture

#### Technology Stack
- **Django 5.0.8**: Web framework
- **Django REST Framework**: API framework
- **PostgreSQL**: Primary database
- **Redis**: Caching layer
- **Gunicorn**: WSGI server (production)
- **Requests**: HTTP library for external API

#### Application Structure

```
backend/
├── config/
│   ├── settings/
│   │   ├── base.py       # Common settings
│   │   ├── development.py # Dev-specific
│   │   └── production.py  # Prod-specific
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI application
├── apps/
│   ├── products/
│   │   ├── models.py     # Product model
│   │   ├── serializers.py # DRF serializers
│   │   ├── views.py      # ViewSets
│   │   ├── urls.py       # URL patterns
│   │   └── admin.py      # Django admin
│   ├── phone_registry/
│   │   ├── models.py     # APICallLog model
│   │   ├── services.py   # External API service
│   │   ├── views.py      # API endpoints
│   │   └── utils.py      # Helper functions
│   └── core/
│       └── views.py      # Health check
└── manage.py
```

#### Request Flow

```
HTTP Request → Django Middleware → URL Router → 
View/ViewSet → Serializer (validation) → Business Logic → 
Database/External API → Serializer (formatting) → Response
```

### Database Schema

#### Product Model
```sql
CREATE TABLE products_product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    bot_username_or_link VARCHAR(500),
    contract_months INTEGER,
    status VARCHAR(20),
    customer_link VARCHAR(255),
    created_at TIMESTAMP,
    expiry_date TIMESTAMP,
    last_renewed TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_expiry_date (expiry_date),
    INDEX idx_created_at (created_at)
);
```

#### APICallLog Model
```sql
CREATE TABLE phone_registry_apicalllog (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255),
    method VARCHAR(10),
    request_data JSONB,
    response_data JSONB,
    status_code INTEGER,
    success BOOLEAN,
    error_message TEXT,
    response_time_ms INTEGER,
    created_at TIMESTAMP,
    INDEX idx_endpoint (endpoint),
    INDEX idx_success (success),
    INDEX idx_created_at (created_at)
);
```

### External API Integration

#### Phone Registry Service Architecture

```
┌─────────────────────────────────────────────────────┐
│          Phone Registry API Service                  │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  Retry Mechanism (Exponential Backoff)     │    │
│  │  - Max 3 retries                           │    │
│  │  - Backoff factor: 2.0 (1s, 2s, 4s)       │    │
│  └────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────┐    │
│  │  Circuit Breaker                           │    │
│  │  - Fail fast after repeated failures       │    │
│  └────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────┐    │
│  │  Response Caching (Redis)                  │    │
│  │  - Health check: 5 minutes                 │    │
│  └────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────┐    │
│  │  Request/Response Logging                  │    │
│  │  - All calls logged to database            │    │
│  └────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────┐    │
│  │  Timeout Handling                          │    │
│  │  - 30 second timeout                       │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
                       │
                       ▼
              External Phone Registry API
              (http://checkapi.org)
```

#### Error Handling Strategy

1. **Network Errors**: Retry with exponential backoff
2. **Timeout**: Log and return error to client
3. **4xx Errors**: Return to client (validation error)
4. **5xx Errors**: Retry, then fail gracefully
5. **Circuit Open**: Return cached data or degraded service

### Caching Strategy

#### Redis Cache Structure

```
Key Pattern                    | TTL     | Purpose
-------------------------------|---------|------------------------
phone_registry_health          | 5 min   | API health status
product_statistics             | 1 min   | Dashboard statistics
api_response:{endpoint}:{hash} | 5 min   | API call responses
```

### Security Architecture

#### Authentication & Authorization
- Currently: AllowAny (development)
- Future: JWT tokens or Django sessions
- CORS: Configured for specific origins

#### Security Headers (Production)
```
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'
```

#### Data Protection
- Secrets in environment variables
- PostgreSQL password authentication
- HTTPS in production
- CSRF protection enabled

### Deployment Architecture (Production)

```
                     Internet
                        │
                        ▼
                   Load Balancer
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
      Nginx (Server 1)            Nginx (Server 2)
      │                           │
      ├─ Static Files            ├─ Static Files
      └─ Reverse Proxy           └─ Reverse Proxy
          │                           │
          ▼                           ▼
      Gunicorn                    Gunicorn
      │                           │
      ├─ Worker 1                ├─ Worker 1
      ├─ Worker 2                ├─ Worker 2
      └─ Worker 3                └─ Worker 3
          │                           │
          └────────────┬──────────────┘
                       ▼
              Django Application
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     PostgreSQL     Redis      External API
    (Primary)       Cache      (checkapi.org)
          │
          ▼
     PostgreSQL
    (Replica - Read)
```

### Performance Optimizations

1. **Database**
   - Indexes on frequently queried fields
   - Query optimization with `select_related`
   - Connection pooling

2. **Caching**
   - Redis for frequently accessed data
   - Browser caching for static assets
   - CDN for global distribution

3. **Frontend**
   - Code splitting
   - Lazy loading
   - Asset optimization
   - Gzip compression

4. **API**
   - Pagination for large datasets
   - Response compression
   - Rate limiting (planned)

### Monitoring & Observability

#### Health Checks
- `/health/`: Overall system health
- `/api/phone/health/`: External API status
- Database connectivity check

#### Logging
- Application logs: Django logging framework
- Access logs: Nginx
- Error tracking: Console/file logs
- API call logs: Database (APICallLog model)

#### Metrics (Planned)
- Request/response times
- Error rates
- External API success rate
- Database query performance

### Scalability Considerations

#### Horizontal Scaling
- Stateless application servers
- Load balancer for distribution
- Shared Redis cache
- Database replication

#### Vertical Scaling
- Increase Gunicorn workers
- Database optimization
- Larger server instances

### Technology Decisions

#### Why Django?
- Robust ORM
- Admin interface
- Excellent ecosystem
- Security features
- RESTful API support

#### Why React?
- Component reusability
- Virtual DOM performance
- Large ecosystem
- TypeScript support
- Developer experience

#### Why PostgreSQL?
- ACID compliance
- Advanced features (JSONB)
- Scalability
- Reliability

#### Why Redis?
- Fast in-memory caching
- Simple key-value store
- Excellent Python support

## Future Architecture Enhancements

1. **Microservices**: Split into separate services
2. **GraphQL**: Alternative to REST API
3. **WebSockets**: Real-time updates
4. **Message Queue**: Async task processing
5. **Container Orchestration**: Kubernetes deployment
6. **Service Mesh**: Advanced networking

## Development Workflow

```
Developer → Git Push → CI/CD Pipeline → Tests → 
Build → Deploy to Staging → Manual QA → Deploy to Production
```

## Conclusion

This architecture provides:
- ✅ Scalability
- ✅ Maintainability
- ✅ Security
- ✅ Performance
- ✅ Reliability
- ✅ Developer experience

For questions or suggestions, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) guide.
