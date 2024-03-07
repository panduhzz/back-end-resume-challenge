import azure.functions as func
import logging
import os

from azure.data.tables import TableServiceClient,TableClient

from typing import Any, Dict

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

visitorCount = 0

# Reference
# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/container_management.py#L231
def read_DB():
    from azure.core.exceptions import ResourceExistsError
    #not sure if I need these????
    # endpoint = "https://panduhzresume-db.table.cosmos.azure.com:443/"
    # key = "ptBxKVEGkbIRIBQphiUzERVwyUvXrZMjRc5N2xE6dBGIxhUleKS5E6ShvGzrYOwVU3785RJOjdP2ACDb7UEtlA=="

    # setting Table name as variable
    # tableName = "azurerm"

    # creating an entity to insert if entity does not exist
    entity1: Dict[str, Any] = {
        "PartitionKey" : "pk",
        "RowKey" : "counter",
        "count" : visitorCount,
    }
    connectionString = os.getenv('CosmosConnectionString')
    # initializing tableclient from tableserviceclient
    with TableClient.from_connection_string(conn_str=connectionString
                                                      ,table_name = "azurerm") as table_client:
        try: 
            table_client.create_table()
        except ResourceExistsError:
            logging.info("Table already exists")    
        # Trying to create the entity, if exists update the entity
        try:
            table_client.create_entity(entity=entity1)
        except ResourceExistsError:
            table_client.update_entity(entity=entity1) 
        
            


@app.route(route="http_trigger", auth_level=func.AuthLevel.FUNCTION)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    global visitorCount
    visitorCount += 1
    logging.info(visitorCount)
    read_DB()

    return func.HttpResponse(f"Count recorded")


    

"""
This returns something on the website

return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
"""   
  