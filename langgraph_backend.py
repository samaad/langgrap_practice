from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

CONFIG = {'configurable': {'thread_id': "thread-1"}}

model_llama = ChatOllama(model="llama3")
model_qween = ChatOllama(model="qwen3:4b")
model_gemma = ChatOllama(model="gemma3")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state["messages"]
    response = model_gemma.invoke(messages)
    return {'messages': [response]}

# Checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node", END)

workflow = graph.compile(checkpointer=checkpointer)

# for message_chunk, metadata in workflow.stream(
# {'messages': [HumanMessage(content='What is the recipe to make pasta')]},
#     config=CONFIG,
#     stream_mode='messages'
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)
