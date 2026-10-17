import sqlite3
import hashlib
import time
import os

class OctopusDigitalBridge:
    def __init__(self, db_path="octopus_2_1.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_wallets (
                card_id TEXT PRIMARY KEY,
                holder_name TEXT,
                balance REAL NOT NULL,
                deposit_held REAL DEFAULT 20.0,
                monthly_limit REAL DEFAULT 1000.0,
                monthly_spent REAL DEFAULT 0.0,
                card_status TEXT DEFAULT 'ACTIVE',
                last_updated INTEGER
            )
        ''')
        
        existing_cols = [row[1] for row in cursor.execute("PRAGMA table_info(community_wallets)").fetchall()]
        if 'deposit_held' not in existing_cols:
            cursor.execute("ALTER TABLE community_wallets ADD COLUMN deposit_held REAL DEFAULT 20.0")
        if 'monthly_limit' not in existing_cols:
            cursor.execute("ALTER TABLE community_wallets ADD COLUMN monthly_limit REAL DEFAULT 1000.0")
        if 'monthly_spent' not in existing_cols:
            cursor.execute("ALTER TABLE community_wallets ADD COLUMN monthly_spent REAL DEFAULT 0.0")
        if 'card_status' not in existing_cols:
            cursor.execute("ALTER TABLE community_wallets ADD COLUMN card_status TEXT DEFAULT 'ACTIVE'")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaction_ledger (
                tx_id TEXT PRIMARY KEY,
                card_id TEXT,
                amount REAL,
                tx_type TEXT,
                timestamp INTEGER,
                secure_hash TEXT
            )
        ''')
        self.conn.commit()

    def issue_physical_card(self, card_id, holder_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT card_id FROM community_wallets WHERE card_id = ?", (card_id,))
        if cursor.fetchone():
            return {"status": "error", "message": "Physical card ID already registered."}
        
        cursor.execute('''
            INSERT INTO community_wallets (card_id, holder_name, balance, deposit_held, monthly_limit, monthly_spent, card_status, last_updated)
            VALUES (?, ?, 0.0, 20.0, 1000.0, 0.0, 'ACTIVE', ?)
        ''', (card_id, holder_name, int(time.time())))
        self.conn.commit()
        
        return {
            "status": "success", 
            "card_id": card_id, 
            "holder": holder_name, 
            "deposit_required": 20.0,
            "monthly_limit": 1000.0,
            "message": "Physical card successfully issued with $20 refundable deposit anchor."
        }

    def cash_reload(self, card_id, cash_amount):
        cursor = self.conn.cursor()
        cursor.execute("SELECT balance, monthly_limit, monthly_spent FROM community_wallets WHERE card_id = ?", (card_id,))
        row = cursor.fetchone()
        
        if not row:
            return {"status": "error", "message": "Card ID not found."}
        
        balance, monthly_limit, monthly_spent = row
        new_balance = balance + cash_amount
        
        if (monthly_spent + cash_amount) > monthly_limit:
            return {"status": "error", "message": "Reload exceeds the $1,000 monthly family/community allowance limit."}
        
        cursor.execute("UPDATE community_wallets SET balance = ?, monthly_spent = ?, last_updated = ? WHERE card_id = ?", 
                       (new_balance, monthly_spent + cash_amount, int(time.time()), card_id))
        
        tx_id = hashlib.sha256(f"{card_id}-cash-{time.time()}".encode()).hexdigest()[:16]
        cursor.execute("INSERT INTO transaction_ledger VALUES (?, ?, ?, ?, ?, ?)",
                       (tx_id, card_id, cash_amount, "CASH_RELOAD", int(time.time()), tx_id))
        self.conn.commit()
        
        return {"status": "success", "tx_id": tx_id, "new_balance": new_balance}

    def etransfer_reload(self, card_id, sender_email, transfer_amount):
        cursor = self.conn.cursor()
        cursor.execute("SELECT balance, monthly_limit, monthly_spent FROM community_wallets WHERE card_id = ?", (card_id,))
        row = cursor.fetchone()
        
        if not row:
            return {"status": "error", "message": "Card ID not found."}
        
        balance, monthly_limit, monthly_spent = row
        new_balance = balance + transfer_amount
        
        if (monthly_spent + transfer_amount) > monthly_limit:
            return {"status": "error", "message": "Transfer exceeds the $1,000 monthly family/community allowance limit."}
        
        cursor.execute("UPDATE community_wallets SET balance = ?, monthly_spent = ?, last_updated = ? WHERE card_id = ?", 
                       (new_balance, monthly_spent + transfer_amount, int(time.time()), card_id))
        
        tx_id = hashlib.sha256(f"{card_id}-etransfer-{time.time()}".encode()).hexdigest()[:16]
        cursor.execute("INSERT INTO transaction_ledger VALUES (?, ?, ?, ?, ?, ?)",
                       (tx_id, card_id, transfer_amount, f"ETRANSFER:{sender_email}", int(time.time()), tx_id))
        self.conn.commit()
        
        return {"status": "success", "tx_id": tx_id, "new_balance": new_balance, "sender": sender_email}

    def refund_card_deposit(self, card_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT deposit_held, card_status FROM community_wallets WHERE card_id = ?", (card_id,))
        row = cursor.fetchone()
        
        if not row:
            return {"status": "error", "message": "Card ID not found."}
        
        deposit, status = row
        if status == 'REFUNDED':
            return {"status": "error", "message": "Deposit has already been refunded for this card."}
        
        cursor.execute("UPDATE community_wallets SET deposit_held = 0.0, card_status = 'REFUNDED', last_updated = ? WHERE card_id = ?", 
                       (int(time.time()), card_id))
        self.conn.commit()
        
        return {"status": "success", "refund_amount": deposit, "message": f"${deposit} refundable deposit returned to cardholder."}

if __name__ == "__main__":
    bridge = OctopusDigitalBridge()
    print("Issuing Card:", bridge.issue_physical_card('OCT-PHYSICAL-001', 'Jujita Stairs'))
    print("Cash Reload:", bridge.cash_reload('OCT-PHYSICAL-001', 100.0))
    print("e-Transfer Reload:", bridge.etransfer_reload('OCT-PHYSICAL-001', 'family@example.ca', 50.0))
    print("Deposit Refund:", bridge.refund_card_deposit('OCT-PHYSICAL-001'))
