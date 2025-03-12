"""
Zillow Real Estate Data Scraper
-------------------------------
This script scrapes property data from a Zillow clone website and submits it to a Google Form.
It demonstrates web scraping techniques using both requests/BeautifulSoup and Selenium.
"""
import logging
import time
from typing import List, Dict, Any, Optional, Tuple
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("zillow_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Constants
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM_URL = "https://forms.gle/z4JvQZx8jTBDzMpw8"
RESPONSES_URL = "https://docs.google.com/forms/d/1tSK6EafVovJYyUxPo4tGAGosrzZtcElg7V6d5-Z0Z0g/edit?pli=1#responses"
WAIT_TIME = 5  # Maximum wait time in seconds for Selenium operations


class PropertyScraper:
    """A class to scrape real estate property data from a website."""
    
    def __init__(self, url: str):
        """
        Initialize the scraper with the target URL.
        
        Args:
            url: The URL of the website to scrape
        """
        self.url = url
        self.properties = []
        logger.info(f"Initializing scraper for {url}")
    
    def fetch_page(self) -> Optional[str]:
        """
        Fetch the HTML content of the target page.
        
        Returns:
            The HTML content as string if successful, None otherwise
        """
        try:
            logger.info(f"Fetching page content from {self.url}")
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.content.decode("utf-8")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page: {e}")
            return None
    
    def parse_properties(self, html_content: str) -> bool:
        """
        Parse property data from HTML content.
        
        Args:
            html_content: The HTML content to parse
            
        Returns:
            True if parsing was successful, False otherwise
        """
        try:
            logger.info("Parsing property data from HTML")
            soup = BeautifulSoup(html_content, "html.parser")
            property_cards = soup.find_all(name="li", class_="ListItem-c11n-8-84-3-StyledListCardWrapper")
            
            if not property_cards:
                logger.warning("No property cards found on the page")
                return False
            
            logger.info(f"Found {len(property_cards)} property cards")
            
            for card in property_cards:
                try:
                    # Extract link
                    link_element = card.find(name="a", href=True)
                    link = link_element['href'] if link_element else "N/A"
                    
                    # Extract price
                    price_element = card.find(name="span", class_="PropertyCardWrapper__StyledPriceLine")
                    raw_price = price_element.text if price_element else "N/A"
                    price = raw_price.split("+", 1)[0].split("/", 1)[0].strip()
                    
                    # Extract address
                    address_element = card.find(name="address")
                    raw_address = address_element.text if address_element else "N/A"
                    address = raw_address.strip().replace("|", "")
                    
                    # Add to properties list
                    self.properties.append({
                        "link": link,
                        "price": price,
                        "address": address
                    })
                except Exception as e:
                    logger.error(f"Error parsing property card: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(self.properties)} properties")
            return True
        except Exception as e:
            logger.error(f"Failed to parse properties: {e}")
            return False
    
    def get_properties(self) -> List[Dict[str, str]]:
        """
        Get the list of scraped properties.
        
        Returns:
            List of dictionaries containing property data
        """
        return self.properties
    
    def save_to_csv(self, filename: str = "zillow_properties.csv") -> bool:
        """
        Save the scraped property data to a CSV file.
        
        Args:
            filename: Name of the CSV file to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            if not self.properties:
                logger.warning("No properties to save")
                return False
                
            df = pd.DataFrame(self.properties)
            df.to_csv(filename, index=False)
            logger.info(f"Saved {len(self.properties)} properties to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save to CSV: {e}")
            return False
    
    def scrape(self) -> Tuple[bool, int]:
        """
        Perform the complete scraping process.
        
        Returns:
            Tuple of (success_status, number_of_properties_scraped)
        """
        html_content = self.fetch_page()
        if not html_content:
            return False, 0
            
        success = self.parse_properties(html_content)
        return success, len(self.properties)


class GoogleFormSubmitter:
    """A class to submit data to a Google Form using Selenium."""
    
    def __init__(self, form_url: str, headless: bool = False):
        """
        Initialize the form submitter with the form URL.
        
        Args:
            form_url: The URL of the Google Form
            headless: Whether to run the browser in headless mode
        """
        self.form_url = form_url
        self.driver = None
        self.headless = headless
        logger.info(f"Initializing form submitter for {form_url}")
    
    def setup_driver(self) -> bool:
        """
        Set up the Selenium WebDriver.
        
        Returns:
            True if setup was successful, False otherwise
        """
        try:
            logger.info("Setting up Chrome WebDriver")
            options = Options()
            options.add_experimental_option("detach", True)
            
            if self.headless:
                options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
            
            # Add additional options for stability
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            self.driver = webdriver.Chrome(options=options)
            return True
        except WebDriverException as e:
            logger.error(f"Failed to set up WebDriver: {e}")
            return False
    
    def submit_property(self, property_data: Dict[str, str]) -> bool:
        """
        Submit a property's data to the Google Form.
        
        Args:
            property_data: Dictionary containing property information
            
        Returns:
            True if submission was successful, False otherwise
        """
        try:
            if not self.driver:
                logger.error("WebDriver not initialized")
                return False
                
            logger.info(f"Submitting property: {property_data['address']}")
            
            # Navigate to the form
            self.driver.get(self.form_url)
            
            # Wait for form to load
            wait = WebDriverWait(self.driver, WAIT_TIME)
            input_fields = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']")))
            
            if len(input_fields) < 3:
                logger.error(f"Expected at least 3 input fields, found {len(input_fields)}")
                return False
            
            # Fill in the form fields
            input_fields[0].send_keys(property_data["link"])
            time.sleep(0.5)  # Small delay between inputs
            
            input_fields[1].send_keys(property_data["price"])
            time.sleep(0.5)
            
            input_fields[2].send_keys(property_data["address"])
            time.sleep(0.5)
            
            # Submit the form
            submit_button = self.driver.find_element(By.XPATH, 
                                                    '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            submit_button.click()
            
            # Wait for submission confirmation
            time.sleep(1)
            
            # Check if we're back on the form confirmation page
            current_url = self.driver.current_url
            if "formResponse" in current_url:
                logger.info("Form submitted successfully")
                return True
            else:
                logger.warning("Form submission may have failed")
                return False
                
        except TimeoutException:
            logger.error("Timed out waiting for form elements to load")
            return False
        except NoSuchElementException as e:
            logger.error(f"Element not found: {e}")
            return False
        except Exception as e:
            logger.error(f"Error submitting form: {e}")
            return False
    
    def submit_all_properties(self, properties: List[Dict[str, str]]) -> Tuple[int, int]:
        """
        Submit all properties to the Google Form.
        
        Args:
            properties: List of property dictionaries
            
        Returns:
            Tuple of (successful_submissions, total_submissions)
        """
        if not self.setup_driver():
            return 0, len(properties)
            
        successful = 0
        total = len(properties)
        
        for i, prop in enumerate(properties):
            logger.info(f"Processing property {i+1}/{total}")
            
            # Add retry mechanism
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    if self.submit_property(prop):
                        successful += 1
                        break
                    else:
                        logger.warning(f"Submission failed, attempt {attempt+1}/{max_retries}")
                        time.sleep(2)  # Wait before retry
                except Exception as e:
                    logger.error(f"Error during submission: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2)  # Wait before retry
            
            # Add a delay between submissions to prevent rate limiting
            time.sleep(2)
        
        logger.info(f"Completed submissions: {successful}/{total} successful")
        return successful, total
    
    def close(self):
        """Close the WebDriver if it's open."""
        if self.driver:
            logger.info("Closing WebDriver")
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing WebDriver: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def download_responses(response_url: str) -> bool:
    """
    Download the form responses as CSV.
    
    Args:
        response_url: URL to the form responses page
        
    Returns:
        True if download was successful, False otherwise
    """
    try:
        logger.info(f"Downloading responses from {response_url}")
        options = Options()
        options.add_experimental_option("detach", False)
        
        with webdriver.Chrome(options=options) as driver:
            driver.get(response_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Find and click the download button
            download_button = driver.find_element(
                By.XPATH, 
                '/html/body/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div'
            )
            download_button.click()
            
            # Wait for download to start
            time.sleep(5)
            
            logger.info("Responses download initiated")
            return True
    except Exception as e:
        logger.error(f"Failed to download responses: {e}")
        return False


def main():
    """Main function to run the scraper and form submission process."""
    try:
        logger.info("Starting Zillow Real Estate Data Scraper")
        
        # Scrape properties
        scraper = PropertyScraper(ZILLOW_CLONE_URL)
        success, count = scraper.scrape()
        
        if not success or count == 0:
            logger.error("Scraping failed or no properties found")
            return
        
        # Save properties to CSV
        scraper.save_to_csv()
        
        # Get properties
        properties = scraper.get_properties()
        logger.info(f"Scraped {len(properties)} properties")
        
        # Submit to Google Form
        with GoogleFormSubmitter(GOOGLE_FORM_URL) as submitter:
            successful, total = submitter.submit_all_properties(properties)
            
        logger.info(f"Completed: {successful}/{total} submissions successful")
        
        # Option to download responses
        if successful > 0:
            download = input("Do you want to download form responses? (y/n): ").lower()
            if download == 'y':
                download_responses(RESPONSES_URL)
        
        logger.info("Script execution completed")
    except Exception as e:
        logger.error(f"Unexpected error during execution: {e}")


if __name__ == "__main__":
    main()
