from dotenv import load_dotenv
import os

load_dotenv()

EMP_FILE_PATH = os.getenv("EMP_FILE_PATH", "data/EMP.txt")

ACTIVE_CHAIN = os.getenv("ACTIVE_CHAIN", "ethereum")
ACTIVE_RPC = os.getenv("ACTIVE_RPC")

PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")
PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")

VAULT_ADDR = os.getenv("VAULT_ADDR")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")

FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
