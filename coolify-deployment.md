# Coolify Deployment Guide for Kicat Django

## Prerequisites
- Coolify installed on your server
- Git repository with your project

## Deployment Steps

### 1. Create a New Service in Coolify

1. Log in to your Coolify dashboard
2. Click "Create New Resource" → "Application"
3. Select your Git repository and branch
4. Choose "Docker Compose" as deployment method

### 2. Configure Your Application

#### Basic Configuration
- Set a name for your application (e.g., `kicat-django`)
- Add your domain (e.g., `kicat.yourdomain.com`)
- Enable HTTPS (Coolify will handle certificates with Caddy)

#### Environment Variables
Create these environment variables in Coolify:

```
SECRET_KEY=your_secure_random_key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
POSTGRES_DB=kicat
POSTGRES_USER=kicatuser
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgres://kicatuser:your_secure_password@db:5432/kicat
COMPOSE_PROJECT_NAME=kicat
```

### 3. Deployment

1. Save your configuration
2. Click "Deploy"
3. Wait for the build to complete

### 4. Post-Deployment Tasks

After successful deployment, SSH into your server and run these commands to initialize the database:

```bash
# Connect to your Coolify server
ssh user@your-server

# Find your application container
docker ps | grep kicat

# Run migrations
docker exec -it CONTAINER_ID python manage.py migrate

# Create superuser
docker exec -it CONTAINER_ID python manage.py createsuperuser

# Add initial data (categories)
docker exec -it CONTAINER_ID python manage.py shell -c "from quotes.models import ServiceCategory, ServiceType; cat1 = ServiceCategory.objects.create(name='통역'); ServiceType.objects.create(name='순차통역', category=cat1, is_active=True); ServiceType.objects.create(name='동시통역', category=cat1, is_active=True); cat2 = ServiceCategory.objects.create(name='번역'); ServiceType.objects.create(name='일반번역', category=cat2, is_active=True); ServiceType.objects.create(name='전문번역', category=cat2, is_active=True); print('Service categories and types created!')"
```

### 5. Monitor and Troubleshoot

- Check logs in Coolify dashboard
- Verify that your site is accessible at your domain
- Check for proper static file and media serving

## Important Notes

- Coolify uses Caddy as a reverse proxy, so we've removed the nginx container from docker-compose.yml
- The application is configured to serve static files using WhiteNoise
- We use named volumes with project prefixes to avoid conflicts with other services
- Environment variables are managed through Coolify instead of a .env file

If you need to make changes to your configuration, just update the repository and redeploy through Coolify. 