from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from onetl.connection import SparkHDFS
from onetl.file import FileDFReader
from onetl.file.format import CSV, Parquet
from prefect import flow, task


@task(cache_policy=None)
def create_session():
    print('Initializing SPARK session...')
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
    print('Success!')

    return spark


@task(cache_policy=None)
def extract_data(spark):
    print('Extracting data...')
    hdfs = SparkHDFS(host="team-18-nn", port=9000, spark=spark, cluster="test")
    hdfs.check()
    reader = FileDFReader(connection=hdfs, format=CSV(delimiter=";", header=True), source_path="/input")
    df = reader.run(["customers-2000000.csv"])
    print('Success!')

    return df


@task(cache_policy=None)
def transform_data(df):
    print('Transforming data...')
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
        .groupBy('business_month')
        .agg(
            F.round(F.sum('value'), 2).alias('total_value'),
            F.round(F.avg('value'), 2).alias('avg_value'),
            F.round(F.min('value'), 2).alias('min_value'),
            F.round(F.max('value'), 2).alias('max_value')
        )
        .orderBy('business_month')
    )
    print('Success!')

    return df_final


@task(cache_policy=None)
def load_data(spark, df):
    print('Saving data as table...')
    target_table = 'project.final_agg_datamart_automated'
    (
        df
        .repartition(1)
        .write
        .format('orc')
        .mode('overwrite')
        .partitionBy('business_month')
        .saveAsTable(target_table)
    )
    print('Success!')
    spark.stop()
    print('Spark session is stopped.')


@flow(name="ETL flow")
def etl_process():
    spark_session = create_session()
    df = extract_data(spark_session)
    transformed_df = transform_data(df)
    load_data(spark_session, transformed_df)


if __name__ == "__main__":
    etl_process()
