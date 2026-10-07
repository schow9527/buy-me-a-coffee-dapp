import sqlite3
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
DB_NAME = "coffee.db"

# 部署在 Sepolia 上的智能合约地址
CONTRACT_ADDRESS = "0xd5f75d250210720bA437a144539a82E7eAD65FE2"


def init_db():
    """初始化数据库，只包含一张记录转账记录的表"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            amount REAL NOT NULL,
            name TEXT,
            message TEXT,
            tx_hash TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET"])
def index():
    """DApp 主页：显示转账打赏表单与最新的转账留言墙"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, sender, recipient, amount, name, message, tx_hash, timestamp FROM transfers ORDER BY id DESC")
    records = c.fetchall()
    conn.close()

    total_coffee = len(records)
    total_eth = round(sum(r[3] for r in records), 4) if records else 0.0

    return render_template(
        "index.html",
        records=records,
        total_coffee=total_coffee,
        total_eth=total_eth,
        contract_address=CONTRACT_ADDRESS,
    )


@app.route("/api/transfer", methods=["POST"])
def record_transfer():
    """记录转账到 SQLite 数据库的 API"""
    data = request.get_json(silent=True) or request.form

    sender = data.get("sender", "").strip()
    recipient = data.get("recipient", CONTRACT_ADDRESS).strip()
    amount = data.get("amount", 0)
    name = data.get("name", "Anonymous").strip() or "Anonymous"
    message = data.get("message", "Enjoy your coffee! ☕").strip() or "Enjoy your coffee! ☕"
    tx_hash = data.get("tx_hash", "").strip()

    if not sender:
        return jsonify({"status": "error", "message": "Sender wallet address is required"}), 400

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Invalid amount"}), 400

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO transfers (sender, recipient, amount, name, message, tx_hash, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (sender, recipient, amount, name, message, tx_hash, now),
    )
    conn.commit()
    record_id = c.lastrowid
    conn.close()

    return jsonify({"status": "success", "id": record_id, "message": "Transfer recorded successfully"})


@app.route("/deleteRecords", methods=["POST"])
def delete_records():
    """清空所有转账记录"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM transfers")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
