async def capture_screenshot(page, url):
    path = f"/tmp/{uuid.uuid4()}.png"
    await page.screenshot(path=path, full_page=True)
    return path
