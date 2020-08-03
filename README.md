# Django-Serverless Template

Designed for rapid development of serverless APIs.

### Pre-requisites

- Docker
- Python 3.7
- [serverless-cli](https://www.serverless.com/framework/docs/getting-started/)
- An [AWS profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) with valid credentials on your local machine

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

### Quickstart: creating an API

1. Create a new folder in `functions` with the name of your endpoint.
2. Add the new endpoint and HTTP method to `serverless.yaml`.
3. Update `./sls_django/settings.py` with the name of your new endpoint.
4. Write your business logic to a file in the `./logic` directory.
5. If creating a new model, duplicate one of the existing folders in `sls_django`, and rename with the name of your Entity.
6. Add Models or Serializers accordingly.
7. If you made changes to a model, run `make migrations` followed by `make migrate`. Then, you're ready to run your endpoint locally. Restart your local server, running `make start`.
8. Enjoy your endpoint, and proceed to develop subsequent APIs faster than ever.

### Running endpoint code directly

Run `python -m functions.functionName.handler`

### Testing (WIP)

Write your tests in the `./tests` folder. Then:

1. Create a virtual environment in `./tests`: `virtualenv -p python3 venv`
2. Source it: `source venv/bin/activate`
3. Install requirements: `pip install -U requirements.txt`

Finally, to run tests: `python -m pytest tests` from the root directory.
