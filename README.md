
# OVS Network Agent

This agent connects to an OVS daemon running a custom MCP server.

## Prerequisites

This agent requires the modified OVS build from:
https://github.com/akhillinux/lightweight-mcp-server-in-c

That repo adds:
- MCP server on port 8080 (OVS switch control)
- AP MCP server on port 8081 (WiFi access point control)

Clone and build that repo first, start ovs-vswitchd, then run this agent.
