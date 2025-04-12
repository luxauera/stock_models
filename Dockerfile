FROM python:3.10-bookworm

WORKDIR /financial_models

COPY . . 


ENV  DB_NAME=
ENV  DB_USER=
ENV  DB_PASSWORD=
ENV  DB_PORT=
ENV  DB_HOST=
ENV  RUN_PERIOD= 
#RUN_PERIOD=17:10

RUN pip install -r requirements.txt

CMD ["python","-u","app.py"]

