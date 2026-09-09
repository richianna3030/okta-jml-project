# okta-jml-project

This project automates the "joiner-mover-leaver" process against the Okta identity provider. It provisions new users with role-based assignments, auto updates access when a role changes, deactivates access upon termination, and writes all actions to a SQL database for audit purposes.

## Skill Goals

This project is intended to demonstrate and build towards:

* Hands-on IAM platform experience
* RBAC and least-privilege
* Audit and compliance
* Python proficiency
* SQL application
* Outcome-oriented

## Software & Tools

* Python 3.13
* Okta Developer Edition
* python-dotenv
* SQLite
* pytest
* GitHub

## Architecture

Flow of control through the project:

1. role_mapping.py defines which Okta groups belong to each role (Standard Employee, Manager, IT Admin)
2. provision_user.py (joiner), move_user.py (mover), and remove_user.py (leaver) each read from role_mapping.py to know which groups to assign or remove
3. All three call the Okta API directly to create users and manage group membership
4. Every action (create, group assign, group remove, deactivate, role change) is passed to audit.py's log_action() function
5. log_action() writes a row to audit_log.db (SQLite), recording timestamp, action, user, detail, and success/failure status

## Role Model

| Role | Groups |
|---|---|
| Standard Employee | Standard-Employee |
| Manager | Standard-Employee, Manager |
| IT Admin | Standard-Employee, IT-Admin |

Manager and IT Admin are additive on top of Standard Employee -- elevated roles build on the baseline rather than being siloed, reflecting least-privilege design.

## Setup

1. Sign up for a free Okta Developer Edition org at developer.okta.com (choose Okta Platform, not Auth0).
2. Generate an API token in the Okta Admin Console under Security, API, Tokens.
3. Create a .env file with OKTA_ORG_URL and OKTA_API_TOKEN.
4. Install dependencies: pip install -r requirements.txt
5. Create the audit database: python create_db.py

## Running It

* python provision_user.py -- joiner
* python move_user.py -- mover
* python remove_user.py -- leaver

## Testing

pytest -v

9 tests covering role-mapping logic, audit log writes, and mocked API success/failure handling.

## What I'd Build Next

* A CLI so roles/emails aren't hardcoded per script
* PostgreSQL instead of SQLite for a more enterprise-realistic audit store
* Docker packaging for one-command setup