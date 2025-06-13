import json
import os
import requests
import boto3 # type: ignore
from botocore.exceptions import ClientError


lambda_client = boto3.client('lambda')

def lambda_async_invoker(function_name, payload):
    """
    Asynchronously invokes another Lambda function with the event body as payload.
    Args:
        function_name (str)
        payload (str)
    """
    try:
        lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="Event",
            Payload=payload,
        )
    except ClientError as e:
        print(e)


def lambda_handler(event, context):
    print(f"Event received: {event}")
    try:
        ip = requests.get("http://checkip.amazonaws.com/") 
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print(e)

    lambda_async_invoker(os.environ.get("DOWNSTREAM_FUNCTION_NAME"), json.dumps(event.get("Body")))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "location": ip.text.replace("\n", "")
        }),
    }
