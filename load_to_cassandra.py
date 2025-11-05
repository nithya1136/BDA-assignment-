from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import csv
from dateutil import parser

CSV_PATH = "canteen_transactions.csv"

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
session.execute("USE canteen")

insert_tx = session.prepare("""
    INSERT INTO transactions (transaction_id, ts, user_id, items) VALUES (?, ?, ?, ?)
""")

inc_item = session.prepare("UPDATE item_counts SET count = count + ? WHERE item = ?")
inc_daily_item = session.prepare("UPDATE daily_item_counts SET count = count + ? WHERE day = ? AND item = ?")
inc_pair = session.prepare("UPDATE item_pairs SET count = count + ? WHERE pair = ?")

def canonical_pair(a, b):
    return "|".join(sorted([a,b]))

def process():
    with open(CSV_PATH, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tid = row['transaction_id']
            ts = parser.parse(row['timestamp'])
            user = row['user_id']
            items = [it.strip() for it in row['items'].split(';') if it.strip()]

            # Insert into transactions table
            session.execute(insert_tx, (tid, ts, user, items))

            # Update item counts and daily item counts
            for it in items:
                session.execute(inc_item, (1, it))
                session.execute(inc_daily_item, (1, ts.date().isoformat(), it))

            # Update co-occurring item pairs
            if len(items) > 1:
                for i in range(len(items)):
                    for j in range(i+1, len(items)):
                        session.execute(inc_pair, (1, canonical_pair(items[i], items[j])))

    print("✅ All data loaded successfully.")

if __name__ == "__main__":
    process()
