# 概要

下記の要件を満たすよう実装した

1. 顧客デバイスから送信される位置情報データを dynamodb に収集するための API
2. 毎日 AM6 時に収集した位置情報を`example_output.csv`のように s3 に保存する
3. 毎日 AM6 時に s3 に作成された一覧を取得する API
4. 毎日 AM6 時に s3 に作成された csv ファイルをダウンロードするための API

## 環境構築

```sh
git clone https://github.com/yoshiyasugimoto/location_info_collection.git

cd location-info-collection
npm i && poetry install
touch .env
```

## デプロイ

```sh
cd location-info-collection
make deploy
```

## localhost:3003 を使って API 検証

```sh
make offline_api

# 概要の1の検証
make local_post

# 概要の2の検証
make local_output

# 概要の3の検証
local_bucket_list

# 概要の4の検証
make local_post
```
