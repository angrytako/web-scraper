CAR_TABLE = f"""CREATE TABLE CAR (
            CAR_URL VARCHAR(40) PRIMARY KEY,
            NOME VARCHAR(40) NOT NULL,
            PREZZO INT NOT NULL,
            IMG_URL VARCHAR(40),
            DATE VARCHAR(12),
            EURO INT NOT NULL,
            KM INT,
            DESCRIPTION VARCHAR(200)
        )"""