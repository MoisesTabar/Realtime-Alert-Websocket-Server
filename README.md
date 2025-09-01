# Realtime Alert WebSocket Server

## Purpose
FastAPI server for real-time alert and chat message broadcasting via WebSocket with REST API support. All data is stored in-memory.

## Architecture
- **FastAPI** application with WebSocket and REST endpoints
- In-memory storage using bounded deques for efficient message handling
- Asynchronous broadcast to all connected WebSocket clients
- Thread-safe connection management with per-socket locks

## Project Structure
```
.
├── main.py                # Application entry point
├── config.py               # Configuration settings
├── dependencies.py        # Dependency injection setup
├── controllers/           # Request/WebSocket handlers
│   ├── alert.py
│   └── websocket.py
├── managers/              # Connection management
│   └── connection_manager.py
├── models/                # Data models
│   ├── alert.py
│   └── message.py
├── repositories/          # Data storage
│   ├── alert.py
│   ├── base.py
│   └── chat.py
├── routes/                # API routes
│   ├── alert.py
│   └── websocket.py
├── services/              # Business logic
│   └── alert_generator.py
└── tests/                 # Test suite
    ├── managers/
    ├── repositories/
    ├── routes/
    └── services/
```

## Getting Started

### Prerequisites
- Python 3.8+
- uv (package manager)

### Installation
1. Install uv:
   ```bash
   curl -sSfL https://astral.sh/uv/install.sh | sh
   ```

2. Install dependencies:
   ```bash
   uv pip install -e .
   ```

### Running the Server
```bash
uv run fastapi run main:app --reload
```
> **Note**: If port 8000 is in use, specify another port with `--port`:
> ```bash
> uv run fastapi run main:app --reload --port 8001
> ```

### Running Tests
```bash
uv run pytest
```

## Data Handling

### Alerts
- Stored in-memory using a bounded deque (FIFO)
- Maximum capacity: 100 alerts (configurable)
- Automatically pruned when capacity is reached
- Broadcast to all connected WebSocket clients on creation

### Chat Messages
- Stored in-memory using a bounded deque (FIFO)
- Maximum capacity: 100 messages (configurable)
- Broadcast to all connected WebSocket clients on new message
- Includes sender information and timestamp

## API Endpoints

### REST API
- `GET /alerts/history` - Retrieve recent alerts
- `POST /alerts/` - Create and broadcast a new alert

### WebSocket
- `GET /ws` - Connect to the WebSocket for real-time chat messages
