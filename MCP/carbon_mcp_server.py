# carbon_mcp_server.py
from datetime import datetime, timezone, date
from typing import Dict, Any

import requests
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.carbonintensity.org.uk"
HEADERS = {"Accept": "application/json"}

# Create an MCP server
mcp = FastMCP("CarbonIntensityServer", json_response=True)


def _get_json(path: str) -> Dict[str, Any]:
    """Helper to call the Carbon Intensity API and return parsed JSON."""
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def get_current_intensity() -> Dict[str, Any]:
    """
    Get national carbon intensity for the current half hour (Great Britain).

    Returns:
        {
          "from": ...,
          "to": ...,
          "forecast": ...,
          "actual": ...,
          "index": ...
        }
    """
    payload = _get_json("/intensity")
    data = payload["data"][0]

    intensity = data["intensity"]
    return {
        "from": data["from"],
        "to": data["to"],
        "forecast": intensity.get("forecast"),
        "actual": intensity.get("actual"),
        "index": intensity.get("index"),
    }


@mcp.tool()
def get_today_intensity_stats() -> Dict[str, Any]:
    """
    Get national carbon intensity statistics (min/avg/max) for today (UTC).

    Uses /intensity/stats/{from}/{to}.

    Returns:
        {
          "from": ...,
          "to": ...,
          "min": ...,
          "average": ...,
          "max": ...,
          "index": ...
        }
    """
    today: date = datetime.now(timezone.utc).date()

    # Carbon Intensity API expects ISO8601 times like 2018-01-20T12:00Z:contentReference[oaicite:4]{index=4}
    start = f"{today}T00:00Z"
    end = f"{today}T23:30Z"  # last half-hour window of the day

    payload = _get_json(f"/intensity/stats/{start}/{end}")
    data = payload["data"][0]
    intensity = data["intensity"]

    return {
        "from": data["from"],
        "to": data["to"],
        "min": intensity["min"],
        "average": intensity["average"],
        "max": intensity["max"],
        "index": intensity["index"],
    }


'''
Now this web endpoint contains:

- The list of tools

- Their definitions

- Their parameters

- Their return schema

- The MCP protocol for communicating with them

'''


if __name__ == "__main__":
    # Expose the MCP server over HTTP (default: http://localhost:8000/mcp)
    mcp.run(transport="streamable-http")
