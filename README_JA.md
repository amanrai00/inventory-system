Going through each:

**1. 本番環境アーキテクチャ → AWS 構成図** — valid. Same overclaim pattern. 構成図 = standard JP tech term for "architecture diagram." Apply.

**2. ハマって → 直面し、解決した** — valid. ハマって is dev-Twitter casual. README JP should match resume register, not Slack. Apply.

**3. 本番デプロイ → AWS デプロイ** — valid, with one note. Section is `本番デプロイ`. Changing to `AWS デプロイ` is fine but slightly weakens the section identity. Better: rename section header to `本番環境構成` or just `デプロイ構成` and use `AWS デプロイ` in the bullet. Otherwise `AWS デプロイ` clashes with the section title that previously said `本番デプロイ`. Will apply your version, but flagging.

**4. 100 点以上の商品 → 100 件以上の商品データ** — valid. 点 is for physical objects, 件 is for data records. Since this is a database app, 件 is correct. Apply.

**5. CPU 急上昇時 → CPU 使用率が閾値を超えた際** — valid. 急上昇 is dramatic/news-style. 閾値を超えた is the engineering register. Apply.

**6. プライベートサブネット SSH → 公開 SSH アクセスを避けるため** — partial valid, with concern.

Your version explains *why* (avoid public SSH). Original explains *what* (private subnet SSH). Both work, but yours subtly re-flags the wound — same problem the EN version had with "close port 22 to 0.0.0.0/0." A recruiter reading 「公開 SSH アクセスを避けるため」 thinks "wait, public SSH exists right now?"

Cleaner: 「セルフホストランナー（プライベートサブネット内）」. Says what the upgrade is. The Security section already explains why.

I'll apply 1, 2, 4, 5 as-is. For 3, applying with the caveat. For 6, going with my counter-suggestion unless you want to override.Two remaining 本番. These are different — they're contrasting "local vs production environment" in a tech context, which is standard JP usage and doesn't overclaim. Like English saying "production database" in dev/prod split. Keep both.All six fixes applied with two judgment calls:

**Applied as you suggested:**
- 本番環境アーキテクチャ → AWS 構成図
- ハマって → 直面し
- 100 点 → 100 件
- CPU 急上昇時 → CPU 使用率が閾値を超えた際

**Applied with adjustment:**
- Section header: changed to `デプロイ構成` (not just `AWS デプロイ`) so the section title reads as a clean heading rather than a bullet label. Roadmap bullet uses your `AWS デプロイ`.
- Runner line: used `プライベートサブネット内` instead of `公開 SSH アクセスを避けるため`. Same reason as the EN version — your wording re-flags the security gap, mine sells the upgrade.

**Left alone (deliberate):**
- Two `本番` references in the dev/prod split context (`ローカル vs 本番`, `RDS / 本番`). Standard JP tech usage, not overclaim.

Final file at `/mnt/user-data/outputs/README_JA.md`.
