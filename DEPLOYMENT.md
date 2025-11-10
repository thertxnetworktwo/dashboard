# Deployment Guide

## Overview

This guide covers deploying the Telegram Bot Dashboard to a production environment.

## Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.10+
- PostgreSQL 14+
- Node.js 18+
- Nginx (recommended)
- Redis (optional, for caching)
- SSL certificate (Let's Encrypt recommended)

## Production Setup

### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib \
  nginx redis-server nodejs npm git

# Install PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Database Setup

```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE dashboard_prod;
CREATE USER dashboard_user WITH PASSWORD 'secure_password_here';
ALTER ROLE dashboard_user SET client_encoding TO 'utf8';
ALTER ROLE dashboard_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE dashboard_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE dashboard_prod TO dashboard_user;
\q
EOF
```

### 3. Application Deployment

```bash
# Create application directory
sudo mkdir -p /var/www/dashboard
sudo chown $USER:$USER /var/www/dashboard
cd /var/www/dashboard

# Clone repository
git clone <your-repo-url> .

# Run setup
./dashboard.sh setup
```

### 4. Environment Configuration

Edit `backend/.env` for production:

```bash
# Database
DATABASE_URL=postgresql://dashboard_user:secure_password_here@localhost:5432/dashboard_prod

# Django
SECRET_KEY=<generate-a-secure-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# External Phone Registry API
PHONE_REGISTRY_API_URL=http://checkapi.org
PHONE_REGISTRY_API_KEY=<your-production-api-key>
PHONE_REGISTRY_API_TIMEOUT=30

# Redis
REDIS_URL=redis://localhost:6379/0
```

Generate a secure SECRET_KEY:
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Static Files

```bash
cd backend
source venv/bin/activate
python manage.py collectstatic --noinput
```

### 6. Gunicorn Setup

Install Gunicorn:
```bash
cd backend
source venv/bin/activate
pip install gunicorn
```

Create Gunicorn service file:
```bash
sudo nano /etc/systemd/system/dashboard-gunicorn.service
```

Add:
```ini
[Unit]
Description=Dashboard Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/dashboard/backend
Environment="PATH=/var/www/dashboard/backend/venv/bin"
ExecStart=/var/www/dashboard/backend/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/dashboard/backend/gunicorn.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start Gunicorn:
```bash
sudo systemctl start dashboard-gunicorn
sudo systemctl enable dashboard-gunicorn
```

### 7. Frontend Build

```bash
cd /var/www/dashboard/frontend

# Update environment
echo "VITE_API_BASE_URL=https://yourdomain.com" > .env

# Build
npm run build
```

### 8. Nginx Configuration

Create Nginx config:
```bash
sudo nano /etc/nginx/sites-available/dashboard
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

    # Frontend
    location / {
        root /var/www/dashboard/frontend/dist;
        try_files $uri $uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api {
        include proxy_params;
        proxy_pass http://unix:/var/www/dashboard/backend/gunicorn.sock;
    }

    location /health {
        include proxy_params;
        proxy_pass http://unix:/var/www/dashboard/backend/gunicorn.sock;
    }

    # Django static files
    location /static {
        alias /var/www/dashboard/backend/staticfiles;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Max upload size
    client_max_body_size 10M;
}
```

Enable site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### 10. Firewall Configuration

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## Monitoring and Logging

### Application Logs

```bash
# View application logs
sudo journalctl -u dashboard-gunicorn -f

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Health Monitoring

Set up a cron job to check health:
```bash
crontab -e
```

Add:
```
*/5 * * * * curl -f https://yourdomain.com/health/ || echo "Health check failed" | mail -s "Dashboard Health Alert" admin@yourdomain.com
```

## Backup Strategy

### Automated Database Backups

```bash
# Create backup script
sudo nano /usr/local/bin/dashboard-backup.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/dashboard"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
pg_dump dashboard_prod > $BACKUP_DIR/dashboard_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "dashboard_*.sql" -mtime +7 -delete
```

Make executable and schedule:
```bash
sudo chmod +x /usr/local/bin/dashboard-backup.sh
sudo crontab -e
```

Add:
```
0 2 * * * /usr/local/bin/dashboard-backup.sh
```

## Performance Optimization

### 1. Database Optimization

```sql
-- Create indexes (already in migrations)
-- Analyze tables regularly
ANALYZE products_product;
ANALYZE phone_registry_apicalllog;
```

### 2. Redis Caching

Ensure Redis is running and configured in settings:
```bash
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 3. Nginx Caching

Add to Nginx config:
```nginx
# Cache zone
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m;

# In location /api
proxy_cache api_cache;
proxy_cache_valid 200 5m;
proxy_cache_bypass $http_cache_control;
```

## Scaling

### Horizontal Scaling

For high traffic, consider:

1. **Load Balancer**: Use multiple application servers behind a load balancer
2. **Database Replication**: Set up PostgreSQL replication
3. **CDN**: Use CloudFlare or similar for static assets
4. **Separate Services**: Run frontend and backend on different servers

### Vertical Scaling

Increase Gunicorn workers:
```bash
# In gunicorn.service
--workers 5  # Increase based on CPU cores
```

## Security Checklist

- [ ] Change SECRET_KEY to a secure random value
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set up firewall (ufw)
- [ ] Configure secure headers in Nginx
- [ ] Keep dependencies updated
- [ ] Regular security audits
- [ ] Monitor logs for suspicious activity
- [ ] Secure API keys in environment variables
- [ ] Set up rate limiting (optional)

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check Gunicorn is running: `sudo systemctl status dashboard-gunicorn`
   - Check socket file exists: `ls -l /var/www/dashboard/backend/gunicorn.sock`
   - Check Nginx error logs

2. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check Nginx static file configuration
   - Verify file permissions

3. **Database connection errors**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env
   - Verify database user permissions

4. **External API failures**
   - Check PHONE_REGISTRY_API_KEY is valid
   - Verify network connectivity
   - Check API logs: `/api/phone/logs/`

## Rollback Procedure

If deployment fails:

```bash
# Restore database from backup
psql dashboard_prod < /var/backups/dashboard/dashboard_YYYYMMDD_HHMMSS.sql

# Revert to previous commit
git checkout <previous-commit-hash>
./dashboard.sh restart
```

## Maintenance

### Regular Tasks

- Weekly: Review application logs
- Weekly: Check disk space
- Monthly: Update dependencies
- Monthly: Review security patches
- Quarterly: Review and optimize database
- Yearly: Renew SSL certificates (automatic with Let's Encrypt)

### Updating the Application

```bash
cd /var/www/dashboard

# Pull latest changes
git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Update frontend
cd ../frontend
npm install
npm run build

# Restart services
sudo systemctl restart dashboard-gunicorn
sudo systemctl reload nginx
```

## Support

For production issues:
- Check application health: `https://yourdomain.com/health/`
- Review logs: `sudo journalctl -u dashboard-gunicorn -f`
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Monitor external API: `https://yourdomain.com/api/phone/health/`
