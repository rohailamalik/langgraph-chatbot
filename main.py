from llm import llm
from agent import Agent
from langchain_community.tools import DuckDuckGoSearchRun, TavilySearchResults
import getpass
import os

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")

search_tool = DuckDuckGoSearchRun()

#search_tool = TavilySearchResults(max_results=5)
tools = [search_tool]
tool_names = [tool.name for tool in tools]

prompt = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

bot = Agent(llm, tools, system=prompt)