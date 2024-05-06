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

# TODO: rename runners -> tasks
# TODO: schedule tasks like cron
runners:
  - type: update_youtube_channel
    enabled: true

  - type: download_youtube_channel_icon
    enabled: true
    options:
      object_key_prefix: youtube_channel_icons/
```
