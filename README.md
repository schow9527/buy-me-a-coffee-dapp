# ☕ Buy Me a Coffee - Web3 DApp

A decentralized tipping & message wall DApp built with Python Flask, Web3.js, and SQLite.

## ✨ Features

- 🦊 **MetaMask Wallet Connection**: Connect with one click, auto-detect account and network (Sepolia, Holesky, Mainnet, etc.).
- ☕ **Native EVM Transfer**: Send native ETH directly from user wallet to creator address without requiring smart contract deployment.
- 💬 **Supporter Wall**: Leave supporter name and encouraging messages, live rendered on the supporters wall.
- 🗄️ **Single-Table SQLite Database**: Stores all transfer records, sender address, recipient address, amount, message, timestamp, and blockchain transaction hash (`tx_hash`).
- 🗑️ **Log Management**: Built-in one-click clear records feature.
- 🚀 **Render-Ready**: Fully configured with `gunicorn` for zero-configuration deployment on Render.

---

## 🗄️ Database Schema

The database uses a single table `transfers`:

```sql
CREATE TABLE transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,         -- 打赏者钱包地址
    recipient TEXT NOT NULL,      -- 创作者收款钱包地址
    amount REAL NOT NULL,         -- 转账金额 (ETH)
    name TEXT,                    -- 打赏者昵称
    message TEXT,                 -- 留言内容
    tx_hash TEXT,                 -- 区块链交易哈希
    timestamp TEXT NOT NULL       -- 记录时间
);
```

---

## 💻 Local Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

---

## 🌐 Deploy to Render

1. Create a new repository on your GitHub (e.g. `buy-me-a-coffee-dapp`) and push this code.
2. Go to [render.com](https://render.com/) -> **New +** -> **Web Service**.
3. Connect your repository and configure:
   - **Environment / Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`
4. Click **Deploy Web Service**!
