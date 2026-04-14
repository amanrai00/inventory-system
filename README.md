# Inventory Management System

> 🇯🇵 日本語版はこちら → [README_JA.md](./README_JA.md)

A production-grade internal inventory management dashboard built with **Flask**, **Jinja2**, and **AdminLTE 3**, fully deployed on **AWS** (EC2 + RDS MySQL). Features AI-powered demand forecasting via **Amazon Bedrock**, automated low-stock email alerts via **Amazon SES**, and a complete **CI/CD pipeline** through GitHub Actions.

> **Live:** [http://35.77.96.153](http://35.77.96.153/login) — AWS EC2 · ap-northeast-1 (Tokyo)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask (Blueprints) |
| Frontend | Jinja2, AdminLTE 3, Bootstrap 4 |
| Database | MySQL 8.4 on AWS RDS (prod) / SQLite (local dev) |
| Server | Ubuntu 24 EC2 · Nginx reverse proxy · systemd |
| AI / ML | Amazon Bedrock — Claude Haiku 4.5 (jp inference profile) |
| Alerts | Amazon SES (low stock) · CloudWatch + SNS (CPU alarm) |
| CI/CD | GitHub Actions — auto-deploy on push to `main` |
| Auth | IAM Role (`inventory-ec2-ses-role`) — no hardcoded AWS keys |

---

## Features

### Core Application
- Secure employee login / logout with session handling
- Dashboard: total products, low-stock count, out-of-stock count, total sales
- **Product management** — add, edit, search by name or SKU, filter by stock status
- **Sales management** — record sales with automatic stock deduction and oversell protection
- Sales history with search and date-range filtering
- Server-side validation throughout

### AWS Integrations
- **Amazon SES** — triggers a low-stock email alert automatically when a sale brings `stock_quantity` below `minimum_stock_level`
- **CloudWatch Alarm** — monitors EC2 CPU; fires SNS email notification when utilization exceeds 80% for 1 consecutive minute
- **Amazon Bedrock (Claude Haiku 4.5)** — daily cron job at 2 AM (EC2 time) queries all low-stock products, fetches 30-day sales history per product, and calls Bedrock to generate `recommended_restock_qty` + reasoning; results are stored in the `predictions` table and displayed on the dashboard

---

## Architecture

```
Browser
  │
  ▼
Nginx (port 80)
  │  reverse proxy
  ▼
Flask app (port 5000, internal)
  │             │              │
  ▼             ▼              ▼
MySQL RDS    Amazon SES    Amazon Bedrock
(inventory)  (email alerts) (AI predictions)
                              │
                         CloudWatch
                        (CPU alarm → SNS → email)
```

---

## Database Schema

```
products      — id, name, sku, price, stock_quantity, minimum_stock_level
sales         — id, product_id, quantity_sold, sale_date
users         — id, name, email, password_hash, role
predictions   — id, product_id, recommended_restock_qty, reasoning, predicted_at
```

**Stock status logic:**
- `OUT OF STOCK` → `stock_quantity == 0`
- `LOW STOCK` → `stock_quantity <= minimum_stock_level`
- `NORMAL` → `stock_quantity > minimum_stock_level`

---

## Project Structure

```
inventory-system/
├── .github/workflows/deploy.yml   # GitHub Actions CI/CD
├── database/
│   ├── client.py                  # SQLite wrapper (local dev)
│   ├── schema.sql                 # MySQL schema (production)
│   └── schema_sqlite.sql
├── logs/
│   └── predict.log                # Bedrock cron output
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
│   ├── init_db.py                 # DB initializer + admin seed
│   ├── import_csv.py              # Bulk CSV import
│   └── predict.py                 # Bedrock AI demand prediction
├── static/
│   ├── css/style.css
│   └── js/app.js
├── templates/
│   ├── base.html
│   ├── dashboard.html             # includes AI Restock Recommendations
│   ├── login.html
│   ├── products/
│   └── sales/
├── utils/
│   └── email_alerts.py            # SES low-stock alert helper
├── .env.example
├── app.py
├── config.py
└── requirements.txt
```

---

## Local Development Setup

### 1. Clone and set up environment

```bash
git clone https://github.com/amanrai00/inventory-system.git
cd inventory-system
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` for local SQLite development:

```env
DB_BACKEND=sqlite
SQLITE_PATH=instance/inventory.db
FLASK_DEBUG=1
SECRET_KEY=replace_with_a_real_secret_key
```

### 3. Initialize the database

```bash
python scripts/init_db.py
```

### 4. Run

```bash
python app.py
# Open http://127.0.0.1:5000/login
```

**Default login:** `admin@company.com` / `admin123`

---

## Deployment (AWS)

| Resource | Value |
|---|---|
| EC2 instance | `aman-inventory-prod` — Ubuntu 24, ap-northeast-1 |
| Public IP | `35.77.96.153` |
| RDS endpoint | `inventory-db.cle6c28amu35.ap-northeast-1.rds.amazonaws.com` |
| RDS engine | MySQL Community 8.4.8 (db.t4g.micro) |
| Process manager | systemd (`inventory.service`) |
| Reverse proxy | Nginx — port 80 → Flask port 5000 (internal) |

The GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically SSHs into EC2, pulls the latest code, installs dependencies, and restarts the Flask service on every push to `main`.

---

## Useful Commands (on EC2)

```bash
# App status and logs
sudo systemctl status inventory
journalctl -u inventory -f

# Manual deploy
git pull origin main && pip install -r requirements.txt && sudo systemctl restart inventory

# Run AI predictions manually
cd ~/inventory-system && source venv/bin/activate && python3 scripts/predict.py
tail -50 logs/predict.log

# Nginx
sudo nginx -t && sudo systemctl reload nginx

# Test CloudWatch alarm manually
aws cloudwatch set-alarm-state \
  --alarm-name "inventory-ec2-cpu-high" \
  --state-value ALARM \
  --state-reason "Manual test" \
  --region ap-northeast-1
```

---

## Roadmap

- [x] Flask app with Blueprints
- [x] EC2 + RDS deployment (Tokyo region)
- [x] systemd process management (survives reboots)
- [x] Nginx reverse proxy
- [x] GitHub Actions CI/CD
- [x] SES low-stock email alerts
- [x] CloudWatch CPU alarm → SNS
- [x] Amazon Bedrock AI demand prediction (daily cron)
- [ ] S3 product image uploads
- [ ] HTTPS / SSL certificate
- [ ] Gunicorn production WSGI server
- [ ] Automated tests

---

## Security Notes

- No AWS credentials are hardcoded — the EC2 instance authenticates via IAM role (`inventory-ec2-ses-role`)
- `.env` is gitignored and never pushed to GitHub
- Port 5000 is not exposed externally — all traffic goes through Nginx on port 80
- RDS security group restricts MySQL access to the EC2 security group only (`inventory-sg`)
- SSH key pair: `aman-inventory-prod-v2.pem`

---

## License

This project is for portfolio and learning purposes.