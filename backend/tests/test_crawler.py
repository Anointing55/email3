import pytest
from app.crawler import crawl_single_site
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_crawler_basic():
    with patch('app.crawler.async_playwright') as mock_playwright:
        # Setup mock browser and page
        mock_browser = AsyncMock()
        mock_context = AsyncMock()
        mock_page = AsyncMock()
        
        mock_playwright.return_value.__aenter__.return_value = mock_playwright
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        
        # Mock page content
        mock_page.content.return_value = '''
            <html>
            <body>
                <a href="/contact">Contact Us</a>
                <a href="/about">About</a>
                <a href="https://facebook.com/company">Facebook</a>
                <p>Email: contact@example.com</p>
            </body>
            </html>
        '''
        
        # Mock navigation
        mock_page.goto = AsyncMock()
        
        # Run the crawler
        results = await crawl_single_site(mock_context, 'https://example.com')
        
        # Assertions
        assert 'contact@example.com' in results['emails']
        assert 'https://facebook.com/company' in results['facebook']
        assert len(results['screenshots']) > 0
        assert mock_page.goto.call_count == 1
