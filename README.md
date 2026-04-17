# Inventory Management System
 
> 🇯🇵 日本語版はこちら → [README\_JA.md](README_JA.md)
 
A production-grade internal inventory management dashboard built with **Flask**, **Jinja2**, and **AdminLTE 3**, deployed on **AWS** (EC2 + RDS MySQL). Features AI-powered demand forecasting via **Amazon Bedrock**, bilingual EN/JA UI, automated low-stock email alerts via **Amazon SES**, EC2 CPU monitoring via **CloudWatch**, and a complete **CI/CD pipeline** through GitHub Actions.
 
> **Live:** [http://35.77.96.153](http://35.77.96.153/login) — AWS EC2 · ap-northeast-1 (Tokyo) · HTTP only (HTTPS pending — requires custom domain)
 
---
 
## Tech Stack
 
| Layer | Technology |
| --- | --- |
| Backend | Python 3, Flask (Application Factory + Blueprints) |
| Frontend | Jinja2, AdminLTE 3, Bootstrap 4, Font Awesome |
| Database | MySQL 8.4 on AWS RDS (production) / SQLite (local dev) |
| Server | Ubuntu 24 EC2 · Nginx reverse proxy · Gunicorn · systemd |
| AI / ML | Amazon Bedrock — Claude Haiku 4.5 (jp inference profile) |
| Alerts | Amazon SES (low stock email) · CloudWatch + SNS (CPU alarm) |
| CI/CD | GitHub Actions — auto-deploy on push to `main` |
| Auth | IAM Role (`inventory-ec2-ses-role`) — no hardcoded AWS credentials |
| i18n | Bilingual EN/JA — Flask session-based language switching |
 
---
 
## Features
 
### Core Application
 
- Secure employee login / logout with session management
- Dashboard: total products, low-stock count, out-of-stock count, total sales
- **Product management** — add, edit, search by name or SKU, filter by stock status
- **Sales management** — record sales with automatic stock deduction and oversell protection
- Sales history with search and date-range filtering
- Server-side input validation throughout
- Stock status computed dynamically — always reflects real-time inventory state
- **Bilingual UI (EN/JA)** — full English/Japanese language toggle persisted via Flask session; all UI strings, flash messages, and stock status labels rendered in the active language
### AWS Integrations
 
- **Amazon SES** — automatically sends a low-stock email alert when a sale brings `stock_quantity` below `minimum_stock_level`
- **CloudWatch Alarm** — monitors EC2 CPU utilization; triggers SNS email when usage exceeds 80% for 1 consecutive minute
- **Amazon Bedrock (Claude Haiku 4.5)** — daily cron job at 2 AM (EC2 time) fetches all low-stock products, retrieves 30-day sales history per product, and calls Bedrock to generate `recommended_restock_qty` and reasoning in both English and Japanese; predictions are saved to the `predictions` table and displayed on the dashboard in the active language
---
 
## Screenshots
 
### Dashboard
 
![Dashboard](screenshots/dashboard.png)
 
### Product Inventory
 
![Products](screenshots/products.png)
 
### AI Restock Recommendations (Powered by Amazon Bedrock)
 
![AI Predictions](screenshots/ai-predictions.png)
 
---
 
## Architecture
 
```
+----------------------------------------------------------------+
|                      Developer                                 |
|              Edit code and git push -> main                    |
+------------------------------+---------------------------------+
                               |
                               v
+----------------------------------------------------------------+
|                GitHub Actions  (CI/CD Pipeline)                |
|    SSH -> pull latest code -> install dependencies -> restart  |
+------------------------------+---------------------------------+
                               |
                               v
+----------------------------------------------------------------+
|         EC2 Production Server  aman-inventory-prod (Tokyo)     |
|                                                                |
|   Browser -> Nginx (port 80) -> Gunicorn -> Flask (port 5000)  |
|                                                                |
|           IAM Role Auth (no hardcoded AWS credentials)         |
+------------+---------------------------------------------------+
             |                         |
             v                         v
+--------------------+   +------------------------------------+
|   RDS MySQL 8.4    |   |        AWS Integrated Services     |
|   Inventory DB     |   |                                    |
|   (Tokyo Region)   |   |  SES      -> low stock email alert |
+--------------------+   |  Bedrock  -> AI restock prediction |
                         |             (daily cron 2AM)       |
                         |  CloudWatch-> CPU monitor SNS alert|
                         +------------------------------------+
```
 
---
 
## Database Schema
 
```
products     — id, name, sku, price, stock_quantity, minimum_stock_level, created_at, updated_at
sales        — id, product_id, quantity_sold, sale_date
users        — id, name, email, password_hash, role, created_at
predictions  — id, product_id, recommended_restock_qty, reasoning, reason_en, reason_ja, predicted_at
```
 
**Stock status logic:**
 
- `OUT OF STOCK` → `stock_quantity == 0`
- `LOW STOCK` → `stock_quantity <= minimum_stock_level`
- `NORMAL` → `stock_quantity > minimum_stock_level`
**Sale transaction flow:**
 
1. Employee selects product and enters quantity
2. System validates available stock
3. If sufficient → sale record inserted + `stock_quantity` reduced atomically
4. If insufficient → error returned, no changes made
---
 
## Project Structure
 
```
inventory-system/
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions CI/CD
├── database/
│   ├── client.py              # DB abstraction layer (SQLite for local dev)
│   ├── schema.sql             # MySQL schema (production)
│   └── schema_sqlite.sql      # SQLite schema (local dev)
├── logs/
│   └── predict.log            # Bedrock cron job output log
├── models/
│   ├── product.py             # Product CRUD + stock status logic
│   ├── sale.py                # Sale recording + stock deduction
│   └── user.py                # User lookup + password hashing
├── routes/
│   ├── auth.py                # Login, logout, /set-lang/ route, @login_required
│   ├── dashboard.py           # Dashboard stats + AI predictions
│   ├── products.py            # Product CRUD routes
│   └── sales.py               # Sales record + history routes
├── scripts/
│   ├── init_db.py             # DB initializer + admin user seed
│   ├── import_csv.py          # Bulk CSV import (100 products, 240 sales)
│   └── predict.py             # Bedrock AI demand prediction (daily cron, bilingual)
├── static/
│   ├── css/style.css
│   └── js/
│       ├── app.js
│       └── i18n.js            # EN/JA language toggle (calls /set-lang/ route)
├── templates/
│   ├── base.html              # AdminLTE shell (sidebar + navbar)
│   ├── dashboard.html         # Dashboard with AI Restock Recommendations (bilingual)
│   ├── login.html
│   ├── products/              # list, add, edit templates
│   └── sales/                 # record, history templates
├── utils/
│   └── email_alerts.py        # SES low-stock alert helper
├── .env.example
├── .gitignore
├── app.py                     # Flask entry point (factory pattern)
├── config.py                  # Config reads from .env
└── requirements.txt
```
 
---
 
## Local Development Setup
 
### 1. Clone and create virtual environment
 
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
 
Default local config (SQLite — no MySQL setup needed):
 
```
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
 
**Default demo login:** `admin@company.com` / `admin123`  
*(Change this password immediately in any real deployment)*
 
---
 
## Production Deployment (AWS)
 
| Resource | Details |
| --- | --- |
| EC2 instance | `aman-inventory-prod` — Ubuntu 24, ap-northeast-1 (Tokyo) |
| Public IP | `35.77.96.153` |
| RDS endpoint | `inventory-db.cle6c28amu35.ap-northeast-1.rds.amazonaws.com` |
| RDS engine | MySQL Community 8.4.8, db.t4g.micro |
| WSGI server | Gunicorn (3 workers, factory pattern) |
| Process manager | systemd (`inventory.service`) — survives reboots |
| Reverse proxy | Nginx — port 80 → Gunicorn port 5000 (internal only) |
| IAM Role | `inventory-ec2-ses-role` (SES + CloudWatch + Bedrock) |
 
GitHub Actions (`.github/workflows/deploy.yml`) automatically SSHs into EC2, pulls latest code, installs dependencies, and restarts the Flask service on every push to `main`.
 
---
 
## Useful Commands (EC2)
 
```bash
# App status and live logs
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
 
- [x] Flask app — Application Factory + Blueprints
- [x] SQLite (local) + MySQL (production) dual-backend support
- [x] EC2 + RDS deployment — Tokyo region
- [x] Nginx reverse proxy
- [x] Gunicorn production WSGI server (3 workers)
- [x] systemd process management (auto-restart on reboot)
- [x] GitHub Actions CI/CD pipeline
- [x] Amazon SES low-stock email alerts
- [x] CloudWatch EC2 CPU alarm → SNS email notification
- [x] Amazon Bedrock AI demand prediction (daily cron, dashboard display)
- [x] 100 products + 240 sales records imported via CSV
- [x] Bilingual EN/JA UI — full language toggle via Flask session
- [x] Bilingual Bedrock predictions (reason_en + reason_ja)
- [x] Role-based access control (admin vs employee)
- [ ] HTTPS / SSL certificate (Let's Encrypt — requires custom domain)
- [ ] S3 product image uploads
- [ ] Automated tests
---
 
## Security
 
- No AWS credentials hardcoded — EC2 authenticates via IAM role
- `.env` is gitignored and never pushed to GitHub
- Passwords hashed with PBKDF2 via `werkzeug.security`
- All routes protected with `@login_required` decorator
- Port 5000 not exposed externally — all traffic routed through Nginx on port 80
- RDS security group allows MySQL connections from the EC2 security group only
- SSH key-pair auth only (password authentication disabled in `sshd_config`); port 22 open to `0.0.0.0/0` to support GitHub Actions CI/CD runners, which use dynamic Azure IPs
---
 
## License
 
This project is built for portfolio and learning purposes.
