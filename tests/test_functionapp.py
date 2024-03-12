import pytest

from playwright.async_api import async_playwright
import re

import pytest_asyncio

@pytest.mark.asyncio
async def test_returns_200():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        response = await page.goto('https://www.panduhz.com/$web/index.html')
        assert response.status == 200
        print(response)
        await browser.close()

@pytest.mark.asyncio
async def test_number_updates():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.panduhz.com/$web/index.html")
        #waiting for the DOM content to load from JavaScript to update with current visitor count
        await page.wait_for_function("document.querySelector('.visitor-counter').textContent.includes('Visitor Count: ')")
        getVisitorCounter = await page.query_selector('.visitor-counter')
        text = await getVisitorCounter.text_content()
        firstCount = int(re.search(r'\d+', text))

        #now that we got the current count, we will need to get an updated count
        await page.reload()
        await page.wait_for_load_state('domcontentloaded')
        # Now verify the counter has updated. This requires the counter on the page to actually change.
        updatedElement = await page.query_selector('.visitor-counter')
        updatedText = await updatedElement.text_content()
        updatedCount = int(re.search(r'\d+', updatedText))
        # This assertion might need to be adjusted based on how the counter updates.
        assert updatedCount == firstCount + 1, "Counter did not update as expected."   


    """
    await page.goto("https://www.panduhz.com/$web/index.html")
    element = await page.query_selector('.visitor-counter')
    
    # Assuming '.visitor-counter' exists and contains a number.
    text = await element.text_content()
    firstCount = int(re.search(r'\d+', text).group())
    
    await page.reload()
    await page.wait_for_load_state('domcontentloaded')
    
    # Now verify the counter has updated. This requires the counter on the page to actually change.
    updatedElement = await page.query_selector('.visitor-counter')
    updatedText = await updatedElement.text_content()
    updatedCount = int(re.search(r'\d+', updatedText).group())

    # This assertion might need to be adjusted based on how the counter updates.
    assert updatedCount == firstCount + 1, "Counter did not update as expected."
    """   


    
'''
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.panduhz.com//index.html")
    page.goto("https://www.panduhz.com/$web/index.html")
    page.get_by_text("Visitor Count: 34").click()
    page.get_by_text("Visitor Count: 34").click()
    page.get_by_text("Visitor Count: 34").click()

    # ---------------------
    context.close()
    browser.close()    
'''
'''def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
'''
