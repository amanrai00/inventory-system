<p align="right">
  <strong>English</strong> |
  <a href="./README_JA.md">日本語</a>
</p>

<div align="center">

# Inventory Management System

### Full-stack inventory dashboard with AWS Bedrock AI restock predictions


[![Live Demo](https://img.shields.io/badge/🟢_Live_Demo-Open-2ea44f?style=for-the-badge)](http://35.77.96.153/login)
[![日本語](https://img.shields.io/badge/日本語-README__JA.md-red?style=for-the-badge)](README_JA.md)

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)
![EC2](https://img.shields.io/badge/EC2-FF9900?style=flat&logo=amazon-ec2&logoColor=white)
![RDS](https://img.shields.io/badge/RDS-527FFF?style=flat&logo=amazon-rds&logoColor=white)
![Bedrock](https://img.shields.io/badge/Bedrock-%23232F3E.svg?style=flat&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL_8.4-4479A1?style=flat&logo=mysql&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-2088FF?style=flat&logo=github-actions&logoColor=white)

---

**Flask app deployed on AWS EC2 + RDS in Tokyo. Amazon Bedrock generates daily restock recommendations in English and Japanese. SES sends low-stock alerts. CloudWatch monitors CPU. GitHub Actions deploys on every push to `main`.**

</div>

---

## Try It

| | |
|---|---|
| **Live demo** | [http://35.77.96.153/login](http://35.77.96.153/login) |
| **Region** | AWS ap-northeast-1 (Tokyo) |
| **Demo login** | `demo@company.com` / `demo123` (read-only) |

> Demo runs on HTTP. HTTPS via custom domain + Let's Encrypt is on the roadmap.

---

## Screenshots

<table>
  <tr>
    <td align="center"><b>Dashboard</b></td>
    <td align="center"><b>AI Restock Recommendations</b></td>
  </tr>
  <tr>
    <td><img src="screenshots/dashboard.png" /></td>
    <td><img src="screenshots/ai-predictions.png" /></td>
  </tr>
  <tr>
    <td align="center"><b>Product Inventory</b></td>
    <td align="center"><b>Production Architecture</b></td>
  </tr>
  <tr>
    <td><img src="screenshots/products.png" /></td>
    <td><img src="screenshots/Architecture.PNG" /></td>
  </tr>
</table>

---

## What This Does

A small business has 100+ products and needs to know:

1. **What's running low right now:** dashboard shows current stock counts with color-coded status
2. **What to reorder, and how much:** Amazon Bedrock (Claude Haiku 4.5) reads 30-day sales history per product and suggests restock quantities daily, with reasoning in the user's language
3. **When something breaks:** SES emails the manager when stock drops below threshold; CloudWatch fires an SNS email when EC2 CPU spikes

Everything runs on AWS, deploys automatically on `git push`, and uses IAM role authentication, so no AWS keys live in code or environment.

---

## Architecture

```
                    GitHub Actions (push to main)
                              │
                              ▼ SSH deploy
   ┌──────────────────────────────────────────────┐
   │                EC2 (Ubuntu 24)               │
   │   Nginx :80  →  Gunicorn :5000  →  Flask     │
   │                       │                      │
   │              IAM Role (no keys)              │
   └────┬───────────┬────────────┬────────────┬───┘
        │           │            │            │
        ▼           ▼            ▼            ▼
      RDS         Bedrock       SES       CloudWatch
     MySQL    Claude Haiku   Email       CPU alarm
  (internal)  (daily cron)  alerts      → SNS
```

| Decision | Why |
|---|---|
| **EC2 + Nginx + Gunicorn** over App Runner | Full control over the stack; learning AWS fundamentals end-to-end |
| **RDS not publicly accessible** | MySQL port 3306 reachable only from the EC2 security group, never from the internet |
| **IAM role on EC2** over access keys | No credentials to leak, rotate, or commit |
| **Bedrock inference profile** (`jp.anthropic...`) | Standard model IDs fail for cross-region inference in `ap-northeast-1` |
| **Server-side language toggle** over localStorage | Bedrock predictions are rendered server-side, so the language must persist in Flask session |
| **SQLite locally, MySQL in production** | Zero-setup local dev with a real DB engine in production |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask (Application Factory + Blueprints) |
| Frontend | Jinja2, AdminLTE 3, Bootstrap 4 |
| Database | MySQL 8.4 on RDS (prod), SQLite (local) |
| Server | Ubuntu 24 EC2, Nginx, Gunicorn (3 workers), systemd |
| AI / ML | Amazon Bedrock: Claude Haiku 4.5 (JP inference profile) |
| Alerts | Amazon SES (low stock), CloudWatch + SNS (CPU) |
| CI/CD | GitHub Actions: auto-deploy on push to `main` |
| Auth | EC2 IAM Role: no hardcoded AWS credentials |
| i18n | Flask session-based EN/JA toggle |

---

## Features

- **Inventory CRUD:** add, edit, search by name/SKU, filter by stock status
- **Sales recording:** atomic stock deduction with oversell protection
- **AI restock predictions:** daily Bedrock cron job writes recommendations in EN and JA to the `predictions` table
- **Low-stock alerts:** SES email fires when a sale drops a product below threshold
- **CPU alarm:** CloudWatch and SNS email when EC2 CPU exceeds 80% for 1 minute
- **Bilingual UI:** full EN/JA toggle (UI strings, flash messages, Bedrock reasoning) persisted in Flask session
- **Role-based access:** admin role can write; employee/demo role is read-only, with admin UI hidden at template and route level
- **CI/CD:** push to `main` triggers GitHub Actions to SSH into EC2, pull, install, and restart the systemd unit

---

## Problems Solved During Build

These are the actual blockers I hit and how I worked through them. Each one was a real debugging session.

**Bedrock inference profile in Tokyo region.** Calling Bedrock with the standard model ID `anthropic.claude-haiku-4-5-20251001-v1:0` returned a cross-region inference error in `ap-northeast-1`. The fix was the Japan inference profile ID: `jp.anthropic.claude-haiku-4-5-20251001-v1:0`. Found in the Bedrock inference profile docs. Model IDs and inference profile IDs look nearly identical but behave differently in cross-region setups.

**Bilingual AI predictions returning English only.** UI toggled to Japanese but Bedrock kept replying in English. Root cause: language was stored only in `localStorage`, so the Flask dashboard route had no way to know which language to render. Fix: added a `/set-lang/<lang>` route to persist language in server-side session, and stored both `reason_en` and `reason_ja` in the `predictions` table so the dashboard can render the active language.

**GitHub Actions runner IPs are dynamic.** Tried IP-allowlisting port 22 to GitHub's runner range; it changes too often to maintain. Current setup: port 22 open to `0.0.0.0/0` at the security group, hardened at the OS level (password auth disabled, key-pair only via `sshd_config`). Not ideal. A self-hosted runner in a private subnet would be cleaner and is on the roadmap.

**Gunicorn and the factory pattern.** `app = create_app()` inside `if __name__ == '__main__':` is invisible to Gunicorn. Fixed by passing the factory directly: `gunicorn "app:create_app()"`. Easy fix once located, but the error message did not point at this clearly.

---

## Database Schema

```
products      id, name, sku, price, stock_quantity, minimum_stock_level, created_at, updated_at
sales         id, product_id, quantity_sold, sale_date
users         id, name, email, password_hash, role, created_at
predictions   id, product_id, recommended_restock_qty, reasoning, reason_en, reason_ja, predicted_at
```

**Stock status (computed live, never stored):**

- `OUT OF STOCK` → `stock_quantity == 0`
- `LOW STOCK` → `stock_quantity <= minimum_stock_level`
- `NORMAL` → `stock_quantity > minimum_stock_level`

**Sale flow (atomic):**

```
1. Validate available stock
2. INSERT sales row + UPDATE products.stock_quantity in one transaction
3. If stock insufficient → reject, no changes made
4. After commit → check threshold → SES alert if breached
```

---

## Security

- No AWS credentials in code or `.env`; EC2 uses IAM role `inventory-ec2-ses-role`
- `.env` is gitignored
- Passwords hashed with PBKDF2 (`werkzeug.security`)
- All routes behind `@login_required`; writes additionally behind `@admin_required`
- Demo account is read-only; admin UI hidden at template level and blocked at route level
- Port 5000 not exposed externally; all traffic routed through Nginx on port 80
- RDS port 3306 reachable only from the EC2 security group, never from the public internet
- SSH key-pair only (password auth disabled in `sshd_config`)

**Known gaps on the roadmap:**

- HTTP only (HTTPS requires a custom domain, planned)
- SSH port 22 open to `0.0.0.0/0` (tradeoff for GitHub Actions; self-hosted runner planned)

---

## Local Development

```bash
git clone https://github.com/amanrai00/inventory-system.git
cd inventory-system
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env       # SQLite by default, no MySQL setup needed
python scripts/init_db.py
python app.py              # http://127.0.0.1:5000/login
```

Local default login (seeded by `init_db.py`): `admin@company.com` / `admin123`. Change before any real use.

---

## Production Deployment

| Resource | Details |
|---|---|
| EC2 | `aman-inventory-prod`, Ubuntu 24, ap-northeast-1 |
| RDS | MySQL 8.4.8, `db.t4g.micro`, not publicly accessible |
| WSGI | Gunicorn (3 workers, factory pattern) |
| Process manager | systemd (`inventory.service`, auto-restart) |
| Reverse proxy | Nginx port 80 to Gunicorn port 5000 |
| IAM | `inventory-ec2-ses-role` (SES + CloudWatch + Bedrock) |

GitHub Actions (`.github/workflows/deploy.yml`) runs on every push to `main`: SSH into EC2, `git pull`, `pip install -r requirements.txt`, `systemctl restart inventory`.

<details>
<summary><b>Useful EC2 commands</b></summary>

```bash
# App status + live logs
sudo systemctl status inventory
journalctl -u inventory -f

# Manual deploy
git pull origin main && pip install -r requirements.txt && sudo systemctl restart inventory

# Run AI predictions manually
cd ~/inventory-system && source venv/bin/activate && python3 scripts/predict.py
tail -50 logs/predict.log

# Nginx
sudo nginx -t && sudo systemctl reload nginx

# Test CloudWatch alarm
aws cloudwatch set-alarm-state \
  --alarm-name "inventory-ec2-cpu-high" \
  --state-value ALARM \
  --state-reason "Manual test" \
  --region ap-northeast-1
```

</details>

---

## Project Structure

<details>
<summary><b>Click to expand</b></summary>

```
inventory-system/
├── .github/workflows/deploy.yml    # GitHub Actions CI/CD
├── database/
│   ├── client.py                   # DB abstraction (SQLite/MySQL)
│   ├── schema.sql                  # MySQL schema
│   └── schema_sqlite.sql           # SQLite schema
├── models/
│   ├── product.py                  # Product CRUD + stock status
│   ├── sale.py                     # Sale recording + stock deduction
│   └── user.py                     # User lookup + password hashing
├── routes/
│   ├── auth.py                     # Login, logout, /set-lang/<lang>
│   ├── dashboard.py                # Stats + AI predictions
│   ├── products.py
│   └── sales.py
├── scripts/
│   ├── init_db.py                  # DB init + admin seed
│   ├── import_csv.py               # Bulk import (100 products, 240 sales)
│   └── predict.py                  # Bedrock AI prediction (daily cron, bilingual)
├── static/
│   ├── css/style.css
│   └── js/i18n.js                  # EN/JA toggle (calls /set-lang/)
├── templates/
│   ├── base.html                   # AdminLTE shell
│   ├── dashboard.html              # AI Restock Recommendations
│   ├── products/
│   └── sales/
├── utils/email_alerts.py           # SES helper
├── app.py                          # Flask entry (factory pattern)
├── config.py                       # Reads from .env
└── requirements.txt
```

</details>

---

## Roadmap

**Done**

- [x] Production deployment: EC2, RDS, Nginx, Gunicorn, systemd
- [x] CI/CD pipeline: GitHub Actions auto-deploy on push to `main`
- [x] AI features: Bedrock daily restock predictions, bilingual EN/JA reasoning
- [x] Operations: SES low-stock alerts, CloudWatch CPU alarm → SNS
- [x] Access control: role-based admin/employee, demo account, IAM role auth
- [x] Architecture: Application Factory + Blueprints, dual-backend DB (SQLite/MySQL)
- [x] Seed data: 100 products + 240 sales

**Next**

- [ ] Automated test suite (pytest, smoke + integration coverage)
- [ ] HTTPS via Let's Encrypt + custom domain
- [ ] Self-hosted GitHub Actions runner (private subnet SSH)
- [ ] S3 product image uploads

---

<div align="center">

### Built by [Aman Rai](https://www.linkedin.com/in/amanrai00) · Tokyo

**AWS Certified Cloud Practitioner (CLF-C02)** · Studying for SAA-C03 · Building toward Cloud Engineer roles

[LinkedIn](https://www.linkedin.com/in/amanrai00) · [GitHub](https://github.com/amanrai00) · [AWS Badge](https://www.credly.com/badges/095a2b8e-c94f-4af6-b77c-51ec2fa64d56)

</div>
