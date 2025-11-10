# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API uses AllowAny permissions for development. In production, you should implement proper authentication.

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

---

## Endpoints

### Health Check

#### GET /health/

Check the overall health of the application including database and external API connectivity.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "database": "connected",
  "external_api": "connected"
}
```

**Status Codes:**
- `200 OK` - System is healthy or degraded (external API down but app functional)
- `503 Service Unavailable` - Critical failure (database down)

---

## Products API

### List Products

#### GET /api/products/

Get a paginated list of products with optional filtering.

**Query Parameters:**
- `status` (string, optional): Filter by status (`active`, `expired`, `renewed`)
- `search` (string, optional): Search in name, description, and customer_link
- `expiring_soon` (boolean, optional): Filter products expiring in next 7 days
- `page` (integer, optional): Page number for pagination (default: 1)

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Customer Support Bot",
      "description": "AI-powered customer support bot",
      "bot_username_or_link": "@customer_support_bot",
      "contract_months": 6,
      "status": "active",
      "customer_link": "@acme_corp",
      "created_at": "2024-01-15T10:30:00Z",
      "expiry_date": "2024-07-15T10:30:00Z",
      "last_renewed": null,
      "is_expiring_soon": false,
      "days_until_expiry": 150
    }
  ]
}
```

### Get Product

#### GET /api/products/{id}/

Get details of a specific product.

**Response:**
```json
{
  "id": 1,
  "name": "Customer Support Bot",
  "description": "AI-powered customer support bot",
  "bot_username_or_link": "@customer_support_bot",
  "contract_months": 6,
  "status": "active",
  "customer_link": "@acme_corp",
  "created_at": "2024-01-15T10:30:00Z",
  "expiry_date": "2024-07-15T10:30:00Z",
  "last_renewed": null,
  "is_expiring_soon": false,
  "days_until_expiry": 150
}
```

### Create Product

#### POST /api/products/

Create a new product.

**Request Body:**
```json
{
  "name": "New Bot",
  "description": "Description of the bot",
  "bot_username_or_link": "@new_bot",
  "contract_months": 6,
  "customer_link": "@customer"
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "name": "New Bot",
  ...
}
```

**Validation Errors:** `400 Bad Request`
```json
{
  "bot_username_or_link": [
    "Must be a valid URL (http:// or https://) or Telegram username (starting with @)"
  ]
}
```

### Update Product

#### PUT /api/products/{id}/

Update an existing product.

**Request Body:** Same as Create Product

**Response:** `200 OK`

#### PATCH /api/products/{id}/

Partially update a product.

**Request Body:** Any subset of product fields

**Response:** `200 OK`

### Delete Product

#### DELETE /api/products/{id}/

Delete a product.

**Response:** `204 No Content`

### Get Statistics

#### GET /api/products/statistics/

Get dashboard statistics about products.

**Response:**
```json
{
  "total": 5,
  "active": 3,
  "expired": 1,
  "renewed": 1,
  "expiring_soon": 2
}
```

### Renew Product

#### POST /api/products/{id}/renew/

Renew a product's contract.

**Request Body:**
```json
{
  "months": 6
}
```
_Note: If `months` is not provided, the product's current `contract_months` value is used._

**Response:**
```json
{
  "message": "Product renewed for 6 months",
  "product": {
    "id": 1,
    "status": "renewed",
    "expiry_date": "2024-12-15T10:30:00Z",
    "last_renewed": "2024-06-15T10:30:00Z",
    ...
  }
}
```

### Bulk Action

#### POST /api/products/bulk_action/

Perform bulk actions on multiple products.

**Request Body:**
```json
{
  "product_ids": [1, 2, 3],
  "action": "renew",
  "months": 6
}
```

**Actions:**
- `renew` - Renew multiple products (requires `months` parameter)
- `delete` - Delete multiple products

**Response:**
```json
{
  "message": "3 products renewed successfully",
  "count": 3
}
```

### Export Products

#### GET /api/products/export/

Export products to CSV file.

**Response:** CSV file download
```csv
ID,Name,Description,Bot Username/Link,Contract Months,Status,Customer Link,Created At,Expiry Date,Last Renewed
1,Customer Support Bot,AI-powered...,@customer_support_bot,6,active,@acme_corp,2024-01-15...,2024-07-15...,
```

---

## Phone Registry API

### Health Check

#### GET /api/phone/health/

Check the health status of the external Phone Registry API.

**Response:**
```json
{
  "external_api": {
    "status": "healthy",
    "database": "connected",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK` - External API is healthy
- `503 Service Unavailable` - External API is unavailable

### Check Phone Number

#### POST /api/phone/check/

Check if a phone number exists in the registry.

**Request Body:**
```json
{
  "phone_number": "+1234567890"
}
```

**Response:**
```json
{
  "exists": true,
  "registered_at": "2024-01-15T10:30:00Z"
}
```

**Validation Errors:** `400 Bad Request`
```json
{
  "phone_number": [
    "Invalid phone number format. Must start with + and contain 10-15 digits."
  ]
}
```

**External API Error:** `503 Service Unavailable`
```json
{
  "error": "Failed to check phone number",
  "details": "Connection timeout"
}
```

### Register Phone Number

#### POST /api/phone/register/

Register a single phone number.

**Request Body:**
```json
{
  "phone_number": "+1234567890"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Phone number registered successfully",
  "registered_at": "2024-01-15T10:30:00Z"
}
```

### Bulk Register Phone Numbers

#### POST /api/phone/bulk-register/

Register multiple phone numbers (up to 1000).

**Request Body:**
```json
{
  "phone_numbers": [
    "+1234567890",
    "+9876543210",
    "+5555555555"
  ]
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "total_submitted": 3,
  "newly_registered": 2,
  "already_exists": 1,
  "failed": 0,
  "message": "Bulk registration completed"
}
```

**Validation Errors:** `400 Bad Request`
```json
{
  "phone_numbers": [
    "Invalid phone numbers found: 1234567890, +123"
  ]
}
```

### Cleanup Old Records

#### POST /api/phone/cleanup/

Delete phone number records older than the specified retention period.

**Request Body:**
```json
{
  "retention_days": 7
}
```

**Response:**
```json
{
  "success": true,
  "deleted_count": 1523,
  "retention_days": 7,
  "cutoff_date": "2024-01-08T10:30:00Z",
  "message": "Deleted 1523 records older than 7 days"
}
```

### API Call Logs

#### GET /api/phone/logs/

Get logs of external API calls for monitoring.

**Query Parameters:**
- `endpoint` (string, optional): Filter by endpoint
- `success` (boolean, optional): Filter by success status (`true`/`false`)
- `page` (integer, optional): Page number

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/phone/logs/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "endpoint": "/api/phone/check",
      "method": "POST",
      "request_data": {
        "phone_number": "+1234567890"
      },
      "response_data": {
        "exists": true,
        "registered_at": "2024-01-15T10:30:00Z"
      },
      "status_code": 200,
      "success": true,
      "error_message": null,
      "response_time_ms": 245,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": "Error message",
  "details": "Detailed error description"
}
```

### HTTP Status Codes

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `400 Bad Request` - Validation error or invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable (e.g., external API down)

### Common Errors

#### Validation Error (400)
```json
{
  "field_name": [
    "This field is required."
  ]
}
```

#### Not Found (404)
```json
{
  "detail": "Not found."
}
```

#### External API Error (503)
```json
{
  "error": "Failed to communicate with external API",
  "details": "Connection timeout after 30 seconds"
}
```

---

## Rate Limiting

Currently, there are no rate limits enforced by the application. However, the external Phone Registry API may have its own rate limits. The application handles rate limit errors gracefully with retry logic.

---

## Pagination

All list endpoints support pagination:

**Response Format:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

**Default Page Size:** 20 items per page

To request a specific page: `?page=2`

---

## Filtering and Searching

### Products Filtering

```
GET /api/products/?status=active
GET /api/products/?search=bot
GET /api/products/?expiring_soon=true
GET /api/products/?status=active&search=customer
```

### Combining Filters

Multiple filters can be combined:
```
GET /api/products/?status=active&expiring_soon=true&search=support
```

---

## Examples

### Complete Product Lifecycle

1. **Create a product:**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Bot",
    "description": "A helpful bot",
    "bot_username_or_link": "@my_bot",
    "contract_months": 12,
    "customer_link": "@customer"
  }'
```

2. **Get all products:**
```bash
curl http://localhost:8000/api/products/
```

3. **Renew the product:**
```bash
curl -X POST http://localhost:8000/api/products/1/renew/ \
  -H "Content-Type: application/json" \
  -d '{"months": 6}'
```

4. **Export products:**
```bash
curl http://localhost:8000/api/products/export/ -o products.csv
```

### Phone Registry Operations

1. **Check phone number:**
```bash
curl -X POST http://localhost:8000/api/phone/check/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890"}'
```

2. **Register phone number:**
```bash
curl -X POST http://localhost:8000/api/phone/register/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890"}'
```

3. **Bulk register:**
```bash
curl -X POST http://localhost:8000/api/phone/bulk-register/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_numbers": ["+1234567890", "+9876543210"]
  }'
```

---

## Webhooks (Future Feature)

Webhook support for product events is planned for future releases.

---

## Versioning

API Version: `v1`

Future versions will be accessible via `/api/v2/` endpoint prefix.

---

## Support

For API issues or questions:
- Check the Swagger documentation at `/api/docs/`
- Review the application logs with `./dashboard.sh logs`
- Check external API status with `GET /api/phone/health/`
