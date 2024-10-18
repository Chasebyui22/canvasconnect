import csv
from playwright.sync_api import sync_playwright
import time

def search_linkedin(name, school):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to LinkedIn
        page.goto("https://www.linkedin.com/")
        
        # Wait for the search box to appear and type the name
        page.wait_for_selector('input[aria-label="Search"]')
        page.fill('input[aria-label="Search"]', f"{name} {school}")
        page.press('input[aria-label="Search"]', "Enter")
        
        # Wait for search results
        page.wait_for_selector('.search-results__list')
        
        # Get the first result URL
        first_result = page.query_selector('.search-result__info a')
        url = first_result.get_attribute('href') if first_result else "No results found"
        
        browser.close()
        return url

def process_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write header
        writer.writerow(['Name', 'Section', 'Role', 'LinkedIn URL'])
        
        # Skip header
        next(reader)
        
        for row in reader:
            name, _, section, role = row
            url = search_linkedin(name, "byui")
            writer.writerow([name, section, role, url])
            time.sleep(2)  # Add a delay to avoid rate limiting

if __name__ == "__main__":
    input_file = r"ScrapedData\names.csv"
    output_file = r"ScrapedData\output.csv"
    process_csv(input_file, output_file)
