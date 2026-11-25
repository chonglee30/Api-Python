# Api-Python

Python API testing and automation project using `pytest` and `Pipenv`.

## Project Structure
- `config.py` — Environment and test configuration settings
- `main.py` — Entry point or runner script
- `tests/` — API test suites (`pytest`)
- `utils/` — Reusable request helpers, assertions, and utilities
- `Pipfile` & `Pipfile.lock` — Dependency definitions and locked versions

## Test Scenarios
- Prerequisite: Obtain authentication token using username and password
- Create & Cleanup: Create an article and delete it afterward
- Read: Retrieve and verify all articles
Contract / Schema Validation: Validate API response payloads against expected schemas
