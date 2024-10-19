import csv
import io
import time
from playwright.sync_api import sync_playwright

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

def process_csv_content(csv_content):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        input_file = io.StringIO(csv_content)
        output_file = io.StringIO()

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

        return output_file.getvalue()

# This function can be called from Django views
def process_csv_from_django(csv_content):
    return process_csv_content(csv_content)

# if __name__ == "__main__":
#     # For testing purposes
#     test_csv_content = """Name
# John Doe
# Jane Smith"""
#     result = process_csv_content(test_csv_content)
#     print(result)
