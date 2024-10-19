import csv
import os
import time
from playwright.sync_api import sync_playwright

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_')).rstrip()

def get_linkedin_profile(page, name):
    page.goto("https://www.google.com")
    search_box = page.get_by_role("combobox", name="Search")
    search_box.click()
    search_box.fill(f"LinkedIn {name} at BYUI")
    search_box.press("Enter")
    
    # Wait for the search results to load
    page.wait_for_selector("div#search")
    
    # Get the first search result
    first_result = page.query_selector("div.g a")
    if first_result:
        return first_result.get_attribute("href")
    return None

# This function is no longer needed

def process_csv(input_csv_path, output_csv_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        with open(input_csv_path, 'r') as input_file, open(output_csv_path, 'w', newline='') as output_file:
            csv_reader = csv.reader(input_file)
            csv_writer = csv.writer(output_file)
            
            # Write header to output CSV
            csv_writer.writerow(['Name', 'LinkedIn URL'])
            
            next(csv_reader)  # Skip header row if present
            
            for row in csv_reader:
                name = row[0]  # Assuming the name is in the first column
                print(f"Processing: {name}")
                
                profile_url = get_linkedin_profile(page, name)
                if profile_url:
                    print(f"Found search result for {name}: {profile_url}")
                    csv_writer.writerow([name, profile_url])
                else:
                    print(f"Could not find search result for {name}")
                    csv_writer.writerow([name, ''])
                
                time.sleep(2)  # Delay to avoid rate limiting

        browser.close()

if __name__ == "__main__":
    input_csv_path = "ScrapedData/names.csv"
    output_csv_path = "ScrapedData/linkedin_profiles.csv"
    process_csv(input_csv_path, output_csv_path)
