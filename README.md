# Cycling Climbs api 🛡️

## Requirements

Python version 3
PostgreSQL 10.10 or greater
PostGIS extension for Postgres
Pip installed
Python-psycopg2 installed
libpq-dev installed


## Local Deployment

Install dependencies (use pip3)

```
pip3 install -r requirements.txt
```

Copy env.example.py to env.py and define environment settings

Create database in postgres. Don't forget to add the postgis extension to the database `CREATE EXTENSION postgis;` and the unaccent extension `CREATE EXTENSION unaccent;
`

Migrate schema

```
python3 manage.py migrate
```

Use seed scripts found in /data for initial data

```
python3 manage.py loaddata ./data/climbs.yaml
python3 manage.py loaddata ./data/regions.yaml
python3 manage.py loaddata ./data/provinces.yaml
```

python3 manage.py dumpdata api_region > ./data/regions.yaml

## Local Deployment

Tests are run with django TestCase. Fixtures are found in api/tests/fixtures. Please test all new functionality

Test Command

```
python3 manage.py test
```

Test One Test Case

```
python3 manage.py test api.tests.ClimbTestCase
```

Run Single Test 

```
python3 manage.py test api.tests.ClimbTestCase.test_climb_viewset_destroy_route
```