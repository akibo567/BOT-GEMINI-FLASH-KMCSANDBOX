import cohere
import os
from dotenv import load_dotenv

def ask(system_message,user_message):
    load_dotenv()
    COHERE_API_KEY=os.environ['COHERE_API_KEY']
    res_mes=""
    try:
        co = cohere.ClientV2(api_key=COHERE_API_KEY)

        res = co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": user_message,
                },
            ],  # "Designing Perfect APIs"
        )
        res_mes=res.message.content[0].text
    except Exception as e:
        res_mes = str(e)
    return res_mes
