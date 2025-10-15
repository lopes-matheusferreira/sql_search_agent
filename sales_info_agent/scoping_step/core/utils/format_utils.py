"""Utility functions for formatting and displaying messages."""

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


def format_messages(messages):
    """
    Format and display messages in a readable format.

    Args:
        messages: List of BaseMessage objects
    """
    if not messages:
        print("No messages to display.")
        return

    print("=" * 50)
    print("CONVERSATION HISTORY")
    print("=" * 50)

    for i, message in enumerate(messages, 1):
        message_type = get_message_type(message)
        content = message.content if hasattr(message, 'content') else str(message)

        print(f"\n[{i}] {message_type}:")
        print("-" * 30)
        print(content)
        print()


def get_message_type(message: BaseMessage) -> str:
    """
    Get the display name for a message type.

    Args:
        message: Message object

    Returns:
        String representation of message type
    """
    if isinstance(message, HumanMessage):
        return "USER"
    elif isinstance(message, AIMessage):
        return "ASSISTANT"
    else:
        return message.__class__.__name__.upper()


def print_workflow_status(step: str, status: str = "RUNNING"):
    """
    Print workflow step status.

    Args:
        step: Name of the workflow step
        status: Status of the step (RUNNING, COMPLETED, ERROR)
    """
    print(f"[{status}] {step}")


def print_sql_query(sql_query: str, product_name: str = None, product_specs: str = None):
    """
    Format and print SQL query details.

    Args:
        sql_query: The generated SQL query
        product_name: The product name/category (optional)
        product_specs: The product specifications (optional)
    """
    print("\n" + "=" * 50)
    print("GENERATED SQL QUERY")
    print("=" * 50)
    print(f"\n{sql_query}\n")
    if product_name:
        print(f"Product: {product_name}")
    if product_specs:
        print(f"Specs: {product_specs}")
    print("=" * 50 + "\n")


print_budget_search_query = print_sql_query
print_search_query = print_sql_query
print_research_brief = print_sql_query