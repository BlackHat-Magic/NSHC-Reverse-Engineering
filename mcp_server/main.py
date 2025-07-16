from mcp.server.fastmcp import FastMCP
from typing import Any
# import httpx
import subprocess

mcp = FastMCP("reverse_engineer")

@mcp.tool()
async def call_strings(filename: str) -> tuple[int, str, str]:
    """Call the `strings` application on a given file (usually a binary)"""
    try:
        process = subprocess.Popen(
            ["strings", filename],
            executable="/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process,communicate()
        exit_code = process.returncode
        return(exit_code, stdout, stderr)
    except FileNotFoundError as e:
        if(e.filename == "strings"):
            return(127, "", "The `strings` command was not found.")
        elif(filename in e.filename):
            return(127, "", f"{filename} not found.")
        else:
            return(127, "", "Bash not found.")
    except Exception as e:
        return(127, "", f"Other error: {e}")

@mcp.tool()
async def call_objdump(filename:str) -> tuple[int, str, str]:
    """Call the `objdump` application with the `-d` flag on a given file (usually a binary)"""
    try:
        process = subprocess.Popen(
            ["objdump", "-d", filename],
            executable="/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process,communicate()
        exit_code = process.returncode
        return(exit_code, stdout, stderr)
    except FileNotFoundError as e:
        if(e.filename == "strings"):
            return(127, "", "The `objdump` command was not found.")
        elif(filename in e.filename):
            return(127, "", f"{filename} not found.")
        else:
            return(127, "", "Bash not found.")
    except Exception as e:
        return(127, "", f"Other error: {e}")

if(__name__ == "__main__"):
    print("starting mcp server")
    mcp.run(transport="stdio")
