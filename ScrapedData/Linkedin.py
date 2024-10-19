import csv
import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect

def sanitize_filename(name):
    return re.sub(r'[^\w\-_\. ]', '_', name).strip()

def run(playwright: Playwright, input_csv_path: str, output_csv_path: str) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    os.makedirs("pictures", exist_ok=True)

    with open(input_csv_path, 'r') as input_file, open(output_csv_path, 'w', newline='') as output_file:
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)
        
        csv_writer.writerow(['Name', 'LinkedIn URL'])
        
        next(csv_reader)  # Skip header row if present
        
        for row in csv_reader:
            name = row[0]  # Assuming the name is in the first column
            print(f"Processing: {name}")
            
            page.goto("https://www.google.com/")
            page.get_by_label("Search", exact=True).fill(f"Linkedin {name} at byui")
            page.get_by_role("combobox", name="Search").press("Enter")
            
            linkedin_link = page.get_by_role("link", name=re.compile(f"{name}", re.IGNORECASE)).first
            if linkedin_link:
                profile_url = linkedin_link.get_attribute("href")
                print(f"Found LinkedIn profile for {name}: {profile_url}")
                
                page.goto(profile_url)
                page.wait_for_load_state("networkidle")
                
                try:
                    page.get_by_role("button", name="Dismiss").click(timeout=5000)
                except:
                    pass  # No pop-up found or unable to close
                
                profile_image = page.get_by_role("img", name=re.compile(f"{name}", re.IGNORECASE)).first
                if profile_image:
                    sanitized_name = sanitize_filename(name)
                    image_path = os.path.join("pictures", f"{sanitized_name}.png")
                    profile_image.screenshot(path=image_path)
                    print(f"Saved profile picture for {name}")
                else:
                    print(f"Could not find profile picture for {name}")
                
                csv_writer.writerow([name, profile_url])
            else:
                print(f"Could not find LinkedIn profile for {name}")
                csv_writer.writerow([name, ''])

    context.close()
    browser.close()

if __name__ == "__main__":
    input_csv_path = "ScrapedData/names.csv"
    output_csv_path = "ScrapedData/linkedin_profiles.csv"
    with sync_playwright() as playwright:
        run(playwright, input_csv_path, output_csv_path)


