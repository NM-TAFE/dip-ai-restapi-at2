# Miles-to-Kilometers Refactor Review

This activity reviews the completed Session 7 refactor. The final
application separates reusable conversion logic, REST
authentication/authorization, and MCP tool registration.

## 1. Review the base conversion pattern

Open `mcp_tools/converter_tools.py` and identify reusable conversion
functions, FastAPI routes, and `TOOL_DEFINITIONS`.

``` text
HTTP route ─┐
            ├── reusable Python function
MCP tool ───┘
```

## 2. Review miles-to-kilometers

Open `mcp_tools/miles_to_km.py` and identify:

-   `ConversionRequest`
-   `ConversionResponse`
-   `miles_to_kilometers_value()`
-   authenticated FastAPI route
-   `TOOL_DEFINITION`

## 3. Authentication

Open `utils/get_principal.py`.

The REST route requires:

``` text
Authorization: Bearer <token>
```

Missing/malformed bearer authentication produces
`401 Missing or invalid token`.

For the demo, tokens containing `demo-token` receive roles
`utility.read`, `conversion.run`, and scope `miles:convert`.

## 4. Authorization

Open `utils/enforce_permissions.py`.

Required roles/scopes are checked after authentication. A syntactically
valid bearer token without the required permissions produces
`403 Forbidden`.

## 5. Request and response

REST request:

``` json
{"miles": 3.1}
```

A successful response contains `result`, `operation`, and runtime
`audited_at`.

## 6. Test REST security

Start:

``` bash
python converter_streamable_http_server.py
```

401:

``` bash
curl -i -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -d '{"miles": 5}'
```

403:

``` bash
curl -i -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer other-token" \
  -d '{"miles": 5}'
```

200:

``` bash
curl -i -X POST "http://localhost:8003/miles-to-kilometers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer demo-token" \
  -d '{"miles": 5}'
```

## 7. Compare the MCP tool

In Inspector call `miles_to_kilometers` with:

``` json
{"miles": 5}
```

No REST bearer token is required because the MCP server manually
registers `miles_to_kilometers_value()` rather than generating a tool
from the authenticated FastAPI route.

## 8. Trace both paths

``` text
REST
POST /miles-to-kilometers
        ↓
get_current_principal()
        ↓
enforce_permissions()
        ↓
miles_to_kilometers_value()

MCP
miles_to_kilometers
        ↓
miles_to_kilometers_value()
```

## 9. Session 7 checkpoint

Confirm you can explain authentication (`401`) versus authorization
(`403`), why the reusable function contains no HTTP dependency, why the
REST route is protected, why the manually registered MCP tool currently
does not use the REST bearer token, and how STDIO and Streamable HTTP
expose the same MCP tool definitions.

This is the completed state before Session 8 adds dynamic resources.
