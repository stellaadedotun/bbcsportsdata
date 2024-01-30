from scrape import *
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
from azure.storage.blob import (BlobServiceClient, BlobClient, ContainerClient)

from dotenv import load_dotenv
import os
load_dotenv()

storage_account_key: str = os.getenv('STORAGE_ACCOUNT_KEY')
storage_account_name = 'ctostorage123'
connection_string='DefaultEndpointsProtocol=https;AccountName=ctostorage123;AccountKey=VV9n7k7aoaa76iDTwWvgRiBug3NDSYUWfj+smLPa9R4wZmSHdd2zT7dHf7PckDfbZM+VtAIu+WqJ+AStfi0REw==;EndpointSuffix=core.windows.net'
container_name = 'bbcsportsmastercopy'

functions = [league_table,top_scorers,detail_top,player_table,all_time_table,all_time_winner_club,top_scorers_seasons,goals_per_season]

def to_blob(func: functions) -> functions:

    '''
    Converts the output of a given function to Parquet format and uploads it to Azure Blob Storage.
    Args:
        func (function): The function that retrieves data to be processed and uploaded.
        Consider the function "top_scorers". Calling "to_blob(top_scorers)" will process the output
        of "top_scorers", convert it to Parquet format, and upload it to Azure Blob Storage.
        '''

    file_name = func.__name__
    func = func()


    # Convert DataFrame to Arrow Table
    table = pa.Table.from_pandas(func)

    parquet_buffer = BytesIO()
    pq.write_table(table, parquet_buffer)


    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    blob_name = f"{file_name}.parquet"
    container_client = blob_service_client.get_container_client(container_name)

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(parquet_buffer.getvalue(), overwrite=True)
    print(f"{blob_name} successfully updated")


for items in functions:
    to_blob(items)
