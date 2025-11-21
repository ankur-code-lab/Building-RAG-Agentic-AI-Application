#!/usr/bin/env python
"""
client.py

Simple MCP-style client that spawns server.py as a subprocess
and sends JSON-RPC requests over stdin/stdout.

This is for:
  - "Creating MCP Client"
  - "Client testing" in your training agenda
"""

import json
import subprocess
import sys
import itertools
from pathlib import Path


PYTHON = sys.executable  # current Python interpreter
SERVER_SCRIPT = str(Path(__file__).with_name("server.py"))

_id_counter = itertools.count(1)


class MCPClient:
    def __init__(self):
        self.proc = subprocess.Popen(
            [PYTHON, SERVER_SCRIPT],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,  # line-buffered
        )

    def call(self, method, params=None):
        """Send a single JSON-RPC request and wait for the response."""
        if self.proc.poll() is not None:
            raise RuntimeError("Server process has exited")

        rid = next(_id_counter)
        request = {
            "jsonrpc": "2.0",
            "id": rid,
            "method": method,
            "params": params or {},
        }

        # send
        self.proc.stdin.write(json.dumps(request) + "\n")
        self.proc.stdin.flush()

        # receive single-line response
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("No response from server")

        response = json.loads(line)
        if "error" in response:
            raise RuntimeError(f"Server error: {response['error']}")

        return response["result"]

    def close(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()


def pretty_print_current_intensity(result):
    print("\n=== Current Carbon Intensity (UK National) ===")
    print(f"From      : {result['from']}")
    print(f"To        : {result['to']}")
    print(f"Forecast  : {result['forecast']}")
    print(f"Actual    : {result['actual']}")
    print(f"Index     : {result['index']}")
    print("=============================================\n")


def pretty_print_forecast(results):
    print("\n=== Forecast ===")
    for slot in results:
        print(
            f"{slot['from']} -> {slot['to']}: "
            f"forecast={slot['forecast']} index={slot['index']}"
        )
    print("=============================================\n")


def run_example_scenarios():
    client = MCPClient()
    try:
        # 1. Health check
        print("Calling ping() ...")
        pong = client.call("ping")
        print("Server responded:", pong)

        # 2. Get current intensity
        current = client.call("get_current_intensity")
        pretty_print_current_intensity(current)

        # 3. Get forecast for next 3 hours
        forecast = client.call("get_intensity_forecast", {"hours": 3})
        pretty_print_forecast(forecast)

    finally:
        client.close()


def interactive_menu():
    client = MCPClient()
    try:
        while True:
            print("=== UK Carbon Intensity MCP Client ===")
            print("1. Ping server")
            print("2. Get current intensity")
            print("3. Get forecast (next N hours)")
            print("4. Exit")
            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    print("Result:", client.call("ping"))

                elif choice == "2":
                    result = client.call("get_current_intensity")
                    pretty_print_current_intensity(result)

                elif choice == "3":
                    hours_str = input("Enter number of hours (e.g. 3): ").strip()
                    hours = int(hours_str)
                    result = client.call("get_intensity_forecast", {"hours": hours})
                    pretty_print_forecast(result)

                elif choice == "4":
                    break
                else:
                    print("Invalid choice, please try again.")

            except Exception as e:
                print("Error:", e)

    finally:
        client.close()


if __name__ == "__main__":
    # For training, you can choose either:
    #   run_example_scenarios()
    # or
    #   interactive_menu()
    interactive_menu()
