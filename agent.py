from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

class Agent:
    """Agent to handle an LLM with tools and a system prompt."""
    def __init__(self, model, tools, system=""):
        self.system = system

        # Initialize the state graph
        print("[INFO] Building the state graph...")
        graph = StateGraph(AgentState)

        tool_node = ToolNode(tools=tools)

        # Add nodes
        graph.add_node("chatbot", self.chatbot)
        graph.add_node("tools", tool_node)

        # Define conditional edges
        graph.add_conditional_edges(
            "chatbot",
            tools_condition,
        )
        graph.add_edge("tools", "chatbot")  # Connect tools back to chatbot
        graph.set_entry_point("chatbot")

        # Compile the graph
        self.memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "1"}}
        self.graph = graph.compile(checkpointer=self.memory)
        print("[INFO] State graph compiled successfully.")

        # Bind tools to the LLM
        self.model = model.bind_tools(tools)

    def chatbot(self, state: AgentState):
        """LLM Chatbot node."""
        messages = state["messages"]
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        try:
            response = self.model.invoke(messages)
            print(f"[DEBUG] Chatbot response: {response}")
            return {"messages": state["messages"] + [response]}
        except Exception as e:
            print(f"[ERROR] Chatbot node failed: {e}")
            return {"messages": state["messages"] + [AIMessage(content="I'm sorry, something went wrong.")]}

    def respond(self, user_input):
        """Process user input and return chatbot response using graph.stream."""
        try:
            # Initialize the state with user input
            state = {"messages": [HumanMessage(content=user_input)]}

            response = []

            # Stream the events from the graph
            for event in self.graph.stream(state, self.config):
                for value in event.values():
                    messages = value.get("messages", [])
                    if messages:
                        final_message = messages[-1]
                        response.append(final_message.content)

            # Extract and return the final answer
            if response:
                final_content = response[-1]
                if "Final Answer:" in final_content:
                    final_answer = final_content.split("Final Answer:")[-1].strip()
                    return final_answer
                else:
                    return final_content
            else:
                return "No response generated."
        except Exception as e:
            print(f"[ERROR] Failed to generate response: {e}")
            return "Sorry, an error occurred while processing your request."