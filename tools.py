# tools.py
# Defines the MCP tools available to Claude

MCP_TOOLS = [
    {
        "name": "get_ports",
        "description": (
            "List all ports and interfaces across all OVS bridges. "
            "Returns port name, type, and which bridge it belongs to. "
            "Call this first before any other tool to understand the current topology."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_flows",
        "description": (
            "Dump the OpenFlow flow tables from all bridges. "
            "Shows all packet forwarding rules currently programmed in the switch. "
            "Use this to diagnose routing or forwarding issues."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_port_stats",
        "description": (
            "Get per-port packet and byte counters (rx/tx) for all interfaces. "
            "Use this to check traffic levels or diagnose packet loss."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "set_vlan",
        "description": (
            "Tag a port with a VLAN ID. "
            "Use this to assign a port to a specific VLAN. "
            "Always call get_ports first to confirm the port name exists."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "port": {
                    "type": "string",
                    "description": "The port name e.g. eth0 or vnet0"
                },
                "vlan": {
                    "type": "integer",
                    "description": "VLAN tag ID between 1 and 4094"
                }
            },
            "required": ["port", "vlan"]
        }
    },
    {
        "name": "set_port_state",
        "description": (
            "Bring a port administratively up or down. "
            "Always call get_ports first to confirm the port name exists."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "port": {
                    "type": "string",
                    "description": "The port name"
                },
                "state": {
                    "type": "string",
                    "enum": ["up", "down"],
                    "description": "Desired state of the port"
                }
            },
            "required": ["port", "state"]
        }
    }
]