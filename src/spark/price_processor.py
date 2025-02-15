from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
import os

def create_spark_session():
    return SparkSession.builder \
        .appName("CryptoPriceProcessor") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,"
                "org.postgresql:postgresql:42.2.18") \
        .config("spark.driver.extraClassPath", "/opt/bitnami/spark/jars/postgresql-42.2.18.jar") \
        .getOrCreate()

def define_schema():
    return StructType([
        StructField("product_id", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("time", StringType(), True),
        StructField("timestamp", TimestampType(), True)
    ])

def process_stream():
    spark = create_spark_session()
    
    # Kafka에서 스트림 데이터 읽기
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "crypto-prices") \
        .load()

    # JSON 파싱 및 스키마 적용
    schema = define_schema()
    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    # time 컬럼을 timestamp로 변환
    parsed_df = parsed_df.withColumn("time", to_timestamp("time"))

    # PostgreSQL에 데이터 저장
    def write_to_postgres(df, epoch_id):
        df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://timescaledb:5432/crypto_db?ssl=true&sslmode=verify-full") \
            .option("dbtable", "crypto_prices") \
            .option("user", "crypto_user") \
            .option("password", "crypto_password") \
            .option("ssl", "true") \
            .option("sslmode", "verify-full") \
            .option("sslrootcert", "/root/.postgresql/root.crt") \
            .mode("append") \
            .save()

    # 스트리밍 쿼리 시작
    query = parsed_df.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("append") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    process_stream() 