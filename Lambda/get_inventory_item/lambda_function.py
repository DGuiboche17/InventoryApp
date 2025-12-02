import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    if 'pathParameters' not in event or 'item_id' not in event['pathParameters'] or 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'item_id' or 'location_id' path parameter")
        }

    item_id = event['pathParameters']['item_id']
    location_id = event['pathParameters']['location_id']

    try:
        location_id = int(location_id)
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps("'location_id' must be an integer")
        }

    key = {
        'item_id': {'S': item_id},
        'location_id': {'N': str(location_id)}
    }

    try:
        response = dynamo_client.get_item(TableName=table_name, Key=key)
        item = response.get('Item', {})

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item, default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
