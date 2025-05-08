from utils import get_openai_api_key
from autogen import AssistantAgent

OPENAI_API_KEY = get_openai_api_key()

llm_config = { "model": "gpt-3.5-turbo"}

task = "Write a concise but engaging blogpost about"
"DeepLearning.ai. Make sure the blogpost is within 100 words."

writer = AssistantAgent(
    name="Writer",
    system_message="You are a writer. You write engaging and concise "
    "blogpost ( with title ) on give topics. You must polish your "
    "writing based on the feedback you receive and give a refined "
    "version. Only return your final work without additional comments.",
    llm_config=llm_config
)

reply = writer.generate_reply(messages=[{"content": task, "role": "user"}])

## Reflection part
critic = AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message="You are a critic. You review the work of "
    "the writer and provide constructive "
    "feedback to help improve the quality of the content."
)

res = critic.initiate_chat(
    name="Critic",
    recipient=writer,
    message=task, 
    max_turns=2,
    summary_method="last_msg"
)

## Adding SEO
SEO_reviewer = AssistantAgent(
    name="SEO Reviewer",
    llm_config=llm_config,
    system_message="You are a SEO reviewer, know for "
    "you ability to optimize content for search engines,"
    "ensuring that it ranks well and attracts organic traffic"
    "Make sure your suggestion is concise (within 3 bullet points),"
    "concrete and to the point"
    "Begin the review by stating your role."
)

## Adding legal reviewer 
legal_reviewer = AssistantAgent(
   name="Legal Reviewer",
   llm_config=llm_config,
   system_message="You are a legal reviewer, known for " 
   "you ability to ensure that content is legally compliant "
   "and free from any potential legal issues."
   "Make sure your suggestion is concise (within 3 bullet points),"
   "concrete and to the point."
   "Begin the review by stating your role."
)

ethics_reviewer = AssistantAgent(
    name="Ethics Reviewer",
    llm_config=llm_config,
    system_message="You are an ethics reviewer, known for "
    "your ability to ensure that content is ethically sound"
    "Make sure your suggestion is concise (withing 3 bullet points),"
    "concrete and to the point"
    "Begin the review by stating your role."
)

meta_reviewer = AssistantAgent(
    name="Meta Reviewer",
    llm_config=llm_config,
    system_message="You are a meta reviewer, you aggregate and review"
    "the work of the other reviewers and give a final suggestion on the content"
)

def reflection_message(recipient, messages, sender, config):
    return (f"Review the following content."
    f"\n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}")

review_chats = [
    {
     "recipient": SEO_reviewer, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}. Here Reviewer should be your role",},
     "max_turns": 1},
    {
    "recipient": legal_reviewer, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}.",},
     "max_turns": 1},
    {"recipient": ethics_reviewer, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'reviewer': '', 'review': ''}",},
     "max_turns": 1},
     {"recipient": meta_reviewer, 
      "message": "Aggregrate feedback from all reviewers and give final suggestions on the writing.", 
     "max_turns": 1},
]

critic.register_nested_chats(
    review_chats,
    trigger=writer
)

res= critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

print(res.summary)