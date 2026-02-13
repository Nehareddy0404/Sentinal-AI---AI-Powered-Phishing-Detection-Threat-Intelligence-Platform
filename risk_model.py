import tldextract
from redirects import is_shortener

def calculate_risk(features, redirect_chain, original_url):
    score = 0
    reasons = []

    # Redirect behavior
    if len(redirect_chain) > 2:
        score += 15
        reasons.append("Multiple redirects detected")

    # Shortener detection
    ext = tldextract.extract(original_url)
    domain = ext.domain + "." + ext.suffix
    if is_shortener(domain):
        score += 20
        reasons.append("URL shortener used")

    # IP detection
    if features["has_ip"]:
        score += 30
        reasons.append("IP address used instead of domain")

    # Suspicious keywords
    if features["suspicious_words"] > 0:
        score += 20
        reasons.append("Suspicious keywords detected")

    # Too many dots
    if features["dot_count"] > 3:
        score += 10
        reasons.append("Too many dots in domain")

    # No HTTPS
    if not features["has_https"]:
        score += 10
        reasons.append("No HTTPS used")

    # High entropy
    if features["entropy"] > 3.5:
        score += 20
        reasons.append("Random-looking domain (high entropy)")

    # -----------------------------
    # Category
    # -----------------------------
    if score >= 70:
        category = "Likely Credential Phishing"
    elif features["has_ip"]:
        category = "Suspicious Infrastructure"
    elif features["suspicious_words"] > 0:
        category = "Brand Impersonation Attempt"
    else:
        category = "Low Risk / Benign"

    # -----------------------------
    # Risk Level
    # -----------------------------
    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    # -----------------------------
    # Confidence
    # -----------------------------
    confidence = round(min(0.95, 0.4 + score / 150), 2)

    # IMPORTANT: Return 5 values
    return score, level, category, confidence, reasons

