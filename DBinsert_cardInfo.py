'''
Simple program that adds a card to the cardInfo TABLE

Make sure DB exists by running createDB.py before using this

This can be Deer homework (((((((blet)))))))
'''

#%% Imports and Vars

import sqlite3

db_filename = 'pkmn_cards.db'

#%% Functions
def convToBool(input):
    return input.lower() in ('y', 'true', '1')

def getInput():
    # gets entry input from console
    dexNum = int(input('Pokedex Number: '))
    seriesNum = input('Series Info: ')
    isFullArt = convToBool(input('Full Art? (Y/N): '))
    isRevFoil = convToBool(input('Reverse Foil? (Y/N): '))
    isFoil = convToBool(input('Normal Foil? (Y/N): '))
    notes = input('Additional Notes: ')

    return dexNum, seriesNum, isFullArt, isRevFoil, isFoil, notes


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
