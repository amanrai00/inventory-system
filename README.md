# Inventory Management System

Internal inventory management dashboard built with Flask, Jinja2, and AdminLTE.

This project is designed as a portfolio MVP for demonstrating:
- authentication and session handling
- product inventory management
- stock status logic
- sales recording with stock deduction
- operational dashboard design
- structured Flask app organization

## Features

- Employee login/logout flow
- Dashboard with:
  - total products
  - low stock count
  - out of stock count
  - total sales count
  - critical inventory section
  - recent sales activity
- Product management:
  - add product
  - edit product
  - stock status badges
  - search by name or SKU
  - filter by stock status
- Sales management:
  - record sale
  - automatic stock deduction
  - oversell protection
  - sales history search and date filtering
- Server-side validation for products and sales

## Tech Stack

- Python
- Flask
- Jinja2
- AdminLTE 3
- Bootstrap 4
- Font Awesome
- SQLite for local development by default
- MySQL config supported through environment variables

## Project Structure

```text
inventory-system/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── DESIGN.md
├── inventory-project-guide.md
├── database/
│   ├── client.py
│   ├── schema.sql
│   └── schema_sqlite.sql
├── models/
│   ├── product.py
│   ├── sale.py
│   └── user.py
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── products.py
│   └── sales.py
├── scripts/
│   └── init_db.py
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── login.html
    ├── products/
    └── sales/
```

## Local Setup

### 1. Clone the repository

```powershell
git clone https://github.com/amanrai00/inventory-system.git
cd inventory-system
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create your environment file

Copy `.env.example` to `.env` and update values if needed.

Example:

```env
DB_BACKEND=sqlite
SQLITE_PATH=instance/inventory.db
FLASK_DEBUG=1
DB_HOST=localhost
DB_PORT=3306
DB_NAME=inventory_db
DB_USER=root
DB_PASSWORD=your_mysql_password
SECRET_KEY=replace_with_a_real_secret_key
```

## Database Setup

### Default local setup: SQLite

The project currently defaults to SQLite for easy local development.

Run:

```powershell
.\venv\Scripts\python.exe scripts\init_db.py
```

This creates the local database and seeds a default admin user.

### Optional: MySQL

If you want to use MySQL instead:

1. Set `DB_BACKEND=mysql` in `.env`
2. Update `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`
3. Run:

```powershell
.\venv\Scripts\python.exe scripts\init_db.py
```

## Run the App

```powershell
.\venv\Scripts\python.exe app.py
```

Open in your browser:

```text
http://127.0.0.1:5000/login
```

For production, set:

```env
FLASK_DEBUG=0
DB_BACKEND=mysql
```

## Demo Login

Use the seeded admin account:

- Email: `admin@company.com`
- Password: `admin123`

## Business Logic

Stock status rules:

- `OUT OF STOCK` when `stock_quantity == 0`
- `LOW STOCK` when `stock_quantity <= minimum_stock_level`
- `NORMAL` when `stock_quantity > minimum_stock_level`

Sales flow:

1. Select product
2. Enter quantity sold
3. Validate available stock
4. Save sale
5. Reduce stock automatically

## Current Status

Implemented:

- authentication
- dashboard
- product add/edit/list
- sales record/history
- dashboard operational panels
- product search/filter
- sales history filtering
- server-side validation
- local git initialization

Planned next steps:

- GitHub publishing
- README screenshots
- automated tests
- MySQL-only cleanup if required
- EC2 and RDS deployment

## Screenshots

Add screenshots here after pushing the repo:

- Login page
- Dashboard
- Products page
- Sales history page

## Notes

- `.env`, local database files, and virtual environments are ignored by git
- `FLASK_DEBUG=1` is intended for local development only
- This project uses a clean Flask blueprint structure suitable for extension and deployment
