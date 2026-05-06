import sqlite3
from typing import List, Tuple
import ipaddress
import os

class DatabaseManager:
    def __init__(self):
        # Create a 'data' directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
        
        self.db_path = os.path.join('data', 'trusted_ips.db')
        self.setup_database()
    
    def setup_database(self) -> None:
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trusted_ips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT NOT NULL UNIQUE,
                    description TEXT,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_ip(self, ip: str, description: str = "") -> bool:
        """Add a new trusted IP address"""
        try:
            # Validate IP address
            ipaddress.ip_address(ip)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO trusted_ips (ip_address, description) VALUES (?, ?)",
                    (ip, description)
                )
                conn.commit()
                return True
        except (ValueError, sqlite3.IntegrityError) as e:
            print(f"Error adding IP: {e}")
            return False

    def remove_ip(self, ip: str) -> bool:
        """Remove an IP from trusted list"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM trusted_ips WHERE ip_address = ?", (ip,))
            conn.commit()
            return cursor.rowcount > 0

    def is_trusted(self, ip: str) -> bool:
        """Check if an IP is trusted"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM trusted_ips WHERE ip_address = ?", (ip,))
            return cursor.fetchone()[0] > 0

    def get_all_ips(self) -> List[Tuple[str, str, str]]:
        """Get all trusted IPs with their details"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ip_address, description, date_added FROM trusted_ips")
            return cursor.fetchall()