import json
import os
import requests
import boto3 # type: ignore
from botocore.exceptions import ClientError

sns_client = boto3.client('sns')
s3_client = boto3.client('s3')

def sns_publisher():
    """
    Publishes a message to an SNS topic.
    """
    try:
        sns_client.publish(
            TopicArn=os.environ.get("SNS_TOPIC_ARN"),
            Message="Check bucket!",
            Subject="Hello from Downstream Lambda"
        )
    except ClientError as e:
        print(e)

def s3_uploader(body):
    """
    Uploads a file to S3.
    """
    try:
        s3_client.put_object(
            Body=body,
            Bucket=os.environ.get("BUCKET_NAME"),
            Key="cat.jpg",
        )
    except ClientError as e:
        print(e)

def lambda_handler(event, context):
    try:
        response = requests.get("https://cataas.com/cat")
        s3_uploader(response.content)
        sns_publisher()
    except requests.RequestException as e:
        print(e)
