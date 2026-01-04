import streamlit as st
from database_langgraph_backend import workflow, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid

# **************************************** utility functions *************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].add(thread_id)

def load_messages(thread_id):
    config = {'configurable': {'thread_id': thread_id}}
    state = workflow.get_state(config=config)
    # No state yet for this thread -> no messages
    if state is None:
        return []
    return state.values.get("messages", [])

    # return workflow.get_state(config=config).values['messages']
# **************************************** Session Setup ******************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# **************************************** Sidebar UI *********************************
st.sidebar.title('Language Graph Tutorial')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')
for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        list_messages = load_messages(thread_id)

        temp_messages = []
        for message in list_messages:
            role='user' if isinstance(message, HumanMessage) else 'assistant'
            temp_messages.append({'role': role, 'content': message.content})
        st.session_state['message_history'] = temp_messages


# **************************************** Main UI ************************************

# Render history
for message in st.session_state['message_history']:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Enter your chat message")

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {
        'configurable': {'thread_id': st.session_state['thread_id']},
        'metadata': {
            'thread_id': st.session_state['thread_id'],
        },
        "run_name": "chat_run"
    }
    # first add the message to message_history
    with st.chat_message('assistant'):
        # Use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
             for message_chunk, metadata in workflow.stream(
                {'messages': [HumanMessage(content=user_input)]},
                    config=CONFIG,
                    stream_mode='messages'
            ):
                 # Lazily create & update the SAME status container when any tool runs
                 if isinstance(message_chunk, ToolMessage):
                     tool_name = getattr(message_chunk, "name", "tool")
                     if status_holder["box"] is None:
                         status_holder["box"] = st.status(
                             f"🔧 Using `{tool_name}` …", expanded=True
                         )
                     else:
                         status_holder["box"].update(
                             label=f"🔧 Using `{tool_name}` …",
                             state="running",
                             expanded=True,
                         )
                 # Stream ONLY assistant tokens
                 if isinstance(message_chunk, AIMessage):
                    # yield only assistant tokens
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    # Save assistant message
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
