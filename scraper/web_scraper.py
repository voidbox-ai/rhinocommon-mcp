"""Web scraper for RhinoCommon documentation"""

import requests
from bs4 import BeautifulSoup
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin
import re

import config

logger = logging.getLogger(__name__)


class WebScraper:
    """Scrape RhinoCommon documentation from web"""
    
    def __init__(self, output_dir: Path, version: str = "8"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.version = version
        self.base_url = config.API_BASE_URL
        self.visited = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RhinoCommon-MCP-Scraper/1.0'
        })
    
    def scrape_namespace(self, namespace: str) -> Dict:
        """Scrape a specific namespace"""
        logger.info(f"Scraping namespace: {namespace}")
        
        url = f"{self.base_url}{namespace}"
        
        try:
            response = self.session.get(url, timeout=config.SCRAPER_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        namespace_data = {
            'namespace': namespace,
            'classes': []
        }
        
        # Extract class list
        # This is a simplified version - actual implementation depends on website structure
        # You may need to adjust selectors based on actual HTML
        
        # For now, create a basic structure
        logger.warning("Web scraping implementation is basic - XML parsing recommended")
        
        # Save the namespace data
        filename = namespace.replace('.', '_') + '.json'
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(namespace_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {namespace}")
        
        time.sleep(config.SCRAPER_DELAY)
        
        return namespace_data
    
    def scrape_all(self):
        """Scrape all configured namespaces"""
        logger.info("Scraping all namespaces")
        
        for namespace in config.NAMESPACES:
            self.scrape_namespace(namespace)
        
        self.create_index()
    
    def create_index(self):
        """Create index of all scraped documentation"""
        logger.info("Creating index")
        
        namespaces = []
        total_classes = 0
        
        for json_file in self.output_dir.glob('*.json'):
            if json_file.name == 'index.json':
                continue
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                namespaces.append(data['namespace'])
                total_classes += len(data.get('classes', []))
        
        index = {
            'version': self.version,
            'namespaces': sorted(namespaces),
            'total_classes': total_classes
        }
        
        index_path = self.output_dir / 'index.json'
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        logger.info(f"Index created: {len(namespaces)} namespaces, {total_classes} classes")