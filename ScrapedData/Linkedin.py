import csv
from playwright.sync_api import sync_playwright
import time

def search_linkedin(name, school):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(30000)  # 30 seconds timeout
            
            # Navigate to LinkedIn
            page.goto("https://www.linkedin.com/")
            
            # Wait for the search box to appear and type the name
            page.wait_for_selector('input[aria-label="Search"]')
            page.fill('input[aria-label="Search"]', f"{name} {school}")
            page.press('input[aria-label="Search"]', "Enter")
            
            # Wait for search results
            page.wait_for_selector('.search-results__list', state='visible')
            
            # Get the first result URL
            first_result = page.query_selector('.search-result__info a')
            url = first_result.get_attribute('href') if first_result else "No results found"
            
            browser.close()
            return url
    except Exception as e:
        print(f"Error searching for {name}: {str(e)}")
        return "Error occurred during search"

def process_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read header
        header = next(reader)
        
        # Write header
        writer.writerow(header + ['LinkedIn URL'])
        
        for row in reader:
            if len(row) >= 2:  # Ensure there are at least 2 columns (name and section)
                name = row[0]
                section = row[1] if len(row) > 1 else ""
                role = row[2] if len(row) > 2 else ""
                
                url = search_linkedin(name, "byui")
                writer.writerow(row + [url])
                time.sleep(2)  # Add a delay to avoid rate limiting
            else:
                print(f"Skipping invalid row: {row}")

if __name__ == "__main__":
    input_file = r"ScrapedData\names.csv"
    output_file = r"ScrapedData\output.csv"
    process_csv(input_file, output_file)
