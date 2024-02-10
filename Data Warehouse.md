# BigQuery Warehousing:
```
--- Create an external table from list of files in google storage

CREATE OR REPLACE TABLE 'rides.table1'
OPTIONS (
    format = 'CSV',
    uris = ['gs://nyc_bikes/trips_data/nyc_greens_2019*.csv'], ['gs://nyc_bikes/trips_data/nyc_greens_2020*.csv']
    );


--- Query the created table
SELECT * FROM rides.table1 LIMIT 3;

--- Create subset of tables from the created table
CREATE OR REPLACE TABLE rides.table_backup AS 
    SELECT * FROM rides.table1; 

--- Partitioning data: Reduces space during processing
CREATE OR REPLACE TABLE rides.table_partitioned
    PARTITIONED BY DATE(lp_pickup_date) AS 
    SELECT * FROM rides.table1; 


--- Check information per pertition
SELECT table_name, partition_id, total_rows
    FROM 'rides.INFORMATION_SCHEMA.PARTITIONS'
    WHERE table_name = 'table_partitioned'
    ORDER BY total_rows DESC;

--- Clustering (Sorting by): Further reduces space during processing
CREATE OR REPLACE TABLE rides.table_partitioned_clustered
    PARTITIONED BY DATE(lp_pickup_date) 
    CLUSTER BY Type AS 
    SELECT * FROM rides.table1; 

```

Notes
- BigQuery has a limit of 4000 partitions and a maximum of 4 columns to cluster. 
- Types of columns to cluster: Date, Bool, Geography, Int64, Numeric,BigNumeric, String, Timestamp, Datatime.
- Place largest table as first, then second with the smallest and then the remaining in the descending ordering after.
- Partition by columns used for filtering/aggregate
- Cluster by the columns used for sorting


### BigQuery for ML
```
--- CREATE A LR Machine Learning Model
CREATE OR REPLACE MODEL 'rides.lr_model'
    OPTIONS (
            MODEL_TYPE='LINEAR_REG',
            INPUT_LABEL_COLS=['price'],
            DATA_SPLIT_METHOD='AUTO_SPLIT'
        ) AS
        SELECT * FROM rides.table_partitioned_clustered
            WHERE tip_amount IS NOT NULL;


--- Check features of the model
SELECT * FROM ML.FEATURE_INFO(MODEL 'rides.lr_model');

--- Evaluate model
SELECT * FROM 
    ML.EVALUATE(MODEL 'rides.lr_model',  
                (SELECT * FROM 'rides.table_partitioned_clustered' WHERE WHERE tip_amount IS NOT NUL)
    );


--- Predict model
SELECT * FROM ML.PREDICT(MODEL 'rides.lr_model', 
                        (SELECT * FROM 'rides.table_partitioned_clustered' WHERE WHERE tip_amount IS NOT NUL)    
    );

--- Predict and Explain model
SELECT * FROM ML.EXPLAIN_PREDICT(MODEL 'rides.lr_model', 
                                (SELECT * FROM 'rides.table_partitioned_clustered' WHERE WHERE tip_amount IS NOT NUL),
                                STRUCT(3 AS top_k_features)   
    );


--- Hyper-Parameter Tuning
CREATE OR REPLACE MODEL 'rides.lr_model_hypertune'
    OPTIONS (
            MODEL_TYPE='LINEAR_REG',
            INPUT_LABEL_COLS=['price'],
            DATA_SPLIT_METHOD='AUTO_SPLIT',
            NUM_TRIALS=5,
            MAX_PARALLEL_TRIALS = 2,
            L1_REG=hparam_range(0, 20),
            L2_REG=hparam_candidates([0, 0.1, 1, 10])
        ) AS
        SELECT * FROM rides.table_partitioned_clustered
            WHERE tip_amount IS NOT NULL;
```

### Export model and use docker
Run the command below in your terminal
```
bq --project_id=<project_id> extract -m rides.lr_model_hypertune gs://nyc_bikes/rides/lr_model_hypertune
mkdir /tmp/model 
gsutil cp -r gs://nyc_bikes/rides/lr_model_hypertune /tmp/model
mkdir -p server_dir/lr_model_hypertune/1
cp -r /tmp/model/lr_model_hypertune* /server_dir/model/1
docker pull tensorflow/serving
docker run -p 8501:8501 --mount type=bind, source=`pwd`/server_dir/lr_model_hypertune target=/models/lr_model_hypertune -e MODEL_NAME=price_model -t tensorflow/serving &

-- You can use post master to test the predict API for url: http://localhost:8501/v1/models/lr_model_hypertune:predict and type a json data format like: {"instances": [{"passenger_count":1, "trip_distances":10}]}
```