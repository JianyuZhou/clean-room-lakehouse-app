
import time
from openai import OpenAI

class LLM:
    def __init__(self, base_model:str):
        self.client = OpenAI(
            api_key="<api-key>"
        )
        self.assistant = self.client.beta.assistants.create(
            name = "Clean Room Expert",
            instructions="You are a databricks architect that has deep understanding of databricks clean room, as you're the creator of it.",
            model = base_model
        )
        self.thread = self.client.beta.threads.create()

    
    
    def infer(self, user_query: str):
        self.client.beta.threads.messages.create(
            thread_id = self.thread.id,
            role = "user",
            content = user_query
        )

        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id，
            instructions=
        )

        print(f"thread_id: {self.thread.id}, assistant_id: {self.assistant.id}")
        while run.status != "completed":
            print(run.status)
            run = self.client.beta.threads.runs.retrieve(
                thread_id = self.thread.id,
                run_id = run.id
            )
            time.sleep(10)
        
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id,
        )
        return messages.data
    
    def fine_tune(self, knowlege:str):
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content = knowlege
        )
            

llm = LLM(base_model="gpt-3.5-turbo")
text = open("<file_name>", 'r').read()
llm.fine_tune(text)
answer = llm.infer("what is clean room?")
print(answer)