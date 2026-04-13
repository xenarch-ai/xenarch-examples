"""LangChain agent with Xenarch payment tools.

The agent can autonomously discover gates, pay for content,
and review its payment history.

Usage:
    python main.py
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from xenarch.tools.langchain import CheckGateTool, GetHistoryTool, PayTool

load_dotenv()

# Set up the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Xenarch payment tools
tools = [CheckGateTool(), PayTool(), GetHistoryTool()]

# Create and run the agent
agent = create_react_agent(
    llm,
    tools,
    prompt=(
        "You are a helpful assistant with access to Xenarch payment tools. "
        "You can check if URLs have payment gates, pay for gated content "
        "using USDC micropayments on Base, and review payment history. "
        "When asked to access gated content, check the gate first, then pay if needed."
    ),
)

if __name__ == "__main__":
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Check if https://gate.xenarch.dev/sample-page/ has a paywall. If it does, pay for access."}]}
    )
    print("\n---")
    for msg in result["messages"]:
        print(f"[{msg.type}] {msg.content if isinstance(msg.content, str) else msg.content}")
