from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from models.product import (
    get_all_products,
    get_product_by_id,
    get_product_by_sku,
    add_product,
    update_product,
    update_stock,
    get_stock_status,
)
from routes.auth import login_required

products_bp = Blueprint('products', __name__)


def _build_product_form_data(source=None, product=None):
    return {
        'name': (source.get('name') if source else (product[1] if product else '')).strip() if (source and source.get('name') is not None) or product else '',
        'sku': (source.get('sku') if source else (product[2] if product else '')).strip().upper() if (source and source.get('sku') is not None) or product else '',
        'price': source.get('price') if source else (product[3] if product else ''),
        'stock_quantity': source.get('stock_quantity') if source else (product[4] if product else 0),
        'minimum_stock_level': source.get('minimum_stock_level') if source else (product[5] if product else 10),
    }


def _validate_product_form(mysql, form_data, current_product_id=None):
    errors = []

    if not form_data['name']:
        errors.append('Product name is required.')

    if not form_data['sku']:
        errors.append('SKU is required.')

    try:
        price = float(form_data['price'])
        if price <= 0:
            errors.append('Price must be greater than 0.')
    except (TypeError, ValueError):
        errors.append('Price must be a valid number.')
        price = None

    try:
        stock_quantity = int(form_data['stock_quantity'])
        if stock_quantity < 0:
            errors.append('Stock quantity cannot be negative.')
    except (TypeError, ValueError):
        errors.append('Stock quantity must be a whole number.')
        stock_quantity = None

    try:
        minimum_stock_level = int(form_data['minimum_stock_level'])
        if minimum_stock_level < 0:
            errors.append('Minimum stock level cannot be negative.')
    except (TypeError, ValueError):
        errors.append('Minimum stock level must be a whole number.')
        minimum_stock_level = None

    existing_product = get_product_by_sku(mysql, form_data['sku']) if form_data['sku'] else None
    if existing_product and existing_product[0] != current_product_id:
        errors.append('SKU already exists. Use a unique SKU for each product.')

    cleaned_data = {
        'name': form_data['name'],
        'sku': form_data['sku'],
        'price': price,
        'stock_quantity': stock_quantity,
        'minimum_stock_level': minimum_stock_level,
    }

    return errors, cleaned_data


@products_bp.route('/products')
@login_required
def list_products():
    mysql = current_app.extensions['mysql']
    products = get_all_products(mysql)
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', 'ALL').strip().upper()
    allowed_statuses = {'ALL', 'NORMAL', 'LOW STOCK', 'OUT OF STOCK'}
    if status_filter not in allowed_statuses:
        status_filter = 'ALL'

    products_with_status = []
    for p in products:
        product_data = {
            'id': p[0],
            'name': p[1],
            'sku': p[2],
            'price': p[3],
            'stock_quantity': p[4],
            'minimum_stock_level': p[5],
            'status': get_stock_status(p[4], p[5]),
        }

        if search:
            search_text = search.lower()
            if search_text not in product_data['name'].lower() and search_text not in product_data['sku'].lower():
                continue

        if status_filter != 'ALL' and product_data['status'] != status_filter:
            continue

        products_with_status.append(product_data)

    filters = {
        'search': search,
        'status': status_filter,
    }

    return render_template('products/list.html', products=products_with_status, filters=filters)


@products_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product_route():
    mysql = current_app.extensions['mysql']
    if request.method == 'POST':
        form_data = _build_product_form_data(request.form)
        errors, cleaned_data = _validate_product_form(mysql, form_data)
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('products/add.html', form_data=form_data), 400

        add_product(
            mysql,
            cleaned_data['name'],
            cleaned_data['sku'],
            cleaned_data['price'],
            cleaned_data['stock_quantity'],
            cleaned_data['minimum_stock_level'],
        )
        flash('Product added successfully!', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/add.html', form_data=_build_product_form_data())


@products_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    mysql = current_app.extensions['mysql']
    product = get_product_by_id(mysql, id)
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('products.list_products'))

    if request.method == 'POST':
        form_data = _build_product_form_data(request.form, product)
        errors, cleaned_data = _validate_product_form(mysql, form_data, current_product_id=id)
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('products/edit.html', product=product, form_data=form_data), 400

        update_product(
            mysql,
            id,
            cleaned_data['name'],
            cleaned_data['sku'],
            cleaned_data['price'],
            cleaned_data['stock_quantity'],
            cleaned_data['minimum_stock_level'],
        )
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/edit.html', product=product, form_data=_build_product_form_data(product=product))


@products_bp.route('/products/update-stock/<int:id>', methods=['POST'])
@login_required
def update_stock_route(id):
    mysql = current_app.extensions['mysql']
    try:
        new_quantity = int(request.form['stock_quantity'])
    except (TypeError, ValueError):
        flash('Stock quantity must be a whole number.', 'danger')
        return redirect(url_for('products.list_products'))

    if new_quantity < 0:
        flash('Stock quantity cannot be negative.', 'danger')
        return redirect(url_for('products.list_products'))

    update_stock(mysql, id, new_quantity)
    flash('Stock updated successfully!', 'success')
    return redirect(url_for('products.list_products'))
