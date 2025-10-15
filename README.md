# SQL Search Agent

A conversational AI agent that transforms natural language queries into SQL searches. Built with LangChain, LangGraph, and FastAPI, this agent provides an intuitive interface for querying databases through natural conversation.

## Overview

This agent uses a multi-step workflow to understand user intent, generate appropriate SQL queries, execute them against a MySQL database, and format results into natural language responses. Conversation context is maintained using Redis for persistent storage.

## Architecture

### High-Level Flow

```
User Input → Scoping → SQL Generation → Execution → Formatting → Response
    ↓          ↓             ↓              ↓           ↓
 FastAPI    Clarify      Generate       MySQL      Natural
   API     (if needed)    Query          DB        Language
    ↓
  Redis
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                    (API Layer)                               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼────────┐      ┌──────▼──────┐
        │  Redis Storage │      │  LangGraph  │
        │  (State mgmt)  │      │   Workflow  │
        └────────────────┘      └──────┬──────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
            ┌───────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
            │  Scoping Step  │ │ Execution   │ │  Formatting     │
            │  (Clarify)     │ │    Step     │ │     Step        │
            └────────────────┘ └──────┬──────┘ └─────────────────┘
                                      │
                              ┌───────▼────────┐
                              │   MySQL DB     │
                              └────────────────┘
```

## Core Features

- Natural language to SQL query translation
- Multi-turn conversational interface with context awareness
- Automatic query type detection (count, list, specific)
- Safe SQL execution with error handling
- Natural language response generation
- Persistent conversation state with Redis

## Workflow

### 1. Scoping Step

Analyzes user input to determine if sufficient information exists to generate a query.

**Responsibilities:**
- Parse user intent from conversation history
- Identify missing information
- Ask clarification questions when needed
- Route to SQL generation when ready

**Decision Flow:**
```
User Message → Parse Intent → Sufficient Info?
                                    │
                          ┌─────────┴─────────┐
                         No                  Yes
                          │                   │
                    Ask Question         Generate SQL
                          │                   │
                        END              Continue →
```

### 2. Execution Step

Executes SQL queries against the database with connection management and error handling.

**Responsibilities:**
- Establish database connections
- Execute queries safely
- Handle errors gracefully
- Return structured results

### 3. Formatting Step

Transforms SQL results into contextual natural language responses.

**Responsibilities:**
- Analyze query results
- Generate appropriate response format
- Handle empty results
- Present data in user-friendly format

## LangGraph Workflow

```
        START
          │
          ▼
    ┌──────────┐
    │ Scoping  │
    │  Node    │
    └────┬─────┘
         │
         ▼
    Need Info? ──Yes──► END (with question)
         │
        No
         │
         ▼
    ┌──────────┐
    │SQL Query │
    │Generation│
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │ Execute  │
    │  Query   │
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │  Format  │
    │ Response │
    └────┬─────┘
         │
         ▼
        END
```

## Tech Stack

- **Framework:** FastAPI
- **Agent Framework:** LangChain + LangGraph
- **LLM:** OpenAI GPT-4
- **Database:** MySQL
- **Cache/State:** Redis
- **Language:** Python 3.10+

## Project Structure

```
.
├── sales_info_agent/
│   ├── scoping_step/
│   │   └── core/
│   │       ├── config/
│   │       │   ├── scope_research.py      # Scoping logic
│   │       │   └── state_and_schemas.py   # State definitions
│   │       └── prompts/
│   │           └── scoping.py             # Prompt templates
│   ├── execution_step/
│   │   └── core/
│   │       ├── config/
│   │       │   └── sql_executor.py        # Query execution
│   │       └── database/
│   │           └── mysql_connection.py    # DB connection
│   ├── formatting_step/
│   │   └── core/
│   │       ├── config/
│   │       │   └── response_formatter.py  # Response generation
│   │       └── prompts/
│   │           └── formatting.py          # Formatting prompts
│   ├── workflow/
│   │   └── agent_graph.py                 # LangGraph definition
│   └── main.py                             # Agent initialization
├── src/
│   ├── app.py                              # FastAPI app
│   ├── redis/
│   │   ├── config.py                       # Redis setup
│   │   └── db_operations.py               # State persistence
│   └── sales_agent_api/
│       ├── routes/
│       ├── controller/
│       ├── service/
│       └── models/
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- Redis 6.0+
- OpenAI API key

### Setup

```bash
# Clone repository
git clone https://github.com/Optimus-Data/sql_search_agent.git
cd sql_search_agent

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Start services
redis-server &
uvicorn src.app:app --reload --port 8000
```

### Environment Variables

```env
OPENAI_API_KEY=your_key
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=your_db
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Usage

### API Endpoint

```bash
POST /chat
Content-Type: application/json

{
  "thread_id": "user-123",
  "message": "Your natural language query here"
}
```

### Response

```json
{
  "response": "Natural language response with query results",
  "thread_id": "user-123"
}
```

## State Management

The agent maintains state across conversation turns using a structured state object:

```python
class AgentState(MessagesState):
    sql_query: Optional[str]           # Generated SQL
    sql_results: Optional[List[Dict]]  # Query results
    sql_error: Optional[str]           # Error messages
    formatted_response: Optional[str]  # Final response
    supervisor_messages: List          # Internal messages
```

State is persisted in Redis, allowing conversation resumption and multi-session support.

## Key Design Decisions

**Why LangGraph?**
- Provides structured workflow for multi-step agent processes
- Enables conditional routing based on state
- Built-in state management and checkpointing
- Better than simple chains for complex decision trees

**Why Separate Steps?**
- Clear separation of concerns
- Easier testing and debugging
- Modular architecture for future extensions
- Each step has single responsibility

**Why Redis for State?**
- Fast in-memory access
- Simple key-value storage
- Easy deployment
- Sufficient for conversation state

## Error Handling

- Database connection failures return user-friendly messages
- SQL errors are caught and don't expose system details
- Empty results handled gracefully
- Proper HTTP status codes on API errors

## Inspiration

This project was developed after completing the "Deep Research With LangGraph" course from LangChain Academy. The course provides excellent insights into building AI agents with LangGraph.

Learning to build agents with code rather than no-code platforms provides flexibility, control, and avoids vendor lock-in.

## License

MIT License

---

Built with LangChain, LangGraph, and FastAPI.
