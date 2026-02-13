import requests
import os

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate_threat_report(url, final_url, score, level, reasons, features):

    prompt = f"""
You are a SOC analyst.

URL: {url}
Final URL: {final_url}
Risk Score: {score}
Risk Level: {level}

Indicators:
{reasons}

Features:
{features}

Generate:
1. Executive Summary
2. MITRE ATT&CK mapping
3. Recommended remediation
4. Possible false positives
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.3
        }
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return "LLM error: " + str(response.text)

    result = response.json()

    if isinstance(result, list):
        return result[0]["generated_text"]

    return str(result)



