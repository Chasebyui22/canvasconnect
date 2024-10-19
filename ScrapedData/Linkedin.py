import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/search?q=google&oq=google&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBBzg4NGowajKoAgCwAgE&sourceid=chrome&ie=UTF-8")
    page.get_by_role("link", name="Google Google https://www.").click()
    page.get_by_label("Search", exact=True).click()
    page.get_by_label("Search", exact=True).fill("Andrew Allen ")
    page.get_by_label("Search", exact=True).press("Home")
    page.get_by_label("Search", exact=True).fill("Linkedin Andrew Allen ")
    page.get_by_label("Search", exact=True).press("End")
    page.get_by_label("Search", exact=True).fill("Linkedin Andrew Allen at BYUI")
    page.get_by_role("link", name="Andrew Allen - FSY - For the").click(button="right")
    page1 = context.new_page()
    page1.goto("https://www.linkedin.com/in/andrew-allen-054826176")
    page1.get_by_role("button", name="Dismiss").click()
    page1.get_by_role("button", name="see more").click()
    page1.get_by_role("button", name="Dismiss").click()
    page1.get_by_text("- Self-motivated, optimistic").click()
    page1.get_by_text("- Self-motivated, optimistic").click(button="right")
    page1.get_by_role("heading", name="Others named Andrew Allen in").click()
    page1.locator("section").filter(has_text="Sign in Stay updated on your").click()
    page1.locator("section").filter(has_text="Sign in to manage").first.click()
    page1.goto("https://www.linkedin.com/in/andrew-allen-054826176")
    page1.get_by_role("heading", name="Honors & Awards").click()
    page1.get_by_role("heading", name="Volunteer Experience").click()
    page1.get_by_text("Skip to main content LinkedIn").press("ControlOrMeta+c")
    page1.get_by_role("heading", name="Languages").click(modifiers=["ControlOrMeta"])
    page1.get_by_text("Skip to main content LinkedIn").press("ControlOrMeta+c")
    page1.locator("[data-test-id=\"logo-button\"]").click(button="right")
    # Select the image element (using src part for identification)
    image_element = page.query_selector('img[src*="profile-displayphoto"]')
    # Take screenshot of the selected image
    image_element.screenshot(path="profile_image.png")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)


