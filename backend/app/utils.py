import re
from urllib.parse import urlparse, urljoin

def normalize_url(url):
    """Normalize URL for comparison"""
    return url.lower().rstrip('/')

def should_crawl(url, base_url):
    """Determine if a URL should be crawled based on path"""
    parsed = urlparse(url)
    base_parsed = urlparse(base_url)
    
    # Ensure same domain
    if parsed.netloc != base_parsed.netloc:
        return False
    
    # Check for contact-related paths
    path = parsed.path.lower()
    return any(kw in path for kw in ['contact', 'about', 'team', 'support', 'connect'])

def normalize_social_url(url, platform):
    """Normalize social media URLs"""
    url = url.strip().lower()
    
    # Handle handle formats (@username)
    if url.startswith('@'):
        if platform == 'facebook':
            return f'https://facebook.com/{url[1:]}'
        elif platform == 'instagram':
            return f'https://instagram.com/{url[1:]}'
        elif platform == 'tiktok':
            return f'https://tiktok.com/@{url[1:]}'
    
    # Ensure proper URL format
    if not url.startswith('http'):
        if platform == 'facebook':
            return f'https://facebook.com/{url}'
        elif platform == 'instagram':
            return f'https://instagram.com/{url}'
        elif platform == 'tiktok':
            return f'https://tiktok.com/@{url}'
    
    return url

def validate_urls(urls):
    """Validate and normalize a list of URLs"""
    valid_urls = []
    for url in urls:
        url = url.strip()
        if not url:
            continue
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        valid_urls.append(url)
    return valid_urls

def process_uploaded_file(file):
    """Process uploaded CSV/JSON file to extract URLs"""
    content = file.read().decode('utf-8')
    
    # CSV format
    if file.filename.endswith('.csv'):
        import csv
        from io import StringIO
        reader = csv.reader(StringIO(content))
        urls = [row[0] for row in reader if row]
        return validate_urls(urls)
    
    # JSON format
    elif file.filename.endswith('.json'):
        import json
        data = json.loads(content)
        if isinstance(data, list):
            return validate_urls(data)
        elif 'urls' in data:
            return validate_urls(data['urls'])
    
    return []
