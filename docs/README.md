# Journal Application Documentation

## Table of Contents
1. [Getting Started](./getting-started.md)
2. [User Guide](./user-guide.md)
3. [Developer Guide](./developer-guide.md)
4. [API Documentation](./api-documentation.md)
5. [Data Pipeline Documentation](./data-pipeline.md)
6. [Security Documentation](./security.md)
7. [Deployment Guide](./deployment.md)

## Overview
The Journal Application is a comprehensive personal journaling and productivity platform that combines traditional journaling with modern data analytics and task management features. The application helps users track their daily activities, set and monitor goals, and maintain a structured approach to personal development.

## Key Features
- **Journal Entries**: Create and manage personal journal entries with sentiment analysis
- **Daily Tasks**: Track and manage daily tasks with priority levels
- **Goals**: Set and monitor progress towards personal and professional goals
- **Pointed Journal**: Create structured journal entries with specific focus areas
- **Daily Tracker**: Monitor daily metrics and habits
- **Vent Feature**: Private space for emotional expression with sentiment analysis

## System Requirements
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Redis 6 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see [Getting Started](./getting-started.md))
4. Initialize the database: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`

## Support
For support and questions, please:
1. Check the [User Guide](./user-guide.md) for common issues
2. Review the [FAQ](./faq.md)
3. Open an issue on our GitHub repository
4. Contact support at support@journalapp.com 