import sys
import os
import csv
import sqlite3
from rich.console import Console
from rich.table import Table

# Akses root path project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from main import main as run_executor
from config import EMP_FILE_PATH, ACTIVE_CHAIN
from app.core.proxy import get_proxy
from app.core.signer import sign_with_vault
from app.utils.vault_client import get_vault_token
from app.core.executor import retry_send_transaction
from app.core.parser import parse_emp
from app.storage.log_db import (
    list_transactions,
    get_failed_transactions,
    log_transaction
)

DB_PATH = "logs/transactions.db"
console = Console()


def show_menu():
    console.rule("[bold green]EMP Executor CLI Menu")
    console.print("[1] Eksekusi Transaksi dari EMP")
    console.print("[2] Lihat 5 Histori Transaksi")
    console.print("[3] Export Histori ke CSV")
    console.print("[4] Retry Transaksi Gagal")
    console.print("[5] Cari Transaksi berdasarkan TX Hash")
    console.print("[6] Keluar")


def show_history():
    rows = list_transactions(limit=5)
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Timestamp")
    table.add_column("Chain")
    table.add_column("Status")
    table.add_column("TX Hash")
    table.add_column("Error")

    for r in rows:
        table.add_row(r[0], r[1].upper(), r[3], r[2] or "-", r[4] or "-")

    console.print(table)


def export_csv():
    rows = list_transactions(limit=1000)
    os.makedirs("exports", exist_ok=True)
    path = "exports/transactions.csv"
    with open(path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Chain", "TX Hash", "Status", "Error"])
        for r in rows:
            writer.writerow(r)
    console.print(f"✅ Histori berhasil di-export ke: [bold yellow]{path}[/]")


def retry_failed_transactions():
    rows = get_failed_transactions(limit=3)
    if not rows:
        console.print("[yellow]Tidak ada transaksi gagal untuk di-retry.[/]")
        return

    for row in rows:
        id, raw_tx = row
        console.print(f"\n🔁 Retry transaksi ID {id}...")
        proxy_url = get_proxy()
        signed_tx = sign_with_vault(raw_tx, get_vault_token())
        result = retry_send_transaction(signed_tx, proxy_url)
        log_transaction(chain=ACTIVE_CHAIN, raw_tx=signed_tx, result=result)


def search_by_tx_hash():
    search = input("Masukkan seluruh atau sebagian TX Hash: ").strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, chain, tx_hash, status, error_message
        FROM transactions
        WHERE tx_hash LIKE ?
        ORDER BY id DESC
    """, (f"%{search}%",))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[red]❌ Tidak ditemukan transaksi dengan TX Hash tersebut.[/]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Timestamp")
    table.add_column("Chain")
    table.add_column("TX Hash")
    table.add_column("Status")
    table.add_column("Error")

    for r in rows:
        table.add_row(r[0], r[1].upper(), r[2], r[3], r[4] or "-")

    console.print(table)


def interactive_cli():
    while True:
        show_menu()
        choice = input("\nPilih opsi (1-6): ").strip()

        if choice == "1":
            confirm = input("⚠️ Eksekusi transaksi EMP? (y/n): ").lower()
            if confirm == "y":
                run_executor()
            else:
                console.print("[yellow]❌ Dibatalkan oleh user.[/]")
        elif choice == "2":
            show_history()
        elif choice == "3":
            export_csv()
        elif choice == "4":
            retry_failed_transactions()
        elif choice == "5":
            search_by_tx_hash()
        elif choice == "6":
            console.print("👋 Sampai jumpa!")
            break
        else:
            console.print("[red]Pilihan tidak valid, coba lagi...[/]")


if __name__ == "__main__":
    interactive_cli()
