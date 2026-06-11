# Getting Started with Journal Application

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Redis 6 or higher
- Git

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/journal-app.git
cd journal-app
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory with the following variables:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/journal_db
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup
```bash
# Create PostgreSQL database
createdb journal_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Start Redis Server
```bash
# On Linux/Mac
redis-server

# On Windows
# Start Redis server from Windows Services
```

### 7. Start Celery Worker
```bash
celery -A journal worker -l info
```

### 8. Run Development Server
```bash
python manage.py runserver
```

## Initial Configuration

### 1. User Setup
1. Visit `http://localhost:8000/admin`
2. Log in with your superuser credentials
3. Create initial user groups and permissions

### 2. Feature Configuration
1. Configure email settings in `settings.py`
2. Set up file storage (local or cloud)
3. Configure analytics settings

### 3. Testing the Setup
1. Create a test user account
2. Create a sample journal entry
3. Test the daily task feature
4. Verify goal tracking functionality

## Common Issues and Solutions

### Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists

### Redis Connection Issues
- Verify Redis server is running
- Check Redis connection URL
- Test Redis connection using redis-cli

### Celery Worker Issues
- Check Celery worker logs
- Verify Redis connection
- Ensure all dependencies are installed

## Next Steps
1. Review the [User Guide](./user-guide.md)
2. Explore the [API Documentation](./api-documentation.md)
3. Check out the [Developer Guide](./developer-guide.md)

## Support
If you encounter any issues during setup:
1. Check the [FAQ](./faq.md)
2. Review error logs
3. Contact support at support@journalapp.com 