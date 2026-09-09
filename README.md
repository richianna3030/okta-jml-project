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

\```
                    ┌─────────────────┐
                    │   role_mapping   │
                    │  (role → groups) │
                    └────────┬─────────┘
                             │
       ┌─────────────────┼─────────────────┐
       ▼                    ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│  provision  │     │    move     │     │    remove     │
│    _user    │     │    _user    │     │    _user      │
│  (joiner)   │     │  (mover)    │     │  (leaver)     │
└──────┬──────┘     └──────┬──────┘     └───────┬───────┘
       │                    │                     │
       └────────────────────┼─────────────────────┘
                             ▼
                    ┌─────────────────┐
                    │   Okta API      │
                    │ (users/groups)  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  audit.py       │
                    │  log_action()   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ audit_log.db    │
                    │   (SQLite)      │
                    └─────────────────┘
\```

## Role model

| Role | Groups |
|---|---|
| Standard Employee | Standard-Employee |
| Manager | Standard-Employee, Manager |
| IT Admin | Standard-Employee, IT-Admin |

Manager and IT Admin are additive on top of Standard Employee — this reflects least-privilege design, where elevated roles build on the baseline rather than being siloed.

## Setup

1. Sign up for a free Okta Developer Edition org at developer.okta.com (choose **Okta Platform**, not Auth0).
2. Generate an API token in the Okta Admin Console under Security → API → Tokens.
3. Create a `.env` file:
   \```
   OKTA_ORG_URL=https://your-org.okta.com
   OKTA_API_TOKEN=your_token_here
   \```
4. Install dependencies:
   \```
   pip install -r requirements.txt
   \```
5. Create the audit database:
   \```
   python create_db.py
   \```

## Running it

\```
python provision_user.py    # joiner
python move_user.py         # mover
python remove_user.py       # leaver
\```

## Testing

\```
pytest -v
\```

9 tests covering role-mapping logic, audit log writes, and mocked API success/failure handling.

## What I'd build next

- A CLI so the roles/emails aren't hardcoded per script
- PostgreSQL instead of SQLite for a more enterprise-realistic audit store
- Docker packaging for one-command setup