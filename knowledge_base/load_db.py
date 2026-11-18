import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "customer_support.db"
DATA_DIR = Path(__file__).parent / "data"

def create_tables(conn):
    """Create the database tables."""
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            stock_quantity INTEGER DEFAULT 0,
            specifications TEXT,
            average_rating REAL DEFAULT 0.0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            status TEXT NOT NULL,
            items TEXT,
            total_amount REAL,
            shipping_address TEXT,
            tracking_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estimated_delivery TEXT,
            notes TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT,
            keywords TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            last_updated TEXT
        )
    ''')
    
    conn.commit()

def load_products(conn):
    """Load products from JSON file."""
    with open(DATA_DIR / "products.json", "r") as f:
        products = json.load(f)
    
    cursor = conn.cursor()
    for product in products:
        cursor.execute('''
            INSERT OR REPLACE INTO products 
            (id, name, description, price, category, stock_quantity, specifications, average_rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['id'], product['name'], product['description'],
            product['price'], product['category'], product['stock_quantity'],
            product['specifications'], product['average_rating']
        ))
    conn.commit()
    print(f"Loaded {len(products)} products")

def load_orders(conn):
    """Load orders from JSON file."""
    with open(DATA_DIR / "order_status.json", "r") as f:
        orders = json.load(f)
    
    cursor = conn.cursor()
    for order in orders:
        cursor.execute('''
            INSERT OR REPLACE INTO orders 
            (id, customer_id, status, items, total_amount, shipping_address, 
             tracking_number, created_at, updated_at, estimated_delivery, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order['order_id'], order['customer_id'], order['status'],
            order['items'], order['total_amount'], order['shipping_address'],
            order['tracking_number'], order['created_at'], order['updated_at'],
            order['estimated_delivery'], order['notes']
        ))
    conn.commit()
    print(f"Loaded {len(orders)} orders")

def load_faq(conn):
    """Load FAQ entries from JSON file."""
    with open(DATA_DIR / "faq.json", "r") as f:
        faqs = json.load(f)
    
    cursor = conn.cursor()
    for faq in faqs:
        cursor.execute('''
            INSERT INTO faq (question, answer, category, keywords)
            VALUES (?, ?, ?, ?)
        ''', (faq['question'], faq['answer'], faq['category'], faq['keywords']))
    conn.commit()
    print(f"Loaded {len(faqs)} FAQ entries")

def load_policies(conn):
    """Load policies from JSON file."""
    with open(DATA_DIR / "policies.json", "r") as f:
        policies = json.load(f)
    
    cursor = conn.cursor()
    for policy in policies:
        cursor.execute('''
            INSERT INTO policies (title, content, category, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (policy['title'], policy['content'], policy['category'], policy['last_updated']))
    conn.commit()
    print(f"Loaded {len(policies)} policies")

def main():
    """Main function to create tables and load all data."""
    print(f"Database path: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        create_tables(conn)
        print("Tables created successfully")
        
        load_products(conn)
        load_orders(conn)
        load_faq(conn)
        load_policies(conn)
        
        print("\nAll data loaded successfully!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
