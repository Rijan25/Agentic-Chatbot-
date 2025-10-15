from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import InMemorySaver
import os


load_dotenv()

api_key=os.getenv('GOOGLE_API_KEY')

model=ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite-preview-09-2025',temperature=0.8,api_key=api_key)

# make the state of the graph
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]


# make the nodes
def chat_node(state:ChatState):
    messages=state['messages']
    response=model.invoke(messages)
    return {'messages':[response]}

# checkpointer
thread_id='1'
checkpointer=InMemorySaver()

# make the graph
graph=StateGraph(ChatState)

# add the nodes
graph.add_node('chat_node',chat_node)

# make the edges
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

config={'configurable':{'thread_id':thread_id}}

# compile the graph
chatflow=graph.compile(checkpointer=checkpointer)
chatflow

# invoke the graph

initial_state={'messages':'Who is the PM of India?'}
output_state=chatflow.invoke(initial_state,config=config)
print(output_state)

