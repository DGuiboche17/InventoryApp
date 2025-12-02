import json
import boto3
import uuid
from decimal import Decimal

def lambda_handler(event):
    try:

        ## will this make it to lambda?

        data = json.loads(event.get("body", "{}"))

        location_id = int(data['location_id'])
        item_name = data['item_name']
        item_description = data['item_description']
        item_qty = int(data['item_qty'])
        item_price = Decimal(str(data['item_price']))

        item_id = str(uuid.uuid4())

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Inventory')

        table.put_item(
            Item={
                'location_id': location_id,
                'item_id': item_id,
                'item_name': item_name,
                'item_description': item_description,
                'item_qty': item_qty,
                'item_price': item_price
            }
        )

        return {
            'statusCode': 201,
            'body': json.dumps({
                "message": f"Item '{item_name}' added successfully",
                "item_id": item_id
            })
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": f"Missing field: {str(e)}"})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
