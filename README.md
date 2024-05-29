# ISBN番号で書籍データを検索するアプリ

このStreamlitアプリケーションは、Google Books APIを使用してISBN番号から書籍データを検索します。ユーザーは、手動でISBN番号を入力するか、カメラや画像からバーコードを読み取ってISBN番号を取得できます。

## 必要なもの

- Python 3.x
- Streamlit
- requests
- opencv-python
- pyzbar
- Pillow
- streamlit-webrtc

## インストール

必要なパッケージをインストールするために、以下のコマンドを実行してください：

```sh
pip install streamlit requests opencv-python pyzbar Pillow streamlit-webrtc
```

## 使用方法
Google Books APIキーを取得します。以下の手順に従ってAPIキーを取得してください：

Google Cloud Consoleにアクセスします。
プロジェクトを作成または選択します。
「APIとサービス」 > 「ライブラリ」に移動し、「Google Books API」を検索して有効にします。
「APIとサービス」 > 「認証情報」に移動し、「認証情報を作成」ボタンをクリックしてAPIキーを作成します。
作成されたAPIキーをコピーして保存します。
アプリケーションを実行します：
```sh
streamlit run app.py
```

## ブラウザが自動的に開きます。開かない場合は、以下のURLを手動でブラウザに入力してください：
```
http://localhost:8501
```

Google Books APIキーを入力します。

ISBN番号の入力方法を選択します：

ISBN番号を入力: 手動でISBN番号を入力します。
カメラでバーコードを読み取る: カメラを使用してバーコードを読み取ります。
画像からバーコードを読み取る: バーコードを含む画像ファイルをアップロードします。
ISBN番号を入力またはバーコードを読み取ると、書籍情報が表示されます。

## ファイル構成
app.py: アプリケーションのメインスクリプト。
requirements.txt: 必要なPythonパッケージのリスト。
requirements.txt
以下は、必要なパッケージを記載した requirements.txt ファイルの内容です：
```
streamlit
requests
opencv-python
pyzbar
Pillow
streamlit-webrtc
```
## バージョン情報
バージョン 1.1.0変更点: Google Books APIからOpenBD APIに変更しました。理由: OpenBDは日本の書籍情報をより豊富に提供するため、Google Books APIに比べて日本の書籍検索に適しています。
バージョン 1.0.0初回リリース。Google Books APIを使用して書籍情報を取得する機能を提供。

## トラブルシューティング
### エラー: 403 Forbidden
Google Books APIキーが無効であるか、適切な権限がない場合、このエラーが発生することがあります。
APIキーの制限を確認し、必要に応じて制限を緩和してください。
### 書籍情報が見つからない
ISBN番号が正しいことを確認してください。
入力したISBN番号がGoogle Books APIで検索可能な書籍であることを確認してください。

# 貢献
このプロジェクトに貢献する場合は、プルリクエストを送信してください。バグ報告や機能リクエストも歓迎します。

# ライセンス
このプロジェクトはMITライセンスの下で公開されています。詳細については、LICENSEファイルを参照してください。
```
このMarkdownファイルをREADME.mdとして保存し、プロジェクトのルートディレクトリに配置することで、GitHubなどのプラットフォームでプロジェクトの概要と使用方法を簡単に共有することができます。
```
