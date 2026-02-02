# CalorieCounter

## Why this project exists

I completed an MSc Computer Science (Conversion) where the capstone project was heavily front-end focused. I wanted to go deeper on backend engineering: data modelling, validation, API design, authentication/authorization, testing, and deployment.

This project is my “real-world REST API” sandbox. The goal is to build something end-to-end that is not just CRUD, while keeping the scope small enough to iterate quickly.

## Project approach (high level)

1) Pick a production-style web API framework and commit to it (Django REST Framework).
2) Learn the framework properly (docs, tutorials, small spikes).
3) Build an MVP, then iterate via refactors and feature expansion.

## Current status

This is an alpha project under active development. Expect breaking changes: endpoints and the database schema may change frequently. During development, the local database is treated as disposable. 

Main API code lives in `application/restApi/`.

### What works today

- Basic API to create and retrieve food/meal entries stored in a database.
- Early validation and tests for common edge cases (still expanding).

### In progress

- Adding user accounts.
- Implementing authentication, permissions, and refactoring the data model to support per-user data.

### Planned

- Per-user summaries and statistics (weekly/monthly/yearly views).
- A small front-end UI to visualise the backend functionality.
- Deployment of backend (and front end) to the cloud, with a public instance.

## Tech stack

Python </br>
Django + Django REST Framework (web framework and API layer) </br>
SQLite for local development, with a plan to switch to PostgreSQL for deployment </br>
pytest + Hypothesis for automated tests, including property-based testing </br>

## File structure overview

The Django project root is application/ (contains manage.py).</br>
The main API app is application/restApi/ (models, serializers, views, URLs).</br>
Tests live in application/restApi/tests/.</br>
Development notes and workflow live in docs/DEV.md.</br>

For a detailed file tree, look here [look here](docs/DEV.md)

## Quickstart (development)

1) Clone the repository.
2) Create and activate a Python virtual environment (for example, venv).
3) Install dependencies from requirements.lock.txt.
4) Run the local development server from the application/ directory.

