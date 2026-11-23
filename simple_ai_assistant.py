from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"), # ollama serve
    api_key=os.getenv("API_KEY")
)


print("To Exit -> Enter /bye")
while True:

    user_input = input("\nYou : ")
    if user_input == "/bye":
        print("\nThanks for Having me!")
        break
    response = client.chat.completions.create(

        model = os.getenv("MODEL"),
        messages = [
            {
                "role" : "user",
                "content" : user_input

            }
        ]
    )
    print("\nAssistant : ")
    print(response.choices[0].message.content)


