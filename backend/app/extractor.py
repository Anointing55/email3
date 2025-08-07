import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from .utils import normalize_social_url

logger = logging.getLogger(__name__)

# Enhanced email regex to handle various obfuscation techniques
EMAIL_REGEX = re.compile(
    r'\b[A-Za-z0-9._%+-]+'  # Local part
    r'\s*(?:@|\[at\]|\(at\)|\s*at\s*)\s*'  # Obfuscated @
    r'[A-Za-z0-9.-]+'  # Domain part
    r'\s*(?:\.|\[dot\]|\(dot\)|\s*dot\s*)\s*'  # Obfuscated .
    r'[A-Za-z]{2,}\b',  # TLD
    re.IGNORECASE
)

def extract_emails(text):
    """Extract and normalize emails from text, including obfuscated formats"""
    emails = set()
    for match in EMAIL_REGEX.finditer(text):
        email = match.group(0).lower()
        # Normalize obfuscation
        email = email.replace('[at]', '@').replace('(at)', '@').replace(' at ', '@')
        email = email.replace('[dot]', '.').replace('(dot)', '.').replace(' dot ', '.')
        email = email.replace(' ', '')  # Remove any remaining spaces
        emails.add(email)
    return emails

def extract_social_links(soup, base_url):
    """Extract social media links from BeautifulSoup object"""
    social_links = {
        'facebook': set(),
        'instagram': set(),
        'tiktok': set()
    }
    
    # Find all links on the page
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href'].strip()
        text = a_tag.get_text().strip()
        
        # Handle Facebook links
        if 'facebook.com' in href:
            social_links['facebook'].add(normalize_social_url(href, 'facebook'))
        elif text.startswith('@') and 'facebook' in a_tag.get('aria-label', '').lower():
            social_links['facebook'].add(f'https://facebook.com/{text[1:]}')
            
        # Handle Instagram links
        if 'instagram.com' in href:
            social_links['instagram'].add(normalize_social_url(href, 'instagram'))
        elif text.startswith('@') and 'instagram' in a_tag.get('aria-label', '').lower():
            social_links['instagram'].add(f'https://instagram.com/{text[1:]}')
            
        # Handle TikTok links
        if 'tiktok.com' in href:
            social_links['tiktok'].add(normalize_social_url(href, 'tiktok'))
        elif text.startswith('@') and 'tiktok' in a_tag.get('aria-label', '').lower():
            social_links['tiktok'].add(f'https://tiktok.com/@{text[1:]}')
    
    return social_links

def extract_contact_info(html, base_url):
    """
    Extract contact information from HTML content
    Returns: {
        'emails': set(),
        'facebook': set(),
        'instagram': set(),
        'tiktok': set()
    }
    """
    soup = BeautifulSoup(html, 'lxml')
    result = {
        'emails': set(),
        'facebook': set(),
        'instagram': set(),
        'tiktok': set()
    }
    
    # Extract from visible text
    text = soup.get_text()
    result['emails'] = extract_emails(text)
    
    # Extract from meta tags
    for meta in soup.find_all('meta', content=True):
        content = meta['content']
        result['emails'].update(extract_emails(content))
    
    # Extract social links
    social = extract_social_links(soup, base_url)
    result.update(social)
    
    return result
