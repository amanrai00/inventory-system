def record_sale(mysql, product_id, quantity_sold):
    cur = mysql.connection.cursor()

    if quantity_sold <= 0:
        cur.close()
        return False, "Quantity sold must be at least 1"

    # Get current stock
    cur.execute("SELECT stock_quantity FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()

    if not product:
        cur.close()
        return False, "Product not found"

    current_stock = product[0]

    if quantity_sold > current_stock:
        cur.close()
        return False, "Not enough stock available"

    # Record the sale
    cur.execute(
        "INSERT INTO sales (product_id, quantity_sold) VALUES (%s, %s)",
        (product_id, quantity_sold)
    )

    # Reduce stock
    new_stock = current_stock - quantity_sold
    cur.execute(
        "UPDATE products SET stock_quantity = %s WHERE id = %s",
        (new_stock, product_id)
    )

    mysql.connection.commit()
    cur.close()
    return True, "Sale recorded successfully"


def get_sales_history(mysql):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT s.id, p.name, s.quantity_sold, s.sale_date "
        "FROM sales s JOIN products p ON s.product_id = p.id "
        "ORDER BY s.sale_date DESC"
    )
    sales = cur.fetchall()
    cur.close()
    return sales


def get_sales_history_filtered(mysql, search='', date_from='', date_to=''):
    cur = mysql.connection.cursor()

    query = (
        "SELECT s.id, p.name, s.quantity_sold, s.sale_date "
        "FROM sales s "
        "JOIN products p ON s.product_id = p.id "
        "WHERE 1 = 1"
    )
    params = []

    if search:
        query += " AND LOWER(p.name) LIKE %s"
        params.append(f"%{search.lower()}%")

    if date_from:
        query += " AND DATE(s.sale_date) >= %s"
        params.append(date_from)

    if date_to:
        query += " AND DATE(s.sale_date) <= %s"
        params.append(date_to)

    query += " ORDER BY s.sale_date DESC"

    cur.execute(query, tuple(params))
    sales = cur.fetchall()
    cur.close()
    return sales
