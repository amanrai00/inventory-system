# 在庫管理システム

> 🇬🇧 English version → [README.md](./README.md)

**Flask**・**Jinja2**・**AdminLTE 3** で構築した社内向け在庫管理ダッシュボードです。**AWS**（EC2 + RDS MySQL）上に本番デプロイ済みで、**Amazon Bedrock** による AI 需要予測、**Amazon SES** による低在庫メールアラート、**CloudWatch** による EC2 CPU 監視、**GitHub Actions** を使ったフル CI/CD パイプラインを備えています。

> **本番環境:** [http://35.77.96.153](http://35.77.96.153/login) — AWS EC2 · ap-northeast-1（東京）

-----

## 技術スタック

|レイヤー   |技術                                                  |
|-------|----------------------------------------------------|
|バックエンド |Python 3、Flask（Application Factory + Blueprints）    |
|フロントエンド|Jinja2、AdminLTE 3、Bootstrap 4、Font Awesome          |
|データベース |MySQL 8.4（AWS RDS・本番）/ SQLite（ローカル開発）               |
|サーバー   |Ubuntu 24 EC2 · Nginx リバースプロキシ · systemd            |
|AI / ML|Amazon Bedrock — Claude Haiku 4.5（jp 推論プロファイル）      |
|アラート   |Amazon SES（低在庫メール）· CloudWatch + SNS（CPU アラーム）      |
|CI/CD  |GitHub Actions — `main` ブランチへのプッシュで自動デプロイ           |
|認証     |IAM ロール（`inventory-ec2-ses-role`）— AWS 認証情報のハードコードなし|

-----

## 機能一覧

### アプリケーション基本機能

- セッション管理付きの社員ログイン・ログアウト
- ダッシュボード：総商品数・低在庫数・在庫切れ数・総売上数の一覧表示
- **商品管理** — 商品の追加・編集・名称／SKU 検索・在庫ステータスフィルタリング
- **売上管理** — 売上登録・在庫自動控除・過剰販売防止
- 売上履歴の検索・日付範囲フィルタリング
- サーバーサイドバリデーション
- 在庫ステータスは動的に算出 — 常にリアルタイムの在庫状態を反映

### AWS 連携機能

- **Amazon SES** — 売上登録後に `stock_quantity` が `minimum_stock_level` を下回った際、低在庫メールアラートを自動送信
- **CloudWatch アラーム** — EC2 の CPU 使用率を監視し、1分間連続で 80% を超えた場合に SNS 経由でメール通知
- **Amazon Bedrock（Claude Haiku 4.5）** — 毎日午前 2 時（EC2 時刻）の cron ジョブが低在庫商品の過去 30 日分の売上実績を取得し、Bedrock を呼び出して `recommended_restock_qty`（推奨補充数量）と `reasoning`（根拠）を生成。結果は `predictions` テーブルに保存され、ダッシュボードの「AI 補充推奨」セクションに表示

-----

## システムアーキテクチャ

```
+----------------------------------------------------------------+
|                  開発者 (Developer)                            |
|              コードを編集して git push -> main                 |
+------------------------------+---------------------------------+
                               |
                               v
+----------------------------------------------------------------+
|             GitHub Actions  (CI/CD パイプライン)               |
|   SSH接続 -> 最新コード取得 -> 依存関係インストール -> 再起動   |
+------------------------------+---------------------------------+
                               |
                               v
+----------------------------------------------------------------+
|        EC2 本番サーバー  aman-inventory-prod (東京)            |
|                                                                |
|   ブラウザ -> Nginx (80番) -> Flask アプリ (5000番 内部のみ)   |
|                                                                |
|        IAM ロール認証 (AWSキーのハードコードなし)              |
+------------+---------------------------------------------------+
             |                         |
             v                         v
+--------------------+   +------------------------------------+
|   RDS MySQL 8.4    |   |        AWS 連携サービス            |
|   在庫データベース  |   |                                    |
|   (東京リージョン) |   |  SES      -> 低在庫メール自動送信  |
+--------------------+   |  Bedrock  -> AI補充数量予測(毎朝2時)|
                         |  CloudWatch-> CPU監視 SNSアラート  |
                         +------------------------------------+
```


-----

## データベーススキーマ

```
products     — id, name, sku, price, stock_quantity, minimum_stock_level, created_at, updated_at
sales        — id, product_id, quantity_sold, sale_date
users        — id, name, email, password_hash, role, created_at
predictions  — id, product_id, recommended_restock_qty, reasoning, predicted_at
```

**在庫ステータスのロジック:**

- `在庫切れ（OUT OF STOCK）` → `stock_quantity == 0`
- `低在庫（LOW STOCK）` → `stock_quantity <= minimum_stock_level`
- `正常（NORMAL）` → `stock_quantity > minimum_stock_level`

**売上登録フロー:**

1. 社員が商品と数量を選択
1. システムが在庫数を検証
1. 在庫が十分な場合 → 売上レコードを挿入し `stock_quantity` をアトミックに減算
1. 在庫が不足する場合 → エラーを返し、データは変更しない

-----

## プロジェクト構成

```
inventory-system/
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions CI/CD
├── database/
│   ├── client.py              # DB 抽象化レイヤー（ローカル開発用 SQLite）
│   ├── schema.sql             # MySQL スキーマ（本番用）
│   └── schema_sqlite.sql      # SQLite スキーマ（ローカル開発用）
├── logs/
│   └── predict.log            # Bedrock cron ジョブの実行ログ
├── models/
│   ├── product.py             # 商品 CRUD + 在庫ステータスロジック
│   ├── sale.py                # 売上登録 + 在庫控除
│   └── user.py                # ユーザー検索 + パスワードハッシュ
├── routes/
│   ├── auth.py                # ログイン・ログアウト・@login_required デコレータ
│   ├── dashboard.py           # ダッシュボード統計 + AI 予測
│   ├── products.py            # 商品 CRUD ルート
│   └── sales.py               # 売上登録・履歴ルート
├── scripts/
│   ├── init_db.py             # DB 初期化 + 管理者ユーザーのシード
│   ├── import_csv.py          # CSV 一括インポート（商品 100件・売上 240件）
│   └── predict.py             # Bedrock AI 需要予測（日次 cron）
├── static/
│   ├── css/style.css
│   └── js/app.js
├── templates/
│   ├── base.html              # AdminLTE シェル（サイドバー + ナビバー）
│   ├── dashboard.html         # AI 補充推奨セクションを含むダッシュボード
│   ├── login.html
│   ├── products/              # 一覧・追加・編集テンプレート
│   └── sales/                 # 売上登録・履歴テンプレート
├── utils/
│   └── email_alerts.py        # SES 低在庫アラートヘルパー
├── .env.example
├── .gitignore
├── app.py                     # Flask エントリーポイント（ファクトリパターン）
├── config.py                  # .env から設定を読み込む
└── requirements.txt
```

-----

## ローカル開発環境のセットアップ

### 1. クローンと仮想環境の構築

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

ローカルのデフォルト設定（SQLite — MySQL 不要）:

```env
DB_BACKEND=sqlite
SQLITE_PATH=instance/inventory.db
FLASK_DEBUG=1
SECRET_KEY=任意の安全なキーに変更してください
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

**デモ用デフォルトログイン:** `admin@company.com` / `admin123`
*（実運用環境では必ずパスワードを変更してください）*

-----

## 本番デプロイ構成（AWS）

|リソース       |詳細                                                          |
|-----------|------------------------------------------------------------|
|EC2 インスタンス |`aman-inventory-prod` — Ubuntu 24, ap-northeast-1（東京）       |
|パブリック IP   |`35.77.96.153`                                              |
|RDS エンドポイント|`inventory-db.cle6c28amu35.ap-northeast-1.rds.amazonaws.com`|
|RDS エンジン   |MySQL Community 8.4.8、db.t4g.micro                          |
|プロセス管理     |systemd（`inventory.service`）— 再起動後も自動起動                     |
|リバースプロキシ   |Nginx — ポート 80 → Flask ポート 5000（内部のみ）                       |
|IAM ロール    |`inventory-ec2-ses-role`（SES + CloudWatch + Bedrock）        |

GitHub Actions（`.github/workflows/deploy.yml`）が `main` ブランチへのプッシュを検知し、EC2 に SSH 接続・最新コードのプル・依存パッケージのインストール・Flask サービスの再起動を自動実行します。

-----

## EC2 上でよく使うコマンド

```bash
# アプリの状態確認とライブログ
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

-----

## 実装ロードマップ

- [x] Flask アプリ — Application Factory + Blueprints
- [x] SQLite（ローカル）+ MySQL（本番）デュアルバックエンド対応
- [x] EC2 + RDS デプロイ — 東京リージョン
- [x] Nginx リバースプロキシ
- [x] systemd プロセス管理（再起動後も自動起動）
- [x] GitHub Actions CI/CD パイプライン
- [x] Amazon SES 低在庫メールアラート
- [x] CloudWatch EC2 CPU アラーム → SNS メール通知
- [x] Amazon Bedrock AI 需要予測（日次 cron・ダッシュボード表示）
- [x] CSV から商品 100件・売上 240件をインポート
- [ ] S3 商品画像アップロード
- [ ] HTTPS / SSL 証明書（Let’s Encrypt）
- [ ] Gunicorn 本番 WSGI サーバー
- [ ] ロールベースアクセス制御（管理者 vs 社員）
- [ ] 自動テスト

-----

## セキュリティ

- AWS 認証情報はハードコードなし — EC2 は IAM ロールで認証
- `.env` は `.gitignore` 済みで GitHub には絶対にプッシュしない
- パスワードは `werkzeug.security` の PBKDF2 でハッシュ化
- 全ルートに `@login_required` デコレータを適用
- ポート 5000 は外部に非公開 — 全トラフィックは Nginx（ポート 80）を経由
- RDS セキュリティグループは EC2 セキュリティグループからの接続のみ許可
- SSH アクセスはキーペアのみ

-----

## ライセンス

本プロジェクトはポートフォリオおよび学習目的で作成されています。