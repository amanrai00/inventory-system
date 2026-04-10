# Internal Inventory Management System — Project Guide
**Portfolio MVP | Flask + SQLite (default) / MySQL + AWS EC2 + RDS**

---

## Project Summary

A private company inventory system where employees:
- Log in securely
- Manage products (add, edit, view)
- Track stock levels with automatic status alerts
- Record sales (auto-reduces stock)
- View dashboard with real-time inventory stats
- Monitor low stock and out-of-stock items

**Stack:** Python Flask + SQLite (local dev default) or MySQL → EC2 + RDS MySQL (production)  
**Frontend:** AdminLTE 3 (Bootstrap admin template via CDN, rendered with Jinja2)  
**Goal:** Demonstrate backend logic, database design, security practices, and AWS deployment for IT/Cloud portfolio

---

## Database Schema

```sql
-- Users table
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'employee',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(100) NOT NULL,
  sku VARCHAR(50) UNIQUE NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  stock_quantity INT DEFAULT 0,
  minimum_stock_level INT DEFAULT 10,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sales table
CREATE TABLE sales (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INT NOT NULL,
  quantity_sold INT NOT NULL,
  sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

> The MySQL schema is in `database/schema.sql` and the SQLite schema is in `database/schema_sqlite.sql`. The `scripts/init_db.py` script handles database initialization and admin user seeding for both backends.

---

## Stock Logic

```
If stock_quantity == 0          → Status: OUT OF STOCK  (red badge)
If stock_quantity <= min_level  → Status: LOW STOCK     (yellow badge)
If stock_quantity > min_level   → Status: NORMAL        (green badge)
```

Sale transaction flow:
1. Employee selects product and quantity
2. System checks if enough stock is available
3. If yes → inserts sale record + reduces `stock_quantity`
4. If no → returns error message, no changes made

---

## Flask Project Structure

```
inventory-system/
├── app.py                  # Main Flask app entry point (factory pattern)
├── config.py               # DB config, secret key (reads from .env)
├── .env                    # Environment variables (NEVER commit this)
├── .env.example            # Example env file for new developers
├── .gitignore              # Ignores venv/, .env, __pycache__/
├── requirements.txt        # Python dependencies
├── DESIGN.md               # Design notes
│
├── database/
│   ├── client.py           # Database abstraction layer (SQLite + MySQL)
│   ├── schema.sql          # MySQL schema
│   └── schema_sqlite.sql   # SQLite schema
│
├── scripts/
│   └── init_db.py          # Database initialization + admin user seeding
│
├── models/
│   ├── __init__.py
│   ├── user.py             # User lookup, password hashing/verification
│   ├── product.py          # Product CRUD, stock status logic
│   └── sale.py             # Record sale, reduce stock, sales history
│
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Login/logout + @login_required decorator
│   ├── products.py         # Product CRUD routes
│   ├── sales.py            # Sales recording + history routes
│   └── dashboard.py        # Dashboard stats route
│
├── templates/              # Jinja2 HTML templates (AdminLTE 3)
│   ├── base.html           # Base layout with sidebar + navbar
│   ├── login.html          # Standalone login page
│   ├── dashboard.html      # Dashboard with stat cards
│   ├── products/
│   │   ├── list.html       # Product table with status badges
│   │   ├── add.html        # Add product form
│   │   └── edit.html       # Edit product form
│   └── sales/
│       ├── record.html     # Record sale form (product dropdown)
│       └── history.html    # Sales history table
│
├── static/
│   ├── css/style.css       # Custom overrides
│   └── js/app.js           # Custom scripts
│
└── venv/                   # Python virtual environment (not committed)
```

---

## Environment Variables (.env)

```
DB_BACKEND=sqlite
SQLITE_PATH=instance/inventory.db
DB_HOST=localhost
DB_PORT=3306
DB_NAME=inventory_db
DB_USER=root
DB_PASSWORD=your_password
SECRET_KEY=your_secret_key_here
```

> **Default:** `DB_BACKEND=sqlite` uses a local SQLite file — no MySQL setup required.  
> **MySQL:** Set `DB_BACKEND=mysql` and configure the `DB_*` variables.  
> **Production:** `DB_HOST=your-rds-endpoint.amazonaws.com`

---

## Key Flask Routes

```
GET  /                              → Redirect to /login

GET  /login                         → Show login form
POST /login                         → Authenticate user, start session
GET  /logout                        → Clear session, redirect to login

GET  /dashboard                     → Show stats (protected)

GET  /products                      → List all products with status (protected)
GET  /products/add                  → Add product form (protected)
POST /products/add                  → Save new product (protected)
GET  /products/edit/<id>            → Edit product form (protected)
POST /products/edit/<id>            → Update product (protected)
POST /products/update-stock/<id>    → Update stock quantity (protected)

GET  /sales                         → Sales history (protected)
GET  /sales/record                  → Record sale form (protected)
POST /sales/record                  → Save sale + reduce stock (protected)
```

---

## Build Order (Phase 1 — Local Development)

| Step | Task | Details |
|------|------|---------|
| 1 | Project setup | Virtual environment, install packages, configure `.env` |
| 2 | Database setup | Run `scripts/init_db.py` (SQLite default, MySQL optional) |
| 3 | Auth system | Login, session management, logout, `@login_required` decorator |
| 4 | Products CRUD | Add, list, edit, update stock, minimum stock levels |
| 5 | Sales system | Record sale, auto-reduce stock, validate quantity, view history |
| 6 | Dashboard | Total products, low stock count, out of stock count, total sales |
| 7 | AdminLTE templates | Wire AdminLTE 3 layout to all pages via Jinja2 base template |
| 8 | Testing | Test all routes, edge cases (0 stock, oversell), flash messages |

---

## Build Order (Phase 2 — AWS Deployment)

| Step | Task | Details |
|------|------|---------|
| 9 | Launch EC2 | Amazon Linux 2, t2.micro (free tier) |
| 10 | Security Groups | Configure inbound rules (SSH, HTTP, Flask dev port) |
| 11 | Launch RDS MySQL | Free tier, private subnet, not publicly accessible |
| 12 | Configure EC2 | SSH in, install Python, Flask, MySQL client, upload project |
| 13 | Set production .env | Set `DB_BACKEND=mysql`, point `DB_HOST` to RDS endpoint |
| 14 | Run and test | Start Flask app, verify in browser via EC2 public IP |

---

## AWS Architecture

```
[ Browser ]
     |
     | HTTP (port 80 / 5000)
     v
[ EC2 Instance — t2.micro ]      ← SSH access (port 22, your IP only)
  Python + Flask app
     |
     | MySQL (port 3306, internal only)
     v
[ RDS MySQL — free tier ]         ← Private subnet, NOT publicly accessible
```

**Security Groups:**

| Group | Port | Source | Purpose |
|-------|------|--------|---------|
| EC2 | 22 | Your IP only | SSH access |
| EC2 | 80 | 0.0.0.0/0 | HTTP traffic |
| EC2 | 5000 | 0.0.0.0/0 | Flask dev server (remove in production) |
| RDS | 3306 | EC2 Security Group | MySQL — internal traffic only |

---

## Security Checklist

- [ ] Passwords hashed with `werkzeug.security` (PBKDF2 with SHA-256)
- [ ] Session secret key set via environment variable (not hardcoded)
- [ ] All routes protected with `@login_required` decorator
- [ ] Input validated before database insert (type casting, required fields)
- [ ] Sale quantity validated against available stock before processing
- [ ] No credentials hardcoded anywhere in source code
- [ ] `.env` added to `.gitignore`
- [ ] RDS not publicly accessible (private subnet only)
- [ ] EC2 SSH port restricted to your IP only
- [ ] Flask `debug=True` disabled in production

---

## Python Dependencies

```
Flask==2.3.3
Flask-MySQLdb==1.0.1
Werkzeug==2.3.8
python-dotenv==1.0.0
mysqlclient==2.2.0
```

> `mysqlclient` is the underlying MySQL driver required by Flask-MySQLdb — needed if someone switches to `DB_BACKEND=mysql`.

---

## Interview Talking Points

**Architecture:**
> "I built a Flask app using the application factory pattern with Blueprints for modular routing. It supports both SQLite for local development and MySQL for production. The production setup connects to an RDS MySQL instance in a private subnet — the database is never publicly accessible."

**Security:**
> "All credentials are managed through environment variables. Passwords are hashed using PBKDF2 via Werkzeug. Every route is protected with a custom login_required decorator, and the RDS security group only accepts traffic from the EC2 instance."

**Business Logic:**
> "When a sale is recorded, the system validates that enough stock exists, then atomically inserts the sale record and reduces the product's stock quantity. Products are automatically flagged as Low Stock or Out of Stock based on configurable minimum thresholds."

**Deployment:**
> "I deployed on EC2 with the Flask app connecting to a private RDS MySQL instance. Security groups enforce that SSH is restricted to my IP and the database only accepts connections from EC2."

**Problem Solving:**
> "I designed the stock status as a computed value rather than a stored column — this avoids sync issues and always reflects the real-time state of inventory."

---

## Future Improvements (mention in interviews)

- Role-based access control (admin vs employee permissions)
- Audit logs for all inventory changes
- Low-stock email alerts via AWS SES
- Scheduled inventory reports via CloudWatch Events
- AI demand prediction via Amazon Bedrock
- Docker containerization + CI/CD pipeline with GitHub Actions
- Suppliers table and purchase order tracking
- Nginx reverse proxy + HTTPS with Let's Encrypt for production
- Pagination and search/filter on product and sales lists

---

## Current Status Tracker

- [x] Flask project structure created
- [x] .env configured
- [x] Auth working (login/logout/session)
- [x] Products CRUD working
- [x] Sales + stock logic working
- [x] Dashboard working
- [x] AdminLTE template wired to all pages
- [x] Product search/filter
- [x] Sales history filtering
- [x] Server-side validation
- [x] SQLite support for local development
- [x] Database abstraction layer (SQLite + MySQL)
- [x] Local git initialization
- [ ] GitHub publishing
- [ ] README screenshots
- [ ] Automated tests
- [ ] EC2 launched
- [ ] RDS launched
- [ ] App deployed and live
- [ ] Added to resume + LinkedIn

---

*Start each new Claude session by sharing this file so context is restored instantly.*
