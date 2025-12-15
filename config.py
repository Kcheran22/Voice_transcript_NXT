import os
import json

import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()


AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET = os.getenv('S3_BUCKET')
 
def aws_connection(aws_service:str):
    """
    Connection Microservice to the Boto3 client 'EMR' Service

    Returns:
        client : boto3.client object.
    """
    client = boto3.client(aws_service,region_name='us-west-2')
    return client

def dev_get_secret():
    """
        Obtain OpenAI API Key from AWS Secrets Manager.

        Returns:
            open_api_key (str): The API key necessary to use OpenAI LLM Models.
    """


    secret_name = "advance_analytics/dev_geninsights"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handle exceptions appropriately
        raise e

    # Parse the JSON string and extract the value associated with "open_api_key"
    secret_string = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret_string)
    
    # Extract the value for "open_api_key"
    openai_api_key = secret_dict.get('open_api_key')

    if openai_api_key is None:
        # Handle the case where the key is not present
        raise ValueError("The 'open_api_key' is not present in the secret.")

    return openai_api_key

