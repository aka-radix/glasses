# Glasses

This is a simple Django based web app, that offers you the ability to list and view frames and lenses, as well as adding items to basket and creating orders. This app also includes authentication APIs, authentication and authorization dispatch whch also depends on whether you are an admin or a regular user.

## Setup

### Locally

Create a virtual environment:

```bash
python -m venv env
```

Activate the virtual environment:

```bash
source env/bin/activate
```

Install Poetry for dependency management:

```bash
pip install poetry
# or from requirements.txt
pip install -r requirements.txt
```

Spawn a virtual environment from Poetry:

```bash
poetry shell
```

Install project dependencies:

```bash
poetry install
# (optional) install development dependencies
poetry install --with dev
```

In case you are running the project locally, you should have running PostgresQL database (MySQL also works), and then you should update the environment variables as seen in .env.exmple, so for example:

```bash
DJANGO_SETTINGS_MODULE=config.settings.local
DJANGO_SECRET_KEY=super-strong-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

DATABASE_URL=psql://user:123@localhost:5432/glasses

```

Once this is set, you should be able to launch the app:

```bash
poetry run python manage.py runserver
```

You should be able to see some warnings regarding pending migrations, because now you should migrate them to the database:

```bash
poetry run python manage.py migrate
```

Now the app should be up and running.

Because it does not make sense for admin users to sign up and log in like regular users, and because they are usually limited and manually added, you should create a “super user” or an admin as follows:

```bash
poetry run python manage.py createsuperuser
```

You will get prompted to provide an email and a password.

The admin user has the previliage to create and update frames and lenses.

### Using Docker

Just the following:

```bash
docker-compose up --build

```

Once the containers are launched make sure to run the migrations:

```bash
docker exec -i <web-container-name> sh -c "poetry run python manage.py migrate"

```

---

## Exparimenting

You should be able to find an exported Postman collection in the repo, you should import that collection in order to be able to experiment.

You will have to set the URL environment variable in the collection, but you will have to copy and paste access and refresh tokens for some endpoints, however, you could also create a script which sets them as environment variables as well.

---

## Structure

```bash
.
├── config
│   ├── __init__.py
│   ├── settings
│   ├── urls.py
│   └── wsgi.py
├── CONTRIBUTORS.txt
├── glasses
│   ├── __init__.py
│   ├── orders
│   ├── products
│   └── users
├── manage.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt
```

### Config

This is the directory that contains Django project specific settings and configurations.

Most noteably. the settings directoy which contains 3 settings files:

The base module contains the shared settings and the most essential ones for the project.

The local and production modules inherit all settings from base and add specific settings to that environment.

### Glasses

This is the apps directory. An app within the context of Django is a package that contains specific set of features that are related. For example, the users app contains primarily the functionality related to users and authentication and any related functionality like serialization, database tables/models, views and so on.

Glasses contains 3 app:

- products: primarily concerned with frames and lenses functionality.
- orders: primarily concered with orders, basket and purchases functionality.
- users: user mangement and authentication.

### Others

The rest of the files in the root directory are mainly configuration or management files.

---

## More on structure

```bash
glasses/products
├── admin.py
├── api
│   ├── __init__.py
│   ├── serializers.py
│   └── viewsets.py
├── apps.py
├── __init__.py
├── migrations
│   ├── 0001_initial.py
│   └── __init__.py
├── models.py
└── urls.py
```

All 3 apps follow the same structure, also adhering to the standard Django layout and structure. The api directory primarily contains REST API related functionality like serializers and viewsets (a bundle of common as well as custom actions like GET, POST, and so on. Serializers are responsible for validating, serializing and deserializing data. Models contains models/tables definitions.

---

## Functionality

### Auth

You must be either a regular user or an admin. Admins are the ones added manually, and are able to create, delete and update products (frames and lenses). Regular users can view frames and lenses, add them to basket and create orders. Users are also able to change thier currency of preference.

Authentication here is based on JWTs. A user can sign up, log in, refresh token, verify and blacklist tokens as well. Users can only view items if they are not logged in.

### Ecommerce

As a business requirement, a user can only purchase one frame along with one pair of lenses, so at any given time, an order will always have one frame and one pair of lenses.

Users can add these items to their basket, then they should be able to create orders from those baskets.

Adding items to basket as well as creating orders includes a number of validations:

- A user must be logged in.
- Users can list frames and lenses.
  - **Note that here, since frames and lenses have a constraint that price and currency must be unique, only frames and lenses of the same currency as the user’s currency will be shown. Only “active” frames will be shown as well.**
- Move to “add_to_basket” and set the frame and lenses IDs that you have chosen.
  - Suppose a product was unavailable for some reason, for example its stock changed on the same time, or it was set to be “inactive” by some admin, the user will receive a validation error that that item is unavailable, and they will have to replace it to proceed.
  - If a user was trying to select a frame for example, and that frame is in another currency, they will get the same validation error as well, **as a frame with a different currency, could have a differnt price and is considered a completely different item (based on the business requirements).**
- Move to “create_order”, and you should be able to create an order in case the basket contains valid items and is considered in a valid state.
  - In case some weird thing happens in the background as mentioned above, the transaction will roll back and nothing will be commited, and the user will recieve a validation error.
  - In case things go well, the basket will be reset, the stock of the selected frame and lenses will get decremented by 1.

---

## More Utilities

You could benefit from the schema generation feature which allows you to check each endpoint along with its required and optional payload values, and possible responses and errors. Available schemas endpoint can be found by going to:

- <host>/api/schema/swagger-ui/
- <host>/api/schema/redoc/

---

## Development

I use quite a number of development tools including but not limited to:

```bash
ruff mypy isort autoflake flake8 djlint django-silk django_extensions ipython nplusone pre-commit
```

In addition to these, there are other utilties of various uses, including:

- pre-commit hooks
- editorconfig
- poetry
