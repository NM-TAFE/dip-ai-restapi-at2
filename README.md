# Unit Converter API + MCP Tutorial

This project is the completed Session 7 unit-converter example and the
starting point for Session 8 dynamic MCP resources.

It demonstrates the same conversion logic through two interfaces:

-   **FastAPI REST routes** for conventional HTTP access.
-   **FastMCP** for MCP tools, static resources, and prompts over STDIO
    or Streamable HTTP.

The MCP tools are registered manually from reusable Python conversion
functions. They are **not** auto-generated from the FastAPI/OpenAPI
routes.

## Current architecture

``` text
FastAPI application
├── REST conversion routes
│   ├── celsius-to-fahrenheit
│   ├── fahrenheit-to-celsius
│   ├── kilometers-to-miles
│   └── miles-to-kilometers
│       └── authentication + permission checks
├── /health
└── /mcp
    └── FastMCP
        ├── Tools
        ├── Static resources
        └── Prompts

STDIO
└── converter_stdio_server.py
    └── FastMCP
        ├── Tools
        ├── Static resources
        └── Prompts
```

The REST and MCP interfaces reuse the same core conversion functions.
The authenticated REST route and the MCP tool are separate interfaces.

## Prerequisites

-   Python 3.10+
-   Python virtual environment
-   Node.js/npm for MCP Inspector

## Setup

``` bash
python -m venv .venv

# macOS / Linux / Git Bash
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\activate

python -m pip install -r requirements.txt
```

## Run FastAPI + Streamable HTTP MCP

``` bash
python converter_streamable_http_server.py

# or
python -m converter_streamable_http_server
```

The server uses port `8003`:

-   Swagger UI: `http://localhost:8003/docs`
-   ReDoc: `http://localhost:8003/redoc`
-   Health: `http://localhost:8003/health`
-   MCP Streamable HTTP: `http://localhost:8003/mcp`

There is no separate SSE endpoint in this version.

## REST API tests

The first three routes accept their conversion value as a query
parameter.

``` bash
curl -X POST "http://localhost:8003/celsius-to-fahrenheit?celsius=25"
curl -X POST "http://localhost:8003/fahrenheit-to-celsius?fahrenheit=86"
curl -X POST "http://localhost:8003/kilometers-to-miles?kilometers=5"
```

### Authenticated miles-to-kilometers route

No token --- expect `401`:

``` bash
curl -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -d '{"miles": 3.1}'
```

Valid bearer format but no demo permissions --- expect `403`:

``` bash
curl -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer other-token" \
  -d '{"miles": 3.1}'
```

Valid demo token --- expect `200`:

``` bash
curl -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer demo-token" \
  -d '{"miles": 3.1}'
```

The demo authentication rule grants the required roles and scope to
bearer tokens containing `demo-token`.

## MCP tools

Both MCP transports manually register:

-   `celsius_to_fahrenheit`
-   `fahrenheit_to_celsius`
-   `kilometers_to_miles`
-   `miles_to_kilometers`

The MCP `miles_to_kilometers` tool calls `miles_to_kilometers_value()`
directly. It does **not** call the authenticated REST endpoint, so the
REST bearer token is not required for this MCP tool.

## Current static MCP resources

Before Session 8 dynamic resources, the server exposes:

-   `resource://unit_reference`
-   `resource://troubleshooting_guide`

These are intentionally static. Session 8 extends this design with
resource templates and dynamic values.

## MCP prompts

-   `explain_conversion`
-   `api_usage`

Prompt functions return FastMCP `Message` objects.

## Test Streamable HTTP with MCP Inspector

Start the server:

``` bash
python converter_streamable_http_server.py
```

Connect Inspector using **Streamable HTTP** to:

``` text
http://localhost:8003/mcp
```

You should see four tools, two static resources, and two prompts.

## Test STDIO with MCP Inspector

Do **not** start the STDIO server separately. Inspector launches it as a
child process.

``` bash
npx @modelcontextprotocol/inspector python converter_stdio_server.py
```

Windows virtual environment:

``` powershell
npx @modelcontextprotocol/inspector .\.venv\Scripts\python.exe converter_stdio_server.py
```

macOS/Linux virtual environment:

``` bash
npx @modelcontextprotocol/inspector ./.venv/bin/python converter_stdio_server.py
```

## STDIO logging

STDIO reserves stdout for MCP protocol traffic. Do not use `print()` for
application debugging in the STDIO server.

Persistent STDIO logs:

``` text
logs/mcp_log_stdio.log
```

Persistent Streamable HTTP logs:

``` text
logs/mcp_log_streamable_http.log
```

Watch a log on macOS/Linux:

``` bash
tail -f logs/mcp_log_stdio.log
```

## Activities

See `docs/activities/`:

-   `mcp_curl_tests.md` --- REST and Streamable HTTP testing.
-   `mcp_stdio_tests.md` --- Inspector and STDIO testing.
-   `mcp_sdk_repl_lab.md` --- inspect the current FastAPI/FastMCP
    objects.
-   `miles_to_km_refactor_lab.md` --- review authentication,
    permissions, and reusable-function separation.

## Session 8 starting point

The application now has reusable conversion functions, conventional
FastAPI routes, one authenticated/authorised REST route, manually
registered MCP tools, two static MCP resources, two MCP prompts, STDIO
and Streamable HTTP transports, and logging.

The next step is to extend the **resource layer** without changing this
overall architecture.
