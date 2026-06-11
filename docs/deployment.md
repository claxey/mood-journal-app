# Deployment Guide

## Deployment Options

### 1. Docker Deployment (Recommended)

#### Prerequisites
- Docker
- Docker Compose
- Git

#### Steps

1. **Clone and Setup**
```bash
git clone https://github.com/yourusername/journal-app.git
cd journal-app
```

2. **Environment Configuration**
Create `.env` file:
```env
DEBUG=False
SECRET_KEY=your-secure-secret-key
DATABASE_URL=postgresql://user:password@db:5432/journal_db
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=your-domain.com
DJANGO_SETTINGS_MODULE=journal.settings.production
```

3. **Build and Run**
```bash
docker-compose up --build
```

### 2. Traditional Server Deployment

#### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Nginx
- Gunicorn

#### Steps

1. **Server Setup**
```bash
# Update system
sudo apt update
sudo apt upgrade

# Install dependencies
sudo apt install python3-pip python3-venv postgresql nginx redis-server
```

2. **Application Setup**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate
```

3. **Gunicorn Setup**
Create `/etc/systemd/system/journal.service`:
```ini
[Unit]
Description=Journal Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/journal-app
Environment="PATH=/path/to/journal-app/venv/bin"
ExecStart=/path/to/journal-app/venv/bin/gunicorn --workers 3 --bind unix:/path/to/journal-app/journal.sock journal.wsgi:application

[Install]
WantedBy=multi-user.target
```

4. **Nginx Configuration**
Create `/etc/nginx/sites-available/journal`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/journal-app;
    }

    location /media/ {
        root /path/to/journal-app;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/journal-app/journal.sock;
    }
}
```

5. **Enable and Start Services**
```bash
sudo ln -s /etc/nginx/sites-available/journal /etc/nginx/sites-enabled
sudo systemctl start journal
sudo systemctl enable journal
sudo systemctl restart nginx
```

## Production Settings

Create `journal/settings/production.py`:
```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'journal_db',
        'USER': 'journal_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/journal/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Docker Configuration

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn journal.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - 8000
    env_file:
      - .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env

  redis:
    image: redis:6
    volumes:
      - redis_data:/data

  nginx:
    build: ./nginx
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
```

Create `Dockerfile`:
```dockerfile
FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput
```

Create `nginx/Dockerfile`:
```dockerfile
FROM nginx:1.19

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```

Create `nginx/nginx.conf`:
```nginx
upstream journal {
    server web:8000;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://journal;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

## Deployment Checklist

### Pre-deployment
- [ ] Update all dependencies
- [ ] Run security checks
- [ ] Backup database
- [ ] Test in staging environment
- [ ] Update environment variables
- [ ] Configure SSL certificates

### Deployment
- [ ] Deploy code changes
- [ ] Run database migrations
- [ ] Collect static files
- [ ] Restart services
- [ ] Verify application status
- [ ] Check error logs

### Post-deployment
- [ ] Monitor application performance
- [ ] Check security logs
- [ ] Verify backups
- [ ] Test all features
- [ ] Update documentation

## Monitoring Setup

### 1. Application Monitoring
- Set up error tracking (e.g., Sentry)
- Configure performance monitoring
- Set up uptime monitoring
- Configure alerting

### 2. Server Monitoring
- Set up resource monitoring
- Configure log aggregation
- Set up backup monitoring
- Configure security monitoring

## Backup Strategy

### 1. Database Backups
```bash
# Daily backup
pg_dump -U journal_user journal_db > backup_$(date +%Y%m%d).sql

# Weekly backup
tar -czf backup_$(date +%Y%m%d).tar.gz backup_*.sql
```

### 2. File Backups
```bash
# Daily backup of media files
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# Weekly backup
tar -czf weekly_backup_$(date +%Y%m%d).tar.gz media_backup_*.tar.gz
```

## Scaling Strategy

### 1. Horizontal Scaling
- Add more application servers
- Configure load balancer
- Set up database replication
- Configure Redis cluster

### 2. Vertical Scaling
- Increase server resources
- Optimize database performance
- Configure caching
- Optimize static file serving 