"""XML documentation parser for RhinoCommon"""

import xml.etree.ElementTree as ET
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class XMLDocParser:
    """Parse RhinoCommon XML documentation"""
    
    def __init__(self, xml_path: str, output_dir: Path):
        self.xml_path = Path(xml_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.xml_path.exists():
            raise FileNotFoundError(f"XML file not found: {xml_path}")
    
    def parse(self) -> Dict[str, List[Dict]]:
        """Parse XML documentation"""
        logger.info(f"Parsing XML: {self.xml_path}")
        
        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
        except ET.ParseError as e:
            logger.error(f"Failed to parse XML: {e}")
            return {}
        
        # Group by namespace
        docs_by_namespace = {}
        
        for member in root.findall('.//member'):
            name = member.get('name', '')
            
            if not name:
                continue
            
            # Parse member type and name
            if name.startswith('T:'):  # Type (Class)
                self._parse_type(member, name[2:], docs_by_namespace)
            elif name.startswith('M:'):  # Method
                self._parse_method(member, name[2:], docs_by_namespace)
            elif name.startswith('P:'):  # Property
                self._parse_property(member, name[2:], docs_by_namespace)
            elif name.startswith('F:'):  # Field
                self._parse_field(member, name[2:], docs_by_namespace)
        
        logger.info(f"Parsed {len(docs_by_namespace)} namespaces")
        return docs_by_namespace
    
    def _parse_type(self, element: ET.Element, full_name: str, docs: Dict):
        """Parse class/type documentation"""
        if not full_name.startswith('Rhino.'):
            return
        
        parts = full_name.rsplit('.', 1)
        if len(parts) != 2:
            return
        
        namespace = parts[0].lower()
        class_name = parts[1]
        
        if namespace not in docs:
            docs[namespace] = {'namespace': namespace, 'classes': []}
        
        class_info = {
            'name': class_name,
            'full_name': full_name,
            'description': self._get_text(element, 'summary'),
            'remarks': self._get_text(element, 'remarks'),
            'methods': [],
            'properties': [],
            'fields': [],
            'url': f"https://mcneel-apidocs.herokuapp.com/api/rhinocommon/{full_name.lower()}"
        }
        
        docs[namespace]['classes'].append(class_info)
    
    def _parse_method(self, element: ET.Element, full_name: str, docs: Dict):
        """Parse method documentation"""
        # Extract class and method name
        # Format: Rhino.Geometry.NurbsSurface.Create(...)
        if '(' in full_name:
            full_name = full_name.split('(')[0]
        
        parts = full_name.rsplit('.', 1)
        if len(parts) != 2:
            return
        
        class_full_name = parts[0]
        method_name = parts[1]
        
        if not class_full_name.startswith('Rhino.'):
            return
        
        # Find namespace and class
        class_parts = class_full_name.rsplit('.', 1)
        if len(class_parts) != 2:
            return
        
        namespace = class_parts[0].lower()
        
        if namespace not in docs:
            return
        
        # Find the class
        for cls in docs[namespace]['classes']:
            if cls['full_name'] == class_full_name:
                method_info = {
                    'name': method_name,
                    'signature': full_name,
                    'description': self._get_text(element, 'summary'),
                    'parameters': self._get_params(element),
                    'returns': self._get_text(element, 'returns'),
                    'remarks': self._get_text(element, 'remarks')
                }
                cls['methods'].append(method_info)
                break
    
    def _parse_property(self, element: ET.Element, full_name: str, docs: Dict):
        """Parse property documentation"""
        parts = full_name.rsplit('.', 1)
        if len(parts) != 2:
            return
        
        class_full_name = parts[0]
        property_name = parts[1]
        
        if not class_full_name.startswith('Rhino.'):
            return
        
        class_parts = class_full_name.rsplit('.', 1)
        if len(class_parts) != 2:
            return
        
        namespace = class_parts[0].lower()
        
        if namespace not in docs:
            return
        
        for cls in docs[namespace]['classes']:
            if cls['full_name'] == class_full_name:
                property_info = {
                    'name': property_name,
                    'description': self._get_text(element, 'summary'),
                    'value': self._get_text(element, 'value')
                }
                cls['properties'].append(property_info)
                break
    
    def _parse_field(self, element: ET.Element, full_name: str, docs: Dict):
        """Parse field documentation"""
        parts = full_name.rsplit('.', 1)
        if len(parts) != 2:
            return
        
        class_full_name = parts[0]
        field_name = parts[1]
        
        if not class_full_name.startswith('Rhino.'):
            return
        
        class_parts = class_full_name.rsplit('.', 1)
        if len(class_parts) != 2:
            return
        
        namespace = class_parts[0].lower()
        
        if namespace not in docs:
            return
        
        for cls in docs[namespace]['classes']:
            if cls['full_name'] == class_full_name:
                field_info = {
                    'name': field_name,
                    'description': self._get_text(element, 'summary')
                }
                cls['fields'].append(field_info)
                break
    
    def _get_text(self, element: ET.Element, tag: str) -> str:
        """Get text from XML element"""
        child = element.find(tag)
        if child is not None and child.text:
            return child.text.strip()
        return ""
    
    def _get_params(self, element: ET.Element) -> List[Dict]:
        """Get parameter information"""
        params = []
        for param in element.findall('param'):
            params.append({
                'name': param.get('name', ''),
                'description': param.text.strip() if param.text else ""
            })
        return params
    
    def save(self, docs: Dict[str, List[Dict]]):
        """Save parsed documentation to JSON files"""
        logger.info(f"Saving documentation to {self.output_dir}")
        
        # Save each namespace
        for namespace, data in docs.items():
            filename = namespace.replace('.', '_') + '.json'
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {namespace}: {len(data['classes'])} classes")
        
        # Create index
        index = {
            'version': '8.0',
            'namespaces': list(docs.keys()),
            'total_classes': sum(len(ns['classes']) for ns in docs.values())
        }
        
        index_path = self.output_dir / 'index.json'
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        logger.info(f"Created index: {len(docs)} namespaces, {index['total_classes']} classes")