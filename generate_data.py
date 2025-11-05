import csv, random, datetime

items = ["idli","dosa","vada","filter_coffee","masala_tea","rice_plate","sambar","chutney","upma","sandwich","juice"]
users = [f"u{100+i}" for i in range(200)]

def random_basket():
    k = random.choices([1,2,3,4], weights=[0.4,0.35,0.2,0.05])[0]
    return ";".join(random.sample(items, k))

with open("canteen_transactions.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["transaction_id","timestamp","user_id","items"])
    for i in range(1_000):  # change to 10000 if you want larger
        tid = f"t{i:05d}"
        ts = (datetime.datetime.now() - datetime.timedelta(days=random.randint(0,30), minutes=random.randint(0,1440))).isoformat()
        uid = random.choice(users)
        writer.writerow([tid, ts, uid, random_basket()])
