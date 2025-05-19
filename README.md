# Kicat Django

A comprehensive website for a translation company built with Django and Docker.

## Features

- Professional translation services showcase
- Quote request form with customizable service categories
- Admin panel for managing quotes and services
- Multilingual support
- Mobile-responsive design
- Contact information and company details

## Technology Stack

- Django (Python web framework)
- PostgreSQL (Database)
- Docker (Containerization)
- WhiteNoise (Static file serving)
- Tailwind CSS (Styling)

## Running Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/kicat-django.git
cd kicat-django

# Create .env file
cp env.example .env
# Edit .env with your settings

# Build and start Docker containers
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Create initial service categories (optional)
docker-compose exec web python manage.py shell -c "from quotes.models import ServiceCategory, ServiceType; cat1 = ServiceCategory.objects.create(name='통역'); ServiceType.objects.create(name='순차통역', category=cat1, is_active=True); ServiceType.objects.create(name='동시통역', category=cat1, is_active=True); cat2 = ServiceCategory.objects.create(name='번역'); ServiceType.objects.create(name='일반번역', category=cat2, is_active=True); ServiceType.objects.create(name='전문번역', category=cat2, is_active=True); print('Service categories and types created!')"
```

## Deployment

This project is designed to be deployed with Coolify. Check the [coolify-deployment.md](coolify-deployment.md) for detailed instructions.

## Project Structure

- `kicat/` - Main Django project directory
- `quotes/` - Quote request app
- `core/` - Core website functionality
- `docker-compose.yml` - Docker Compose configuration
- `Dockerfile` - Docker build file

## License

[MIT](LICENSE) 