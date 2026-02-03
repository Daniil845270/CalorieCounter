# Repository structure (view as code)
├── README.md                         # Project overview
├── requirements.lock.txt             # Pinned Python dependencies (install source)
├── docs/
│   └── DEV.md                        # Development notes (setup, workflow, troubleshooting)
├── application/                      # Django project root
│   ├── manage.py                     # Django entry point
│   ├── db.sqlite3                    # Local dev DB (disposable)
│   ├── pytest.ini                    # pytest configuration
│   ├── application/                  # Django project package (settings, urls, wsgi/asgi)
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── restApi/                      # Main API app (models, serializers, views)
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── migrations/               # DB schema migrations
│       └── tests/                    # pytest tests
│           ├── conftest.py           
│           └── test_serializer.py

[go back](/README.md)

# how to squash commits

1) Start an interactive rebase for the last N commits:</br>
`git rebase -i HEAD~N`</br>
2) An editor opens with something like:</br>
`pick 3e6d31f api improvements...`</br>
`pick a1a53f7 added food entry description validator...`</br>
Change it to:</br>
`pick 3e6d31f api improvements...`</br>
`squash a1a53f7 added food entry description validator...`</br>
Save and close.</br>
3) Git will open another editor to edit the combined commit message. Keep one message or rewrite it. Save and close.</br>
4) Push the rewritten history safely:</br>
`git push --force-with-lease`</br>

# Protocol for when I (eventually) break the schema again:

Scorched earth approach:

1) Move into the Django project root
From CalorieCounter/:

    `cd application`

You should now be in the directory that contains manage.py and db.sqlite3.

2) Delete the SQLite database
Your DB file is here: CalorieCounter/application/db.sqlite3
Delete it:

    `rm -f db.sqlite3`
    `rm -f db.sqlite3-journal db.sqlite3-wal db.sqlite3-shm`

3) Delete all restApi migrations (keep __init__.py)
Your migrations live here:CalorieCounter/application/restApi/migrations/
Delete all migration files except __init__.py:

    `find restApi/migrations -type f -name "*.py" ! -name "__init__.py" -delete`

    Optional but recommended: wipe compiled migration caches too:

    `find restApi/migrations -type d -name "__pycache__" -exec rm -rf {} +`

At this point, restApi/migrations/ should contain only __init__.py (and possibly an empty __pycache__ if recreated later).

4) Optional cleanup: clear other Python caches
Not required, but keeps things tidy:

    `find . -type d -name "__pycache__" -exec rm -rf {} +`
    `find . -type f -name "*.pyc" -delete`

5) Recreate fresh initial migrations and migrate

    `python manage.py makemigrations restApi`
    `python manage.py migrate`

You should see it create restApi/migrations/0001_initial.py, a brand new db.sqlite3