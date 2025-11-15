"""Configuration for MCP server"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

# Default Rhino version
DEFAULT_VERSION = "8"

# Server settings
CACHE_ENABLED = True
CACHE_SIZE = 100  # Number of documents to cache

# Logging
LOG_LEVEL = "INFO"