import time
import json
from openai import OpenAI

# Get API key from api_key.txt
f = open("api_key.txt")
API_KEY = f.read().strip()
client = OpenAI(api_key=API_KEY)

# Fetch the assistant if there is one with the given name
# Otherwise, make a new one with the documentation file provided
assistant_name = "Clean Room Bot"
assistant = next((x for x in client.beta.assistants.list() if x.name == assistant_name), None)
if assistant is None:
    assistant = client.beta.assistants.create(
        name=assistant_name,
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo",
        description="You are a chatbot to help users understand Databricks Clean Rooms. There will be a set of "
                    "messages giving you information about clean rooms in the form of files, and then you can reply "
                    "to questions."
    )

# Read file
data_files = "data.json"
f = open(data_files)
info_dump = json.load(f)
messages = [
    {
        "role": "user",
        "content": f"{info['contents']}"
    } for info in info_dump
]
messages.append({
    "role": "user",
    "content": "There will be no further information. Please use previous information to answer questions from now on."
})

# Make a thread for the conversation
thread = client.beta.threads.create(
    messages=messages
)
print("Hi! I'm a chat bot to help you with Clean Rooms.")

while True:

    # Get input
    question = input(">> ")
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )

    # Make the run
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id
    )

    # Wait for run to complete
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(0.1)

    # Get messages and print output
    messages = client.beta.threads.messages.list(
      thread_id=thread.id
    )
    print(messages.data[0].content[0].text.value)
