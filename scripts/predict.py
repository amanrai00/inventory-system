import boto3
import json
import os
import pymysql
from dotenv import load_dotenv

load_dotenv('/home/ubuntu/inventory-system/.env')

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = int(os.getenv('DB_PORT', 3306))

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

def get_sales_last_30_days(product_id, cursor):
    cursor.execute("""
        SELECT SUM(quantity_sold)
        FROM sales
        WHERE product_id = %s
          AND sale_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
    """, (product_id,))
    row = cursor.fetchone()
    return row[0] if row[0] else 0

def get_low_stock_products(cursor):
    cursor.execute("""
        SELECT id, name, sku, stock_quantity, minimum_stock_level
        FROM products
        WHERE stock_quantity <= minimum_stock_level
        ORDER BY stock_quantity ASC
    """)
    return cursor.fetchall()

def call_bedrock(product_name, sku, stock_qty, min_stock, sold_last_30):
    client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")
    prompt = (
        "You are an inventory management assistant.\n\n"
        f"Product: {product_name} (SKU: {sku})\n"
        f"Current stock: {stock_qty} units\n"
        f"Minimum stock level: {min_stock} units\n"
        f"Units sold in last 30 days: {sold_last_30} units\n\n"
        "Recommend how many units to restock.\n"
        "Respond in this exact JSON format with no extra text:\n"
        "{\n"
        '  "recommended_restock_qty": <integer>,\n'
        '  "reasoning": {\n'
        '    "en": "<one sentence explanation in English>",\n'
        '    "ja": "<one sentence explanation in natural, professional business Japanese>"\n'
        "  }\n"
        "}"
    )
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = client.invoke_model(
        modelId="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
        body=json.dumps(body)
    )
    raw = response["body"].read()
    result = json.loads(raw.decode("utf-8"))
    text = result["content"][0]["text"].strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def save_prediction(cursor, conn, product_id, restock_qty, reasoning, reasoning_en, reasoning_ja):
    cursor.execute(
        "INSERT INTO predictions (product_id, recommended_restock_qty, reasoning, reason_en, reason_ja) VALUES (%s, %s, %s, %s, %s)",
        (product_id, restock_qty, reasoning, reasoning_en, reasoning_ja)
    )
    conn.commit()

def run():
    conn = get_connection()
    cursor = conn.cursor()
    products = get_low_stock_products(cursor)
    print(f"Found {len(products)} low/out-of-stock products")
    for product in products:
        product_id, name, sku, stock_qty, min_stock = product
        sold_last_30 = get_sales_last_30_days(product_id, cursor)
        print(f"  Processing: {name} (stock: {stock_qty}, sold last 30d: {sold_last_30})")
        try:
            prediction = call_bedrock(name, sku, stock_qty, min_stock, sold_last_30)
            reasoning = prediction.get("reasoning", {})
            reasoning_en = reasoning.get("en", "")
            reasoning_ja = reasoning.get("ja", "")
            save_prediction(
                cursor,
                conn,
                product_id,
                prediction["recommended_restock_qty"],
                reasoning_en,
                reasoning_en,
                reasoning_ja
            )
            print(f"    -> Restock {prediction['recommended_restock_qty']} units: {reasoning_en}")
        except Exception as e:
            print(f"    -> ERROR for {name}: {e}")
    cursor.close()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    run()
