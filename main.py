from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

import os

app = Flask(__name__)

# チャネルシークレットを設定
YOUR_CHANNEL_SECRET = "d2f3ffeb3ca5fc872f3254faba1326b2"
# チャネルアクセストークンを設定
YOUR_CHANNEL_ACCESS_TOKEN = "zcykfWZXMJOEFL737EkziA7Wjup3zAnWpVmZGX4K0jfeuHEnvExsUjGg0AFmczL5oya0Vlt+27Y50F0fyWWWYA3kaMrUesYrnrw7KkuQqMkUMEW5J2kGeXabLKXA5xOKstDKFV/ul0wHAg26LXQ6DAdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# https://example.herokuapp.com/callback にアクセスされたら以下の関数を実行する
@app.route("/callback", methods=['POST'])
def callback():
    # アクセス時に送られてきたデータ「X-Line-Signature」を代入
    signature = request.headers['X-Line-Signature']

    # アクセス時に送られてきたデータの主な部分を代入
    body = request.get_data(as_text=True)

    # try 内でエラーが発生したら except の文を実行
    try:
        # ハンドラーに定義されている関数を呼び出す
        handler.handle(body, signature)
    # もし「InvalidSigunatureError」というエラーが発生したら、以下のプログラムを実行
    except InvalidSignatureError:
        # リクエストを送った側に400番(悪いリクエストですよー！)を返す
        abort(400)

    # すべて順調にいけば、リクエストを送った側に「OK」と返す
    return "OK"

# ハンドラーに定義されている関数
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ここにメッセージの内容による処理を書いていこう

    # メッセージの種類が「テキスト」なら
    if (event.type == "message"):
        response_message = ""

    # event.message.text という変数にメッセージの内容が入っている
        if (event.message.text == "開始"):
            response_message = "ルール・応答の文頭に質問数を入力してください 例：１はい、（応答分）\n 始めます \n 質問１\n どうして当社に応募したのですか？"

        elif (event.message.text  .startswith(("1","１"))):
            a1=event.message.text
            response_message = "質問２\n当社に対してどんな印象を持っていますか？"

        elif (event.message.text .startswith(("2","２"))):
            a2=event.message.text
            response_message = "質問３\n当社の店（商品）を利用したことがありますか？"
        
        elif (event.message.text .startswith(("3","3"))):
            a3=event.message.text
            response_message = "質問４\nほかにはどんな会社を受けましたか？"

        elif (event.message.text .startswith(("4","4"))):
            a4=event.message.text
            response_message = "質問は終わりです面接練習を終了します \n 書いた文章を見直して面接本番に備えよう！"
        else:
            response_message = "その言葉はわかりません。"

        # 返信文を送信
        # response_message の中に入っている文を返す
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=response_message)
            ]
        )

# ポート番号を環境変数から取得
port = os.getenv("PORT")
app.run(host="0.0.0.0", port=port)