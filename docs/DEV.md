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

# Security aspects that I should take care of when I implement the frontend

1) How to properly store the JWT tokens
JWS + JWE
https://www.descope.com/blog/post/developer-guide-jwt-storage

2) Read around how to implement the secure tokens (e.g. applying a signature)

3) Read around the best practices to safeguard against CSRF (if I will use sessions), XSS and other attacks 
https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

# Security aspects that I absolutely must sort out in the backend before I proceed to deployment:

Go through this checklist and make sure that my code has protection against each point
https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/ 

Serialiser level vulnerabilities that I noticed when reading API Security Top 10 2023

1) API1:2023 Broken Object Level Authorization

Ensure that authenticated users can create the entries and descriptions only for themselves, and not for other users 
-> obviously in the UI that wouldn't be possible (because I will implement it), but I need to ensure that it is also not possible to do that though an 
authenticated HTTP request
-> essentially ensure in all of the serializer validators that the request.user and data["entry user"] match, otherwise reject the request

2) API2:2023 Broken Authentication

The backend is vulnerable at the moment, because it:

- Permits credential stuffing where the attacker uses brute force with a list of valid usernames and passwords.
My backend endpoints as is allow:
1) unlimited attempts per IP, per account, or per device fingerprint
2) no increasing delays
3) no detection of automated behaviour
4) no secondary checks after repeated failures
Need to implement rate limits via DRF throttling, lockout rules, breached-password checks
- Permits attackers to perform a brute force attack on the same user account, without presenting captcha/account lockout mechanism.
- Doesn't permit weak passwords, although there is definitely room for improvement
- Allows users to change their email address, current password, or do any other sensitive operations without asking for password confirmation.
(changing account details itself in not implemented yet)
- Accepts unsigned/weakly signed JWT tokens ({"alg":"none"})
- Doesn't validate the JWT expiration date (although the backend may does that already -> build the front-end and check)

3) Pretty much the rest of them (I thought I was done making the backend lol)



