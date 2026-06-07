from pyspark import pipelines as dp
from pyspark.sql.functions import col, to_timestamp


@dp.table(name="clickstream_bronze")
def clickstream_bronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/Volumes/source/clickstream")
    )


@dp.table(name="clickstream_silver")
@dp.expect_or_drop("valid_event_id", "event_id IS NOT NULL")
@dp.expect_or_drop("known_event", "event_name IN ('page_view', 'add_to_cart', 'checkout', 'purchase')")
def clickstream_silver():
    return (
        spark.readStream.table("clickstream_bronze")
        .withColumn("event_timestamp", to_timestamp(col("event_timestamp")))
        .select(
            "event_id",
            "anonymous_id",
            "customer_id",
            "session_id",
            "event_name",
            "event_timestamp",
            "market",
            "device_type",
        )
    )

