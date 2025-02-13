from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, col


class WeatherAnalysis:
    def __init__(self, file_path):
        self.spark = SparkSession.builder \
            .appName("WeatherAnalysis") \
            .master("spark://spark-master:7077") \
            .getOrCreate()
        self.file_path = file_path
        self.weather_df = None

    def load_data(self):
        try:
            print("Reading weather data from:", self.file_path)
            self.weather_df = self.spark.read.csv(self.file_path, header=True, inferSchema=True)
            self.weather_df.show()
            if self.weather_df.count() == 0:
                print("The weather dataset is empty. Exiting application.")
                return False
            return True
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            return False

    def compute_avg_weather(self):
        try:
            avg_weather = self.weather_df.groupBy("City").agg(
                avg("Temperature").alias("AvgTemperature"),
                avg("Humidity").alias("AvgHumidity")
            )
            print("Average Temperature and Humidity by City:")
            avg_weather.show()
            output_path = "hdfs://namenode:9000/output/avg_weather"
            avg_weather.write.mode("overwrite").csv(output_path, header=True)
        except Exception as e:
            print(f"An error occurred while computing average weather: {e}")

    def find_max_wind_speed(self):
        try:
            max_wind_speed = self.weather_df.select(max("WindSpeed").alias("MaxWindSpeed")).collect()[0]["MaxWindSpeed"]
            city_with_max_wind = self.weather_df.filter(
                col("WindSpeed") == max_wind_speed
            ).select("City", "Date", "WindSpeed")
            print(f"City with Maximum Wind Speed ({max_wind_speed}):")
            city_with_max_wind.show()
            output_path = "hdfs://namenode:9000/output/max_wind"
            city_with_max_wind.write.mode("overwrite").csv(output_path, header=True)
        except Exception as e:
            print(f"An error occurred while finding max wind speed: {e}")

    def count_extreme_conditions(self):
        try:
            extreme_conditions = self.weather_df.filter(
                (col("Temperature") < 0) | (col("WindSpeed") > 15)
            )
            extreme_days_count = extreme_conditions.count()
            print(f"Number of days with extreme weather conditions: {extreme_days_count}")
            output_path = "hdfs://namenode:9000/output/extreme_conditions"
            extreme_conditions.write.mode("overwrite").csv(output_path, header=True)
        except Exception as e:
            print(f"An error occurred while counting extreme conditions: {e}")

    def run_analysis(self):
        if self.load_data():
            self.compute_avg_weather()
            self.find_max_wind_speed()
            self.count_extreme_conditions()
        self.spark.stop()
        print("Spark session stopped.")


# Usage
if __name__ == "__main__":
    file_path = "hdfs://namenode:9000/input/large_weather.csv"
    weather_analysis = WeatherAnalysis(file_path)
    weather_analysis.run_analysis()
