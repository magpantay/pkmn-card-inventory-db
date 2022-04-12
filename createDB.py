import sqlite3

db_filename = 'pkmn_cards.db'

connection = sqlite3.connect(db_filename)

cursor = connection.cursor()

# Create Pokemon Info table
cursor.execute('''CREATE TABLE IF NOT EXISTS pokemonInfo (
                    "dexNum" INTEGER NOT NULL,
                    "pokemonName" TEXT NOT NULL,
                    PRIMARY KEY("dexNum")
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS cardInfo (
                    "dexNum" INTEGER NOT NULL,
                    "seriesNum" TEXT NOT NULL,
                    "amount" INTEGER NOT NULL,
                    "isFullArt" INEGER NOT NULL,
                    "isFoil" INTEGER NOT NULL,
                    "isReverseFoil" INTEGER NOT NULL,
                    "notes" TEXT,
                    FOREIGN KEY ("dexNum") REFERENCES pokemonInfo("dexNum")
                 )''')

# Save (commit) changes
connection.commit()

# Close the connection to the DB
connection.close()
