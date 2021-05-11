import requests
import json
import sqlite3

# ქვემოთ დაწერილ კოდით შეგვიძლია გამოვიტანოთ ჩვენთვის სასურველი კრიპტოვალურტის შესახებ ინფორმაცია
# value-ში უნდა ჩაიწეროს კრიპტოვალუტის id (მაგ. bitcoin, ethereum, dogecoin და ა.შ.)

# value = input('აქ ჩაწერეთ ის კრიპტოვალუტა, რომლის შესახებ ინფორმაციის მიღება გსურთ: ')
# url = f'https://api.coincap.io/v2/assets/{value}'

# ამ კოდით კი შეგვიძლია გამოვიტანოთ ინფორმაცია ყველა იმ კრიპტოვალუტაზე, რომელიც API-შია ხელმისაწვდომი
url = 'https://api.coincap.io/v2/assets'
r = requests.get(url)
print(r)
# print(dir(r))
# print(r.text)
# print(r.headers)
# print(r.status_code)
# print(r.headers['Content-Type'])
# print(r.headers.get('Content-Type'))
res = r.json()
# print(json.dumps(res, indent=4))
with open('coincap.json', 'w') as f:
    json.dump(res, f, indent=4)

# print(res['data'][0]['name'])
# print(res['data'][0]['priceUsd'])
# print(res['data'][49]['name'])
# print(res['data'][49]['priceUsd'])

# ქვემოთ კოდის მეშვეობით ვქმნი ცხრილს, რომელშიც იქნება კრიპტოვოლუტა და მისი ფასი, USD-ში
# ინფორმაცია შემაქ list-ში ციკლით და შემდეგ ვავსებ ცხრილს

conn = sqlite3.connect('crypto-db.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS crypto
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(20),
            price INTEGER
            )''')
conn.commit()

all_crypto = []
for each in res['data']:
    crypto = each['name']
    price = each['priceUsd']
    row = (crypto, price)
    all_crypto.append(row)

c.executemany('INSERT INTO crypto (name, price) VALUES (?, ?)', all_crypto)

conn.commit()
conn.close()