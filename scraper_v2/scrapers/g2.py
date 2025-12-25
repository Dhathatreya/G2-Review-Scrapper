from selenium.webdriver.common.by import By
from .base import BaseScraper
from ..utils import logger, random_sleep, parse_date

class G2Scraper(BaseScraper):
    """Scraper logic for G2."""

    def scrape(self):
        logger.info("Starting G2 scraping...")
        if not self._google_dork_search(f"{self.company_name} reviews site:g2.com"):
            return

        page = 1
        keep_scraping = True
        
        while keep_scraping:
            logger.info(f"Scraping G2 Page {page} - Title: {self.driver.title}")
            
            try:
                # Primary container: <article itemprop="review">
                review_elements = self.driver.find_elements(By.XPATH, "//article[@itemprop='review']")
                
                if not review_elements:
                    # Fallback for older layouts
                    review_elements = self.driver.find_elements(By.XPATH, "//div[@itemprop='review']")

                if not review_elements:
                    logger.warning(f"No reviews found on page {page}.")
                    break

                logger.info(f"Found {len(review_elements)} review elements on page {page}")

                for review in review_elements:
                    try:
                        # DATE
                        try:
                            date_str = review.find_element(By.XPATH, ".//meta[@itemprop='datePublished']").get_attribute("content")
                        except:
                            date_str = ""
                        
                        review_date = parse_date(date_str)
                        if not review_date:
                            # Try visible text fallback
                            try:
                                date_text = review.find_element(By.XPATH, ".//time | .//div[contains(@class, 'time')]").text
                                review_date = parse_date(date_text)
                            except:
                                pass

                        if not review_date:
                            continue

                        if review_date < self.start_date:
                            logger.info(f"Reached date {review_date.date()} < {self.start_date.date()}. Stopping G2.")
                            keep_scraping = False
                            break
                        
                        if review_date > self.end_date:
                            continue

                        # TITLE
                        try:
                            title = review.find_element(By.XPATH, ".//div[@itemprop='name']").text.strip()
                        except:
                            title = "No Title"

                        # RATING
                        try:
                            rating_val = review.find_element(By.XPATH, ".//span[@itemprop='reviewRating']/meta[@itemprop='ratingValue']").get_attribute("content")
                            rating = float(rating_val)
                        except:
                            rating = 0.0

                        # BODY
                        try:
                            body_element = review.find_element(By.XPATH, ".//div[@itemprop='reviewBody']")
                            text = body_element.text.strip()
                        except:
                            text = ""

                        # REVIEWER
                        try:
                            reviewer = review.find_element(By.XPATH, ".//div[@itemprop='author']//meta[@itemprop='name']").get_attribute("content")
                        except:
                            reviewer = "Anonymous"

                        self.reviews.append({
                            "source": "G2",
                            "company": self.company_name,
                            "review_title": title,
                            "review_text": text,
                            "date": review_date.strftime("%Y-%m-%d"),
                            "rating": rating,
                            "reviewer_info": reviewer
                        })
                        
                    except Exception as e:
                        logger.error(f"Error extracting single review: {e}")
                        continue
                
                if not keep_scraping:
                    break

            except Exception as e:
                logger.error(f"Error finding G2 reviews: {e}")
                break

            # Pagination
            try:
                next_button = self.driver.find_element(By.XPATH, "//a[contains(@class, 'next') and not(contains(@class, 'disabled'))] | //li[contains(@class, 'pagination-page--next')]/a")
                next_button.click()
                page += 1
                random_sleep(3, 6)
            except:
                logger.info("No next button found on G2. Ending.")
                break
