from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3
import requests
import os

os.environ['LANGCHAIN_PROJECT'] = 'langgraph-chatbot'


load_dotenv()

CONFIG = {'configurable': {'thread_id': "thread-2"}}

model_llama = ChatOllama(model="llama3")
model_qween = ChatOllama(model="qwen3:4b")
model_gemma = ChatOllama(model="gemma3")



#------------
# 2. Tools
#------------

# Tools
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}

        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA')
    using Alpha Vantage with API key in the URL.
    """
    alpha_key = os.getenv("ALPHA_KEY")

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={alpha_key}"
    r = requests.get(url)
    return r.json()

# Make tool list
tools = [get_stock_price, search_tool, calculator]

# Make the LLM tool-aware
llm_with_tools = model_qween.bind_tools(tools)

#------------
# 3. STATE
#------------

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#------------
# 4. Node
#------------

def chat_node(state: ChatState):
    messages = state["messages"]
    response = model_gemma.invoke(messages)
    return {'messages': [response]}

# graph nodes
def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)  # Executes tool calls
#------------
# 5. Checkpointer
#------------

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

#------------
# 6. Graph
#------------
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START,"chat_node")
# If the LLM asked for a tool, go to ToolNode; else finish
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")
# graph.add_edge("chat_node", END)

workflow = graph.compile(checkpointer=checkpointer)

#------------
# 7. Helper
#------------


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    print(list(all_threads))
    return all_threads


# response = workflow.invoke(
# {'messages': [HumanMessage(content='what is capital of indai')]},
#     config=CONFIG
# )
#
# print(response)