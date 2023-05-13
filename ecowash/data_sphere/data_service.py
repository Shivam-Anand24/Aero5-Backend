from pyspark.sql import SparkSession

class DataService:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName('Data Service') \
            .config('spark.executor.memory', '1g') \
            .config('spark.driver.memory', '1g') \
            .getOrCreate()

    def read_data(self, table_name):
        url = 'jdbc:postgresql://localhost:5432/aero'
        user = 'postgres'
        pwd = 'postgres'

        df = self.spark.read.format('jdbc') \
            .option('url', url) \
            .option('dbtable', table_name) \
            .option('user', user) \
            .option('password', pwd) \
            .option('driver', 'org.postgresql.Driver') \
            .load()

        return df