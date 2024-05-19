# Amaterus Crawler

## aptパッケージのインストール

```shell
sudo apt install ffmpeg libmagic1
```

## 設定ファイルの作成例

```yaml
global:
  hasura_url: "http://hasura.example.com"
  hasura_access_token: "MY_HASURA_ACCESS_TOKEN"
  # hasura_admin_secret: "my-hasura-admin-secret-key"
  # hasura_role: "my-hasura-role"
  youtube_api_key: "MY_YOUTUBE_API_KEY"
  s3_endpoint_url: "https://s3.example.com"
  s3_bucket: "my-example-bucket"
  s3_access_key_id: "MY_S3_ACCESS_KEY_ID"
  s3_secret_access_key: "MY_S3_SECRET_ACCESS_KEY"

server:
  host: "127.0.0.1"
  port: 8000

# TODO: schedule tasks like cron
tasks:
  - type: update_youtube_channel
    enabled: true

  - type: download_youtube_channel_thumbnail
    enabled: true
    options:
      object_key_prefix: youtube_channel_thumbnails/

  - type: search_youtube_channel_video
    enabled: true

  - type: update_youtube_video_detail
    enabled: true

  - type: download_youtube_video_thumbnail
    enabled: true
    options:
      object_key_prefix: youtube_video_thumbnails/
```

## GraphQL Code Generation

- Node 20
- [graphqurl](https://github.com/hasura/graphqurl) 1.0

```shell
npm install -g graphqurl
```

```shell
poetry run python dev_scripts/fetch_graphql_engine_schema.py
```

```shell
poetry run ariadne-codegen
```
