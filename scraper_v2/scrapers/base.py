from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils import logger, random_sleep

class BaseScraper:
    """Base class for all scrapers."""

    def __init__(self, driver, company_name, start_date, end_date):
        self.driver = driver
        self.company_name = company_name
        self.start_date = start_date
        self.end_date = end_date
        self.reviews = []

    def scrape(self):
        """Abstract method to run the scraper."""
        raise NotImplementedError("Scrapers must implement scrape()")

    def _google_dork_search(self, query):
        """
        Performs a Google search to find the review page URL.
        """
        logger.info(f"Performing Google Dork search for: {query}")
        self.driver.get("https://www.google.com")
        random_sleep()
        
        # Handle Google Consent Popup (if any)
        try:
            consent_buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Accept all') or contains(., 'I agree')]")
            if consent_buttons:
                logger.info("Handling Google Consent Popup...")
                consent_buttons[0].click()
                random_sleep()
        except Exception:
            pass

        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(query)
            from selenium.webdriver.common.keys import Keys
            search_box.send_keys(Keys.RETURN)
            
            random_sleep(3, 6)

            # Click the first organic result
            results = self.driver.find_elements(By.XPATH, "//a/h3")
            if not results:
                results = self.driver.find_elements(By.CSS_SELECTOR, "div.g a h3")

            if results:
                logger.info(f"Found {len(results)} results. Clicking the first one: {results[0].text}")
                parent_link = results[0].find_element(By.XPATH, "..")
                parent_link.click()
                random_sleep(4, 7)
                return True
            else:
                logger.warning("No search results found.")
                
                # FALLBACK: Direct URL Construction
                logger.info("Search failed. Attempting direct URL fallback...")
                if "g2.com" in query:
                    term = query.split(" reviews")[0].lower().replace(" ", "-")
                    direct_url = f"https://www.g2.com/products/{term}/reviews"
                    logger.info(f"Navigating directly to: {direct_url}")
                    self.driver.get(direct_url)
                    random_sleep(5, 8)
                    return True
                return False

        except Exception as e:
            logger.error(f"Error during Google search: {e}")
            # FALLBACK
            if "g2.com" in query:
                 term = query.split(" reviews")[0].lower().replace(" ", "-")
                 self.driver.get(f"https://www.g2.com/products/{term}/reviews")
                 return True
            return False
