# Cycling Climbs api 🛡️

## Requirements

Python version 3
Pip version 3
PostgreSQL 10.10 
PostGIS extension for Postgres

## Local Deployment

Copy env.example.py to env.py and define environment settings

Create database in psql and migrate schema

```
python manage.py migrate
```

Use seed scripts found in /data for initial data

```
python3 manage.py loaddata ./data/climbs.yaml
python3 manage.py loaddata ./data/provinces.yaml
```

