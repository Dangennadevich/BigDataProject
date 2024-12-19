from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from onetl.connection import SparkHDFS
from onetl.file import FileDFReader
from onetl.db import DBWriter
from onetl.connection import Hive
from onetl.file.format import CSV, Parquet

spark = SparkSession.builder \
    .master('yarn') \
    .appName('spark-with-yarn') \
    .config("spark.sql.hive.metastore.version", "3.1.2") \
    .config("spark.sql.hive.metastore.jars", "maven") \
    .config('spark.sql.warehouse.dir', '/user/hive/warehouse') \
    .config('spark.hive.metastore.uris', 'thrift://team-18-jn:9083') \
    .config("spark.logLevel", "DEBUG") \
    .enableHiveSupport() \
    .getOrCreate()

hdfs = SparkHDFS(host="team-18-nn", port=9000, spark=spark, cluster="test") # cluster project?
hdfs.check()

reader = FileDFReader(connection=hdfs, format=CSV(delimiter=";", header=True), source_path="/input")
df = reader.run(["customers-2000000.csv"])
df.show(5, 0)
print(df.count())
print(df.rdd.getNumPartitions())
df.write.mode("overwrite").parquet("/input/customers_data")

import subprocess
result = subprocess.run(["hadoop", "fs", "-ls", "/input/customers_data"], capture_output=True, text=True)
print(result.stdout)

reader = FileDFReader(connection=hdfs, format=Parquet(), source_path="/input/customers_data")
df = reader.run()
df_final = (
    df
    .withColumnRenamed('4962fdbE6Bfee6D', 'hash')
    .withColumnRenamed('Pam', 'name')
    .withColumnRenamed('Sparks', 'surname')
    .withColumnRenamed('Patel-Deleon', 'company')
    .withColumnRenamed('Blakemouth', 'location')
    .withColumnRenamed('British Indian Ocean Territory (Chagos Archipelago)', 'country')
    .withColumnRenamed('267-243-9490x035', 'fax1')
    .withColumnRenamed('480-078-0535x889', 'fax2')
    .withColumnRenamed('nicolas00@faulkner-kramer.com', 'email')
    .withColumnRenamed('2020-11-29', 'date')
    .withColumnRenamed('https://nelson.com/', 'link')
    .withColumnRenamed('98891.41', 'value')
    .withColumn('business_month', F.to_date(F.date_trunc('month', F.col('date'))))
    .groupBy('company', 'business_month')
    .agg(
        F.round(F.sum('value'), 2).alias('total_value'),
        F.round(F.avg('value'), 2).alias('avg_value'),
        F.round(F.min('value'), 2).alias('min_value'),
        F.round(F.max('value'), 2).alias('max_value'),
        F.max('date').alias('last_date')
    )
    .orderBy('company', 'business_month')
)

target_table = 'project.final_agg_datamart'
(
    df_final
    .repartition(1)
    .write
    .format('orc')
    .mode('overwrite')
    .partitionBy('business_month')
    .saveAsTable(target_table)
)

rows_cnt = str(spark.table(target_table).count())
print(f'Table {target_table} is repartitioned and saved successfully! Number of rows: {rows_cnt}')

spark.stop()
