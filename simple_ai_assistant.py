from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"), # ollama serve
    api_key=os.getenv("API_KEY")
)

messages = []
MAX_STEPS = 5

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
    step = 0
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
        
                model = os.getenv("MODEL"),
                messages = messages,
                tools = TOOLS
            )
        msg = response.choices[0].message
        if not msg.tool_calls:
            break

        if msg.tool_calls:
            messages.append(msg)
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                func_args = {}
                # handling errors while tool calling
                try:
                    func_args = json.loads(tool_call.function.arguments or "{}")
                    fn = FUNCTION_NAME_TO_FUNCTION_MAP.get(func_name)
                    result = fn(**func_args)
                except Exception as e:
                    result = f"Error while running {func_name} : {e}"
                messages.append(
                    {
                        "role" : "tool",
                        "tool_id" : tool_call.id,
                        "content" : str(result)
                    }
                )
    else:
        # we ran out of steps and the model did not gave a final answer
        fallback = "Sorry, This could not be finished within the given step limit"
        messages.append(
            {
                "role" : "assistant",
                "content" : fallback
            }
        )
        print("\nAssistant : " + fallback)
        continue

    messages.append(

        {
            "role" : "assistant",
            "content" : response.choices[0].message.content
        }
    )
    print("\nAssistant : " + response.choices[0].message.content)


