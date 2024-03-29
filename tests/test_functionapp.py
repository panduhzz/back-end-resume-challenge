import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from azure.data.tables import TableClient
import os

import re


# Obtain your connection string and table name
connection_string = os.getenv('CosmosConnectionString')
table_name = "azurerm"

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
        await page.wait_for_function(r"document.querySelector('.visitor-counter').textContent.match(/\d+/)")
        text = await page.query_selector('.visitor-counter')
        getVisitorCounter = await text.text_content()
        reMatch1 = re.search(r'\d+', getVisitorCounter)
        firstCount = int(reMatch1.group())

        #now that we got the current count, we will need to get an updated count
        await page.reload()
        await page.wait_for_load_state('domcontentloaded')
        # Now verify the counter has updated. This requires the counter on the page to actually change.
        await page.wait_for_function(r"document.querySelector('.visitor-counter').textContent.match(/\d+/)")
        text2 = await page.query_selector('.visitor-counter')
        updatedVisitorCount = await text2.text_content()
        reMatch2 = re.search(r'\d+', updatedVisitorCount)
        updatedCount = int(reMatch2.group()) 
        
        # This assertion might need to be adjusted baed on how the counter updates.
        assert updatedCount == firstCount + 1, "Counter did not update as expected."

@pytest.mark.asyncio
async def test_counter_at_0():
    with TableClient.from_connection_string(connection_string, table_name="azurerm") as table_client:
        entityCount = table_client.get_entity(partition_key="pk", row_key="counter")
        entityCount["count"] = 0
        table_client.update_entity(entity=entityCount)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.panduhz.com/$web/index.html")
        #waiting for the DOM content to load from JavaScript to update with current visitor count
        await page.wait_for_function(r"document.querySelector('.visitor-counter').textContent.match(/\d+/)")
        text = await page.query_selector('.visitor-counter')
        getVisitorCounter = await text.text_content()
        reMatch1 = re.search(r'\d+', getVisitorCounter)
        firstCount = int(reMatch1.group())
        
        #asserting that the first count is 1
        assert firstCount == 1, "Update entity to 0, counter did not update correctly"
    
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
