import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

## will this make it to lambda?

def lambda_handler(event, context):
    try:
        response = table.scan() 
        items = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
