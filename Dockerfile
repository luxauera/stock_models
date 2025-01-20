FROM python:3.10-bookworm

WORKDIR /financial_models

COPY . . 


ENV  DB_NAME=hcap
ENV  DB_USER=hyenauser
ENV  DB_PASSWORD=hyena_admin
ENV  DB_PORT=5432
ENV  DB_HOST=172.17.0.1
ENV  RUN_PERIOD=17:00

RUN pip install -r requirements.txt

CMD ["python","-u","app.py"]

