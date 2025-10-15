"""
State Definitions and Pydantic Schemas for Cooler Query Agent.
"""

import operator
from typing_extensions import Optional, Annotated, List, Sequence, Dict, Any

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class AgentInputState(MessagesState):
    """Input state for the full agent - only contains messages from user input."""
    pass


class AgentState(MessagesState):
    """
    Main state for the cooler query system.
    Extends MessagesState with additional fields for query workflow.
    """

    sql_query: Optional[str] = None
    product_filters: Optional[dict] = None

    sql_results: Optional[List[Dict[str, Any]]] = None
    sql_error: Optional[str] = None

    formatted_response: Optional[str] = None

    supervisor_messages: Annotated[Sequence[BaseMessage], add_messages]
    raw_notes: Annotated[list[str], operator.add] = []
    notes: Annotated[list[str], operator.add] = []
    final_report: Optional[str] = None


class ClarifyWithUser(BaseModel):
    """Schema for user clarification decision and questions."""

    need_clarification: bool = Field(
        description="Whether the user needs to be asked a clarifying question.",
    )
    question: str = Field(
        description="A question to ask the user to clarify the cooler query",
    )
    verification: str = Field(
        description="Verification message that we have sufficient information and will generate the SQL query.",
    )


class CoolerSearchQuery(BaseModel):
    """Schema for structured SQL query generation."""

    query_type: str = Field(
        description="Type of query: 'specific' (single cooler), 'count' (aggregate), 'list' (multiple results)",
    )
    cooler_criteria: Optional[str] = Field(
        description="Main criteria extracted from user request (e.g., 'coolerId 1010001', 'in service', 'moved')",
        default=None,
    )
    sql_query: str = Field(
        description="The complete SQL SELECT query formatted for MySQL that will retrieve the cooler data",
    )