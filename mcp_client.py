# mcp_client.py
# Handles HTTP communication with the OVS MCP server

import requests
import json

MCP_URL = "http://localhost:8080/mcp"
TIMEOUT = None # seconds


def call_tool(tool_name: str, arguments: dict = None) -> dict:
    """
    Send a tool call to the OVS MCP server.
    Returns the parsed JSON response or an error dict.
    """
    payload = {"tool": tool_name}
    if arguments:
        payload["arguments"] = arguments
    print(f"[MCP] Sending request to OVS: {tool_name}")
    try:
        response = requests.post(
            MCP_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        return {
            "error": f"Could not connect to OVS MCP server at {MCP_URL}. "
                     f"Is ovs-vswitchd running?"
        }
    except requests.exceptions.Timeout:
        return {
            "error": f"Request timed out after {TIMEOUT} seconds."
        }
    except requests.exceptions.HTTPError as e:
        return {
            "error": f"HTTP error: {e.response.status_code} {e.response.text}"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }