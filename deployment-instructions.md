# Deployment Instructions for Kicat-Django

## Prerequisites
- Docker and Docker Compose installed on your server
- Domain name (optional but recommended)
- SSH access to your server

## Deployment Steps

### 1. Prepare Environment

1. Copy your project to the server:
   ```
   scp -r kicat-django/ user@your-server:/path/to/deployment/
   ```

2. Create the `.env` file from the template:
   ```
   cd /path/to/deployment/kicat-django/
   cp env.example .env
   nano .env
   ```

3. Update the environment variables in the `.env` file:
   - Set a secure `SECRET_KEY`
   - Set `DEBUG=False`
   - Add your domain to `ALLOWED_HOSTS`
   - Configure the database credentials
   - Set up email settings if needed

### 2. Build and Start Docker Containers

1. Build the Docker images:
   ```
   docker-compose build
   ```

2. Start the services:
   ```
   docker-compose up -d
   ```

3. Check if all services are running:
   ```
   docker-compose ps
   ```

### 3. Database Setup

1. Run migrations:
   ```
   docker-compose exec web python manage.py migrate
   ```

2. Create a superuser:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

3. Load initial data (if needed):
   ```
   docker-compose exec web python manage.py loaddata initial_data.json
   ```

### 4. Set up your domain (optional)

1. Update the Nginx configuration in `nginx/conf.d/default.conf` to include your domain:
   ```
   server_name yourdomain.com www.yourdomain.com;
   ```

2. Set up SSL with Certbot (recommended):
   ```
   docker-compose down
   
   # Install certbot on your host machine
   sudo apt-get update
   sudo apt-get install certbot
   
   # Get certificate
   sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
   
   # Update Nginx config to use SSL
   nano nginx/conf.d/default.conf
   
   # Start containers again
   docker-compose up -d
   ```

### 5. Maintenance Commands

- View logs:
  ```
  docker-compose logs -f
  ```

- Restart services:
  ```
  docker-compose restart
  ```

- Update the application:
  ```
  git pull
  docker-compose build web
  docker-compose up -d
  docker-compose exec web python manage.py migrate
  docker-compose exec web python manage.py collectstatic --noinput
  ```

- Backup the database:
  ```
  docker-compose exec db pg_dump -U kicatuser kicat > backup_$(date +%Y%m%d).sql
  ```

### 6. Troubleshooting

- Check logs:
  ```
  docker-compose logs -f web
  ```

- Access the container shell:
  ```
  docker-compose exec web bash
  ```

- Check the database connection:
  ```
  docker-compose exec web python manage.py shell -c "from django.db import connection; connection.ensure_connection()"
  ```

- Restart a specific service:
  ```
  docker-compose restart web
  ```

## Security Notes

1. Keep your `.env` file secure and never commit it to version control
2. Regularly update your Docker images and packages
3. Set up a firewall to allow only necessary ports (80, 443)
4. Consider setting up automated backups for your database 