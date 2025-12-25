# G2 & Capterra Review Scraper

A modular Python tool designed to scrape SaaS product reviews from G2 and Capterra. It utilizes `selenium` and `undetected-chromedriver` to handle dynamic content and bypass basic anti-bot protections.

## Features
-   **Multi-Source Support**: Scrape reviews from both G2 and Capterra.
-   **Anti-Bot Evasion**: Uses `undetected-chromedriver` and random sleep intervals.
-   **Smart Navigation**: Implements "Google Dorking" to find review pages directly, avoiding internal search blocks.
-   **Robust Extraction**: Uses XPath `itemprop` selectors to reliably extract review data (Rating, Date, Title, Body, Reviewer).
-   **Modular Design**: Clean architecture with separated concerns for easier maintenance.

## Prerequisites
-   Python 3.8+
-   Google Chrome installed

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Dhathatreya/G2-Review-Scrapper.git
    cd G2-Review-Scrapper
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the scraper as a module from the root directory:

```bash
python -m scraper_v2.main [Company] [Start_Date] [End_Date] --source [Source]
```

### Arguments
-   `Company`: Name of the product or company (e.g., "Slack").
-   `Start_Date`: Format `YYYY-MM-DD` (e.g., "2024-01-01").
-   `End_Date`: Format `YYYY-MM-DD` (e.g., "2024-12-31").
-   `--source`: `G2`, `Capterra`, or `All` (default).

### Example
Scrape Slack reviews from G2 for the year 2024:
```bash
python -m scraper_v2.main Slack 2024-01-01 2024-12-31 --source G2
```

The results will be saved to `Slack_reviews_v2.json`.

## Project Structure
```
├── scraper_v2/
│   ├── main.py          # Entry point
│   ├── browser.py       # Driver management
│   ├── utils.py         # Helper functions
│   └── scrapers/        # Scraper logic
│       ├── base.py
│       ├── g2.py
│       └── capterra.py
├── requirements.txt
└── scraping_solutions.txt # Detailed technical report
```

## Disclaimer
This tool is for **educational and internal research purposes only**. Scraping data from G2 and Capterra may violate their Terms of Service. Use responsibly and respect the website's `robots.txt` and rate limits.
