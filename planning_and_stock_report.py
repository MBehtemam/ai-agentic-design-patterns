from utils import get_openai_api_key
import autogen

OPENAI_API_KEY = get_openai_api_key()
llm_config = { "model": "gpt-4-turbo"}

task = "Write a blogpost the stock price performance of"\
    "Nvidia in the past month. Today's date is 2024-04-23."

user_proxy = autogen.ConversableAgent(
    name="Admin",
    system_message="Give the task, and send ",
    code_execution_config=False,
    llm_config=llm_config,
    human_input_mode="ALWAYS"
)

planner = autogen.ConversableAgent(
    name="Planner",
    system_message="Given a task, please determine "
    "what information is needed to complete the task. "
    "Please note that the information will all be retrieved using "
    "Python code. Please only suggest information that can be retrieved using Python code. "
    "After each step is done by others, check the progress and "
    "instruct the remaining steps. If a step fails, try to "
    "workaround",
    description="Planner. Give a task, determine what "
    "information is needed to complete the task. "
    "instruct the remaining steps",
    llm_config=llm_config
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    description="An engineer that writes code based on the plan provided by the planner."
)

executor = autogen.ConversableAgent(
    name="Executor",
    system_message="Execute the code written by the engineer and report the result",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages":3,
        "work_dir": "coding",
        "use_docker": False
    }
)

writer = autogen.ConversableAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="Writer."
    "Please write blogs in markdown format ( with relevant titles)"
    " and put the content in pseudo ```md``` code block. "
    "You take feedback from the admin to refine the blog."
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, writer, executor, planner],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

groupchat_result = user_proxy.initiate_chat(
    manager,
    message=task
)