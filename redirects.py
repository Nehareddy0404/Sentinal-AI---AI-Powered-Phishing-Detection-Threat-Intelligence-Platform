import requests

SHORTENERS = {"bit.ly","t.co","tinyurl.com","goo.gl","ow.ly","is.gd","buff.ly","cutt.ly","rb.gy"}

def get_redirect_chain(url, timeout=3):
    try:
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        chain = [resp.url for resp in response.history]
        chain.append(response.url)
        return chain
    except Exception:
        return [url]

def is_shortener(domain):
    return domain.lower() in SHORTENERS
