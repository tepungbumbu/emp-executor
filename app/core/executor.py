import requests
from config import ACTIVE_RPC

def send_transaction(raw_tx, proxy_url=None):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_sendRawTransaction",
        "params": [raw_tx],
        "id": 1
    }

    proxies = {"https": proxy_url} if proxy_url else None

    try:
        response = requests.post(
            ACTIVE_RPC,
            json=payload,
            headers={"Content-Type": "application/json"},
            proxies=proxies,
            timeout=30
        )

        return response.json()

    except requests.RequestException as e:
        return {
            "result": None,
            "error": {"message": f"Request failed: {str(e)}"}
        }
