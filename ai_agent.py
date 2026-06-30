# agent.py
'''import httpx

# Patch httpx default timeout globally before importing genai
original_init = httpx.Client.__init__
def patched_init(self, **kwargs):
    kwargs.setdefault("timeout", httpx.Timeout(connect=30, read=None, write=30, pool=30))
    original_init(self, **kwargs)
httpx.Client.__init__ = patched_init

from google import genai
from google.genai import types
import os
import json
from mcp_client import call_tool
import os
import json
from google import genai
from google.genai import types
from mcp_client import call_tool



client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_PROMPT = """You are a network operations assistant with direct access
to a live Open vSwitch (OVS) daemon running on this machine.
You can inspect and modify the virtual switch using the provided tools.
Guidelines:
- Always call get_ports first before any operation
- Before modifying anything, explain what you are about to do and why
- After making a change, verify it by calling get_ports again
- If a tool returns an error, report it clearly
- Be concise but thorough in your explanations
"""

TOOLS = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="get_ports",
        description="List all ports and interfaces across all OVS bridges.",
        parameters=types.Schema(type="OBJECT", properties={})
    ),
    types.FunctionDeclaration(
        name="get_flows",
        description="Dump the OpenFlow flow tables from all bridges.",
        parameters=types.Schema(type="OBJECT", properties={})
    ),
    types.FunctionDeclaration(
        name="get_port_stats",
        description="Get per-port packet and byte counters for all interfaces.",
        parameters=types.Schema(type="OBJECT", properties={})
    ),
    types.FunctionDeclaration(
        name="set_vlan",
        description="Tag a port with a VLAN ID.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "port": types.Schema(type="STRING", description="Port name"),
                "vlan": types.Schema(type="INTEGER", description="VLAN ID 1-4094")
            },
            required=["port", "vlan"]
        )
    ),
    types.FunctionDeclaration(
        name="set_port_state",
        description="Bring a port administratively up or down.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "port": types.Schema(type="STRING", description="Port name"),
                "state": types.Schema(type="STRING", description="up or down")
            },
            required=["port", "state"]
        )
    )
])


def run_agent(user_question: str) -> str:
    print(f"\n{'='*50}")
    print(f"Question: {user_question}")
    print(f"{'='*50}")

    contents = [types.Content(
        role="user",
        parts=[types.Part(text=user_question)]
    )]

    while True:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[TOOLS]
            )
        )

        # Collect tool calls if any
        tool_calls = []
        for part in response.candidates[0].content.parts:
            if part.function_call:
                tool_calls.append(part.function_call)

        # No tool calls — final answer
        if not tool_calls:
            for part in response.candidates[0].content.parts:
                if part.text:
                    return part.text
            return "No response from agent."

        # Append Gemini's response to contents
        contents.append(response.candidates[0].content)

        # Execute tools and collect results
        tool_response_parts = []
        for fn_call in tool_calls:
            tool_name = fn_call.name
            tool_args = dict(fn_call.args) if fn_call.args else {}

            print(f"\n[Tool call]: {tool_name}")
            if tool_args:
                print(f"[Arguments]: {json.dumps(tool_args, indent=2)}")

            result = call_tool(tool_name, tool_args)
            print(f"[Result]: {json.dumps(result, indent=2)[:500]}")

            tool_response_parts.append(types.Part(
                function_response=types.FunctionResponse(
                    name=tool_name,
                    response={"result": json.dumps(result)}
                )
            ))

        # Feed results back to Gemini
        contents.append(types.Content(
            role="user",
            parts=tool_response_parts
        ))

        /////'''
        # agent.py
import os
import json
from groq import Groq
from mcp_client import call_tool

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are a network operations assistant with direct access
to a live Open vSwitch (OVS) daemon running on this machine.
You can inspect and modify the virtual switch using the provided tools.
Guidelines:
- Always call get_ports first before any operation
- Before modifying anything, explain what you are about to do and why
- After making a change, verify it by calling get_ports again
- If a tool returns an error, report it clearly
- Be concise but thorough in your explanations
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_ports",
            "description": "List all ports and interfaces across all OVS bridges.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_flows",
            "description": "Dump the OpenFlow flow tables from all bridges.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_port_stats",
            "description": "Get per-port packet and byte counters for all interfaces.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_vlan",
            "description": "Tag a port with a VLAN ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "port": {
                        "type": "string",
                        "description": "The port name e.g. eth0 or vnet0"
                    },
                    "vlan": {
                        "type": "integer",
                        "description": "VLAN ID between 1 and 4094"
                    }
                },
                "required": ["port", "vlan"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_port_state",
            "description": "Bring a port administratively up or down.",
            "parameters": {
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
    }
]


def run_agent(user_question: str) -> str:
    print(f"\n{'='*50}")
    print(f"Question: {user_question}")
    print(f"{'='*50}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]

    while True:
        print("[Calling Groq API...]")
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=4096
        )
        print("[Groq responded]")

        msg = response.choices[0].message
        messages.append(msg)

        # No tool calls — final answer
        if not msg.tool_calls:
            return msg.content or "No response from agent."

        # Execute tool calls
        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments or "{}")

            print(f"\n[Tool call]: {tool_name}")
            if tool_args:
                print(f"[Arguments]: {json.dumps(tool_args, indent=2)}")

            result = call_tool(tool_name, tool_args)
            print(f"[Result]: {json.dumps(result, indent=2)[:500]}")

            # Feed result back
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })
        print("[Sending tool results back to Groq...]")