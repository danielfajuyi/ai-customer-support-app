import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
import random

DB_PATH = Path(__file__).parent.parent / "customer_support.db"

def seed_additional_orders(conn):
    """Add more orders with various statuses for testing."""
    
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    customers = [
        ("CUST-005", "100 Silicon Valley Rd, Palo Alto, CA 94301"),
        ("CUST-006", "200 Startup Lane, New York, NY 10001"),
        ("CUST-007", "300 Cloud Ave, Chicago, IL 60601"),
        ("CUST-008", "400 Data Drive, Boston, MA 02101"),
        ("CUST-009", "500 AI Boulevard, Miami, FL 33101"),
        ("CUST-010", "600 Robot Way, Portland, OR 97201"),
    ]
    
    products = [
        (1, "TechPro Ultrabook 15", 1299.99),
        (2, "TechPro Ultrabook 13", 999.99),
        (3, "ProDesk Desktop Tower", 1899.99),
        (4, "SmartTab Pro 11", 599.99),
        (5, "UltraWide Monitor 34", 799.99),
        (6, "ErgoComfort Keyboard", 149.99),
        (7, "PrecisionMouse Elite", 79.99),
        (8, "CloudStore SSD 2TB", 189.99),
        (9, "TechPro Docking Station", 199.99),
        (10, "SecureConnect VPN Router", 249.99),
    ]
    
    cursor = conn.cursor()
    
    for i in range(6, 21):
        customer = random.choice(customers)
        num_items = random.randint(1, 3)
        selected_products = random.sample(products, num_items)
        
        items = [
            {
                "product_id": p[0],
                "name": p[1],
                "quantity": random.randint(1, 2),
                "price": p[2]
            }
            for p in selected_products
        ]
        
        total = sum(item['price'] * item['quantity'] for item in items)
        status = random.choice(statuses)
        
        created = datetime(2024, 1, random.randint(1, 28), 
                          random.randint(8, 20), random.randint(0, 59))
        updated = created + timedelta(days=random.randint(0, 5))
        estimated = created + timedelta(days=random.randint(5, 10))
        
        tracking = f"TRK-{random.choice(['SF', 'NY', 'CH', 'BOS', 'MIA'])}-{random.randint(10000, 99999)}" if status in ['shipped', 'delivered'] else None
        
        order_id = f"ORD-2024-{i:03d}"
        
        cursor.execute('''
            INSERT OR REPLACE INTO orders 
            (id, customer_id, status, items, total_amount, shipping_address,
             tracking_number, created_at, updated_at, estimated_delivery, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_id, customer[0], status, json.dumps(items),
            round(total, 2), customer[1], tracking,
            created.isoformat(), updated.isoformat(),
            estimated.strftime("%Y-%m-%d"),
            f"Seed order {order_id}"
        ))
    
    conn.commit()
    print("Added 15 additional seed orders")

def main():
    """Main function to seed additional data."""
    if not DB_PATH.exists():
        print("Database not found. Please run load_db.py first.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        seed_additional_orders(conn)
        print("\nSeed data added successfully!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
