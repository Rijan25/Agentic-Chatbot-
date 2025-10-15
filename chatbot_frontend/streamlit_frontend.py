from langgraph_backend import chatflow,config
from langchain_core.messages import HumanMessage
import streamlit as st

message_history=[]

# managing the session history
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

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

   

   

    # Displaying the AI Messages
    with st.chat_message(name='AI'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatflow.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config=config,
                stream_mode='messages'
            )
        ) 
        st.session_state['message_history'].append({'role':'AI','content':ai_message})  

