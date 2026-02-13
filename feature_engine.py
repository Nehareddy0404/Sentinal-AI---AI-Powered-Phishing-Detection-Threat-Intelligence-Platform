import re
import math
import tldextract
from urllib.parse import urlparse

SUSPICIOUS_WORDS = ["login", "verify", "secure", "account", "update"]

def entropy(s):
    if not s:
        return 0
    probs = [s.count(c) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in probs)

def extract_features(url):
    parsed = urlparse(url)
    ext = tldextract.extract(url)

    domain = ext.domain
    host = parsed.netloc

    features = {
        "url_length": len(url),
        "dot_count": host.count("."),
        "has_ip": bool(re.search(r"\d+\.\d+\.\d+\.\d+", host)),
        "suspicious_words": sum(word in url.lower() for word in SUSPICIOUS_WORDS),
        "entropy": entropy(domain),
        "has_https": parsed.scheme == "https"
    }

    return features

