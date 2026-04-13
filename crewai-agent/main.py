"""CrewAI crew with Xenarch payment tools.

A research agent that can discover and pay for gated content.

Usage:
    python main.py
"""

from dotenv import load_dotenv
from crewai import Agent, Crew, Task

from xenarch.tools.crewai import check_gate, get_history, pay

load_dotenv()

# Agent with Xenarch payment capabilities
researcher = Agent(
    role="Research Agent",
    goal="Access and summarize gated web content by paying for it when needed",
    backstory=(
        "You are a research agent that can pay for gated content using "
        "Xenarch micropayments. When you encounter a payment gate, you "
        "check the price, pay with USDC on Base, and use the access token "
        "to retrieve the content."
    ),
    tools=[check_gate, pay, get_history],
    verbose=True,
)

# Task: research a gated URL
task = Task(
    description=(
        "Check if https://gate.xenarch.dev/hello-world/ has a Xenarch payment gate. "
        "If it does, pay for access and report what you found. "
        "If not, report that the content is freely accessible."
    ),
    expected_output="A summary of the gate status and any payment made.",
    agent=researcher,
)

crew = Crew(agents=[researcher], tasks=[task], verbose=True)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n---")
    print(result)
