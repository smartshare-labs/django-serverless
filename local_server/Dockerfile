FROM python:3.7

WORKDIR /workspace

COPY ./local_server/requirements.txt /workspace/requirements.txt

RUN pip install -r requirements.txt

CMD python app.py