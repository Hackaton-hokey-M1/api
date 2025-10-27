Hockey API (minimal)
=====================

deployed on: http://apihockey-api.francecentral.azurecontainer.io:8000

Documentation (Swagger): http://apihockey-api.francecentral.azurecontainer.io:8000/docs

Quick start (local)
-------------------

1. Create and activate the venv, then install dependencies:

```bash
make install
```

2. Run the server locally:

```bash
uvicorn main:app --reload
```

3. Open the interactive docs (local): http://127.0.0.1:8000/docs

Available GET endpoints
- `GET /teams`
- `GET /teams/{id}`
- `GET /tournaments`
- `GET /tournaments/{id}`
- `GET /matches`
- `GET /matches/{id}`
- `GET /tournaments/{id}/matches`

Examples
--------

List teams (deployed):

```bash
curl http://apihockey-api.francecentral.azurecontainer.io:8000/teams
```

List matches (deployed):

```bash
curl http://apihockey-api.francecentral.azurecontainer.io:8000/matches
```

Notes
-----
- The DB file is `dev.db` in the project root (ignored by git).
- The project seeds fake data at startup using Faker.
