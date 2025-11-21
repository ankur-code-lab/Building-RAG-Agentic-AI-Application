#!/usr/bin/env python
"""
server.py

A minimal MCP-style server that exposes tools for the
UK Carbon Intensity API over JSON-RPC via stdin/stdout.

Methods:
  - get_current_intensity()
  - get_intensity_forecast(hours: int = 2)

You can adapt these methods to your real MCP framework.
"""

import sys
import json
import traceback
from datetime import datetime, timedelta, timezone

import requests

BASE_URL = "https://api.carbonintensity.org.uk"


# ---------- Helper functions to talk to the external API ----------

def fetch_current_intensity():
    """Fetch current national carbon intensity."""
    url = f"{BASE_URL}/intensity"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    payload = resp.json()

    # API structure: { "data": [ { "from":..., "to":..., "intensity": {...} } ] }
    data = payload["data"][0]
    return {
        "from": data["from"],
        "to": data["to"],
        "forecast": data["intensity"].get("forecast"),
        "actual": data["intensity"].get("actual"),
        "index": data["intensity"].get("index"),
    }


def fetch_intensity_forecast(hours=2):
    """
    Fetch carbon intensity forecast for the next N hours.
    Uses the /intensity/{from}/{to} endpoint.
    """
    if hours <= 0:
        raise ValueError("hours must be > 0")

    now = datetime.now(timezone.utc)
    end = now + timedelta(hours=hours)

    # Format: YYYY-MM-DDThh:mmZ
    start_str = now.strftime("%Y-%m-%dT%H:%MZ")
    end_str = end.strftime("%Y-%m-%dT%H:%MZ")

    url = f"{BASE_URL}/intensity/{start_str}/{end_str}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    payload = resp.json()

    # Returns list of half-hourly slots
    results = []
    for entry in payload["data"]:
        results.append(
            {
                "from": entry["from"],
                "to": entry["to"],
                "forecast": entry["intensity"].get("forecast"),
                "index": entry["intensity"].get("index"),
            }
        )
    return results


# ---------- JSON-RPC / MCP-style plumbing ----------

def make_error(id_, code, message, data=None):
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": "2.0", "id": id_, "error": err}


def handle_request(request):
    """
    Handle a single JSON-RPC request dict.
    Expected format:
      { "jsonrpc": "2.0", "id": 1, "method": "get_current_intensity", "params": {} }
    """
    rid = request.get("id")

    try:
        method = request.get("method")
        params = request.get("params") or {}

        if method == "get_current_intensity":
            result = fetch_current_intensity()
            return {"jsonrpc": "2.0", "id": rid, "result": result}

        elif method == "get_intensity_forecast":
            hours = int(params.get("hours", 2))
            result = fetch_intensity_forecast(hours=hours)
            return {"jsonrpc": "2.0", "id": rid, "result": result}

        elif method == "ping":
            return {"jsonrpc": "2.0", "id": rid, "result": "pong"}

        else:
            return make_error(rid, -32601, f"Method not found: {method}")

    except requests.HTTPError as e:
        return make_error(
            rid,
            -32001,
            "HTTP error talking to Carbon Intensity API",
            {"status_code": e.response.status_code, "body": e.response.text},
        )
    except Exception as e:
        # For training, we return the traceback in error.data to help learners debug.
        tb = traceback.format_exc()
        return make_error(
            rid,
            -32603,
            f"Internal error: {e}",
            {"traceback": tb},
        )


def main():
    """
    Main loop: read one JSON line per request from stdin,
    write one JSON line per response to stdout.
    This is the stdio pattern used by many MCP servers.
    """
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError as e:
            # We don't know the id here, so use None
            resp = make_error(None, -32700, f"Parse error: {e}")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
            continue

        response = handle_request(request)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
