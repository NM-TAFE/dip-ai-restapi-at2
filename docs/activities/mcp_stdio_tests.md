# MCP STDIO Tests

Use this activity to test the completed Session 7 MCP server over STDIO.

## 1. Setup

``` bash
python -m venv .venv

# macOS / Linux / Git Bash
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\activate

python -m pip install -r requirements.txt
```

## 2. Launch STDIO with MCP Inspector

Inspector launches `converter_stdio_server.py` as a child process. Do
**not** start the STDIO server manually first.

``` bash
npx @modelcontextprotocol/inspector python converter_stdio_server.py
```

Windows venv:

``` powershell
npx @modelcontextprotocol/inspector .\.venv\Scripts\python.exe converter_stdio_server.py
```

macOS/Linux venv:

``` bash
npx @modelcontextprotocol/inspector ./.venv/bin/python converter_stdio_server.py
```

## 3. Confirm the MCP primitives

Tools:

-   `celsius_to_fahrenheit`
-   `fahrenheit_to_celsius`
-   `kilometers_to_miles`
-   `miles_to_kilometers`

Static resources:

-   `resource://unit_reference`
-   `resource://troubleshooting_guide`

Prompts:

-   `explain_conversion`
-   `api_usage`

## 4. Test tools

Suggested values:

``` text
celsius_to_fahrenheit: 25
fahrenheit_to_celsius: 86
kilometers_to_miles: 5
miles_to_kilometers: 3.1
```

Then call `miles_to_kilometers` with a negative value and observe the
error behaviour.

The MCP miles tool calls the reusable Python function directly:

``` text
Inspector → FastMCP tool → miles_to_kilometers_value()
```

It does not call the authenticated REST route, so the REST
`Authorization` header is not required.

## 5. Test static resources

Read:

``` text
resource://unit_reference
resource://troubleshooting_guide
```

The first returns JSON reference data; the second returns plain text.
These resources are static. Dynamic resource templates are introduced in
Session 8.

## 6. Test prompts

Open and test:

``` text
explain_conversion
api_usage
```

The prompt functions return FastMCP `Message` objects.

## 7. Check STDIO logging

STDIO uses stdout for MCP protocol traffic, so do not use `print()` for
application debugging.

Persistent logs:

``` text
logs/mcp_log_stdio.log
```

On macOS/Linux:

``` bash
tail -f logs/mcp_log_stdio.log
```

Depending on Inspector version, stderr diagnostics may appear in its
console view rather than its MCP protocol Logs view.

## 8. Troubleshooting

-   Missing tool: confirm it is included in `ALL_TOOLS`.
-   Missing resource: confirm it is in `RESOURCE_DEFINITIONS`.
-   Prompt error `messages[0] must be Message or str`: confirm prompt
    functions return FastMCP `Message` objects.
-   Protocol parsing problems: remove stray `print()` calls from the
    STDIO server.
-   Inspector cannot launch Python: use the venv Python explicitly.

## 9. Checkpoint

Confirm you can connect Inspector, call all four tools, read both static
resources, open both prompts, locate the STDIO log file, and explain why
the REST bearer token is not required by the manually registered MCP
tool.
