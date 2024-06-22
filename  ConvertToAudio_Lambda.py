import boto3
import os
import json
from contextlib import closing
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    try:
        post_id = event["Records"][0]["Sns"]["Message"]
    except KeyError as e:
        print(f"KeyError: {e}")
        print(f"Event received: {event}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f"KeyError: {e}"})
        }
    
    print(f"Text to Speech function. Post ID in DynamoDB: {post_id}")
    
    # Retrieving information about the post from DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    post_item = table.query(
        KeyConditionExpression=Key('id').eq(post_id)
    )
    
    if not post_item["Items"]:
        print(f"No post found with ID {post_id}")
        return {
            'statusCode': 404,
            'body': json.dumps({'error': f"No post found with ID {post_id}"})
        }
    
    text = post_item["Items"][0]["text"]
    voice = post_item["Items"][0]["voice"]
    
    # Divide text into blocks of approximately 1,000 characters
    text_blocks = []
    while len(text) > 1100:
        end = text.rfind('.', 0, 1100)
        if end == -1:
            end = text.rfind(' ', 0, 1100)
        if end == -1:
            end = 1100
        text_blocks.append(text[:end].strip())
        text = text[end:].strip()
    text_blocks.append(text)
    
    # Invoke Polly API to transform text into audio
    polly = boto3.client('polly')
    output_path = os.path.join("/tmp/", post_id + ".mp3")
    
    with open(output_path, "wb") as file:
        for text_block in text_blocks:
            response = polly.synthesize_speech(
                OutputFormat='mp3',
                Text=text_block,
                VoiceId=voice
            )
            if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    file.write(stream.read())
            else:
                print(f"Error: Polly did not return an audio stream for block: {text_block}")
    
    # Upload the audio file to S3
    s3 = boto3.client('s3')
    s3.upload_file(output_path, os.environ['BUCKET_NAME'], post_id + ".mp3")
    print(f"Uploaded MP3 file to S3: {os.environ['BUCKET_NAME']}/{post_id}.mp3")
    
    # Construct the URL
    location = s3.get_bucket_location(Bucket=os.environ['BUCKET_NAME'])
    region = location['LocationConstraint']
    
    if region is None:
        url_beginning = "https://s3.amazonaws.com/"
    else:
        url_beginning = f"https://s3-{region}.amazonaws.com/"
    
    url = f"{url_beginning}{os.environ['BUCKET_NAME']}/{post_id}.mp3"
    print(f"MP3 file URL: {url}")

    # Updating the item in DynamoDB
    table.update_item(
        Key={'id': post_id},
        UpdateExpression="SET #statusAtt = :statusValue, #urlAtt = :urlValue",
        ExpressionAttributeValues={
            ':statusValue': 'UPDATED',
            ':urlValue': url
        },
        ExpressionAttributeNames={
            '#statusAtt': 'status',
            '#urlAtt': 'url'
        },
        ReturnValues="UPDATED_NEW"
    )
    print(f"Post {post_id} updated successfully in DynamoDB")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'id': post_id,
            'voice': voice,
            'text': text,
            'status': 'UPDATED',
            'url': url
        })
    }