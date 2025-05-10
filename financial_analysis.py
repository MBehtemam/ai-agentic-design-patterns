from utils import get_openai_api_key
from autogen.coding import LocalCommandLineCodeExecutor
from autogen import ConversableAgent, AssistantAgent
import datetime
import os
from IPython.display import Image
import yfinance

OPENAI_API_KEY = get_openai_api_key()
llm_config = {"model": "gpt-4-turbo"}

executor = LocalCommandLineCodeExecutor(timeout=60, work_dir="coding")

code_executor_agent = ConversableAgent(
    name="code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": executor},
    human_input_mode="ALWAYS",
    default_auto_reply="Please continue. If everything is done, reply 'TERMINATE'.",
)

code_writer_agent = AssistantAgent(
    name="code_writer_agent",
    llm_config=llm_config,
    # code_executor_config=False,
    human_input_mode="NEVER",
)

code_writer_agent_system_message = code_writer_agent.system_message

print(code_writer_agent_system_message)

today = datetime.datetime.now().date()
message = (
    f"Today is {today}"
    " Create a plot showing stock gain YTD for NVDA and TLSA"
    "Make sure the code is in markdown code block and save the figure."
    "to a file ytd_stock_gains.png"
    ""
)

chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=message
)

Image(os.path.join("coding", "ytd_stock_gains.png"))

def get_stock_prices(stock_symbols, start_date, end_date):
    """Get the stock prices for the given stock symbols between 
    the start and end dates.
    
    Args:
        stock_symbols(str or list): The stock symbols to get the price for.
        start_date (str): the start date in the format 'YYYY-MM-DD'.
        end_date (str): The end date in the format 'YYYY-MM-DD'.
        
    Returns:
        pandas.DataFrame: the stock prices for the given stock
        symbols indexed by date, with one column per stock
        symbol. 
    """

    stock_data = yfinance.download(
        stock_symbols, start=start_date, end=end_date
    )
    return stock_data.get("Close")

def plot_stock_prices(stock_prices, filename):
    """Plot the stock prices for the given stock symbols
    
    Args:
        stock_prices (pandas.DateFrame): The stock prices for the give stock symbols.
    """
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,5))

    for column in stock_prices.columns:
        plt.plot(
            stock_prices.index, stock_prices[column], label=column
        )
    plt.title("Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.savefig(filename)