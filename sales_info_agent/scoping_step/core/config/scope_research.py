"""
User Clarification and SQL Query Generation.

This module implements the scoping phase of the cooler query workflow.
"""

from datetime import datetime
from typing_extensions import Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string
from langgraph.types import Command

from sales_info_agent.scoping_step.core.prompts.scoping import (
    clarify_with_user_instructions,
    transform_messages_into_research_topic_prompt,
)
from sales_info_agent.scoping_step.core.config.state_and_schemas import (
    AgentState,
    ClarifyWithUser,
    CoolerSearchQuery,
)


def get_today_str() -> str:
    """Get current date in a human-readable format."""
    return datetime.now().strftime("%a %b %-d, %Y")


model = init_chat_model(model="openai:gpt-4o", temperature=0.0)


def clarify_with_user(
    state: AgentState,
) -> Command[Literal["write_sql_query", "__end__"]]:
    """
    Determine if the user's request contains sufficient information.

    Uses structured output to make deterministic decisions.
    Routes to either SQL query generation or ends with a clarification question.
    """
    structured_output_model = model.with_structured_output(ClarifyWithUser)

    response = structured_output_model.invoke(
        [
            HumanMessage(
                content=clarify_with_user_instructions.format(
                    messages=get_buffer_string(messages=state["messages"]),
                    date=get_today_str(),
                )
            )
        ]
    )

    if response.need_clarification:
        return Command(
            goto="__end__",
            update={"messages": [AIMessage(content=response.question)]},
        )
    else:
        return Command(
            goto="write_sql_query",
            update={"messages": [AIMessage(content=response.verification)]},
        )


def write_sql_query(state: AgentState):
    """
    Transform the conversation history into a SQL query for MySQL.

    Uses structured output to ensure the query follows the required format.
    """
    structured_output_model = model.with_structured_output(CoolerSearchQuery)

    response = structured_output_model.invoke(
        [
            HumanMessage(
                content=transform_messages_into_research_topic_prompt.format(
                    messages=get_buffer_string(state.get("messages", [])),
                    date=get_today_str(),
                )
            )
        ]
    )

    product_filters = {
        "query_type": response.query_type,
        "cooler_criteria": response.cooler_criteria,
    }

    return {
        "sql_query": response.sql_query,
        "product_filters": product_filters,
        "supervisor_messages": [
            HumanMessage(content=f"SQL Query generated: {response.query_type} query")
        ],
    }