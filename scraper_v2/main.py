import argparse
from datetime import datetime
from .browser import BrowserManager
from .scrapers.g2 import G2Scraper
from .scrapers.capterra import CapterraScraper
from .utils import logger, save_results

def main():
    parser = argparse.ArgumentParser(description="Modular Scraper for G2 and Capterra.")
    parser.add_argument("company_name", help="Name of the company/product")
    parser.add_argument("start_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("end_date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--source", choices=["G2", "Capterra", "All"], default="All", help="Source to scrape")

    args = parser.parse_args()

    # Parse dates
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        logger.error("Invalid date format. Use YYYY-MM-DD.")
        return

    browser_mgr = BrowserManager()
    
    all_reviews = []

    try:
        driver = browser_mgr.init_driver()
        
        # G2
        if args.source in ["G2", "All"]:
            try:
                g2 = G2Scraper(driver, args.company_name, start_date, end_date)
                g2.scrape()
                all_reviews.extend(g2.reviews)
            except Exception as e:
                logger.error(f"G2 scraping failed: {e}")

        # Capterra
        if args.source in ["Capterra", "All"]:
            try:
                cap = CapterraScraper(driver, args.company_name, start_date, end_date)
                cap.scrape()
                all_reviews.extend(cap.reviews)
            except Exception as e:
                logger.error(f"Capterra scraping failed: {e}")

    finally:
        filename = f"{args.company_name}_reviews_v2.json"
        save_results(all_reviews, filename)
        browser_mgr.quit()

if __name__ == "__main__":
    main()
