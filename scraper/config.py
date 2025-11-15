"""Configuration for RhinoCommon scraper"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

# Rhino versions
SUPPORTED_VERSIONS = ["7", "8"]
DEFAULT_VERSION = "8"

# API endpoints
API_BASE_URL = "https://developer.rhino3d.com/api/rhinocommon/"
# API_BASE_URL = "https://mcneel-apidocs.herokuapp.com/api/rhinocommon/"

# Namespaces to scrape
NAMESPACES = [
    "rhino",
    "rhino.geometry",
    "rhino.docobjects",
    "rhino.commands",
    "rhino.input",
    "rhino.input.custom",
    "rhino.display",
    "rhino.fileio",
    "rhino.render",
    "rhino.plugins",
]

# Scraper settings
SCRAPER_DELAY = 0.5  # seconds between requests
SCRAPER_TIMEOUT = 10  # seconds
MAX_RETRIES = 3

# XML paths by platform
XML_PATHS = {
    "windows": "C:\\Program Files\\Rhino {version}\\System\\RhinoCommon.xml",
    "mac": "/Applications/Rhino {version}.app/Contents/Frameworks/RhinoCommon.xml",
}