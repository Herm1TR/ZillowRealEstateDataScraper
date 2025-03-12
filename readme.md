# Zillow Real Estate Data Scraper

## Project Overview

This Python application scrapes real estate data from a Zillow clone website and automatically submits the collected information to a Google Form. The project demonstrates web scraping and automated form submission techniques using `requests`, `BeautifulSoup`, and `Selenium`.

## Features

- Scrapes property prices, addresses, and links from a Zillow clone website
- Implements crawler and form submission logic using an object-oriented approach
- Detailed error handling and logging
- Saves scraped data as a CSV file
- Automatically submits data to a Google Form
- Optional download of form responses

## Technology Stack

- **Python 3.7+**
- **Requests**: For sending HTTP requests
- **BeautifulSoup4**: For HTML parsing
- **Selenium**: For browser automation and form submission
- **Pandas**: For data processing and CSV export
- **Logging**: For detailed logging

## Installation Guide

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/zillow-scraper.git
   cd zillow-scraper
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Install Chrome browser and ChromeDriver
   
   Ensure Chrome browser is installed and download the [ChromeDriver](https://sites.google.com/chromium.org/driver/) that matches your Chrome version.

## Usage

### Basic Usage

Run the main script to start scraping data and submitting forms:

```bash
python zillow_scraper.py
```

### Configuration

To change the target URL or form URL, modify the following constants in the `zillow_scraper.py` file:

```python
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM_URL = "https://forms.gle/z4JvQZx8jTBDzMpw8"
RESPONSES_URL = "https://docs.google.com/forms/d/1tSK6EafVovJYyUxPo4tGAGosrzZtcElg7V6d5-Z0Z0g/edit?pli=1#responses"
```

### Running in Headless Mode

If you want to run the program without a visible browser window, you can modify the initialization of the `GoogleFormSubmitter` class:

```python
submitter = GoogleFormSubmitter(GOOGLE_FORM_URL, headless=True)
```

## Code Structure

### Main Classes

1. **PropertyScraper**: Responsible for scraping and parsing property data from websites
   - `fetch_page()`: Gets the HTML content of the target webpage
   - `parse_properties()`: Parses property data from HTML
   - `save_to_csv()`: Saves the scraped data as a CSV
   - `scrape()`: Performs the complete scraping process

2. **GoogleFormSubmitter**: Responsible for submitting data to Google Forms
   - `setup_driver()`: Sets up the Selenium WebDriver
   - `submit_property()`: Submits a single property's data
   - `submit_all_properties()`: Submits all property data
   - Implements the context manager interface (`__enter__` and `__exit__`)

### Helper Functions

- `download_responses()`: Downloads response data from Google Forms
- `main()`: Coordinates the execution flow of the entire program

## Error Handling

This program implements a comprehensive error handling mechanism:

1. **Network Request Errors**: Handles connection timeouts, 404s, and 5XX HTTP errors
2. **Parsing Errors**: Gracefully handles when HTML structure changes
3. **Selenium Errors**: Handles element not found, wait timeouts, and other issues
4. **Retry Mechanism**: Automatically retries when form submission fails
5. **Detailed Logging**: Records all key events during execution

## Logging

All operations are logged in the `zillow_scraper.log` file and displayed in the console. Logs include:

- Info level: Regular operations and progress reports
- Warning level: Non-fatal issues and potential problems
- Error level: Operation failures that need attention

## Improvement Plans

1. Add command-line arguments to customize crawler behavior
2. Implement proxy IP rotation to avoid being blocked
3. Add more data validation and cleaning steps
4. Create a web interface for easier use
5. Add unit tests and integration tests
6. Implement more robust anti-anti-scraping measures

## Dependencies

```
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2
pandas==2.1.1
```

## License

MIT License

## Author

Your Name
