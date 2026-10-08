# 🔌 ConnectorHub

A clean, minimal, and high-performance **AI Agent Connector Gateway & Hub**. Connect user accounts once, securely store credentials in SQLite (AES-256-GCM), and expose curated tool actions to AI agents via **Model Context Protocol (MCP)** and **REST /v1**.

---

## 🌟 Key Architecture & Stack

- **Frontend (`client/`)**:
  - **Next.js 15** (App Router) + **Tailwind CSS**.
  - Typography: **Inter** (`next/font/google`).
  - **Custom Accessible Dropdowns** (`CustomSelect`) replacing raw browser `<select>` tags everywhere.
  - Minimal, high-density monochrome design (clean borders, zero heavy shadows, neutral tones).
- **Backend (`server/`)**:
  - **FastAPI** (Python 3.11+, asynchronous).
  - **SQLite Database** (`aiosqlite` + `SQLAlchemy 2.0`).
  - **SSRF Guarded Fetcher**: Pre-request DNS resolution blocking loopback, LAN, and cloud metadata targets (`169.254.169.254`).
  - **Security Vault**: AES-256-GCM encryption for stored API keys and tokens.
  - **Idempotency Engine**: 24-hour request fingerprint caching with duplicate execution locks.
  - **MCP Server**: 5-tool meta-discovery pattern (`list_apps`, `list_connections`, `search_actions`, `get_action_guide`, `execute_action`).

---

## 🚀 Quick Start

### 1. Start the Backend (`server/`)
```bash
cd server
python -m venv venv
# On Windows:
.\venv\Scripts\pip.exe install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
- API is running at: `http://localhost:8000`
- Interactive API Docs: `http://localhost:8000/docs`
- MCP Endpoint: `http://localhost:8000/mcp`

### 2. Start the Frontend (`client/`)
```bash
cd client
npm install
npm run dev
```
- Web Console: `http://localhost:3000`

---

## 🤖 Connecting to AI Agents via MCP

Add ConnectorHub to your agent host (Cursor, Claude Desktop, Windsurf, or LangChain):

```json
{
  "mcpServers": {
    "connector-hub": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

The agent gains access to the 5 meta-tools without blowing up context windows or receiving raw credentials!
