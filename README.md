# Django CRUD `demo`

This project demonstrates a simple Django-based CRUD (Create, Read, Update, Delete) application. It features a custom user model, uses PostgreSQL as the database, and employs Bootstrap for front-end styling.

## Features

- Custom User Model
- CRUD operations for managing resources
- PostgreSQL as the database backend
- Bootstrap for a responsive UI
- Django’s built-in authentication system

### Structure

<pre>
django-crud-demo
│ 
├───.github
│   └───workflows
├───requirements
├───screenshots
├───src
│   ├───apps
│   │   └───users
│   │       ├───management
│   │       │   ├───commands
│   │       │   └───lists
│   │       ├───migrations
│   │       ├───templatetags
│   │       └───...
│   ├───core
│   │   ├───settings
│   │   │   ├───base
│   │   │   ├───development
│   │   │   └───production
│   │   └───...
│   ├───media
│   ├───staticfiles
│   └───templates
│       ├───auth
│       │   └───passwords
│       ├───layouts
│       ├───main
│       └───users
└───static
    └───css  
</pre>

### Requirements

To run this project locally, you’ll need:

- [Python 3.11](https://python.org/downloads)
- [Django 5.1](https://docs.djangoproject.com/en/5.1/)
- [PostgreSQL](https://www.postgresql.org/download/)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mkeithX/django-crud-demo.git
   ```
   ```bash
   cd django-crud-demo
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   # For Linux/Mac
   source .venv/bin/activate
   # For Windows
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   py -m pip install -- upgrade -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Create a PostgreSQL database for the project.
   - Update the `DATABASES` setting in `development.settings.py` with your PostgreSQL credentials:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Run migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Collect static files:

   ```bash
   python manage.py collectstatic
   ```

8. Run the development server:

   ```bash
   python manage.py runserver
   ```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser to view the application.


## Custom User Model

This project uses a custom user model defined in the accounts app. It’s important to configure the custom user model before running the initial migration. Ensure that the `AUTH_USER_MODEL` setting in `settings.py` is properly set:

```python
AUTH_USER_MODEL = 'apps_users.User'
```

## Bootstrap Integration

[Bootstrap](https://getbootstrap.com) is used for styling the frontend of the application. All templates are configured to include Bootstrap’s CSS and JavaScript files. You can find the templates in the `templates` directory and the static files (CSS/JS) in the `static` directory.

## License

This project is licensed under the MIT License.
