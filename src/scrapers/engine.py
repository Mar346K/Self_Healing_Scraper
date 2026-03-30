from playwright.sync_api import sync_playwright
from typing import Dict, Any


class StandardScraper:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def fetch_html(self, url: str) -> str:
        """Grabs the full HTML payload for the AI Healer."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(user_agent=self.user_agent)
            page = context.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
                return page.content()
            finally:
                browser.close()

    def fast_extract(self, url: str, rules: Dict[str, str]) -> Dict[str, Any]:
        """Attempts to extract data instantly using cached CSS selectors."""
        extracted_data = {}
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(user_agent=self.user_agent)
            page = context.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=10000)

                # Attempt to grab the text for every cached rule
                for key, selector in rules.items():
                    element = page.locator(selector).first
                    if element.count() == 0:
                        raise ValueError(
                            f"Cached selector '{selector}' for key '{key}' failed. UI might have changed."
                        )

                    extracted_data[key] = element.inner_text().strip()

                return extracted_data
            finally:
                browser.close()
