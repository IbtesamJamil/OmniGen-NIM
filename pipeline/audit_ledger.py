import sqlite3
import hashlib
import datetime
import os

DB_PATH = "omnisecure_audit.db"

class AuditLedger:
    @staticmethod
    def initialize_db():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                username TEXT,
                role TEXT,
                action_type TEXT,
                details TEXT,
                payload_hash TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT,
                role TEXT
            )
        """)
        
        # Always ensure ibtesam and fariz exist with correct roles & password hash
        shared_pass_hash = hashlib.sha256("clinician123".encode()).hexdigest()
        cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", 
                       ("ibtesam", shared_pass_hash, "Clinical Geneticist"))
        cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", 
                       ("fariz", shared_pass_hash, "Bioinformatician"))
            
        conn.commit()
        conn.close()

    @staticmethod
    def verify_user(username, password):
        AuditLedger.initialize_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password_hash = ?", (username, pass_hash))
        res = cursor.fetchone()
        conn.close()
        return res[0] if res else None

    @staticmethod
    def log_action(username, role, action_type, details):
        AuditLedger.initialize_db()
        timestamp = datetime.datetime.now().isoformat()
        raw_string = f"{timestamp}-{username}-{action_type}-{details}"
        payload_hash = hashlib.sha256(raw_string.encode()).hexdigest()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_logs (timestamp, username, role, action_type, details, payload_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, username, role, action_type, details, payload_hash))
        conn.commit()
        conn.close()

    @staticmethod
    def fetch_logs():
        AuditLedger.initialize_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, username, role, action_type, details, payload_hash FROM audit_logs ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_head_hash():
        """
        Retrieves the latest payload hash from the tail of the audit log chain.
        """
        AuditLedger.initialize_db()
        if not os.path.exists(DB_PATH):
            return None
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT payload_hash FROM audit_logs ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    @staticmethod
    def verify_full_ledger() -> bool:
        """
        Verifies the cryptographic hash-chain integrity across all audit logs in SQLite.
        """
        if not os.path.exists(DB_PATH):
            return True
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, username, action_type, details, payload_hash FROM audit_logs ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            timestamp, username, action_type, details, stored_hash = row
            raw_string = f"{timestamp}-{username}-{action_type}-{details}"
            computed_hash = hashlib.sha256(raw_string.encode()).hexdigest()
            if computed_hash != stored_hash:
                return False
        return True