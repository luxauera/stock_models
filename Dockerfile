FROM python:3.10-bookworm

WORKDIR /financial_models

COPY . . 


ENV  DB_NAME=hcap
ENV  DB_USER=postgres
ENV  DB_PASSWORD=mysecretpassword
ENV  DB_PORT=5432
ENV  DB_HOST=172.17.0.1
ENV  RUN_PERIOD=1800

RUN pip install -r requirements.txt

CMD ["python","-u","app.py"]