import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "testdb", table_name = "table1", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "testdb", table_name = "table1", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("year", "long", "year", "long"), ("quarter", "long", "quarter", "long"), ("month", "long", "month", "long"), ("day_of_month", "long", "day_of_month", "long"), ("mon", "long", "mon", "long")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("year", "long", "year", "long"), ("quarter", "long", "quarter", "long"), ("month", "long", "month", "long"), ("day_of_month", "long", "day_of_month", "long"), ("mon", "long", "mon", "long")], transformation_ctx = "applymapping1")
## @type: SelectFields
## @args: [paths = ["year", "quarter", "month", "day_of_month"], transformation_ctx = "selectfields2"]
## @return: selectfields2
## @inputs: [frame = applymapping1]
selectfields2 = SelectFields.apply(frame = applymapping1, paths = ["year", "quarter", "month", "day_of_month"], transformation_ctx = "selectfields2")
## @type: ResolveChoice
## @args: [choice = "MATCH_CATALOG", database = "testdb", table_name = "table1", transformation_ctx = "resolvechoice3"]
## @return: resolvechoice3
## @inputs: [frame = selectfields2]
resolvechoice3 = ResolveChoice.apply(frame = selectfields2, choice = "MATCH_CATALOG", database = "testdb", table_name = "table1", transformation_ctx = "resolvechoice3")
## @type: DataSink
## @args: [database = "testdb", table_name = "table1", transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = resolvechoice3]
datasink4 = glueContext.write_dynamic_frame.from_catalog(frame = resolvechoice3, database = "testdb", table_name = "table1", transformation_ctx = "datasink4")
job.commit()