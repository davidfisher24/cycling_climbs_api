# Cycling Climbs api 🛡️

## Requirements

Python version 3
PostgreSQL 10.10 or greater
PostGIS extension for Postgres
Pip installed
Python-psycopg2 installed
libpq-dev installed


## Local Deployment

Install dependencies

```
pip install -r requirements.txt
```

Copy env.example.py to env.py and define environment settings

Create database in psql and migrate schema

```
python3 manage.py migrate
```

Use seed scripts found in /data for initial data

```
python3 manage.py loaddata ./data/climbs.yaml
python3 manage.py loaddata ./data/provinces.yaml
```

