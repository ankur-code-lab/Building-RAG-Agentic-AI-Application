# agent_with_mcp.py
import asyncio

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
load_dotenv()
# from pydantic_ai.models.openai import OpenAIChatModel

# Model: Groq's OpenAI-compatible GPT-OSS 120B
# Assumes:
#   OPENAI_API_KEY   = your Groq API key
#   OPENAI_BASE_URL  = "https://api.groq.com/openai/v1"
# model = OpenAIChatModel("openai/gpt-oss-120b")
model = "groq:openai/gpt-oss-120b"


'''
Connect to whatever MCP server is running at http://localhost:8000/mcp and load all the tools that server exposes
'''

# MCP server (the one we defined in carbon_mcp_server.py)
server = MCPServerStreamableHTTP("http://localhost:8000/mcp")

agent = Agent(
    model,
    toolsets=[server],
    system_prompt=(
        "You are an assistant that answers questions about "
        "UK electricity carbon intensity.\n"
        "- Use the MCP tools from the CarbonIntensityServer.\n"
        "- Never invent numbers; always call a tool when "
        "giving carbon intensity values.\n"
        "- For 'today' questions, prefer get_today_intensity_stats.\n"
        "- For 'right now' questions, prefer get_current_intensity."
    ),
)




'''
The MCP server automatically generates a list of instructions describing:

each tool, its arguments, what it returns.

This decorator: @agent.instructions, Adds those instructions to the LLM's system context

So the model knows what tools exist and how to call them. Without this, the LLM would not know that tools exist.
'''



@agent.instructions
async def mcp_server_instructions() -> str:
    """
    Add the MCP server's own instructions (including tool descriptions)
    into the agent's system context so the model knows what it can call.
    """
    return server.instructions


async def main() -> None:
    # Example question you mentioned
    # question = "What is the carbon intensity currently?"
    # question = "What is the carbon intensity before 2 days?"
    question = "What is the carbon intensity today?"
    result = await agent.run(question)

    print("User:", question)
    print("Assistant:", result.output)


if __name__ == "__main__":
    asyncio.run(main())
