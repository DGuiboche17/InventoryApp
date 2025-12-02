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
    try:
        location_id = int(event['pathParameters']['location_id'])
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps("'location_id' must be an integer")
        }

    try:
        dynamo_client.delete_item(
            TableName=table_name,
            Key={
                'location_id': {'N': str(location_id)},
                'item_id': {'S': item_id}
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item {item_id} at location {location_id} deleted")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
