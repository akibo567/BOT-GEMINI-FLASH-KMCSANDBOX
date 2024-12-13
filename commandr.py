import cohere
import os
from dotenv import load_dotenv

def ask(system_message,user_message):
    load_dotenv()
    COHERE_API_KEY=os.environ['COHERE_API_KEY']
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
    return res.message.content[0].text
