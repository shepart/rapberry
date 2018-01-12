import MySQLdb


config = {
    'host': 'localhost',
    'user': '??????',
    'password': '??????',
    'db': 'statistik'
}


db = MySQLdb.connect(host=config['host'], user=config['user'], passwd=config['password'], db=config['db'])

cursor = db.cursor()

cursor.execute("SELECT * FROM gas ORDER BY Datum")


rows = cursor.fetchall()
prev = None

index = 0
row = rows[index]

missing = []

while row is not None:

    if prev is not None:
        if prev[1] + 1 < row[1]:
            diff = row[1] - prev[1]
            if diff > 2:
                print rows[index - diff]
                missing.append((row, index, rows[index - diff], index-diff, diff))

    prev = row

    index = index + 1
    if index < len(rows):
        row = rows[index]
    else:
        break


for m in missing:
    print m


def fixit():
    for t in missing:
        add = 0
        start = t[3]
        end = t[1]
        for pos in xrange(start, end):
            cursor.execute("UPDATE gas SET Zaehlerstand=%s WHERE Datum=%s", (rows[pos][1]+add, rows[pos][0]))
            add = add + 1

        db.commit()


fixit()


cursor.close()
db.close()
