import logging
import time
import random
import json
from datetime import datetime

def setup_logging(log_file="scraper.log"):
    """Configures logging for the scraper."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("Scraper")

logger = setup_logging()

def random_sleep(min_seconds=2, max_seconds=5):
    """Sleeps for a random interval to mimic human behavior."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def parse_date(date_str):
    """Parses date string into datetime object."""
    if not date_str:
        return None
    
    date_str = date_str.strip()
    formats = [
        "%Y-%m-%d",       # 2023-10-25 (ISO/Meta tag)
        "%B %d, %Y",      # October 25, 2023
        "%b %d, %Y",      # Oct 25, 2023
        "%Y/%m/%d",       # 2023/10/25
        "%d-%m-%Y"        # 25-10-2023
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

def save_results(data, filename):
    """Saves collected reviews to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Saved {len(data)} reviews to {filename}")
    except Exception as e:
        logger.error(f"Failed to save data: {e}")
