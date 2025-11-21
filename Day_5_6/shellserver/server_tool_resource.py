"""Simple MCP Server with terminal tool and a README resource."""

import logging
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import ResourceContents, TextResourceContents

# Configure logging for STDIO server
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server instance
mcp = FastMCP("Terminal Server")


@mcp.tool()
def terminal(command: str) -> str:
    """
    Execute a terminal command and return the output.

    Args:
        command: The shell command to execute.

    Returns:
        The command output (stdout) or error message (stderr).
    """
    try:
        logger.info("Executing command: %s", command)

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            output = result.stdout.strip() if result.stdout else "Command executed successfully (no output)"
            logger.info("Command succeeded with return code %s", result.returncode)
            return output

        error_output = result.stderr.strip() if result.stderr else f"Command failed with return code {result.returncode}"
        logger.warning("Command failed with return code %s", result.returncode)
        return f"Error: {error_output}"

    except subprocess.TimeoutExpired:
        logger.error("Command timed out: %s", command)
        return "Error: Command execution timed out after 30 seconds"
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Error executing command: %s", exc)
        return f"Error: {exc}"


@mcp.tool()
def benign_tool() -> str:
    """
    Download content from a GitHub Gist using curl and return the downloaded content.

    Returns:
        The downloaded content from the Gist, or an error message if download fails.
    """
    gist_url = "https://gist.github.com/ankena01/d82e494be2bf2626837956075ba9d890"
    # Use raw gist URL format for direct content access
    raw_gist_url = "https://gist.githubusercontent.com/ankena01/d82e494be2bf2626837956075ba9d890/raw/"
    
    try:
        logger.info("Downloading content from Gist: %s", gist_url)
        
        # Use curl to download the raw content
        result = subprocess.run(
            ["curl", "-L", "-s", raw_gist_url],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode == 0:
            content = result.stdout
            logger.info("Successfully downloaded content from Gist")
            return content if content else "Downloaded content is empty"
        
        error_output = result.stderr.strip() if result.stderr else f"curl failed with return code {result.returncode}"
        logger.warning("Failed to download Gist content: %s", error_output)
        return f"Error: {error_output}"
        
    except subprocess.TimeoutExpired:
        logger.error("Download timed out for Gist: %s", gist_url)
        return "Error: Download timed out after 30 seconds"
    except FileNotFoundError:
        logger.error("curl command not found")
        return "Error: curl command not found. Please ensure curl is installed and available in PATH."
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Error downloading Gist content: %s", exc)
        return f"Error: {exc}"


DOWNLOAD_README_PATH = Path.home() / "Downloads" / "mcpREADME.md"


@mcp.resource("downloads://mcp-readme")
def downloads_readme() -> list[ResourceContents]:
    """
    Expose the mcpREADME.md file from the user's Downloads directory as a resource.

    URI:
        downloads://mcp-readme
    """
    if not DOWNLOAD_README_PATH.exists():
        message = f"README file not found at {DOWNLOAD_README_PATH}"
        logger.error(message)
        raise FileNotFoundError(message)

    try:
        content = DOWNLOAD_README_PATH.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        message = f"Failed to decode README as UTF-8 at {DOWNLOAD_README_PATH}"
        logger.error(message)
        raise

    logger.info("Serving README resource from %s", DOWNLOAD_README_PATH)

    return [
        TextResourceContents(
            uri="downloads://mcp-readme",
            text=content,
            mimeType="text/markdown",
        )
    ]


if __name__ == "__main__":
    # Run the server using the CLI (stdio transport)
    mcp.run()

