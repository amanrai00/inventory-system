def get_all_products(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return products


def get_product_by_id(mysql, product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()
    return product


def get_product_by_sku(mysql, sku):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE sku = %s", (sku,))
    product = cur.fetchone()
    cur.close()
    return product


def add_product(mysql, name, sku, price, stock_quantity, minimum_stock_level):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO products (name, sku, price, stock_quantity, minimum_stock_level) "
        "VALUES (%s, %s, %s, %s, %s)",
        (name, sku, price, stock_quantity, minimum_stock_level)
    )
    mysql.connection.commit()
    cur.close()


def update_product(mysql, product_id, name, sku, price, stock_quantity, minimum_stock_level):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE products SET name=%s, sku=%s, price=%s, stock_quantity=%s, minimum_stock_level=%s "
        "WHERE id=%s",
        (name, sku, price, stock_quantity, minimum_stock_level, product_id)
    )
    mysql.connection.commit()
    cur.close()


def update_stock(mysql, product_id, new_quantity):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE products SET stock_quantity = %s WHERE id = %s",
        (new_quantity, product_id)
    )
    mysql.connection.commit()
    cur.close()


def get_stock_status(stock_quantity, minimum_stock_level):
    if stock_quantity == 0:
        return 'OUT OF STOCK'
    elif stock_quantity <= minimum_stock_level:
        return 'LOW STOCK'
    else:
        return 'NORMAL'
