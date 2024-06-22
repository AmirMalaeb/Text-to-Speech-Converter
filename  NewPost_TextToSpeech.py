import boto3
import os
import uuid

def lambda_handler(event, context):
    record_id = str(uuid.uuid4())
    voice = event["voice"]
    text = event["text"]

    print(f'Generating new DynamoDB record, with ID: {record_id}')
    print(f'Input Text: {text}')
    print(f'Selected voice: {voice}')
    
    # Creating new record in DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    table.put_item(
        Item={
            'id': record_id,
            'text': text,
            'voice': voice,
            'status': 'PROCESSING'
        }
    )
    
    # Sending notification about new post to SNS
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn=os.environ['SNS_TOPIC'],
        Message=record_id
    )
    
    return record_id