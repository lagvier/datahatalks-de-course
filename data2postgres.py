#!/usr/bin/env python
# coding: utf-8

import os
from sys import platform
import argparse
import pandas as pd #pd.__version__
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # download file
    output_name =  url.split('/')[-1]
    # o1 = "green_tripdata_2019-01.csv.gz"
    if platform[0].lower() == "l": # linux: linux, linux2
        os.system(f'wget {url} -O {output_name}') 
    elif platform[0].lower() == "w": # windows: wind32
        os.system(f'curl {url}') 
    # elif platform[0].lower()  == "w": # OS X:  darwin
    

    # connect database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Work on the data in chunks
    df_iter = pd.read_csv(output_name, compression='gzip', iterator=True, chunksize = 100000)
    df = next(df_iter) # get next chunk
    df.lpep_pickup_datetime=pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime=pd.to_datetime(df.lpep_dropoff_datetime)

    # create the data model in the database
    df.head(n=0).to_sql(name= table_name, con = engine, if_exists='replace') # create the data model

    while True:
        df = next(df_iter) # get next chunk
        
        df.lpep_pickup_datetime=pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime=pd.to_datetime(df.lpep_dropoff_datetime)
        
        df.to_sql(name= table_name, con = engine, if_exists='append') # insert the next chunk


if __name__ == '__main__':

    # argparse arguments
    parser = argparse.ArgumentParser(description='Ingest data model and description into postgres.')

    # arguments: host, user, password
    parser.add_argument('--host', help='host')
    parser.add_argument('--port', help='port')
    parser.add_argument('--user', help='user')
    parser.add_argument('--password', help='password')
    parser.add_argument('--db', help='database')
    parser.add_argument('--table_name', help='table in the database')
    parser.add_argument('--url', help='File location online')
    
    args = parser.parse_args()
    main(args)