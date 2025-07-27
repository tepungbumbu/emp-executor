from config import EMP_FILE_PATH, ACTIVE_CHAIN
from app.core.parser import parse_emp
from app.core.executor import retry_send_transaction  # ganti ke retry
from app.core.proxy import get_proxy
from app.core.signer import sign_with_vault
from app.utils.vault_client import get_vault_token
from app.cli.dashboard import show_cli_dashboard
from app.storage.log_db import init_db, log_transaction, list_transactions

def show_logs():
    rows = list_transactions(limit=5)
    print("\n🧾 Last Transactions:")
    for row in rows:
        timestamp, chain, tx_hash, status, error = row
        print(f"{timestamp} | {chain.upper()} | {status} | TX: {tx_hash or '-'} | Error: {error or '-'}")

def main():
    # 🗂️ Inisialisasi database SQLite
    init_db()

    # 📦 Baca file EMP
    emp = parse_emp(EMP_FILE_PATH)
    raw_tx = emp["blockchain_execution"]["raw_transaction_hex"]

    # 🔐 Tanda tangan dengan Vault (dummy)
    signed_tx = sign_with_vault(raw_tx, get_vault_token())

    # 🌍 Siapkan proxy (jika ada)
    proxy_url = get_proxy()

    # 🚀 Kirim transaksi dengan retry
    result = retry_send_transaction(signed_tx, proxy_url, max_retries=3, delay_seconds=5)

    # 🧾 Logging transaksi ke database
    log_transaction(chain=ACTIVE_CHAIN, raw_tx=signed_tx, result=result)

    # 📺 Tampilkan output di CLI
    show_cli_dashboard(result)
    show_logs()

if __name__ == "__main__":
    main()
