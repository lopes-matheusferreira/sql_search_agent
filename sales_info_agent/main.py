"""
Main entry point for the Cooler Query Agent.

This module centralizes the execution of the complete cooler agent workflow:
1. Scoping: Clarify user intent and generate SQL
2. Execution: Execute SQL query against MySQL database
3. Formatting: Format results into natural language response
"""

from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from sales_info_agent.workflow.cooler_agent_graph import cooler_agent_builder
from sales_info_agent.execution_step.core.database.mysql_connection import test_connection


def create_sales_info_search_agent():
    """
    Create and compile the cooler query agent with Memory checkpointer.

    Returns:
        Compiled cooler agent graph with in-memory state

    Note: Uses MemorySaver for development. For production with Redis Stack,
          replace with: RedisSaver(REDIS_URL)
    """
    print("\n" + "="*50)
    print("COOLER AGENT INITIALIZATION")
    print("="*50)

    if test_connection():
        print("✓ Database connection verified")
    else:
        print("✗ WARNING: Database connection failed - queries will fail")

    print("="*50 + "\n")

    checkpointer = MemorySaver()
    return cooler_agent_builder.compile(checkpointer=checkpointer)


def run_sales_info_search_workflow(agent, user_message: str, thread_id: str = "1"):
    """
    Run the cooler agent workflow with a user message.

    The checkpointer automatically manages conversation history.
    The workflow executes: Scoping → SQL Execution → Response Formatting

    Args:
        agent: Compiled agent graph
        user_message: User's question/request
        thread_id: Thread identifier for conversation history

    Returns:
        Complete agent state with formatted response
    """
    thread = {"configurable": {"thread_id": thread_id}}

    result = agent.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config=thread
    )

    return result


create_research_agent = create_sales_info_search_agent
run_research_workflow = run_sales_info_search_workflow