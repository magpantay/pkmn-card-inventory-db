'''
Simple program that adds a mon and dex num to the PokemonInfo TABLE

Make sure DB esists by running createDB.py before using this

I just delete the DB and recreate it for testing rn
'''

#%% Imports and Vars

import sqlite3

db_filename = 'pkmn_cards.db'

#%% Functions

def getInput():
    # gets entry input from console
    dex = input('Pokedex Number: ')
    mon = input('Pokemon Name: ')
    return int(dex), mon


def insertItem(item, connection):
    cursor = connection.cursor()

    existCheckQuery = '''SELECT *
                         FROM pokemonInfo
                         WHERE pokemonInfo.dexNum = ?
                         OR lower(pokemonInfo.pokemonName) = lower(?)'''

    cursor.execute(existCheckQuery, item)

    existCheckResults = cursor.fetchall()

    if (len(existCheckResults) > 0):
        print("One or more inputs already exists in the database: ")
        for row in existCheckResults:
            print(row)
    else:
        sqlInsert = '''INSERT INTO pokemonInfo(dexNum, pokemonName)
                       VALUES(?, ?)'''

        cursor.execute(sqlInsert, item)
        # command that adds data to the table

        connection.commit()

#%% Main

def main():
    connection = sqlite3.connect(db_filename)
    entry = getInput()
    insertItem(entry, connection)

#%% Root

if __name__ == '__main__':
    main()
