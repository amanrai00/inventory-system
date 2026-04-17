from flask import Blueprint, render_template, current_app
from routes.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()

    # Total products
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    # Low stock count
    cur.execute("SELECT COUNT(*) FROM products WHERE stock_quantity <= minimum_stock_level AND stock_quantity > 0")
    low_stock_count = cur.fetchone()[0]

    # Out of stock count
    cur.execute("SELECT COUNT(*) FROM products WHERE stock_quantity = 0")
    out_of_stock_count = cur.fetchone()[0]

    # Total sales
    cur.execute("SELECT COUNT(*) FROM sales")
    total_sales = cur.fetchone()[0]

    # Critical inventory items for quick action
    cur.execute(
        "SELECT id, name, sku, stock_quantity, minimum_stock_level "
        "FROM products "
        "WHERE stock_quantity <= minimum_stock_level "
        "ORDER BY stock_quantity ASC "
        "LIMIT 5"
    )
    critical_items = []
    for row in cur.fetchall():
        critical_items.append({
            'id': row[0],
            'name': row[1],
            'sku': row[2],
            'stock_quantity': row[3],
            'minimum_stock_level': row[4],
            'status': 'OUT OF STOCK' if row[3] == 0 else 'LOW STOCK',
        })

    # Recent sales activity
    cur.execute(
        "SELECT s.id, p.name, s.quantity_sold, s.sale_date "
        "FROM sales s "
        "JOIN products p ON s.product_id = p.id "
        "ORDER BY s.sale_date DESC "
        "LIMIT 5"
    )
    recent_sales = []
    for row in cur.fetchall():
        recent_sales.append({
            'id': row[0],
            'product_name': row[1],
            'quantity_sold': row[2],
            'sale_date': row[3],
        })

    # AI demand predictions
    cur.execute(
        "SELECT p.id, p.name, p.sku, p.stock_quantity, p.minimum_stock_level, "
        "pr.recommended_restock_qty, pr.reasoning, pr.reason_en, pr.reason_ja, pr.predicted_at "
        "FROM predictions pr "
        "JOIN products p ON p.id = pr.product_id "
        "WHERE pr.id IN (SELECT MAX(id) FROM predictions GROUP BY product_id) "
        "ORDER BY pr.predicted_at DESC "
        "LIMIT 10"
    )
    ai_predictions = []
    for row in cur.fetchall():
        ai_predictions.append({
            'id': row[0],
            'name': row[1],
            'sku': row[2],
            'stock_quantity': row[3],
            'minimum_stock_level': row[4],
            'recommended_restock_qty': row[5],
            'reasoning': row[6],
            'reason_en': row[7] or row[6],
            'reason_ja': row[8] or row[6],
            'predicted_at': row[9],
        })

    cur.close()

    status_breakdown = [
        {'label': 'Normal', 'count': max(total_products - low_stock_count - out_of_stock_count, 0), 'tone': 'success'},
        {'label': 'Low Stock', 'count': low_stock_count, 'tone': 'warning'},
        {'label': 'Out of Stock', 'count': out_of_stock_count, 'tone': 'danger'},
    ]

    return render_template('dashboard.html',
                           total_products=total_products,
                           low_stock_count=low_stock_count,
                           out_of_stock_count=out_of_stock_count,
                           total_sales=total_sales,
                           critical_items=critical_items,
                           recent_sales=recent_sales,
                           status_breakdown=status_breakdown,
                           ai_predictions=ai_predictions)
