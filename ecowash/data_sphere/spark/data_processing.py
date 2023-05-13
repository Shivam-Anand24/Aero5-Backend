from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from io import StringIO
from .DatabaseManager import DatabaseManager
from pyspark.sql import SparkSession
from io import StringIO
import pandas as pd



def process_csv(file_path, key):
    # Process the DataFrame based on the key
    if key == 'fabrication':
        # Process fabrication data
        print('@@@@@@@@@@@@@       ', file_path)
        process_febrication_csv(file_path)
    elif key == 'sub_assembly':
        # Process sub_assembly data
        process_sub_assembly_csv(file_path)
    elif key == 'assembly':
        # Process assembly data
        process_assembly_csv(file_path)
    else:
        return False
    
    # Return True to indicate successful processing
    return True

# Remove columns with all null values
def drop_null_columns(df):
    for column in df.columns:
        null_count = df.filter(df[column].isNull()).count()
        if null_count == df.count():
            df = df.drop(column)
    return df

def process_csv_data(csv_content):
    spark = SparkSession.builder.getOrCreate()

#    # Convert CSV content to Pandas DataFrame
#     csv_data = StringIO(csv_content)
#     pandas_df = pd.read_csv(csv_data)

#     # Create Spark DataFrame from Pandas DataFrame
#     df = spark.createDataFrame(pandas_df)
    # pandas_df = pd.read_csv(StringIO(csv_content))
    # rdd = spark.sparkContext.parallelize(pandas_df.values.tolist())
    df = spark.read.csv(csv_content, header=True, inferSchema=True)
    # df = spark.createDataFrame(rdd, pandas_df.columns.tolist())
    print('------------------------------', df.show(5))
    # Drop duplicates and drop columns with all null values
    df = df.dropDuplicates().na.drop("all")

    

    df = drop_null_columns(df)

    #remove null values rows
    df = df.dropna()

    return df

def process_febrication_csv(csv_content):
    print('@@@  csv_content  @@@', csv_content)
    fabrication_df = process_csv_data(csv_content)

    # Create a DataFrame with distinct combinations of item, raw_material, and quantity
    item_category_df = fabrication_df.select('item', 'raw material', 'Quantity').distinct()

    # Add an ID column to item_category_df
    item_category_df = item_category_df.withColumn('id', monotonically_increasing_id())

    # Rename the columns to match the item_category schema
    item_category_df = item_category_df.select(
        'id',
        item_category_df['item'].alias('name'),
        item_category_df['raw material'].alias('raw_material'),
        item_category_df['Quantity'].alias('quantity_needed')
    )

    # Display the DataFrame
    item_category_df.show(3)


    # Join fabrication_df with item_category_df to create the new fabrication table
    new_fabrication_df = fabrication_df.join(item_category_df, 
                                            (fabrication_df['item'] == item_category_df['name']) & 
                                            (fabrication_df['raw material'] == item_category_df['raw_material']) &
                                            (fabrication_df['Quantity'] == item_category_df['quantity_needed']),
                                            how='left')

    # Select necessary columns and rename them to match the new fabrication schema
    new_fabrication_df = new_fabrication_df.select(
        fabrication_df['item id'].alias('item_id'),
        item_category_df['id'].alias('item_category_id'),
        fabrication_df['in date'].alias('in_date'),
        fabrication_df['out date'].alias('out_date')
    )
    new_fabrication_df.show(3)
    print('saving to database..... febrication, item_category')
    save_to_data_base(item_category_df, "item_category")
    save_to_data_base(new_fabrication_df, "fabrication")
    print('saved to database..... febrication, item_category')


# def process_sub_assembly_csv(csv_content):
#     sub_assembly_df = process_csv_data(csv_content)

#     # Transform sub_assembly_df
#     new_sub_assembly_df = sub_assembly_df.select(
#         sub_assembly_df['sub assembly id'].alias('sub_assembly_id'),
#         sub_assembly_df['sub assembly name'].alias('name'),
#         sub_assembly_df['sub assembly description'].alias('description'),
#         sub_assembly_df['sub assembly cost'].alias('cost')
#     )
#     new_sub_assembly_df.show(3)
#     print('saving to database..... sub_assembly')
#     save_to_data_base(new_sub_assembly_df, "sub_assembly")
#     print('saved to database..... sub_assembly')


def process_sub_assembly_csv(csv_content):
    sub_assembly_df = process_csv_data(csv_content)
    # Rename assembly.Process ID to aub_ass_process_id
    # sub_assembly_df = sub_assembly_df.withColumnRenamed('process', 'aub_ass_process_id')
    sub_assembly_df.show(3)
    # Create a DataFrame with distinct processes from sub_assembly
    process_df = sub_assembly_df.select('process').distinct()

    # Add an ID column to process_df
    process_df = process_df.withColumn('process_id', monotonically_increasing_id())
    # Rename the columns to match the process schema
    process_df = process_df.select(
        'process_id',
        process_df['process'].alias('process_name')
    )
    process_df.show(3)
    # Join sub_assembly_df with process_df to create the new sub_assembly table
    new_sub_assembly_df = sub_assembly_df.join(process_df, 
                                               sub_assembly_df['process'] == process_df['process_name'],
                                               how='left')

    # Select necessary columns and rename them to match the new sub_assembly schema
    new_sub_assembly_df = new_sub_assembly_df.select(
        sub_assembly_df['Assembly ID'].alias('assembly_id'),
        process_df['process_id'].alias('process_id'),
        sub_assembly_df['Item ID'].alias('item_id'),
        sub_assembly_df['Machine ID'].alias('machine_id'),
        sub_assembly_df['start date'].alias('start_date'),
        sub_assembly_df['end date'].alias('end_date')
    )

    print('saving to database..... process')
    save_to_data_base(process_df, "process")    
    print('saved to database..... process')
    # --------------------------------------------
    print('saving to database..... sub_assembly')
    save_to_data_base(new_sub_assembly_df, "sub_assembly")
    print('saved to database..... sub_assembly')
    return new_sub_assembly_df


def process_assembly_csv():
    assembly_df = process_csv_data(csv_content)
    assembly_df = drop_null_columns(assembly_df)
    # Rename assembly.Process ID to aub_ass_process_id
    assembly_df = assembly_df.withColumnRenamed('Process ID', 'aub_ass_process_id')

    # Create a DataFrame with distinct processes from assembly
    process_df = assembly_df.select('process').distinct()

    # Add an ID column to process_df
    process_df = process_df.withColumn('process_id', monotonically_increasing_id())

    # Join assembly_df with process_df to create the new assembly table
    new_assembly_df = assembly_df.join(process_df, 
                                       assembly_df['process'] == process_df['process'],
                                       how='left')

    # Select necessary columns and rename them to match the new assembly schema
    new_assembly_df = new_assembly_df.select(
        process_df['process_id'].alias('process_id'),
        assembly_df['aub_ass_process_id'].alias('aub_ass_process_id'),
        assembly_df['Machine ID'].alias('machine_id'),
        assembly_df['Start Date'].alias('start_date'),
        assembly_df['END DATE'].alias('end_date')
    )

    print('saving to database..... process')
    save_to_data_base(process_df, "process")    
    print('saved to database..... process')
    # --------------------------------------------
    print('saving to database..... assembly')
    save_to_data_base(new_assembly_df, "assembly")
    print('saved to database..... assembly')

    return new_assembly_df


def save_to_data_base(dataframe, tname):
    url = 'jdbc:postgresql://localhost:5432/aero'
    user = 'postgres'
    pwd = 'postgres'
    dbm = DatabaseManager(url,  user, pwd )
    dbm.write_to_db(dataframe, tname)

