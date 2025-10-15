# Sales Info Search Agent

A conversational AI agent that transforms natural language queries into SQL searches against a MySQL database. Built with LangChain, LangGraph, and FastAPI, this agent provides an intuitive interface for querying cooler equipment data.

## Overview

The Sales Info Search Agent uses a multi-step workflow to understand user intent, generate appropriate SQL queries, execute them against a MySQL database, and format the results into natural language responses. The system maintains conversation context using Redis for persistent storage.

## Architecture

### System Flow

```
User Query → Scoping Step → SQL Execution → Response Formatting → User Response
     ↓            ↓               ↓                  ↓
  FastAPI     Clarification    MySQL DB         Natural Language
   API         (if needed)      Query             Response
     ↓
  Redis
(Persistence)
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
│                    (src/app.py)                              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼────────┐      ┌──────▼──────┐
        │  Redis Storage │      │   LangGraph │
        │   (Threads)    │      │   Workflow  │
        └────────────────┘      └──────┬──────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
            ┌───────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
            │ Scoping Step   │ │ Execution   │ │   Formatting    │
            │ (scope_research)│ │   Step      │ │      Step       │
            └────────────────┘ └──────┬──────┘ └─────────────────┘
                                      │
                              ┌───────▼────────┐
                              │   MySQL DB     │
                              │   (coolers)    │
                              └────────────────┘
```

## Features

### Conversational Interface
- Natural language understanding of user queries
- Context-aware clarification questions
- Multi-turn conversations with persistent memory

### Intelligent Query Generation
- Automatic SQL query generation from natural language
- Support for multiple query types (specific, count, list)
- Flexible filtering and search capabilities

### Database Integration
- Direct MySQL connection
- Safe query execution with error handling
- Support for complex queries with joins and aggregations

### Response Formatting
- Natural language response generation
- Structured formatting with emojis and markdown
- Context-aware result presentation

## Workflow Steps

### 1. Scoping Step

The scoping step determines if the user has provided enough information to generate a SQL query.

**Process:**
1. Analyze conversation history
2. Check if sufficient criteria are provided
3. Ask clarification questions if needed
4. Generate SQL query when ready

**Example Flow:**
```
User: "Show me coolers"
Agent: "What information would you like to know about the coolers? 
        For example: location, status, model, or alarms?"

User: "Show coolers in São Paulo"
Agent: "I understand you want to see coolers in São Paulo. 
        Generating query now..."
```

### 2. Execution Step

Executes the generated SQL query against the MySQL database.

**Process:**
1. Receive SQL query from scoping step
2. Establish MySQL connection
3. Execute query safely
4. Return results or error message

**Supported Query Types:**
- **Specific:** Single cooler lookup by ID
- **Count:** Aggregate counts with filters
- **List:** Multiple results with ordering and limits

### 3. Formatting Step

Transforms SQL results into natural language responses.

**Process:**
1. Receive SQL results
2. Analyze user's original question
3. Generate contextual response
4. Format with appropriate structure

**Response Styles:**
- Count queries: Direct numerical answers
- List queries: Formatted lists with key information
- Specific queries: Detailed information cards
- Empty results: Friendly "not found" messages

## Database Schema

```sql
CREATE TABLE `coolers` (
  `coolerId` int NOT NULL AUTO_INCREMENT,
  `installAddress` varchar(255) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL,
  `usageStatus` varchar(50) DEFAULT NULL,
  `customField` varchar(255) DEFAULT NULL,
  `alarmCode` varchar(20) DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `lastStatTime` datetime DEFAULT NULL,
  `distFromInstall` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`coolerId`)
);
```

### Column Descriptions

| Column | Description | Example Values |
|--------|-------------|----------------|
| `coolerId` | Unique cooler identifier | 1010001, 1010002 |
| `installAddress` | Installation location | "Av. Paulista, 1000 - São Paulo/SP" |
| `model` | Equipment model | model1, model2, model3 |
| `usageStatus` | Operation status | "production", "in service" |
| `customField` | Communication type | "Bluetooth", "NetworkPro" |
| `alarmCode` | Active alarm code | "17-low temperature" |
| `lastStatTime` | Last data transmission | 2025-10-15 09:30:00 |
| `distFromInstall` | Distance from install point (km) | 0.4, 2.1 |

## Installation

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- Redis 6.0+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Optimus-Data/sql_search_agent.git
cd sql_search_agent
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# MySQL
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=coolers_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

5. Initialize the database:
```bash
# Run the schema creation script
mysql -u root -p < database/schema.sql
```

6. Start Redis:
```bash
redis-server
```

7. Run the application:
```bash
uvicorn src.app:app --reload --port 8000
```

## Usage

### API Endpoints

#### POST /chat
Send a message to the agent and receive a response.

**Request:**
```json
{
  "thread_id": "user-123",
  "message": "Show me coolers in São Paulo"
}
```

**Response:**
```json
{
  "response": "Found 15 coolers in São Paulo:\n1. Cooler 1010001...",
  "thread_id": "user-123"
}
```

### Example Queries

**Count Queries:**
```
"How many coolers are in production?"
"Count coolers with alarms"
"How many coolers in Curitiba?"
```

**Specific Cooler:**
```
"What is the status of cooler 1010001?"
"Show me information about cooler 1010023"
"Is cooler 1010045 moved?"
```

**List Queries:**
```
"Show me coolers in São Paulo"
"List all NetworkPro coolers"
"Show coolers with low temperature alarms"
```

**Time-based Queries:**
```
"Which coolers sent data today?"
"Show coolers offline for more than 2 days"
"Coolers that haven't communicated this week"
```

## Project Structure

```
sales_info_agent/
├── sales_info_agent/
│   ├── scoping_step/
│   │   └── core/
│   │       ├── config/
│   │       │   ├── scope_research.py      # Query scoping logic
│   │       │   └── state_and_schemas.py   # State definitions
│   │       └── prompts/
│   │           └── scoping.py             # Scoping prompts
│   ├── execution_step/
│   │   └── core/
│   │       ├── config/
│   │       │   └── sql_executor.py        # SQL execution logic
│   │       └── database/
│   │           └── mysql_connection.py    # MySQL connection
│   ├── formatting_step/
│   │   └── core/
│   │       ├── config/
│   │       │   └── response_formatter.py  # Response formatting
│   │       └── prompts/
│   │           └── formatting.py          # Formatting prompts
│   ├── workflow/
│   │   └── cooler_agent_graph.py          # LangGraph workflow
│   └── main.py                             # Agent initialization
├── src/
│   ├── app.py                              # FastAPI application
│   ├── redis/
│   │   ├── config.py                       # Redis configuration
│   │   └── db_operations.py               # Redis operations
│   └── sales_agent_api/
│       ├── routes/
│       │   └── routes.py                   # API routes
│       ├── controller/
│       │   └── controller.py               # Request handling
│       ├── service/
│       │   └── service.py                  # Business logic
│       └── models/
│           └── models.py                   # Pydantic models
├── requirements.txt
├── .env.example
└── README.md
```

## Technical Details

### State Management

The agent uses a graph-based state machine with the following structure:

```python
class AgentState(MessagesState):
    sql_query: Optional[str]
    product_filters: Optional[dict]
    sql_results: Optional[List[Dict[str, Any]]]
    sql_error: Optional[str]
    formatted_response: Optional[str]
    supervisor_messages: Annotated[Sequence[BaseMessage], add_messages]
```

### LangGraph Workflow

```
        START
          │
          ▼
    ┌──────────┐
    │ Clarify  │◄─── Need clarification? ─── Yes ──► END
    │ with User│                                      (Ask question)
    └────┬─────┘
         │ No
         ▼
    ┌──────────┐
    │  Write   │
    │SQL Query │
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
   (Return response)
```

### Persistence Layer

Conversation threads are stored in Redis with the following structure:

```json
{
  "thread_id": "user-123",
  "messages": [...],
  "state": {...},
  "timestamp": "2025-10-15T10:30:00Z"
}
```

## Error Handling

The system implements comprehensive error handling:

- **Database Connection Errors:** Graceful fallback with user-friendly messages
- **SQL Syntax Errors:** Caught and reported without exposing system details
- **Empty Results:** Clear "not found" responses
- **API Errors:** Proper HTTP status codes and error descriptions

## Performance Considerations

- **Connection Pooling:** MySQL connections are created per request
- **Query Optimization:** LIMIT clauses prevent excessive data retrieval
- **Redis Caching:** Thread state cached for fast access
- **Async Operations:** FastAPI async endpoints for better concurrency

## Security

- Environment variables for sensitive credentials
- SQL injection prevention through parameterized queries
- Input validation with Pydantic models
- CORS configuration for API access control

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
black .
flake8 .
mypy .
```

## Inspiration

This project was developed after completing the "Deep Research With LangGraph" course from LangChain Academy. The course provides excellent insights into building sophisticated AI agents with LangGraph.

If you're interested in artificial intelligence and want to learn more about building agents, I highly recommend the LangChain Academy courses. Learning to write code from scratch gives you the freedom of the open-source world and prevents dependency on expensive platform subscriptions.

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.

---

Built with LangChain, LangGraph, FastAPI, and MySQL.
