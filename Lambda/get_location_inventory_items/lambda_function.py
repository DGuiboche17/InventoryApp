import boto3
import json
from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal

deserializer = TypeDeserializer()

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    if 'pathParameters' not in event or event['pathParameters'] is None:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing path parameters")
        }

    if 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' path parameter")
        }

    try:
        location_id = int(event['pathParameters']['location_id'])
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps("'location_id' must be an integer")
        }

    try:
        response = dynamo_client.query(
            TableName=table_name,
            IndexName='LocationIndex',  
            KeyConditionExpression='location_id = :loc',
            ExpressionAttributeValues={
                ':loc': {'N': str(location_id)}
            }
        )

        items = response.get('Items', [])


        parsed_items = []
        for item in items:
            deserialized = {k: deserializer.deserialize(v) for k, v in item.items()}
            for key, value in deserialized.items():
                if isinstance(value, Decimal):
                    if value % 1 == 0:
                        deserialized[key] = int(value)
                    else:
                        deserialized[key] = float(value)
            parsed_items.append(deserialized)

        return {
            'statusCode': 200,
            'body': json.dumps(parsed_items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
