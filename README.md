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
  youtube_api_key: "MY_YOUTUBE_API_KEY"

runners:
  - type: update_youtube_channel
    enabled: true
```
