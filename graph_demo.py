from typing import TypedDict, List
from langgraph.graph import Graph
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.tools import Tool
from langchain_core.tools.base import ToolException
from langchain.agents.tools import BaseTool
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
import requests

load_dotenv(override=True)

class State(TypedDict):
    question: str
    context: str
    answer: str

vectordb = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"))
llm = ChatOpenAI(model="gpt-4o-mini")

# Define MCP tool class
class MCPTool(BaseTool):
    def __init__(self, name, callable):
        super().__init__(name=name)
        self.callable = callable
        
    def _run(self, *args, **kwargs):
        return self.callable(*args, **kwargs)

# Configure MCP client
def get_mcp_tools():
    mcp_server_urls_str = os.getenv("MCP_SERVER_URLS", "").strip()
    if not mcp_server_urls_str:
        return []
    
    mcp_server_urls = mcp_server_urls_str.split(",")
    tools = []
    
    for url in mcp_server_urls:
        if not url.strip():
            continue
            
        try:
            response = requests.get(f"{url.strip()}/mcp")
            if response.status_code == 200:
                data = response.json()
                for tool in data.get("tools", []):
                    tool_name = tool.get("name")
                    if tool_name:
                        # Create a callable for this tool
                        def create_tool_callable(tool_url, tool_name):
                            def call_tool(params):
                                response = requests.post(f"{tool_url}/mcp/{tool_name}", json=params)
                                if response.status_code == 200:
                                    return response.json()
                                else:
                                    raise ToolException(f"Error calling {tool_name}: {response.text}")
                            return call_tool
                            
                        callable_fn = create_tool_callable(url.strip(), tool_name)
                        tools.append(MCPTool(name=tool_name, callable=callable_fn))
        except Exception as e:
            print(f"Error connecting to MCP server {url}: {str(e)}")
            
    return tools

# Get MCP tools
mcp_tools = get_mcp_tools()

# Tool decorator
def as_tool(func):
    return func

@as_tool
def retrieve(state: State):
    hits = vectordb.similarity_search(state["question"], k=4)
    state["context"] = "\n\n".join(d.page_content for d in hits)
    return state

@as_tool
def generate(state: State):
    prompt = f"""Answer for executives only.\nContext:\n{state['context']}\nQuestion: {state['question']}"""
    state["answer"] = llm.invoke(prompt).content
    
    return state



graph = Graph()
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
for t in mcp_tools:
    graph.add_node(t.name, t)                         # tool nodes

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.set_finish_point("generate")

chain = graph.compile()

if __name__ == "__main__":
    while True:
        q = input("Ask ▶ ")
        if q.lower() in ['quit', 'exit', 'q']:
            break
        try:
            out = chain.invoke({"question": q})
            if out and "answer" in out:
                print("\n→", out["answer"], "\n")
            else:
                print("\n→ No answer generated. Please try a different question.\n")
        except Exception as e:
            print(f"\n→ Error: {str(e)}\n")