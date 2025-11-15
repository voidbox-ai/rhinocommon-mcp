"""Utility functions for scraper"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def find_xml_file(version: str = "8") -> Optional[Path]:
    """Try to find RhinoCommon.xml automatically"""
    import platform
    import config
    
    system = platform.system().lower()
    
    if system == 'windows':
        path_template = config.XML_PATHS.get('windows')
    elif system == 'darwin':
        path_template = config.XML_PATHS.get('mac')
    else:
        logger.warning(f"Unsupported platform: {system}")
        return None
    
    if not path_template:
        return None
    
    xml_path = Path(path_template.format(version=version))
    
    if xml_path.exists():
        logger.info(f"Found XML file: {xml_path}")
        return xml_path
    
    logger.warning(f"XML file not found: {xml_path}")
    return None


def create_markdown(json_data: dict, output_path: Path):
    """Convert JSON documentation to Markdown"""
    namespace = json_data.get('namespace', 'Unknown')
    classes = json_data.get('classes', [])
    
    md_content = f"# {namespace}\n\n"
    md_content += f"**Total Classes**: {len(classes)}\n\n"
    
    for cls in classes:
        md_content += f"## {cls['name']}\n\n"
        
        if cls.get('description'):
            md_content += f"{cls['description']}\n\n"
        
        # Methods
        methods = cls.get('methods', [])
        if methods:
            md_content += f"### Methods ({len(methods)})\n\n"
            for method in methods[:10]:  # Limit to first 10
                md_content += f"#### {method['name']}\n\n"
                if method.get('signature'):
                    md_content += f"```csharp\n{method['signature']}\n```\n\n"
                if method.get('description'):
                    md_content += f"{method['description']}\n\n"
        
        # Properties
        properties = cls.get('properties', [])
        if properties:
            md_content += f"### Properties ({len(properties)})\n\n"
            for prop in properties[:10]:  # Limit to first 10
                md_content += f"- **{prop['name']}**: {prop.get('description', 'No description')}\n"
            md_content += "\n"
        
        md_content += "---\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    logger.info(f"Created markdown: {output_path}")