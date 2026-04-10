"""LangChain agent with Xenarch payment tools.

The agent can autonomously discover gates, pay for content,
and review its payment history.

Usage:
    python main.py
"""

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from xenarch.tools.langchain import CheckGateTool, GetHistoryTool, PayTool

load_dotenv()

# Set up the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Xenarch payment tools
tools = [CheckGateTool(), PayTool(), GetHistoryTool()]

# Agent prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant with access to Xenarch payment tools. "
            "You can check if URLs have payment gates, pay for gated content "
            "using USDC micropayments on Base, and review payment history. "
            "When asked to access gated content, check the gate first, then pay if needed.",
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Create and run the agent
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    result = executor.invoke(
        {"input": "Check if example.com has a paywall. If it does, pay for access."}
    )
    print("\n---")
    print(result["output"])
