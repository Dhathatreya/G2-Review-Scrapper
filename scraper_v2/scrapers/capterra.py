from selenium.webdriver.common.by import By
from .base import BaseScraper
from ..utils import logger, random_sleep, parse_date
from datetime import datetime

class CapterraScraper(BaseScraper):
    """Scraper logic for Capterra."""

    def scrape(self):
        logger.info("Starting Capterra scraping...")
        if not self._google_dork_search(f"{self.company_name} reviews site:capterra.com"):
            return

        random_sleep()
        
        while True:
            logger.info(f"Processing Capterra page - Title: {self.driver.title}")
            try:
                review_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'ReviewCard')] | //div[contains(@class, 'review-card')]")
                
                if not review_cards:
                    review_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'card') and .//div[contains(@class, 'stars')]]")
            
            except Exception as e:
                logger.warning(f"Error finding Capterra cards: {e}")
                break
            
            if not review_cards:
                logger.warning("No reviews found on current Capterra view.")
                break
            
            logger.info(f"Found {len(review_cards)} Capterra reviews.")

            for card in review_cards:
                try:
                    # DATE
                    try:
                        date_text = card.find_element(By.XPATH, ".//div[contains(@class, 'source-date') or contains(@class, 'written-on')]").text
                        # "Written on January 12, 2023"
                        date_clean = date_text.replace("Written on", "").strip()
                        review_date = parse_date(date_clean)
                    except:
                        try:
                           date_text = card.find_element(By.XPATH, ".//div[contains(text(), ', 20')]").text
                           review_date = parse_date(date_text)
                        except:
                           # No date found
                           review_date = None

                    if review_date:
                        if review_date < self.start_date:
                            logger.info("Reached older reviews on Capterra. Stopping.")
                            return
                        
                        if review_date > self.end_date:
                            continue
                    else:
                        # If date is missing, capture anyway? original logic allowed fallbacks.
                        # Assuming robust date is needed for range check.
                        pass

                    # TITLE
                    try:
                        title = card.find_element(By.XPATH, ".//h3 | .//div[contains(@class, 'title')]").text
                    except:
                        title = "No Title"

                    # TEXT
                    try:
                        text = card.find_element(By.XPATH, ".//p[contains(@class, 'comments') or contains(@class, 'text')]").text
                    except:
                        text = ""
                    
                    # RATING
                    try:
                        stars = card.find_elements(By.XPATH, ".//*[contains(@class, 'star') and contains(@class, 'full')]")
                        rating = f"{len(stars)}/5"
                    except:
                        rating = "?"

                    reviewer = "Anonymous"
                    try:
                        reviewer = card.find_element(By.XPATH, ".//div[contains(@class, 'avatar') or contains(@class, 'name')]").text
                    except:
                        pass

                    self.reviews.append({
                        "source": "Capterra",
                        "company": self.company_name,
                        "review_title": title,
                        "review_text": text,
                        "date": review_date.strftime("%Y-%m-%d") if review_date else "N/A",
                        "rating": rating,
                        "reviewer_info": reviewer
                    })

                except Exception as e:
                    continue

            # Pagination
            try:
                show_more = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Show more') or contains(text(), 'Load more')]")
                if show_more.is_displayed():
                    show_more.click()
                    random_sleep(3, 5)
                else:
                    break
            except:
                try:
                   next_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Next') or contains(@class, 'next')]")
                   next_link.click()
                   random_sleep(3, 5)
                except:
                    logger.info("No more pages/buttons on Capterra.")
                    break
