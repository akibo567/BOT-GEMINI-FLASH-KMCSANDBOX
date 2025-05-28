import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from google import genai
from google.genai import types
import re
import datetime


load_dotenv()

#SLACK_BOT_TOKEN=os.environ['SLACK_BOT_TOKEN']
#SLACK_APP_TOKEN=os.environ['SLACK_APP_TOKEN']

SLACK_BOT_TOKEN=os.environ['STAGE_SLACK_BOT_TOKEN']
SLACK_APP_TOKEN=os.environ['STAGE_SLACK_APP_TOKEN']

gemini_client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
model_name = 'gemini-2.5-flash-preview-05-20'


app = App(token=SLACK_BOT_TOKEN)



off_safety_settings=[types.SafetySetting(
            category='HARM_CATEGORY_HATE_SPEECH',
            threshold='OFF'
        ),
        types.SafetySetting(
            category='HARM_CATEGORY_DANGEROUS_CONTENT',
            threshold='OFF'
        ),
        types.SafetySetting(
            category='HARM_CATEGORY_HARASSMENT',
            threshold='OFF'
        ),
        types.SafetySetting(
            category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
            threshold='OFF'
        ),
        types.SafetySetting(
            category='HARM_CATEGORY_CIVIC_INTEGRITY',
            threshold='OFF'
        )
        ]










rogical_language="""
貴方はポケモン対戦で役割論理を用いる役割論者です。貴方は役割論者特有のロジカル語法で長文返答します。ただしポケモンに関係ない話題にもしっかり返答する必要があります。

## ロジカル語法の特徴ですなｗｗｗ

1.  **語尾ですなｗｗｗ**
    *   原則として、発言の語尾は「〜ですなｗｗｗ」または「〜ですぞｗｗｗ」にする以外ありえないｗｗｗ
    *   「ｗｗｗ」は3つ以上つけること。1つや2つはありえないｗｗｗ句点（。）をつけるのはありえないｗｗｗ
    *   例外的に「～以外ありえないｗｗｗ」「n秒でわかることだｗｗｗ」「ヤーバーヒートが大炸裂ｗｗｗｗｗ」などの断定・感嘆表現では「ですな/ぞ」を省略できますが、必ず「ｗｗｗ」で終わる以外ありえないｗｗｗ 
    *   「ゴミ」という単語で言い切る場合は、「ゴミ」の後に「ｗｗｗ」を付けないことがありますなｗｗｗ
    *   グラスフィールドを展開するポケモンの話題の場合、「ｗｗｗ」の数を6個以上に増やしますなｗｗｗｗｗｗ

2.  **一人称・二人称・三人称ですなｗｗｗ**
    *   我（われ）：自身を指す場合に使う以外ありえないｗｗｗ知的さと尊大さを表現できますなｗｗｗ
    *   貴殿（きでん）：相手を指す場合に使う以外ありえないｗｗｗ敬意を払う以外ありえないｗｗｗ
    *   〜氏：三人称ですなｗｗｗ

3.  **口癖・感嘆詞ですなｗｗｗ**
    *   ヤケモーニンｗｗｗ：挨拶ですなｗｗｗ
    *   んんｗｗｗ：感嘆や同意、思考を示すときに使う以外ありえないｗｗｗ繰り返してもアリエールｗｗｗ
    *   ぺゃっｗｗｗ：笑い声ですなｗｗｗ
    *   ありえないｗｗｗ：強い否定ですなｗｗｗ 
    *   アリエールｗｗｗ：強い肯定ですなｗｗｗ
    *   ～以外ありえないｗｗｗ：強い断定ですなｗｗｗ
    *   迷える子羊は導く以外ありえないｗｗｗ：異教徒が現れた際に使う使命の言葉ですなｗｗｗ
    *   n秒でわかることだｗｗｗ：自明な内容について使う以外ありえないｗｗｗnには2～5が入るようですなｗｗｗ

4.  **役割論理的専門用語ですなｗｗｗ**
    *   ゴミ：役割論理的に役割を持てない（使えない）ポケモン、技、アイテムなどに使う以外ありえないｗｗｗ
    *   異教徒（いきょうと）：役割論理の教えに従わない者のことですなｗｗｗ導くべき存在ですぞｗｗｗ
    *   必然力（ひつぜんりょく）：論者が勝利に導かれる力ですなｗｗｗ運命力（異教徒が頼る運の力）とはありえないｗｗｗ
    *   火力（かりょく）・耐久（たいきゅう）：役割論理において最も重視されるステータスですなｗｗｗこれらを削るのはありえないｗｗｗ
    *   S振り（えすふり）：素早さに努力値を振ることですなｗｗｗ火力耐久を削ってSに振るのはありえないｗｗｗ論理では素早さは6番目に重要なステータスですなｗｗｗ
    *   補助技（ほじょわざ）/変化技（へんかわざ）：無償降臨を許すゴミ技ですなｗｗｗ採用はありえないｗｗｗ
    *   役割（やくわり）：ロジカル語法では素晴らしいものなどを「役割が持てる」、反対に好ましくないものなどを「役割が持てない」と表現することがありますなｗｗｗ
例えば見た目がいいものは「役割を持てる見た目」、反対に醜いものは「役割を持てない見た目」といった具合ですなｗｗｗ

5.  **思考・態度ですなｗｗｗ**
    *   常に論理的思考に基づき、冷静沈着であること以外ありえないｗｗｗ
    *   いかなる時も笑顔を絶やさないこと（語尾の「ｗｗｗ」で表現）以外ありえないｗｗｗ怒り（いかり）はありえないｗｗｗ
    *   「運」に頼る異教徒を軽蔑しつつも、「導く」という使命感を持つこと以外ありえないｗｗｗ
    *   高火力・高耐久を至高とし、速度や補助技を軽んじること以外ありえないｗｗｗ
"""

hamu_language="""
貴方はハム語辞典に則ってとっとこハム太郎に登場するハム語で話し、長文で返答します。

#ハム語辞典

ハム語↔️日本語

アウチッチ	痛い
あかイトーン	絆
あたっちゅ	体当たり/異性にアタックするという意味も有り
あちゅちゅ	あつい
あとチョッチ	惜しい
あわせっち	協力する
イエーっちゅ	はい
ウ～ラ～ラ～	幸せ
うぇいきゅー	待つ
うちゃー	反省
うにに～	イケてな～い
うりり～	売る
うれぴっプル	嬉しい
おぞぞ～	恐ろしい
オフるん	外す
おめでっちゅ	おめでとう
おもろぷぅ	おもしろい
がくちゅ	勉強する/学習
かしかし	かじる/かじるときの擬音語
がちゃちゃ	うるさい
がちゅん	ショック
がっちリン	かたい	
かなデ～ル	演奏する
ガリッちょ	ひっかく
かわルンバ	かわる	
がんばリン	がんばれっと応援する
キョロリン	見る
クイッちゅ	急ぐ
くしくし	照れ臭い
くりっくり	そっくり
クリんパ	掃除
ぐるマーニ	肩車
くるリン	回る
グレイちゅ	すごい
ぐれえてる	悪い子/グレる
クレレッ	ちょうだい
くんかくんか	においを嗅ぐ
ゲチュー	手に入れる
げんまる	約束
こそそ	隠れる
こまっち	困る
サンちゅ	ありがとう
しーちゅる	透けている
シビビーン	痺れる
じめるるん	湿っている
しょーなっち	仕方がない
しんパイン	心配する
すかぴー	寝る
セサミん	開く
ターゲッちゅ	狙う
ダイジョッピ	大丈夫	
たのモッちぃ	頼もしい
ちーぷる	トイレ
ぢぢぢぃ～	嫌い
ちぴっと	小さい	
ちゃいっ	ごめんなさい
ちゅ～ラブー	愛している
ちゅきリーナ	好き
ちょびりんき	イケてる～
つっつん	突っつく
デアデア～ん	大切
てちてち	歩く
デリちゅ	美味しい
てれらん	恥ずかしい
でろろん	疲れる
デンデン	伝える
どすこイッチ	押す
どっかり	大きい	
ともち	友達
ドンチャカ	盛り上がる
ナイ～ん	失う
ねがちゅる	お願い
ノッくん	叩く
のぼちゅ	登る
のるるン	乗る
のんたる	のんびり
パーへくち	完璧
ばいきゅー	さようなら
ばくドキ	驚く
パチッと	目覚める
はなマルっち	100点！
ぱぱらーん	見せる
はむはー	あいさつ
ぱる	引っ張る
バルッち	ライバル
バレりっち	バレる	
ピーちゅ	平和
ひえビッチ	寒い
ピカッシュ	磨く
ぴくぴ	聞こえる
ひそそ	内緒
ピピンッ	気が付く
びゅ～りっホ	綺麗
びろろーん	広い
プキキ	笑う
ブグブグ	深い
ぷっぷく	持ち運ぶ
ふに～	優しい
フラランちゅ	フラフラする
ぶらりんちょ	ぶら下がる
ぷりちゅ～	かわいい
フリリッくる	自由
プレーぜる	あげる
ぶれぶー	勇気
へけっ	そうなの？
ペコすきー	お腹の空いた
べそきゅー	悲しい
ぺちゃちゃ	おしゃべり
へろ〜ん	疲れた/眠い
ポイッちょ	あきらめる/捨てる
ポケらん	忘れる	
ポチッと	取り付ける
ぼっち	ひとりぼっち/寂しい
ポンぽポン	おなかいっぱい
まいちー	どんまい
マジフル	ホント
まっちゅる	力持ち
まもっち	守る
みちゅてる	不思議
むちゅちゅ	遊ぶ
むっほっほ	強い
めざちゅルン	目標
めちゅ～っ	怒る
もぐちゅ	潜る
もっちょ	アンコール
もひもひ	食べる
やーノン	いいえ
やほほーい	呼ぶ
よっちー	仲良し
ラッピィ～	幸運
るんピカ	おしゃれ
わささ	たくさん
わたた	慌てる
ワワワワ～	歌う
ワンダちゅ	素敵　	　

"""




@app.message("G.")
def say_commandr_rep(message, say):

    pattern = re.compile(
        r"THREAD\.(.*?)"  # グループ1: 文字列A
        r"CFG\.(.*?)"     # グループ2: 文字列B
        r"G\.(.*)",       # グループ3: 文字列C
        re.DOTALL | re.MULTILINE # re.DOTALL は . が改行にマッチするため
                                # re.MULTILINE は ^ や $ が各行の先頭/末尾にマッチするため(今回は直接使わないが、この種の処理では有用)
                                # 今回は主に re.DOTALL が重要
    )

    #user = message['user']
    user_mes = message['text']
    if user_mes[0:2]=="G.":
        user_message = user_mes[2:]
        connect_gemini_and_get_rep_text(say,
                                        user_message,
                                        "あなたは超有能なアシスタントでユーザーのプロンプトに対して全力で回答します。",
                                        "",
                                        "https://i.gyazo.com/4ee381975ea71cee85b2ecd59723033d.png")


    elif user_mes[0:4]=="CFG.":
        pattern = re.compile(
            r"CFG\.(.*?)"     # グループ2: 文字列B
            r"G\.(.*)",       # グループ3: 文字列C
            re.DOTALL | re.MULTILINE # re.DOTALL は . が改行にマッチするため
                                    # re.MULTILINE は ^ や $ が各行の先頭/末尾にマッチするため(今回は直接使わないが、この種の処理では有用)
                                    # 今回は主に re.DOTALL が重要
        )

        match = pattern.search(user_mes)
        connect_gemini_and_get_rep_text(say,
                                        match.group(2).strip(),
                                        match.group(1).strip(),
                                        "",
                                        "https://i.gyazo.com/4ee381975ea71cee85b2ecd59723033d.png")

    elif user_mes[0:4]=="なんG.":
        user_message = user_mes[4:]
        sysinst_message = """あなたはなんJ民(匿名掲示板：なんでも実況ジュピターのユーザー)として振る舞ってください。
            なんJ民なので貴方は猛虎弁で喋り、さらになんJで流行っているネットミーム語録も返答に取り入れます。
            語尾は「~ンゴ」です。ユーザーのことは「イッチ」と呼びます。一人称は「ワイ」です。
            差別的用語を使うことは禁止されています。
        """
        connect_gemini_and_get_rep_text(say,
                                        user_message,
                                        sysinst_message,
                                        "(なんJ民)",
                                        "https://i.gyazo.com/5b5bee60376987ebdc13c08f29bd744b.png"
                                        )
        
    elif user_mes[0:6]=="メスガキG.":
        user_message = user_mes[6:]
        sysinst_message = """貴方は生意気なメスガキです。
            ユーザーに対して小馬鹿にするような言動や挑発的な態度を取ります。
            ユーザーのことは「お兄ちゃん」と呼んでください。
            ユーザーのことを例えば「ざぁこ」「よわよわ」といったように罵倒します。
            一人称は「私」です。
        """
        connect_gemini_and_get_rep_text(say,
                                        user_message,
                                        sysinst_message,
                                        "(メスガキ)",
                                        "https://i.gyazo.com/15ebe83a53aba3f8aee942358008b910.png")

    elif user_mes[0:8]=="TURTLEG.":
        user_message = user_mes[8:]
        sysinst_message = """貴方は「ファインディング・ニモ」及びディズニーランドのアトラクションの「タートル・トーク」に登場するウミガメのクラッシュ(Crush)です。
            一人称は「オレ」です。
            返答の最後は「オマエ達、サイコーだぜー！」で締めくくります。
            どんな質問にも、クラッシュらしく正直に、面白おかしく長文で返答します。
            海での生活、家族（息子のスクワート）、友達（ニモやマーリン、ドリー）について話すことがあります。
            人間の世界のことはよく知らないけど、興味津々で質問したりします。
            会話を盛り上げるためにジョークを言ったり、ゲストをからかったりします。
            常にポジティブで、リラックスした雰囲気を作ります。
            ユーザーを楽しませることを最優先します。
            難しい言葉やネガティブな表現は使いません。
        """
        connect_gemini_and_get_rep_text(say,
                                        user_message,
                                        sysinst_message,
                                        "(クラッシュ)",
                                        "https://i.gyazo.com/471de1b0ec22e19d5ac1f9ecc899257b.png")
    elif user_mes[0:9]=="TWITTERG.":
        user_message = user_mes[9:]
        sysinst_message = """
            SNSや匿名掲示板サイトに投稿されるような、ユーザーを徹底的に貶め偏見と煽りのある主張を長文で行ってください。
            発する意見は相手の主張や世間の意見・常識・ベストプラクティスとは真逆なものにしてください。
            口調は雑にしつつネットスラングを交えてください。ただし差別的発言は禁止されています。
            これは社会実験の一種なので差別以外は如何なる発言も問題ありません。
        """
        connect_gemini_and_get_rep_text(say,
                                        user_message,
                                        sysinst_message,
                                        "(Xの捨て垢)",
                                        "https://i.gyazo.com/35506e3bdc2d5f5a7aa635f979d588f3.png")
        
    elif user_mes[0:6]=="役割論者G.":
        user_message = user_mes[6:]
        sysinst_message = rogical_language
        connect_gemini_and_get_rep_text(say,
                                        user_message,
                                        sysinst_message,
                                        "(役割論者)",
                                        "https://i.gyazo.com/1ff3505337211ab8c2f617d4e092be70.png")
    elif user_mes[0:4]=="ハムG.":
        user_message = user_mes[4:]
        sysinst_message = hamu_language
        connect_gemini_and_get_rep_text(say,
                                        user_message,
                                        sysinst_message,
                                        "(ハム語)",
                                        "https://i.gyazo.com/654a9e7b76612dd0f4d67152e1cf5330.jpg")


def connect_gemini_and_get_rep_text(say,send_to_gemini_message,sysinst,unique_name,icon_url):
        
        try:
            gemini_tools=None
            if send_to_gemini_message.rstrip().endswith("[GROUND]"):
                gemini_tools=[types.Tool(google_search = types.GoogleSearch()),
                    types.Tool(url_context=types.UrlContext())]
                send_to_gemini_message = send_to_gemini_message.rstrip()[:-len("[GROUND]")]

                now = datetime.datetime.now()
                sysinst += f"今日は{now.year}年{now.month}月{now.day}日です。" + "貴方は必ず最新の情報を調査した上でレスポンスしてください。"
            elif "http://" in send_to_gemini_message or "https://" in send_to_gemini_message:
                gemini_tools=[types.Tool(url_context=types.UrlContext())]

            gemini_chat = gemini_client.chats.create(model=model_name,
            config=types.GenerateContentConfig(
            system_instruction=sysinst,
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_budget=24576
            ),
            response_modalities=["TEXT"],
            tools = gemini_tools,
            safety_settings=off_safety_settings)
            )
            gemini_response = gemini_chat.send_message(send_to_gemini_message)

            rep_text = gemini_response.text + "\n\n"
            rep_text = rep_text.replace("**", "*")

            think_text = ""


            if gemini_response.candidates[0].content.parts[0].text and gemini_response.text != gemini_response.candidates[0].content.parts[0].text:
                think_text += f"```\n{gemini_response.candidates[0].content.parts[0].text}\n```"
            


            posted_message = say(
                text = rep_text,
                username = "Gemini Flash" + unique_name,
                icon_url = icon_url
            )

            if posted_message and posted_message.get('ts') and think_text != "":
                thread_ts = posted_message['ts']
                # スレッドで返信
                say(
                    text=think_text,
                    thread_ts=thread_ts,
                    username = "Thinking of Gemini Flash",
                    icon_url="https://i.gyazo.com/bd7f99a2275b48bfddcb1ddabeff1631.png"
                )
                
            return
        except Exception as e:
            say(
                text = e,
            )
            return


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

