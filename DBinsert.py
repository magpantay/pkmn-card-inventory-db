'''
Simple program that adds a mon and dex num to the PokemonInfo TABLE

Make sure DB esists by running createDB.py before using this

I just delete the DB and recreate it for testing rn
'''

#%% Imports and Vars

import sqlite3

db_filename = 'pkmn_cards.db'


#%% Main

def main():
    connection = sqlite3.connect(db_filename)

    entry = getInput()

    insertItem(entry, connection)


#%% Functions

def getInput():
    #gets entry input from console

    dex = input('Enter dex num being added:')
    mon = input('Enter Pokemon Name:')
    return int(dex), mon


def insertItem(item, connection):

    sqlInsert = '''INSERT INTO pokemonInfo(dexNum, pokemonName)
             VALUES(?,?) '''

    cursor = connection.cursor()
    cursor.execute(sqlInsert, item)
    #command that adds data to the table

    connection.commit()


#%% Root

if __name__ == '__main__':
    main()
