from playwright.sync_api import sync_playwright


class StandardScraper:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def fetch_html(self, url: str) -> str:
        """
        Spins up a headless browser, navigates to the URL, and returns the full HTML.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                # Bypassing basic bot-detection
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            try:
                # Wait until the network is mostly idle to ensure JS framework data loads
                page.goto(url, wait_until="networkidle", timeout=15000)
                html_content = page.content()
                return html_content
            except Exception as e:
                # In Sprint 3, we will catch this specifically and send it to the AI Healer
                raise RuntimeError(f"Failed to fetch {url}: {str(e)}")
            finally:
                browser.close()
