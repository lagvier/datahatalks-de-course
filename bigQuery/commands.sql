-- BigQuery Warehousing

select * from data-engineering-akl.parquettables.greens limit 10;

select distinct PULocationID from data-engineering-akl.parquettables.greens;

select DISTINCT PULocationID from data-engineering-akl.parquettables.greens
  where CAST(TIMESTAMP_SECONDS(CAST(lpep_pickup_datetime/1000000000 AS INT64) ) AS DATE)
    BETWEEN CAST("2022-06-01" AS DATE) and CAST("2022-06-30" AS DATE);

select DISTINCT PULocationID from data-engineering-akl.parquettables.partitioned_table
  where CAST(TIMESTAMP_SECONDS(CAST(lpep_pickup_datetime/1000000000 AS INT64) ) AS DATE)
    BETWEEN CAST("2022-06-01" AS DATE) and CAST("2022-06-30" AS DATE);
