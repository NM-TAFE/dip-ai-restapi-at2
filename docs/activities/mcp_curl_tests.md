# REST and Streamable HTTP MCP Tests

Run:

``` bash
python converter_streamable_http_server.py
```

The application defaults to `http://localhost:8003`.

## 1. Health check

``` bash
curl http://localhost:8003/health
```

## 2. Plain REST conversion routes

These routes take their values as query parameters:

``` bash
curl -X POST "http://localhost:8003/celsius-to-fahrenheit?celsius=25"
curl -X POST "http://localhost:8003/fahrenheit-to-celsius?fahrenheit=86"
curl -X POST "http://localhost:8003/kilometers-to-miles?kilometers=5"
```

## 3. Authenticated REST route

Miles-to-kilometers uses a JSON body plus authentication and permission
checks.

No token --- expect `401`:

``` bash
curl -i -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -d '{"miles": 3.1}'
```

Bearer token without demo permissions --- expect `403`:

``` bash
curl -i -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer other-token" \
  -d '{"miles": 3.1}'
```

Valid demo token --- expect `200`:

``` bash
curl -i -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer demo-token" \
  -d '{"miles": 3.1}'
```

## 4. MCP Streamable HTTP endpoint

``` text
http://localhost:8003/mcp
```

The MCP server manually registers its tools. It is not generated from
FastAPI/OpenAPI.

Therefore the MCP `miles_to_kilometers` tool calls
`miles_to_kilometers_value()` directly and does not require the REST
route's bearer token.

## 5. Inspector test

Start the application, then connect MCP Inspector using **Streamable
HTTP** to:

``` text
http://localhost:8003/mcp
```

Confirm:

Tools: - `celsius_to_fahrenheit` - `fahrenheit_to_celsius` -
`kilometers_to_miles` - `miles_to_kilometers`

Static resources: - `resource://unit_reference` -
`resource://troubleshooting_guide`

Prompts: - `explain_conversion` - `api_usage`

## 6. Compare REST and MCP

``` text
REST /miles-to-kilometers
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

Explain why one currently requires an HTTP bearer token while the other
does not.

## 7. Logs

Streamable HTTP/Uvicorn logs are written to:

``` text
logs/mcp_log_streamable_http.log
```

On macOS/Linux:

``` bash
tail -f logs/mcp_log_streamable_http.log
```

Inspector is an HTTP client of the independently running server, so
Python/Uvicorn logs remain with the server process and log file.
