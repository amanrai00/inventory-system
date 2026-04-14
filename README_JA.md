# 在庫管理システム

> 🇬🇧 English version → [README.md](./README.md)

**Flask**・**Jinja2**・**AdminLTE 3** で構築した社内向け在庫管理ダッシュボードです。**AWS**（EC2 + RDS MySQL）上に本番デプロイ済みで、**Amazon Bedrock** による AI 需要予測、**Amazon SES** による低在庫メールアラート、**GitHub Actions** を使ったフルCI/CDパイプラインを備えています。

> **本番環境:** [http://35.77.96.153](http://35.77.96.153/login) — AWS EC2 · ap-northeast-1（東京）

---

## 技術スタック

| レイヤー | 技術 |
|---|---|
| バックエンド | Python 3、Flask（Blueprints構成） |
| フロントエンド | Jinja2、AdminLTE 3、Bootstrap 4 |
| データベース | MySQL 8.4（AWS RDS・本番）/ SQLite（ローカル開発） |
| サーバー | Ubuntu 24 EC2 · Nginx リバースプロキシ · systemd |
| AI / ML | Amazon Bedrock — Claude Haiku 4.5（jp 推論プロファイル） |
| アラート | Amazon SES（低在庫通知）· CloudWatch + SNS（CPU アラーム） |
| CI/CD | GitHub Actions — `main` ブランチへのプッシュで自動デプロイ |
| 認証 | IAM ロール（`inventory-ec2-ses-role`）— AWS キーのハードコードなし |

---

## 機能一覧

### アプリケーション基本機能
- セッション管理付きの社員ログイン・ログアウト
- ダッシュボード：総商品数・低在庫数・在庫切れ数・総売上数の一覧表示
- **商品管理** — 商品の追加・編集・名称／SKU検索・在庫ステータスフィルタリング
- **売上管理** — 売上登録と在庫自動控除、過剰販売防止
- 売上履歴の検索・日付範囲フィルタリング
- サーバーサイドバリデーション

### AWS 連携機能
- **Amazon SES** — 売上登録後に `stock_quantity` が `minimum_stock_level` を下回った場合、低在庫メールアラートを自動送信
- **CloudWatch アラーム** — EC2 の CPU 使用率を監視し、1分間連続で 80% を超えた場合に SNS 経由でメール通知
- **Amazon Bedrock（Claude Haiku 4.5）** — 毎日午前 2 時（EC2 時刻）のcronジョブが低在庫商品の過去30日分の売上実績を取得し、Bedrock を呼び出して `recommended_restock_qty`（推奨補充数量）と `reasoning`（根拠）を生成。結果は `predictions` テーブルに保存され、ダッシュボードに表示されます

---

## システムアーキテクチャ

```
ブラウザ
  │
  ▼
Nginx（ポート 80）
  │  リバースプロキシ
  ▼
Flask アプリ（ポート 5000・内部）
  │             │                │
  ▼             ▼                ▼
MySQL RDS    Amazon SES      Amazon Bedrock
（在庫DB）   （メールアラート）  （AI 需要予測）
                               │
                          CloudWatch
                    （CPU アラーム → SNS → メール）
```

---

## データベーススキーマ

```
products      — id, name, sku, price, stock_quantity, minimum_stock_level
sales         — id, product_id, quantity_sold, sale_date
users         — id, name, email, password_hash, role
predictions   — id, product_id, recommended_restock_qty, reasoning, predicted_at
```

**在庫ステータスのロジック:**
- `在庫切れ（OUT OF STOCK）` → `stock_quantity == 0`
- `低在庫（LOW STOCK）` → `stock_quantity <= minimum_stock_level`
- `正常（NORMAL）` → `stock_quantity > minimum_stock_level`

---

## プロジェクト構成

```
inventory-system/
├── .github/workflows/deploy.yml   # GitHub Actions CI/CD
├── database/
│   ├── client.py                  # SQLite ラッパー（ローカル開発用）
│   ├── schema.sql                 # MySQL スキーマ（本番用）
│   └── schema_sqlite.sql
├── logs/
│   └── predict.log                # Bedrock cron 実行ログ
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
│   ├── init_db.py                 # DB 初期化 + 管理者ユーザーのシード
│   ├── import_csv.py              # CSV 一括インポート
│   └── predict.py                 # Bedrock AI 需要予測スクリプト
├── static/
│   ├── css/style.css
│   └── js/app.js
├── templates/
│   ├── base.html
│   ├── dashboard.html             # AI 補充推奨セクションを含む
│   ├── login.html
│   ├── products/
│   └── sales/
├── utils/
│   └── email_alerts.py            # SES 低在庫アラートヘルパー
├── .env.example
├── app.py
├── config.py
└── requirements.txt
```

---

## ローカル開発環境のセットアップ

### 1. リポジトリのクローンと環境構築

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

### 2. 環境変数の設定

```bash
cp .env.example .env
```

ローカルの SQLite 開発用に `.env` を編集します：

```env
DB_BACKEND=sqlite
SQLITE_PATH=instance/inventory.db
FLASK_DEBUG=1
SECRET_KEY=任意の安全なキー
```

### 3. データベースの初期化

```bash
python scripts/init_db.py
```

### 4. 起動

```bash
python app.py
# ブラウザで http://127.0.0.1:5000/login を開く
```

**デフォルトログイン:** `admin@company.com` / `admin123`

---

## デプロイ構成（AWS）

| リソース | 詳細 |
|---|---|
| EC2 インスタンス | `aman-inventory-prod` — Ubuntu 24, ap-northeast-1 |
| パブリック IP | `35.77.96.153` |
| RDS エンドポイント | `inventory-db.cle6c28amu35.ap-northeast-1.rds.amazonaws.com` |
| RDS エンジン | MySQL Community 8.4.8（db.t4g.micro） |
| プロセス管理 | systemd（`inventory.service`） |
| リバースプロキシ | Nginx — ポート 80 → Flask ポート 5000（内部） |

GitHub Actions のワークフロー（`.github/workflows/deploy.yml`）が `main` ブランチへのプッシュを検知し、EC2 に SSH 接続・最新コードのプル・依存パッケージのインストール・Flask サービスの再起動を自動実行します。

---

## EC2 上でよく使うコマンド

```bash
# アプリの状態確認とログ
sudo systemctl status inventory
journalctl -u inventory -f

# 手動デプロイ
git pull origin main && pip install -r requirements.txt && sudo systemctl restart inventory

# AI 需要予測の手動実行
cd ~/inventory-system && source venv/bin/activate && python3 scripts/predict.py
tail -50 logs/predict.log

# Nginx の確認
sudo nginx -t && sudo systemctl reload nginx

# CloudWatch アラームの手動テスト
aws cloudwatch set-alarm-state \
  --alarm-name "inventory-ec2-cpu-high" \
  --state-value ALARM \
  --state-reason "手動テスト" \
  --region ap-northeast-1
```

---

## 実装ロードマップ

- [x] Flask アプリ（Blueprints 構成）
- [x] EC2 + RDS デプロイ（東京リージョン）
- [x] systemd によるプロセス管理（再起動後も自動起動）
- [x] Nginx リバースプロキシ
- [x] GitHub Actions CI/CD
- [x] SES 低在庫メールアラート
- [x] CloudWatch CPU アラーム → SNS 通知
- [x] Amazon Bedrock AI 需要予測（日次 cron）
- [ ] S3 商品画像アップロード
- [ ] HTTPS / SSL 証明書
- [ ] Gunicorn 本番 WSGI サーバー
- [ ] 自動テスト

---

## セキュリティに関する注意

- AWS の認証情報はハードコードなし — EC2 インスタンスは IAM ロール（`inventory-ec2-ses-role`）で認証
- `.env` は `.gitignore` に追加済みで GitHub には絶対にプッシュしない
- ポート 5000 は外部に公開していない — すべてのトラフィックは Nginx（ポート 80）を経由
- RDS セキュリティグループは EC2 セキュリティグループ（`inventory-sg`）からの MySQL 接続のみ許可
- SSH キーペア：`aman-inventory-prod-v2.pem`

---

## ライセンス

本プロジェクトはポートフォリオおよび学習目的で作成されています。