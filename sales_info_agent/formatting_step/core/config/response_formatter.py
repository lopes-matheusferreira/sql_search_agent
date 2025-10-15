"""
Response Formatting Node - Formats SQL results into natural language.
"""

import json
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from sales_info_agent.scoping_step.core.config.state_and_schemas import AgentState
from sales_info_agent.formatting_step.core.prompts.formatting import format_sql_results_prompt

model = init_chat_model(model="openai:gpt-4o", temperature=0.3)


def format_response(state: AgentState) -> dict:
    """
    Format SQL query results into a natural language response.

    Args:
        state: Current agent state containing sql_results and messages

    Returns:
        Updated state with formatted_response and new message
    """
    sql_results = state.get("sql_results")
    sql_error = state.get("sql_error")
    sql_query = state.get("sql_query")

    user_messages = [msg for msg in state["messages"] if hasattr(msg, 'type') and msg.type == "human"]
    user_question = user_messages[-1].content if user_messages else "Query de banco de dados"

    if sql_error:
        error_response = f"Desculpe, ocorreu um erro ao executar a consulta no banco de dados:\n\n{sql_error}\n\nPor favor, tente reformular sua pergunta."

        return {
            "formatted_response": error_response,
            "messages": [AIMessage(content=error_response)]
        }

    if not sql_results or len(sql_results) == 0:
        empty_response = "Não encontrei resultados para essa consulta no banco de dados."

        return {
            "formatted_response": empty_response,
            "messages": [AIMessage(content=empty_response)]
        }

    results_json = json.dumps(sql_results, indent=2, ensure_ascii=False, default=str)

    print(f"\n{'=' * 50}")
    print("FORMATTING RESPONSE")
    print(f"{'=' * 50}")
    print(f"User Question: {user_question}")
    print(f"Results Count: {len(sql_results)}")
    print(f"{'=' * 50}\n")

    formatted_text = model.invoke([
        HumanMessage(content=format_sql_results_prompt.format(
            user_question=user_question,
            sql_query=sql_query,
            sql_results=results_json
        ))
    ])

    formatted_content = formatted_text.content

    return {
        "formatted_response": formatted_content,
        "messages": [AIMessage(content=formatted_content)]
    }