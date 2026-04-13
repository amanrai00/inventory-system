import boto3
from botocore.exceptions import ClientError

SENDER = "amandevil163@gmail.com"
RECIPIENT = "amandevil163@gmail.com"
AWS_REGION = "ap-northeast-1"

def send_low_stock_alert(product_name, sku, stock_quantity, minimum_stock_level):
    subject = f"[Inventory Alert] Low Stock: {product_name}"
    body_text = f"""
Low Stock Alert

Product       : {product_name}
SKU           : {sku}
Current Stock : {stock_quantity}
Minimum Level : {minimum_stock_level}

Please restock this item soon.
"""
    client = boto3.client("ses", region_name=AWS_REGION)

    try:
        response = client.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [RECIPIENT]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body_text}},
            },
        )
        print(f"[SES] Alert sent for {product_name}, MessageId: {response['MessageId']}")
        return True
    except ClientError as e:
        print(f"[SES] Failed: {e.response['Error']['Message']}")
        return False
