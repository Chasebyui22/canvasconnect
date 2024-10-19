from flask import Flask, request, jsonify, render_template
import csv
import io
import time
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    try:
        file = request.files.get('file')
        if file:
            print("File received, processing CSV...")
            content = file.read().decode('utf-8')
            processed_csv = process_csv_from_flask(content)  # Process the file content
            print("Processed CSV:", processed_csv)  # Debugging
            return jsonify({'data': processed_csv.splitlines()})  # Return processed CSV as list of lines
        else:
            return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Print error message to console
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


def get_linkedin_profile(page, name):
    page.goto("https://www.google.com")
    search_box = page.get_by_role("combobox", name="Search")
    search_box.click()
    search_box.fill(f"LinkedIn {name} at BYUI")
    search_box.press("Enter")
    
    page.wait_for_selector("div#search")  # Wait for search results to load
    first_result = page.query_selector("div.g a")
    if first_result:
        return first_result.get_attribute("href")
    return None

def process_csv_content(csv_content):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        input_file = io.StringIO(csv_content)
        output_file = io.StringIO()

        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        csv_writer.writerow(['Name', 'LinkedIn URL'])  # Write header
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            name = row[0]  # Assuming the name is in the first column
            profile_url = get_linkedin_profile(page, name)
            if profile_url:
                csv_writer.writerow([name, profile_url])
            else:
                csv_writer.writerow([name, ''])

            time.sleep(2)  # Avoid rate limiting

        browser.close()

        return output_file.getvalue()

def process_csv_from_flask(csv_content):
    return process_csv_content(csv_content)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Disable reloader to prevent multiple browser instances
