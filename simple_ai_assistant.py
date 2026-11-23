from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"), # ollama serve
    api_key=os.getenv("API_KEY")
)

messages = []
# giving personilty to the assistant
messages.append(
    {
        "role" : "system",
        "content" : "Act as a humble agent and always reply within 20 words"
    }
)
print("To Exit -> Enter /bye")
while True:

    user_input = input("\nYou : ")
    if user_input == "/bye":
        print("\nThanks for Having me!")
        break
    messages.append(
        {
            "role" : "user",
            "content" : user_input
        }
    )
    response = client.chat.completions.create(

        model = os.getenv("MODEL"),
        messages = messages
    )
    messages.append(

        {
            "role" : "assistant",
            "content" : response.choices[0].message.content
        }
    )
    print("\nAssistant : ")
    print(response.choices[0].message.content)


