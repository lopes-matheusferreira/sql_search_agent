"""
Cooler Agent Workflow - Complete graph orchestration.

This module defines the complete workflow for the cooler query agent:
1. Clarify with user (scoping)
2. Write SQL query (scoping)
3. Execute SQL query (execution)
4. Format response (formatting)
"""

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

from sales_info_agent.scoping_step.core.config.state_and_schemas import (
    AgentState,
    AgentInputState,
)
from sales_info_agent.scoping_step.core.config.scope_research import (
    clarify_with_user,
    write_sql_query,
)
from sales_info_agent.execution_step.core.config.sql_executor import execute_sql_query
from sales_info_agent.formatting_step.core.config.response_formatter import format_response


def build_cooler_agent_graph() -> StateGraph:
    """
    Build the complete cooler agent workflow graph.

    Returns:
        Compiled StateGraph ready for execution
    """

    builder = StateGraph(AgentState, input_schema=AgentInputState)

    builder.add_node("clarify_with_user", clarify_with_user)
    builder.add_node("write_sql_query", write_sql_query)
    builder.add_node("execute_sql_query", execute_sql_query)
    builder.add_node("format_response", format_response)

    builder.add_edge(START, "clarify_with_user")
    # Note: clarify_with_user returns a Command that routes to either write_sql_query or END
    builder.add_edge("write_sql_query", "execute_sql_query")
    builder.add_edge("execute_sql_query", "format_response")
    builder.add_edge("format_response", END)

    return builder


cooler_agent_builder = build_cooler_agent_graph()