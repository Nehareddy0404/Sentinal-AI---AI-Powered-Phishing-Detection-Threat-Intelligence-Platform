from urllib.parse import urlparse

def normalize_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc)
    except:
        return False

