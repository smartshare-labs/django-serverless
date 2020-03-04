### threads backend

---

### Usage

- Get setup: `make init`

- Run local API (binds to _localhost:5000_): `make start`

- Reset local database (completely): `make reset`

- Dump local database (data not structure): `make flush`

- Dump production database (data not structure): `make flush-live`

- Generate new migrations after changing a model: `make migrations`

- Running migrations locally: `make migrate`

- Running migrations in production: `make migrate-live`

- Deploy to lambda in dev: `make deploy-dev`

- Deploy to lambda in prod: `make deploy-prod`

---

### Running endpoint code directly

Run `python -m functions.functionName.handler`

---

### Testing (WIP)

Write your tests in the `./tests` folder. Then:

1. Create a virtual environment in `./tests`: `virtualenv -p python3 venv`
2. Source it: `source venv/bin/activate`
3. Install requirements: `pip install -U requirements.txt`

Finally, to run tests: `python -m pytest tests` from the root directory.
