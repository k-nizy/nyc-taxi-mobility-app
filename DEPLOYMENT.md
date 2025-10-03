# Deployment Guide

Production deployment guide for NYC Taxi Analytics Platform.

## Production Checklist

### Security
- [ ] Change all default passwords
- [ ] Set strong `SECRET_KEY` in Flask
- [ ] Use environment variables for all credentials
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Set up API authentication (if needed)
- [ ] Regular security audits

### Performance
- [ ] Enable database connection pooling
- [ ] Set up Redis caching layer
- [ ] Configure CDN for static assets
- [ ] Optimize database queries
- [ ] Add database query caching
- [ ] Implement API response caching
- [ ] Compress API responses (gzip)
- [ ] Minify frontend assets

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging aggregation
- [ ] Database performance monitoring
- [ ] API endpoint metrics
- [ ] Server resource monitoring
- [ ] Uptime monitoring
- [ ] Alert system for failures

## Deployment Options

### Option 1: Traditional VPS (DigitalOcean, Linode)

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv postgresql nginx supervisor

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

#### 2. PostgreSQL Configuration
```bash
# Create production database
sudo -u postgres psql
CREATE DATABASE nyc_taxi_prod;
CREATE USER prod_user WITH ENCRYPTED PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE nyc_taxi_prod TO prod_user;
\q

# Configure PostgreSQL for remote access (if needed)
sudo nano /etc/postgresql/13/main/postgresql.conf
# Set: listen_addresses = 'localhost'  # Or specific IP

sudo nano /etc/postgresql/13/main/pg_hba.conf
# Add: host    nyc_taxi_prod    prod_user    127.0.0.1/32    md5

sudo systemctl restart postgresql
```

#### 3. Backend Deployment
```bash
# Clone repository
cd /var/www
sudo git clone <your-repo-url> nyc-taxi
cd nyc-taxi/backend

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Configure production environment
sudo nano .env
# Set production values

# Initialize database
python init_db.py

# Test Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 4. Supervisor Configuration
Create `/etc/supervisor/conf.d/nyc-taxi-api.conf`:
```ini
[program:nyc-taxi-api]
directory=/var/www/nyc-taxi/backend
command=/var/www/nyc-taxi/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/nyc-taxi/api.err.log
stdout_logfile=/var/log/nyc-taxi/api.out.log
```

```bash
# Create log directory
sudo mkdir -p /var/log/nyc-taxi

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start nyc-taxi-api
```

#### 5. Frontend Build
```bash
cd /var/www/nyc-taxi/frontend

# Install dependencies
npm install

# Build for production
npm run build

# Files will be in build/ directory
```

#### 6. Nginx Configuration
Create `/etc/nginx/sites-available/nyc-taxi`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/nyc-taxi/frontend/build;
        try_files $uri /index.html;
        
        # Enable gzip
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    }

    # API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers (adjust for production)
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
    }

    # Health check
    location /health {
        proxy_pass http://127.0.0.1:5000/health;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/nyc-taxi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL Setup (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 2: Docker Deployment

#### Dockerfile - Backend
Create `backend/Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Dockerfile - Frontend
Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: nyc_taxi_db
      POSTGRES_USER: taxi_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U taxi_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: nyc_taxi_db
      DB_USER: taxi_user
      DB_PASSWORD: ${DB_PASSWORD}
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
      - ./data:/data

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

```bash
# Deploy with Docker
docker-compose up -d

# Initialize database
docker-compose exec backend python init_db.py

# Process data
docker-compose exec backend python data_processor.py /data/yellow_tripdata_2023-01.parquet
```

### Option 3: Cloud Platforms

#### AWS (Elastic Beanstalk + RDS)
1. Create RDS PostgreSQL instance
2. Deploy backend with Elastic Beanstalk
3. Deploy frontend to S3 + CloudFront
4. Configure environment variables

#### Heroku
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create nyc-taxi-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# Initialize database
heroku run python init_db.py
```

#### Google Cloud Platform
1. Cloud SQL for PostgreSQL
2. Cloud Run for backend
3. Cloud Storage + CDN for frontend

## Production Environment Variables

Backend `.env`:
```bash
# Database
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=nyc_taxi_prod
DB_USER=prod_user
DB_PASSWORD=strong_password_here

# Flask
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=generate-long-random-string-here

# Performance
WORKERS=4
MAX_OVERFLOW=10
POOL_SIZE=20
```

## Performance Optimization

### Database Tuning
```sql
-- Analyze tables
ANALYZE trips;
ANALYZE zones;

-- Vacuum regularly
VACUUM ANALYZE trips;

-- Monitor slow queries
CREATE EXTENSION pg_stat_statements;
```

### Redis Caching
```python
# Install redis
pip install redis

# Add to app.py
from redis import Redis
import json

redis_client = Redis(host='localhost', port=6379, db=0)

@app.route('/api/statistics')
def get_statistics():
    cache_key = f"stats:{request.args.to_dict()}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # ... compute statistics ...
    
    redis_client.setex(cache_key, 300, json.dumps(result))  # 5 min cache
    return result
```

## Backup Strategy

### Database Backups
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
pg_dump -U prod_user nyc_taxi_prod | gzip > /backups/db_$DATE.sql.gz

# Keep last 7 days
find /backups -name "db_*.sql.gz" -mtime +7 -delete
```

### Automated Backups
```cron
# Add to crontab
0 2 * * * /usr/local/bin/backup-database.sh
```

## Monitoring Setup

### Application Logs
```python
# Enhanced logging in app.py
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
```

### Health Checks
```bash
# Simple monitoring script
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)
if [ $response != "200" ]; then
    echo "API is down!" | mail -s "Alert" admin@example.com
fi
```

## Scaling Strategies

### Horizontal Scaling
- Load balancer (Nginx, HAProxy)
- Multiple backend instances
- Database read replicas
- Redis cluster for caching

### Vertical Scaling
- Increase server resources
- Optimize database configuration
- Add more Gunicorn workers

## Rollback Procedure

```bash
# Backend rollback
cd /var/www/nyc-taxi
git checkout <previous-version-tag>
sudo supervisorctl restart nyc-taxi-api

# Frontend rollback
cd frontend
git checkout <previous-version-tag>
npm run build
sudo systemctl reload nginx
```

## Security Hardening

1. **Firewall Configuration**
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

2. **Fail2Ban**
```bash
sudo apt install fail2ban
# Configure to protect SSH and web services
```

3. **Regular Updates**
```bash
sudo apt update && sudo apt upgrade
pip list --outdated
npm outdated
```

## Post-Deployment Testing

- [ ] Health check endpoint responds
- [ ] API endpoints return correct data
- [ ] Frontend loads and displays charts
- [ ] Database queries perform within SLA
- [ ] SSL certificate valid
- [ ] Error tracking receives events
- [ ] Logs are being written
- [ ] Backups are running
- [ ] Monitoring alerts work

---

**For production support, maintain comprehensive documentation and runbooks for common issues.**
