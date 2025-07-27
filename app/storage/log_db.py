import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("logs/transactions.db")


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            chain TEXT,
            raw_tx TEXT,
            tx_hash TEXT,
            status TEXT,
            response TEXT,
            error_message TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_transaction(chain, raw_tx, result, override_status=None):
    """
    Menyimpan transaksi ke database.
    Bisa override status menjadi 'RETRY_FAILED' jika ingin menandai retry total gagal.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.utcnow().isoformat()
    tx_hash = result.get("result") if result.get("result") else None

    # Gunakan override_status jika disediakan
    status = override_status if override_status else ("SUCCESS" if tx_hash else "FAILED")

    error = result.get("error", {}).get("message") if result.get("error") else None

    cursor.execute("""
        INSERT INTO transactions (timestamp, chain, raw_tx, tx_hash, status, response, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        chain,
        raw_tx,
        tx_hash,
        status,
        json.dumps(result, indent=2),
        error
    ))
    conn.commit()
    conn.close()


def list_transactions(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, chain, tx_hash, status, error_message
        FROM transactions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_failed_transactions(limit=5):
    """
    Mengambil transaksi dengan status FAILED atau RETRY_FAILED
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, raw_tx
        FROM transactions
        WHERE status = 'FAILED' OR status = 'RETRY_FAILED'
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows
