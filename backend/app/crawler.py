# backend/app/crawler.py
import asyncio
from playwright.async_api import async_playwright
from .extractor import extract_contact_info
from .screenshot import capture_screenshot
from .storage import update_job
import re
import logging
from urllib.parse import urlparse, urljoin
from .utils import normalize_url, should_crawl

logger = logging.getLogger(__name__)
MAX_DEPTH = 2
MAX_PAGES = 10
REQUEST_DELAY = 1.0

async def crawl_website(job_id: str, urls: list[str]):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            
            results = {}
            for url in urls:
                try:
                    update_job(job_id, f"Processing {url}", url)
                    result = await crawl_single_site(context, url)
                    results[url] = result
                    update_job(job_id, f"Completed {url}", url, "completed")
                except Exception as e:
                    logger.error(f"Error crawling {url}: {str(e)}")
                    update_job(job_id, f"Failed {url}: {str(e)}", url, "failed")
            
            await browser.close()
            update_job(job_id, "All URLs processed", overall_status="completed", results=results)
    except Exception as e:
        logger.error(f"Job failed: {str(e)}")
        update_job(job_id, f"Job failed: {str(e)}", overall_status="failed")

async def crawl_single_site(context, base_url):
    visited = set()
    queue = [(base_url, 0)]
    results = {
        "emails": set(),
        "facebook": set(),
        "instagram": set(),
        "tiktok": set(),
        "screenshots": {}
    }
    
    while queue:
        url, depth = queue.pop(0)
        normalized_url = normalize_url(url)
        
        if depth > MAX_DEPTH or len(visited) >= MAX_PAGES or normalized_url in visited:
            continue
        
        visited.add(normalized_url)
        
        try:
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle")
            await asyncio.sleep(REQUEST_DELAY)
            
            # Capture homepage screenshot
            if depth == 0:
                screenshot_path = await capture_screenshot(page, base_url)
                results["screenshots"]["homepage"] = screenshot_path
            
            # Extract content
            content = await page.content()
            contact_info = extract_contact_info(content, url)
            
            # Process results
            results["emails"].update(contact_info["emails"])
            results["facebook"].update(contact_info["facebook"])
            results["instagram"].update(contact_info["instagram"])
            results["tiktok"].update(contact_info["tiktok"])
            
            # Find links to crawl
            if depth < MAX_DEPTH:
                links = await page.eval_on_selector_all("a", "elements => elements.map(el => el.href)")
                for link in links:
                    full_url = urljoin(url, link)
                    if should_crawl(full_url, base_url) and normalize_url(full_url) not in visited:
                        queue.append((full_url, depth + 1))
            
            await page.close()
        except Exception as e:
            logger.warning(f"Error processing {url}: {str(e)}")
    
    # Convert sets to lists for JSON serialization
    results["emails"] = list(results["emails"])
    results["facebook"] = list(results["facebook"])
    results["instagram"] = list(results["instagram"])
    results["tiktok"] = list(results["tiktok"])
    
    return results
