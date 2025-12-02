from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import sqlite3

load_dotenv()

CONFIG = {'configurable': {'thread_id': "thread-2"}}

model_llama = ChatOllama(model="llama3")
model_qween = ChatOllama(model="qwen3:4b")
model_gemma = ChatOllama(model="gemma3")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state["messages"]
    response = model_gemma.invoke(messages)
    return {'messages': [response]}

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node", END)

workflow = graph.compile(checkpointer=checkpointer)

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