"""MCP Server for RhinoCommon documentation"""

import asyncio
import json
import logging
from typing import Any, Sequence
from pathlib import Path

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from docs_service import DocsService
import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize server and service
app = Server("rhinocommon")
docs_service = DocsService(config.DOCS_DIR, config.DEFAULT_VERSION)


@app.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available documentation resources"""
    resources = []
    
    for namespace in docs_service.list_namespaces():
        resources.append(
            types.Resource(
                uri=f"rhino://{namespace}",
                name=f"{namespace} Documentation",
                mimeType="application/json",
                description=f"RhinoCommon {namespace} API reference"
            )
        )
    
    logger.info(f"Listed {len(resources)} resources")
    return resources


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content"""
    if not uri.startswith("rhino://"):
        raise ValueError(f"Invalid URI scheme: {uri}")
    
    namespace = uri.replace("rhino://", "")
    data = docs_service._load_namespace(namespace)
    
    if not data:
        raise ValueError(f"Namespace not found: {namespace}")
    
    logger.info(f"Read resource: {namespace}")
    return json.dumps(data, indent=2, ensure_ascii=False)


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="search_rhinocommon",
            description="Search RhinoCommon API by class or method name. Returns matching classes and methods with documentation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term (class name, method name, or keyword)"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Optional: limit search to specific namespace (e.g., 'rhino.geometry')"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_class_details",
            description="Get complete information about a specific RhinoCommon class including all methods, properties, and constructors.",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_name": {
                        "type": "string",
                        "description": "The class name (e.g., 'NurbsSurface', 'Brep')"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Optional: namespace hint to speed up search"
                    }
                },
                "required": ["class_name"]
            }
        ),
        types.Tool(
            name="get_code_examples",
            description="Get practical code examples for a RhinoCommon class showing common usage patterns.",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_name": {
                        "type": "string",
                        "description": "The class name to get examples for"
                    }
                },
                "required": ["class_name"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[types.TextContent]:
    """Execute tool"""
    
    try:
        if name == "search_rhinocommon":
            query = arguments.get("query")
            namespace = arguments.get("namespace")
            
            logger.info(f"Searching: '{query}' in namespace: {namespace or 'all'}")
            results = docs_service.search(query, namespace)
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "query": query,
                        "namespace": namespace,
                        "results": results,
                        "count": len(results)
                    }, indent=2, ensure_ascii=False)
                )
            ]
        
        elif name == "get_class_details":
            class_name = arguments.get("class_name")
            namespace = arguments.get("namespace")
            
            logger.info(f"Getting class details: {class_name}")
            info = docs_service.get_class_info(class_name, namespace)
            
            if not info:
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": f"Class '{class_name}' not found",
                            "suggestion": "Try searching first with search_rhinocommon"
                        }, indent=2)
                    )
                ]
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(info, indent=2, ensure_ascii=False)
                )
            ]
        
        elif name == "get_code_examples":
            class_name = arguments.get("class_name")
            
            logger.info(f"Getting examples for: {class_name}")
            examples = docs_service.get_examples(class_name)
            
            if not examples:
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "class": class_name,
                            "examples": [],
                            "message": "No examples available for this class"
                        }, indent=2)
                    )
                ]
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({
                        "class": class_name,
                        "examples": examples
                    }, indent=2, ensure_ascii=False)
                )
            ]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Tool execution error: {e}", exc_info=True)
        return [
            types.TextContent(
                type="text",
                text=json.dumps({
                    "error": str(e),
                    "tool": name
                }, indent=2)
            )
        ]


async def main():
    """Run MCP server"""
    logger.info("Starting RhinoCommon MCP Server...")
    logger.info(f"Docs path: {docs_service.docs_path}")
    logger.info(f"Available namespaces: {len(docs_service.list_namespaces())}")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())