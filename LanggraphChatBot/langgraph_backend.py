# pyrefly: ignore [missing-import]
from langgraph.types import Checkpointer
from langgraph.graph import START,StateGraph,END
from typing  import TypedDict, Annotated
from langchain_core.messages import BaseMessage

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

from langchain_ollama import ChatOllama


llm = ChatOllama( model="llama3.2:3b",
    temperature=0)

class chatState(TypedDict):
    message: Annotated[list[BaseMessage],add_messages]

def chatNode(state:chatState) :
    response = llm.invoke(state["message"])
    return {"message":response}


Checkpointer = InMemorySaver()

graph  = StateGraph(chatState)

graph.add_node('chat_node',chatNode)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

app = graph.compile(checkpointer=Checkpointer)