# 📦 EMP Executor System

This system executes signed **EMP (Encrypted Messaging Payload)** transactions on the blockchain (Ethereum/Testnet). It is modular, secure, and can be run via both CLI and Web GUI.

---

## 🚀 Features

* ✅ Parse EMP file JSON (`EMP.txt`)
* ✅ Send raw transaction to Ethereum/Testnet
* ✅ Support proxy (stealth mode)
* ✅ Sign transactions via Vault (HSM-ready)
* ✅ Interactive CLI + dashboard
* ✅ SQLite logging for transaction history
* ✅ Automatic retry on failure
* ✅ Export history to CSV
* ✅ Search transactions by TX Hash
* ✅ Minimal Web GUI using Flask

---

## 🗂 Folder Structure

```
emp-executor/
├── app/
│   ├── cli/              # Interactive CLI & dashboard
│   ├── core/             # Core logic (parser, executor, signer, proxy)
│   ├── gui/              # Web GUI (Flask)
│   ├── storage/          # SQLite DB logger
│   └── utils/            # Vault client / helper
├── data/                 # EMP.txt file
├── logs/                 # SQLite files and logs
├── exports/              # CSV output directory
├── .env                  # Environment variables (RPC, token, etc.)
├── config.py             # .env loader
├── main.py               # Single transaction executor
├── requirements.txt      # Python dependencies
├── LICENSE               # MIT License
└── README.md             # 📄 This documentation file
```

---

## 🔧 Installation

```bash
git clone https://github.com/yourusername/emp-executor.git
cd emp-executor
pip install -r requirements.txt
cp .env.example .env
```

Edit your `.env` file:

```
ACTIVE_CHAIN=sepolia
ACTIVE_RPC=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
EMP_FILE_PATH=data/EMP.txt
```

---

## 🧪 Run Interactive CLI

```bash
python app/cli/cli_runner.py
```

### CLI Menu:

```
[1] Execute Transaction from EMP
[2] View Last 5 Transactions
[3] Export History to CSV
[4] Retry Failed Transactions
[5] Search Transaction by TX Hash
[6] Exit
```

---

## 🛠 Run One-Off Transaction

```bash
python main.py
```

---

## 📄 EMP.txt Format Example

```json
{
  "blockchain_execution": {
    "raw_transaction_hex": "0x02f8..."
  }
}
```

Use testnet wallet or signing tools like MyCrypto or Ethers.js to generate valid raw transactions.

---

## 📤 Export to CSV

```bash
ls exports/transactions.csv
```

Columns:

* Timestamp
* Chain
* TX Hash
* Status (`SUCCESS`, `FAILED`, `RETRY_FAILED`)
* Error message (optional)

---

## 🧠 Tech Stack

* Python 3.10+
* Flask (Web GUI)
* Rich (CLI interface)
* SQLite3 (logging)
* dotenv (.env support)
* Web3.py (optional transaction generation)

---

## 📜 License

MIT License — Free for personal and commercial use.

---

## 👨‍💻 Contributions

Pull Requests are welcome. Please keep your code modular, testable, and clean.

---

## 📫 Contact

* Telegram: [@LogicDir](https://t.me/LogicDir)
* Email: [support@logicdir.com](mailto:support@logicdir.com)
* Website: [https://logicdir.com](https://logicdir.com)

Execute your blockchain transactions safely, modularly, and professionally. 🐳
s