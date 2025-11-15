"""Document search and retrieval service"""

import json
from pathlib import Path
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)


class DocsService:
    """Service for searching and retrieving RhinoCommon documentation"""
    
    def __init__(self, docs_path: Path, version: str = "8"):
        self.docs_path = docs_path / f"v{version}"
        self.version = version
        self.cache = {}
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load documentation index"""
        index_file = self.docs_path / "index.json"
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"namespaces": [], "version": self.version}
    
    def _load_namespace(self, namespace: str) -> Optional[Dict]:
        """Load namespace documentation"""
        if namespace in self.cache:
            return self.cache[namespace]
        
        filename = namespace.replace('.', '_') + '.json'
        filepath = self.docs_path / filename
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.cache[namespace] = data
                return data
        
        logger.warning(f"Namespace not found: {namespace}")
        return None
    
    def search(self, query: str, namespace: Optional[str] = None) -> List[Dict]:
        """Search API by query string"""
        results = []
        query_lower = query.lower()
        
        namespaces = [namespace] if namespace else self.index.get("namespaces", [])
        
        for ns in namespaces:
            data = self._load_namespace(ns)
            if not data:
                continue
            
            for cls in data.get("classes", []):
                class_name = cls.get("name", "")
                
                # Match class name
                if query_lower in class_name.lower():
                    results.append({
                        "type": "class",
                        "namespace": ns,
                        "name": class_name,
                        "description": cls.get("description", "")[:200],
                        "url": cls.get("url", "")
                    })
                
                # Match methods
                for method in cls.get("methods", []):
                    if query_lower in method.get("name", "").lower():
                        results.append({
                            "type": "method",
                            "class": class_name,
                            "namespace": ns,
                            "name": method.get("name", ""),
                            "signature": method.get("signature", ""),
                            "description": method.get("description", "")[:200]
                        })
        
        return results
    
    def get_class_info(self, class_name: str, namespace: Optional[str] = None) -> Optional[Dict]:
        """Get detailed class information"""
        namespaces = [namespace] if namespace else self.index.get("namespaces", [])
        
        for ns in namespaces:
            data = self._load_namespace(ns)
            if not data:
                continue
            
            for cls in data.get("classes", []):
                if cls.get("name", "").lower() == class_name.lower():
                    return cls
        
        return None
    
    def get_examples(self, class_name: str) -> List[Dict]:
        """Get code examples for a class"""
        examples_dir = self.docs_path.parent / "examples"
        example_file = examples_dir / f"{class_name.lower()}.json"
        
        if example_file.exists():
            with open(example_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return []
    
    def list_namespaces(self) -> List[str]:
        """List all available namespaces"""
        return self.index.get("namespaces", [])