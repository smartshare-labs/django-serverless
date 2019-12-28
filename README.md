### Serverless Lambda Template

This is the template we use when developing new serverless python code on AWS. It includes a number of basic but simple improvements to the standard `aws-python3` template that serverless offers out of the box:

- `./common`: Common configurations for improved readability in yml files
- `./local_server`: A dockerized flask application which is useful if you're building an API. This can be connected to our `local_mysql` container.
- `./modules`: Reusable, tested python code for common things such as database I/O.
- `./functions`: This is where your lambda handlers should go. We include an example of one function that calls into one of our modules.
- `./tests`: Pytest tests for testing modules in `./modules`
 
---

### Usage

To get started, you need to have serverless installed: `npm install -g serverless`

Then, to create a new project using our template, run:

`sls create --template-url https://github.com/smartshare-labs/aws-serverless-api-template --path NEW_PROJECT_PATH`

To deploy your code to lambda:

`sls deploy --stage dev`

or for production:

`sls deploy --stage prod`

Refer to the serverless documentation (https://serverless.com/framework/docs/) for more useful commands.

Note: A good rule of thumb when developing is to keep core application logic out of your lambda handlers. This is the pattern we try to employ with the `./modules` folder. Keeping your complexity in tested, reusable modules such as these allows for simple integration testing of the lambda handlers themselves.

---

### Using the local flask server

We assume you already have docker installed. From the `./local_server` folder, run `docker-compose up --build`. For each lambda handler that you want to expose in the local flask app, add a route in `./local_server/app.py` that forwards the appropriate event/context to your function. 

---

### Testing

Write your tests in the `./tests` folder. Then:

1. Create a virtual environment in `./tests`: `virtualenv -p python3 venv`
2. Source it: `source venv/bin/activate`
3. Install requirements: `pip install -U requirements.txt`

Finally, to run tests: `python -m pytest tests` from the root directory. 