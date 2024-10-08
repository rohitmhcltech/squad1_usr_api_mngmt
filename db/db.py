from azure.cosmos import CosmosClient, exceptions
import os
from dotenv import load_dotenv
load_dotenv()

# Cosmos DB configuration
URL = os.environ.get("COSMOS_DB_URL")
KEY = os.environ.get("COSMOS_DB_KEY")
client = CosmosClient(URL, KEY)
database = client.get_database_client(os.environ.get("COSMOS_DATABASE_NAME"))
container = database.get_container_client(os.environ.get("COSMOS_CONTAINER_NAME"))

def get_user_by_email(email: str):
    query = f"SELECT * FROM c WHERE c.email = '{email}'"
    return list(container.query_items(query=query, enable_cross_partition_query=True))

def create_user_document(user_document):
    print(user_document)
    try:
        container.create_item(user_document)
    except exceptions.CosmosHttpResponseError as e:
        raise e

