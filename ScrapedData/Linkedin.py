import csv
import os
import time
from playwright.sync_api import sync_playwright

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_')).rstrip()

def get_linkedin_profile(page, name):
    search_url = f"https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+{name.replace(' ', '+')}+BYUI"
    page.goto(search_url)
    
    linkedin_link = page.query_selector("a[href^='https://www.linkedin.com/in/']")
    if linkedin_link:
        return linkedin_link.get_attribute("href")
    return None

def save_profile_picture(page, profile_url, name):
    if not profile_url:
        return
    
    page.goto(profile_url)
    time.sleep(2)  # Wait for the page to load
    
    image_element = page.query_selector('img[alt="profile photo"]')
    if image_element:
        sanitized_name = sanitize_filename(name)
        os.makedirs("pictures", exist_ok=True)
        image_path = os.path.join("pictures", f"{sanitized_name}.png")
        image_element.screenshot(path=image_path)
        print(f"Saved profile picture for {name}")
    else:
        print(f"Could not find profile picture for {name}")

def process_csv(csv_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        with open(csv_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header row if present
            
            for row in csv_reader:
                name = row[0]  # Assuming the name is in the first column
                print(f"Processing: {name}")
                
                profile_url = get_linkedin_profile(page, name)
                if profile_url:
                    print(f"Found LinkedIn profile for {name}: {profile_url}")
                    save_profile_picture(page, profile_url, name)
                else:
                    print(f"Could not find LinkedIn profile for {name}")
                
                time.sleep(2)  # Delay to avoid rate limiting

        browser.close()

if __name__ == "__main__":
    csv_path = "ScrapedData/names.csv"
    process_csv(csv_path)


