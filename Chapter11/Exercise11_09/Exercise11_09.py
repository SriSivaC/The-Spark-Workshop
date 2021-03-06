from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import col
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Create a Spark Session
spark = SparkSession \
    .builder \
    .appName("My Spark App") \
    .master("local[2]") \
    .getOrCreate()

# create spark contexts
sc = spark.sparkContext

my_previous_pets = [Row("fido", "dog", 4, "brown"),
                    Row("annabelle", "cat", 15, "white"),
                    Row("fred", "bear", 29, "brown"),
                    Row("daisy", "cat", 8, "black"),
                    Row("jerry", "cat", 1, "white"),
                    Row("fred", "parrot", 1, "brown"),
                    Row("gus", "fish", 1, "gold"),
                    Row("gus", "dog", 11, "black"),
                    Row("daisy", "iguana", 2, "green"),
                    Row("rufus", "dog", 10, "gold")]

# create RDDs
petsRDD = sc.parallelize(my_previous_pets)

# create data frames
petsDF = spark.createDataFrame(petsRDD, ['nickname', 'type', 'age', 'color'])
petsDF.registerTempTable('pets')

# option 1: pure sql
spark.sql("select type, "
          "sum(age) as total_age "
          "from pets "
          "group by type "
          "having total_age > 10 "
          "order by total_age desc").show()

# option 2: functional
petsDF.groupBy("type")\
    .sum("age")\
    .withColumnRenamed("sum(age)", "total_age")\
    .where("total_age > 10")\
    .orderBy(col("total_age").desc())\
    .show()

