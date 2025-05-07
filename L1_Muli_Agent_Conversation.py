from utils import get_openai_api_key
OPENAI_API_KEY = get_openai_api_key()

llm_config = { "model": "gpt-3.5-turbo"}

from autogen import ConversableAgent

agent = ConversableAgent(
    name="chatbot",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

reply = agent.generate_reply(
    messages=[{"content":"Tell me a Joke", "role":"user"}]
)
print(reply)
print("------")
reply = agent.generate_reply(
    messages=[{"content":"Repeat the joke.", "role": "user"}]
)
print(reply)