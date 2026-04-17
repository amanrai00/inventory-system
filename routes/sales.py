from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from models.sale import record_sale, get_sales_history_filtered
from models.product import get_all_products, get_product_by_id
from routes.auth import login_required, admin_required
from utils.email_alerts import send_low_stock_alert

sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/sales')
@login_required
def history():
    mysql = current_app.extensions['mysql']
    filters = {
        'search': request.args.get('search', '').strip(),
        'date_from': request.args.get('date_from', '').strip(),
        'date_to': request.args.get('date_to', '').strip(),
    }
    sales = get_sales_history_filtered(mysql, filters['search'], filters['date_from'], filters['date_to'])
    return render_template('sales/history.html', sales=sales, filters=filters)


@sales_bp.route('/sales/record', methods=['GET', 'POST'])
@login_required
@admin_required
def record():
    mysql = current_app.extensions['mysql']
    products = get_all_products(mysql)
    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
        except (TypeError, ValueError):
            flash('Select a valid product.', 'danger')
            return render_template('sales/record.html', products=products), 400

        try:
            quantity_sold = int(request.form['quantity_sold'])
        except (TypeError, ValueError):
            flash('Quantity sold must be a whole number.', 'danger')
            return render_template('sales/record.html', products=products), 400

        if quantity_sold <= 0:
            flash('Quantity sold must be at least 1.', 'danger')
            return render_template('sales/record.html', products=products), 400

        if not get_product_by_id(mysql, product_id):
            flash('Selected product was not found.', 'danger')
            return render_template('sales/record.html', products=products), 400

        success, message = record_sale(mysql, product_id, quantity_sold)
        if success:
            flash(message, 'success')
            product = get_product_by_id(mysql, product_id)
            if product and product[4] <= product[5]:
                send_low_stock_alert(
                    product_name=product[1],
                    sku=product[2],
                    stock_quantity=product[4],
                    minimum_stock_level=product[5]
                )
            return redirect(url_for('sales.history'))
        else:
            flash(message, 'danger')
            return render_template('sales/record.html', products=products), 400
    return render_template('sales/record.html', products=products)
