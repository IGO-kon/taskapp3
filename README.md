# 在庫管理アプリ

Dockerで管理されたFlaskベースの在庫管理アプリケーションです。

## 機能

- ✅ 商品の追加・編集・削除
- 📊 在庫統計ダッシュボード
- 🔍 商品検索機能
- ⚠️ 低在庫アラート表示
- 💾 SQLiteデータベースによるデータ永続化

## 必要要件

- Docker
- Docker Compose

## セットアップと起動

### 1. Dockerコンテナのビルドと起動

```bash
docker-compose up -d --build
```

### 2. アプリケーションへのアクセス

ブラウザで以下のURLにアクセス:
```
http://localhost:5000
```

### 3. コンテナの停止

```bash
docker-compose down
```

### 4. データを保持したままコンテナを停止

```bash
docker-compose stop
```

### 5. コンテナの再起動

```bash
docker-compose start
```

## プロジェクト構造

```
taskapp3/
├── app.py                 # メインアプリケーション
├── requirements.txt       # Python依存パッケージ
├── Dockerfile            # Dockerイメージ設定
├── docker-compose.yml    # Docker Compose設定
├── .dockerignore         # Docker除外ファイル
├── templates/            # HTMLテンプレート
│   ├── base.html
│   ├── index.html
│   ├── add_item.html
│   ├── edit_item.html
│   └── search.html
└── static/              # 静的ファイル
    └── style.css
```

## 使い方

1. **商品の追加**: トップページの「新規追加」ボタンをクリック
2. **商品の編集**: 各商品の「編集」ボタンをクリック
3. **商品の削除**: 各商品の「削除」ボタンをクリック（確認ダイアログが表示されます）
4. **商品の検索**: ナビゲーションバーの「検索」から商品名・説明・カテゴリで検索

## データベース

- SQLiteを使用
- データは`inventory_data`という名前のDockerボリュームに永続化されます
- コンテナを削除してもデータは保持されます

## 開発モード

開発中にコードの変更を即座に反映させるため、ボリュームマウントが設定されています。
ファイルを編集すると自動的にアプリケーションが再読み込みされます。

## ログの確認

```bash
docker-compose logs -f
```

## トラブルシューティング

### ポート5000が既に使用されている場合

`docker-compose.yml`の`ports`セクションを変更:
```yaml
ports:
  - "8080:5000"  # 8080など別のポートに変更
```

### データベースをリセットしたい場合

```bash
docker-compose down -v  # ボリュームも削除
docker-compose up -d --build
```

## ライセンス

MIT