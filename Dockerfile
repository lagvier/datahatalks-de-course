FROM python:3.9.1

RUN apt-get install wget
RUN pip install Pyarrow pandas sqlalchemy psycopg2

WORKDIR /app
COPY data2postgres.py data2postgres.py

ENTRYPOINT ["python", "data2postgres.py"]