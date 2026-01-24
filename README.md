# CalorieCounter

Protocol for when I (eventually) break the schema again:

Scorched earth approach:

cd application
1) Move into the Django project root
From CalorieCounter/:

    cd application

You should now be in the directory that contains manage.py and db.sqlite3.

2) Delete the SQLite database
Your DB file is here: CalorieCounter/application/db.sqlite3
Delete it:

    rm -f db.sqlite3
    rm -f db.sqlite3-journal db.sqlite3-wal db.sqlite3-shm

3) Delete all restApi migrations (keep __init__.py)
Your migrations live here:CalorieCounter/application/restApi/migrations/
Delete all migration files except __init__.py:

    find restApi/migrations -type f -name "*.py" ! -name "__init__.py" -delete

Optional but recommended: wipe compiled migration caches too:

    find restApi/migrations -type d -name "__pycache__" -exec rm -rf {} +

At this point, restApi/migrations/ should contain only __init__.py (and possibly an empty __pycache__ if recreated later).

4) Optional cleanup: clear other Python caches
Not required, but keeps things tidy:

    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

5) Recreate fresh initial migrations and migrate

    python manage.py makemigrations restApi
    python manage.py migrate

You should see it create restApi/migrations/0001_initial.py, a brand new db.sqlite3 and apply:
Django core migrations (auth/admin/etc.)
your new restApi.0001_initial