import csv
import os
import time
from playwright.sync_api import sync_playwright

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_')).rstrip()

def get_linkedin_profile(page, name):
    try:
        page.goto("https://www.google.com", wait_until="networkidle")
        search_box = page.query_selector('input[name="q"]')
        if not search_box:
            print(f"Search box not found for {name}. Page title: {page.title()}")
            return None
        search_box.fill(f"LinkedIn {name} at BYUI")
        search_box.press("Enter")
        page.wait_for_load_state("networkidle")
        
        linkedin_link = page.query_selector("a[href^='https://www.linkedin.com/in/']")
        if linkedin_link:
            return linkedin_link.get_attribute("href")
        else:
            print(f"LinkedIn link not found for {name}")
        return None
    except Exception as e:
        print(f"Error processing {name}: {str(e)}")
        return None

def save_profile_picture(page, profile_url, name):
    if not profile_url:
        return
    
    page.goto(profile_url)
    time.sleep(2)  # Wait for the page to load
    
    # Close any pop-ups
    try:
        page.click('button[aria-label="Dismiss"]', timeout=5000)
    except:
        pass  # No pop-up found or unable to close
    
    image_element = page.query_selector('button[class*="pv-top-card-profile-picture__container"]')
    if image_element:
        sanitized_name = sanitize_filename(name)
        os.makedirs("pictures", exist_ok=True)
        image_path = os.path.join("pictures", f"{sanitized_name}.png")
        image_element.screenshot(path=image_path)
        print(f"Saved profile picture for {name}")
    else:
        print(f"Could not find profile picture for {name}")

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
                    print(f"Found LinkedIn profile for {name}: {profile_url}")
                    save_profile_picture(page, profile_url, name)
                    csv_writer.writerow([name, profile_url])
                else:
                    print(f"Could not find LinkedIn profile for {name}")
                    csv_writer.writerow([name, ''])
                
                time.sleep(2)  # Delay to avoid rate limiting

        browser.close()

if __name__ == "__main__":
    input_csv_path = "ScrapedData/names.csv"
    output_csv_path = "ScrapedData/linkedin_profiles.csv"
    process_csv(input_csv_path, output_csv_path)


