# 🔌 ConnectorHub

**An open-source, self-hosted integration gateway for AI agents.** Connect app accounts, keep credentials in your own runtime, and expose actions through **Model Context Protocol (MCP)** and a **REST API**.

ConnectorHub is an early-stage open-source alternative for developers evaluating platforms such as [Composio](https://composio.dev/), [Nango](https://nango.dev/), [Merge.dev](https://www.merge.dev/), and [Arcade.dev](https://www.arcade.dev/). It focuses on a small, inspectable self-hosted stack: a FastAPI service, SQLite storage, an MCP interface, and a web console. The current built-in providers are GitHub, Slack, Hacker News, and custom HTTP.

The project is still growing. It does not yet provide the breadth of maintained integrations, managed OAuth catalog, unified normalized APIs, or hosted operations offered by those established platforms. Use it when you want to run the integration layer yourself and extend the provider code to fit your agent.

## Why ConnectorHub

- **Run it yourself:** deploy the API and web console in your own environment.
- **Keep credentials in your runtime:** stored API keys and tokens are encrypted with AES-256-GCM in SQLite.
- **Use MCP or REST:** agents can discover available apps and actions, inspect action guides, and execute actions.
- **Inspect and extend the code:** add providers and actions in Python without depending on a hosted integration catalog.

## How it compares

These products overlap in connecting apps to software and AI agents, but they solve different scopes. Composio focuses on a broad app toolkit and agent execution platform. Nango focuses on building and operating product integrations, including auth and sync. Merge.dev offers unified APIs with common data models across product integration categories. Arcade.dev focuses on agent-ready tools, authentication, and runtime controls. ConnectorHub is a smaller self-hosted project for teams who want to inspect and operate the gateway themselves. Compare their current offerings in the linked product documentation before choosing a platform.

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
