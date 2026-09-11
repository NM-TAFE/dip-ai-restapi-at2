import json
import logging
from pathlib import Path

from fastmcp import FastMCP

from mcp_tools.converter_tools import TOOL_DEFINITIONS
from mcp_tools.miles_to_km import TOOL_DEFINITION
from mcp_resources.converter_resources import RESOURCE_DEFINITIONS
from mcp_prompts.converter_prompts import PROMPT_DEFINITIONS

from utils.logging_utils import build_log_config, configure_logging


# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

LOG_FILE = Path("./logs/mcp_log_stdio.log")

configure_logging(
    build_log_config(
        LOG_FILE,
        console=True,
        logger_handlers={
            "fastmcp": ["rotating_file", "console"],
            __name__: ["rotating_file", "console"],
        },
        root_level="INFO",
        logger_level="DEBUG",
    )
)

logger = logging.getLogger(__name__)

logger.info("STDIO logging configured")
logger.info("Log file: %s", LOG_FILE.resolve())


# -------------------------------------------------------------------
# MCP Server
# -------------------------------------------------------------------

mcp = FastMCP("Unit Converter (STDIO)")

ALL_TOOLS = TOOL_DEFINITIONS + TOOL_DEFINITION


# -------------------------------------------------------------------
# Register tools
# -------------------------------------------------------------------

for tool in ALL_TOOLS:
    logger.debug("Registering MCP tool: %s", tool["name"])

    mcp.tool(
        name=tool["name"],
        description=tool.get("description", tool["name"]),
    )(tool["func"])


# -------------------------------------------------------------------
# Register static resources
# -------------------------------------------------------------------

for resource in RESOURCE_DEFINITIONS:
    uri = f"resource://{resource['name']}"
    display_name = resource.get("description", resource["name"])
    mime = resource.get("mime_type", "text/plain")
    resource_function = resource["func"]

    logger.debug(
        "Registering MCP resource: %s (%s)",
        uri,
        mime,
    )

    def register_static_resource(
        uri: str,
        name: str,
        mime: str,
        resource_function,
    ):
        @mcp.resource(
            uri,
            name=name,
            mime_type=mime,
        )
        def _resource():
            logger.info("Resource requested: %s", uri)

            resource_value = resource_function()

            if isinstance(resource_value, (str, bytes)):
                return resource_value

            # Dicts and other serializable values are returned as JSON text.
            return json.dumps(resource_value)

    register_static_resource(
        uri,
        display_name,
        mime,
        resource_function,
    )


# -------------------------------------------------------------------
# Register prompts
# -------------------------------------------------------------------

for prompt in PROMPT_DEFINITIONS:
    name = prompt["name"]
    desc = prompt.get("description", name)
    prompt_function = prompt["func"]

    logger.debug("Registering MCP prompt: %s", name)

    mcp.prompt(
        name=name,
        description=desc,
    )(prompt_function)


# -------------------------------------------------------------------
# Run STDIO server
# -------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting Unit Converter MCP server using STDIO")
    logger.info(
        "Registered %d tools, %d resources and %d prompts",
        len(ALL_TOOLS),
        len(RESOURCE_DEFINITIONS),
        len(PROMPT_DEFINITIONS),
    )

    mcp.run()