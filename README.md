# EMAIL_SCRAPER

![image](https://github.com/user-attachments/assets/8a37dbd8-6aa1-4231-97ab-318bba28a9cf)

# Features
*  Targeted Email Extraction: Efficiently scrapes email addresses from specified websites.
*  Configurable Crawling Depth: Controls the depth of the website traversal, allowing you to target specific areas of a site or conduct broader searches.
*  Domain Filtering: Restricts the crawler to a single domain, preventing it from leaving the target website.
*  URL Normalization: Automatically removes tracking parameters (like UTM codes) from URLs, preventing redundant visits to the same content.
*  robots.txt Respect: Checks and honors the robots.txt file, ensuring ethical crawling practices.
*  Customizable Request Delay: Configurable delay between requests helps to avoid overloading the target server.
*  Proxy Support: Enables routing requests through a proxy server for anonymity or to bypass geographical restrictions.
*  User-Agent Rotation: Employs a random User-Agent string to mimic different browsers and reduce the likelihood of being blocked.
*  Cookie Consent Handling: Attempts to automatically accept cookie consent forms.
*  CAPTCHA Handling: Detects and attempts to bypass CAPTCHA challenges (by reloading the page).
*  Flexible Input: Accepts a single URL or a file containing a list of URLs as input.
*  Output Options: Saves the extracted email addresses to a file or prints them to the console.
*  Simple Command-Line Interface: Easily configurable through command-line arguments.
*  Page Limit: Limits the number of pages crawled to prevent infinite loops or excessive resource usage.

# Installation
You can install email_scraper using git clone:

$ git clone https://github.com/imnoturbadboy/email_scraper.git
$ cd email_scraper
$ pip install -r requirements.txt

# Usage
To run the script, use the following command in your terminal:
python3 email_scraper.py

This script is an email scraper designed to extract email addresses from websites.  It accepts various command-line arguments to customize the crawling process.

Arguments:

*   -u or --url:  Specifies a single URL to scrape for email addresses.  Example: -u https://example.com
*   -r or --read:  Specifies a file containing a list of URLs (one URL per line) to scrape. Example: -r urls.txt
*   -o or --output: Specifies the file where the extracted email addresses will be saved. If not provided, the emails will be printed to the console. Example: -o emails.txt
*   -d or --depth:  Sets the crawling depth.  The default depth is 1, meaning it only scrapes the initial URL and links directly on that page.  A depth of 2 will scrape the initial URL, links on that page, and links on *those* pages, and so on. Example: -d 3
*   -p or --protocol:  Specifies the protocol to use (either http or https). The default is https. Example: -p http
*   --proxy: Specifies a proxy server to use for the requests.  The format should be http://user:pass@host:port. Example: --proxy http://username:password@123.45.67.89:8080
*   -v or --verbose:  Enables verbose mode.  This will print more detailed information about the crawling process to the console, such as the URLs being visited.  Simply add the flag: -v
*   --delay:  Sets a delay (in seconds) between requests.  If not specified, the script will use a random delay between 2 and 5 seconds.  Example: --delay 1.5
*   --max_pages: Sets the maximum number of pages to crawl. The default value is 10. Example: --max_pages 50

Important Notes:

*   Providing URLs:  You *must* provide either a single URL using -u or a file containing URLs using -r.  If neither is provided, the script will exit with an error.
*   Output File: If you specify an output file using -o, the extracted email addresses will be saved to that file (one email address per line).  If you don't specify an output file, the email addresses will be printed to your terminal.
*   File Naming: This script saves the email addresses into the file with the name you specify using -o. If you do not specify this flag, the results would not be saved.
*   Filtering: The script automatically normalizes URLs (removing UTM parameters and other tracking parameters) to avoid visiting the same page multiple times. It also only crawls within the same domain as the initial URL provided.

Example Usage:
1.  Scrape a single URL and print the emails to the console:
    python3 email_scraper.py -u https://example.com
    
2.  Scrape a list of URLs from a file and save the emails to a file:
    python3 email_scraper.py -r urls.txt -o emails.txt
    
3.  Scrape a single URL with a crawling depth of 2, using a proxy, and enable verbose mode:
    python3 email_scraper.py -u https://example.com -d 2 --proxy http://username:password@123.45.67.89:8080 -v
    
4.  Scrape a single URL, limit the number of pages to 50, and set a delay of 3 seconds:
    python3 email_scraper.py -u https://example.com --max_pages 50 --delay 3
    
**This script is a useful email scraper that can be customized using command-line arguments. Be responsible when scraping websites and always respect the website's terms of service and robots.txt file.**

# Support
If you have any ideas or thoughts on how to improve or implement new features, submit an issue or create a pull request! 
