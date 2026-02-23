Deployment notes - Health Record Management System

1) Set environment variables on the server (PythonAnywhere, Render, etc):

- DJANGO_SECRET_KEY: a long random secret
- DJANGO_DEBUG: 'False'
- DJANGO_ALLOWED_HOSTS: comma-separated hosts (example: youruser.pythonanywhere.com)

2) Install dependencies in virtualenv:

```bash
pip install -r requirements.txt
```

3) Collect static files:

```bash
python manage.py collectstatic --noinput
```

4) Run migrations:

```bash
python manage.py migrate
```

5) Create superuser (optional):

```bash
python manage.py createsuperuser
```

6) Configure webserver (PythonAnywhere: set working directory to project root, WSGI points to `healthmanagement.wsgi`) 

7) Reload the web app and visit your domain.

Notes:
- For production DB use PostgreSQL or MySQL and set DATABASES via environment variables.
- WhiteNoise is used to serve static files in simple deployments. For heavy traffic use a CDN.
