from pyspark.sql import DataFrame

class DatabaseManager:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def write_to_db(self, df, table_name, mode="append"):
        df.write.format('jdbc').options(
            url=self.url,
            driver='org.postgresql.Driver',
            dbtable=table_name,
            user=self.user,
            password=self.password).mode(mode).save()

