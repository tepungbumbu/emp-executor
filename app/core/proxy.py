from config import PROXY_USERNAME, PROXY_PASSWORD, PROXY_HOST, PROXY_PORT

def get_proxy():
    if PROXY_HOST:
        return f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
    return None
