"""Main scraper entry point"""

import argparse
import logging
from pathlib import Path
from xml_parser import XMLDocParser
from web_scraper import WebScraper
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='RhinoCommon Documentation Scraper')
    parser.add_argument('--version', default='8', choices=['7', '8'], 
                       help='Rhino version')
    parser.add_argument('--source', choices=['xml', 'web'], default='web',
                       help='Source type: xml or web')
    parser.add_argument('--path', help='Path to RhinoCommon.xml (for XML source)')
    parser.add_argument('--namespace', help='Specific namespace to scrape')
    parser.add_argument('--all', action='store_true', 
                       help='Scrape all namespaces')
    parser.add_argument('--output', help='Output directory',
                       default=str(config.DOCS_DIR))
    
    args = parser.parse_args()
    
    output_dir = Path(args.output) / f"v{args.version}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Starting scraper for Rhino {args.version}")
    logger.info(f"Output directory: {output_dir}")
    
    if args.source == 'xml':
        if not args.path:
            logger.error("--path is required for XML source")
            return
        
        logger.info(f"Parsing XML: {args.path}")
        parser = XMLDocParser(args.path, output_dir)
        docs = parser.parse()
        parser.save(docs)
        
    else:  # web
        scraper = WebScraper(output_dir, args.version)
        
        if args.namespace:
            logger.info(f"Scraping namespace: {args.namespace}")
            scraper.scrape_namespace(args.namespace)
        elif args.all:
            logger.info("Scraping all namespaces")
            scraper.scrape_all()
        else:
            logger.info("Scraping default namespaces")
            for ns in config.NAMESPACES[:3]:  # First 3 as default
                scraper.scrape_namespace(ns)
        
        scraper.create_index()
    
    logger.info("✅ Scraping complete!")


if __name__ == "__main__":
    main()