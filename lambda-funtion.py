import boto3
import json

sqs = boto3.client('sqs')
ses = boto3.client('ses', region_name='us-east-1')

QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/email-process-queue'
TO_EMAIL = 'yourname@gmail.com'       # same as SES verified
FROM_EMAIL = 'yourname@gmail.com'     # same as SES verified

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        message = f"New file: {key} in bucket: {bucket}"
        print(message)

        # Send message to SQS
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=message)

        # Send email via SES
        ses.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [TO_EMAIL]},
            Message={
                'Subject': {'Data': 'New File Uploaded to S3'},
                'Body': {'Text': {'Data': message}}
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
