'''
Simple program that adds a Pokedex Number and Pokemon to the PokemonInfo TABLE

Make sure DB exists by running createDB.py before using this
'''

#%% Imports and Vars

import pkmnHelperModule

#%% Functions
# Get user input for Pokedex number + name
def getInput():
    retDict = dict()
    retDict['dexNum'] = int(input('Pokedex Number: '))

    pkmnHelperModule.validateDexNum(retDict['dexNum'])

    retDict['pkmnName'] = input('Pokemon Name: ')
    return retDict

# Process and potentially insert the entry received from the user
def insertItem(connection, userInput):
    cursor = connection.cursor()

    # Guarantee the order or be able to cherry pick params by making a param tuple based on the inputted dict
    # instead of relying on tuple order in getInput()
    newEntryParams = (userInput['dexNum'], userInput['pkmnName'])

    pkmnInfoExistQuery = '''SELECT *
                            FROM pokemonInfo
                            WHERE pokemonInfo.dexNum = ?
                            OR lower(pokemonInfo.pokemonName) = lower(?)'''

    cursor.execute(pkmnInfoExistQuery, newEntryParams)

    pkmnInfoExistResult = cursor.fetchall()

    # Check if either dexNum or pokemonName exists in the database
    # If so, console output and exit (without any insertion)
    if (len(pkmnInfoExistResult) > 0):
        print("ERROR: One or more inputs already exists in the database: ")
        for row in pkmnInfoExistResult:
            print(row)
        exit()

    # If not, insert it
    sqlInsert = '''INSERT INTO pokemonInfo(dexNum, pokemonName)
                   VALUES(?, ?)'''

    cursor.execute(sqlInsert, newEntryParams)
    connection.commit()

#%% Main

def main():
    connection = pkmnHelperModule.dbConnect()
    userInput = getInput()
    insertItem(connection, userInput)
    connection.close()

#%% Root

if __name__ == '__main__':
    main()
