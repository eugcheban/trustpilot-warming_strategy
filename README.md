
# How to start project

## 1. Create or enter in env

```bash
python3 -m venv env
source env/bin/activate
```

## 2. Install dependencies

```bash
pip3 install -r requirements.txt
```

## 3. Edit trustpilot/modules/`load_django.py` and set the project path
```python
sys.path.append(' ___ /trustpilot-warming_strategy/trustpilot') 
```

## 4. Prepare `.env` file with DB credentials

```bash
DB_NAME = 'trustpilot'
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = '5001'

PGADMIN_DEFAULT_EMAIL = 'admin@mail.com'
PGADMIN_DEFAULT_PASSWORD = 'admin'

# Multilogin API credentials
USERNAME = ''
PASSWORD = ''
FOLDER_ID = ''
PROFILE_ID = ''
```

## 5. Run docker compose

```bash
docker compose up
```

## 6. Migrations

```bash
python trustpilot/manage.py makemigrations
python trustpilot/manage.py migrate
```

