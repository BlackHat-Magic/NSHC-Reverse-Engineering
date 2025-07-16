from typing import Optional
from contextlib import AsyncExitStack
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# from anthropic import Anthropic

import asyncio
import os
import sys

load_dotenv()

API_BASE_URI = os.environ.get("API_BASE_URI", None)
if(API_BASE_URI is None):
    print("API_BASE_URI is None.")
    sys.exit()

API_KEY = os.environ.get("API_KEY", None)
if(API_KEY is None):
    # this might be okay if we're using something like a ollama server
    # without authentication
    print("Warning:\tAPI_KEY is None.")

class MCP_Client:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm_client = OpenAI()
    
    async def connect_to_server(self, server_script_path: str):
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if(not is_python and not is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"

        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None,
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using LLM and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema,
        } for tool in response.tools]

        response = self.anthropic.messages.create(
            model="",
            max_tokens=1024,
            messages=messages,
            tools=available_tools,
        )

        final_text = []
