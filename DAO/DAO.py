import sqlite3
CAR_TABLE = f"""CREATE TABLE CAR (
            CAR_URL VARCHAR(40) PRIMARY KEY NOT NULL,
            NOME VARCHAR(40) NOT NULL,
            PREZZO INT NOT NULL,
            IMG_URL VARCHAR(40),
            DATE VARCHAR(12),
            EURO INT NOT NULL,
            KM INT,
            DESCRIPTION VARCHAR(200)
        )"""

def getAllUrls(file:str)->set:
    con = sqlite3.connect(file)
    cur = con.cursor()
    cur.execute(f"""SELECT CAR_URL FROM CAR""")
                    # WHERE PREZZO = (SELECT MIN(PREZZO) FROM CAR)
    carUrls = set()
    for url in cur.fetchall():
        carUrls.add(url[0])
    cur.close()
    return carUrls