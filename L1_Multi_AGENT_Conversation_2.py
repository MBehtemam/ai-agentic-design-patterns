from utils import get_openai_api_key
from autogen import ConversableAgent
from pprint import pprint
OPENAI_API_KEY = get_openai_api_key()

llm_config = { "model": "gpt-3.5-turbo"}

cathy = ConversableAgent(
    name="cathy",
    system_message="Your name is Cathy and"
    "and you are a stand-up comedian."
    "When you ready to end the conversation say 'I gotta go",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"]
)

joe = ConversableAgent(
    name="joe",
    system_message=
    "You name is Joe and you are a stand-up comedian."
    "Start the next joke from the punchline of the previous joke."
    "When you ready to end the conversation say 'I gotta go",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"]
)

chat_result = joe.initiate_chat(
    recipient=cathy,
    message="I'm Joe.Cathy, let's keep the jokes rolling",
    max_turns=2,
    summary_method="reflection_with_llm",
    summary_prompt="Summarize the conversation"
)

cathy.send(message="What's last joke we talked about", recipient=joe)

pprint(chat_result.chat_history)
pprint(chat_result.cost)
pprint(chat_result.summary)