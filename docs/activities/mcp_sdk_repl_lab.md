# FastAPI + FastMCP SDK REPL Lab

Use this activity to inspect the completed Session 7 application before
adding dynamic resources.

The current architecture uses `FastMCP(...)` and manually registers
reusable Python functions as MCP tools. It does **not** use
`FastMCP.from_fastapi(...)`.

## 1. Start an async-capable REPL

``` bash
python -m asyncio
```

## 2. Inspect FastAPI

``` python
>>> from fastapi import FastAPI
>>> app = FastAPI(title="Unit Converter MCP Server", version="1.2.1")
>>> app.title
>>> app.version
>>> app.openapi_url
```

## 3. Inspect a basic FastMCP server

``` python
>>> from fastmcp import FastMCP
>>> mcp = FastMCP("Unit Converter MCP Server")
>>> mcp.name
>>> await mcp.list_tools()
```

A new server has no project tools until they are registered.

## 4. Inspect tool definitions

``` python
>>> from mcp_tools.converter_tools import TOOL_DEFINITIONS
>>> from mcp_tools.miles_to_km import TOOL_DEFINITION
>>> ALL_TOOLS = TOOL_DEFINITIONS + TOOL_DEFINITION
>>> [tool["name"] for tool in ALL_TOOLS]
```

Expected:

``` text
celsius_to_fahrenheit
fahrenheit_to_celsius
kilometers_to_miles
miles_to_kilometers
```

Call the reusable function directly:

``` python
>>> from mcp_tools.miles_to_km import miles_to_kilometers_value
>>> miles_to_kilometers_value(3.1)
```

## 5. Manually register tools

``` python
>>> mcp2 = FastMCP("REPL Unit Converter")
>>> for tool in ALL_TOOLS:
...     mcp2.tool(name=tool["name"], description=tool["description"])(tool["func"])
...
>>> await mcp2.list_tools()
```

This is the registration approach used by the project MCP servers.

## 6. Inspect the real project

``` python
>>> import converter_streamable_http_server as srv
>>> srv.app.title
>>> srv.app.version
>>> len(srv.app.routes)
>>> srv.mcp.name
>>> await srv.mcp.list_tools()
```

You should not see an OpenAPI-generated name such as
`miles_to_kilometers_miles_to_kilometers_post`.

## 7. Inspect static resources

``` python
>>> from mcp_resources.converter_resources import RESOURCE_DEFINITIONS
>>> [resource["name"] for resource in RESOURCE_DEFINITIONS]
```

Expected:

``` text
unit_reference
troubleshooting_guide
```

These are the static resources Session 8 will extend.

## 8. Inspect prompts

``` python
>>> from mcp_prompts.converter_prompts import PROMPT_DEFINITIONS
>>> [prompt["name"] for prompt in PROMPT_DEFINITIONS]
```

Expected:

``` text
explain_conversion
api_usage
```

## 9. Compare REST authentication and MCP

``` text
POST /miles-to-kilometers
        ↓
get_current_principal()
        ↓
enforce_permissions()
        ↓
miles_to_kilometers_value()

MCP miles_to_kilometers
        ↓
miles_to_kilometers_value()
```

The pure function has no HTTP dependency. Authentication belongs to the
protected REST interface.

## 10. Health route

With the HTTP server running:

``` bash
curl http://localhost:8003/health
```

## 11. Checkpoint

Explain why `FastMCP.from_fastapi()` is not used, why MCP tool names are
predictable, why the REST route and MCP tool can reuse the same
function, and why the current resources are static.
