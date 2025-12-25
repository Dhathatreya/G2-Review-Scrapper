import undetected_chromedriver as uc
from .utils import logger

class BrowserManager:
    """Manages the Selenium WebDriver instance."""
    
    def __init__(self):
        self.driver = None

    def init_driver(self):
        """Initializes undetected-chromedriver with stealth settings."""
        if self.driver:
            return self.driver

        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-popup-blocking')
        
        try:
            logger.info("Initializing undetected-chromedriver...")
            self.driver = uc.Chrome(options=options)
            logger.info("Browser initialized successfully.")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

    def quit(self):
        """Closes the browser."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing driver: {e}")
            finally:
                self.driver = None
