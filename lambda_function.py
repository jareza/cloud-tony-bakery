import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("cloud-tony-bakery-orders")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        order_id = str(uuid.uuid4())

        item = {
            "orderId": order_id,
            "customerName": body.get("customerName", "Guest"),
            "item": body.get("item", "Bakery Order"),
            "createdAt": datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Order received by Cloud Tony Bakery!",
                "orderId": order_id
            })
        }

    except Exception as e:
        print(f"ERROR: {str(e)}")

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Unable to process order"
            })
        }
