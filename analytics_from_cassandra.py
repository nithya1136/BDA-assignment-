from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('canteen')

def top_items():
    rows = session.execute("SELECT item, count FROM item_counts")
    sorted_rows = sorted(rows, key=lambda r: r.count, reverse=True)
    print("Top 10 Most Sold Items:\n")
    for r in sorted_rows[:10]:
        print(f"{r.item} -> {r.count}")

def top_pairs():
    rows = session.execute("SELECT pair, count FROM item_pairs")
    sorted_rows = sorted(rows, key=lambda r: r.count, reverse=True)
    print("\nTop 10 Frequently Bought Together Pairs:\n")
    for r in sorted_rows[:10]:
        print(f"{r.pair} -> {r.count}")

if __name__ == "__main__":
    top_items()
    top_pairs()
