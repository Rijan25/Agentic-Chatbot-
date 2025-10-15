from langgraph_backend import chatflow
from langchain_core.messages import HumanMessage
import streamlit as st
import uuid

# ****************** Utility Functions **********************************

def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id


# **********************Session Setup ***********************************

# managing the session history
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()   

# ************************ Sidebar UI ********************************

st.sidebar.title('Chatbot')

st.sidebar.button('New Chat')

st.sidebar.header('My Conversation')

st.sidebar.text(st.session_state['thread_id'])

# **********************Main UI **************************************
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
    

# Taking the user Input
user_input=st.chat_input('Type your Queries here')
if user_input:

    # adding the message to the message history
    st.session_state['message_history'].append({'role':'user','content':user_input})

    # Displaying the user messages
    with st.chat_message(name='user'):
        st.text(user_input)

    config={'configurable':{'thread_id':st.session_state['thread_id']}}    

    # Displaying the AI Messages
    with st.chat_message(name='AI'):

        # Streaming feature for the response
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatflow.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config=config,
                stream_mode='messages'
            )
        ) 
        st.session_state['message_history'].append({'role':'AI','content':ai_message})  

