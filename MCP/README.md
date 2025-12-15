# 📘 Carbon Intensity Agent (Pydantic-AI + MCP + Groq LLM)

## 🌍 Overview

This project demonstrates how to build a **tool-calling AI agent**
using:

-   **Pydantic-AI** --- Agent framework\
-   **Groq LLM** (OpenAI-compatible API using `openai/gpt-oss-120b`)\
-   **MCP (Model Context Protocol)** --- to expose real-world tools\
-   **Carbon Intensity API (UK)** ---
    `https://api.carbonintensity.org.uk/`

The AI agent can answer questions like:

> **"What is the carbon intensity today?"**

It does this by calling an MCP server, which fetches real data from the
Carbon Intensity API.

------------------------------------------------------------------------

# 🧱 Architecture

    User → Agent (Pydantic AI) → Groq LLM
                                      │
                                      ▼
                        MCP Server (your tools)
                                      │
                                      ▼
                https://api.carbonintensity.org.uk/

### ✨ Key Idea

The agent **does not import** Python files.\
Instead, it **connects over HTTP** to the MCP server, which exposes
tools like:

-   `get_current_intensity()`
-   `get_today_intensity_stats()`

The MCP server *publishes* these tools, and the agent automatically
discovers them.

------------------------------------------------------------------------

# 📦 Project Structure

    .
    ├── agent_with_mcp.py          # The AI agent using Groq + MCP tools
    ├── carbon_mcp_server.py       # MCP server exposing API tools
    ├── .env                       # Environment variables (Groq API key)
    ├── pyproject.toml             # Project configuration
    └── README.md                  # This file

------------------------------------------------------------------------

# ⚙️ Installation

## 1. Clone the project

``` bash
git clone <your_repo_url>
cd carbon-intensity-agent
```

## 2. Install dependencies

``` bash
pip install -e .
```

Or:

``` bash
pip install .
```

## 3. Install python-dotenv (optional, recommended)

``` bash
pip install python-dotenv
```

------------------------------------------------------------------------

# 🔐 Environment Variables (.env)

Create a `.env` file in the project root:

    GROQ_API_KEY=your_groq_api_key

These are automatically loaded by `python-dotenv` inside your agent.

------------------------------------------------------------------------

# 🚀 Running the System

## Step 1 --- Start the MCP Server

``` bash
python carbon_mcp_server.py
```

This starts a server at:

    http://localhost:8000/mcp

It exposes tools: - `get_current_intensity` -
`get_today_intensity_stats`

------------------------------------------------------------------------

## Step 2 --- Run the Agent

In a second terminal:

``` bash
python agent_with_mcp.py
```

You should see output like:

    User: What is the carbon intensity today?
    Assistant: The average carbon intensity today is 125 gCO2/kWh...

The agent automatically:

1.  Understands the question\
2.  Chooses the correct MCP tool (`get_today_intensity_stats`)\
3.  MCP server calls the API and retrieves real data\
4.  LLM uses the data to generate the final answer

------------------------------------------------------------------------

# 🧠 How MCP Integration Works

The agent connects to the MCP server using:

``` python
server = MCPServerStreamableHTTP("http://localhost:8000/mcp")
```

This does **not** import Python files.

Instead:

-   The MCP server *publishes* its tools at that URL\
-   The agent loads tool definitions from the server\
-   Tools become available to the LLM for tool-calling

This is why you don't need:

``` python
import carbon_mcp_server
```

The server handles everything dynamically.

------------------------------------------------------------------------

# 📚 Code Files

## **carbon_mcp_server.py**

This exposes API tools using the MCP SDK:

-   Fetch current carbon intensity\
-   Fetch today's min/avg/max intensity\
-   Format the result\
-   Serve via the MCP HTTP transport

You run it once as a background process.

------------------------------------------------------------------------

## **agent_with_mcp.py**

This:

-   Loads environment variables\
-   Creates a Groq-compatible model\
-   Connects to the MCP server\
-   Registers tools for auto-calling\
-   Sends your question to the LLM\
-   Prints the final answer

------------------------------------------------------------------------

# 🧪 Example Queries

Try these:

-   **"What is the carbon intensity today?"**
-   **"What is the carbon intensity right now?"**
-   **"Give me today's minimum and maximum intensity."**

------------------------------------------------------------------------

# 🛠️ Customization

You can extend the MCP server to add tools for:

-   Regional carbon intensity\
-   Generation mix (wind, solar, gas, nuclear)\
-   Forecasts\
-   Historical ranges

Just add more `@mcp.tool()` functions.

------------------------------------------------------------------------

# 💡 Tips

-   The MCP server must be running before the agent starts\
-   If the agent cannot reach the MCP server, it will not know any
    tools\
-   Always verify environment variables for Groq

------------------------------------------------------------------------

# 📄 License

MIT (or your preferred license)
