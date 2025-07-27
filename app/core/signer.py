from config import VAULT_ADDR

def sign_with_vault(raw_tx, token):
    print(f"🔐 Signing via Vault at {VAULT_ADDR}...")
    return raw_tx  # Simulasi saja
