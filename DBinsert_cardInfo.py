'''
Simple program that adds a card to the cardInfo TABLE

Make sure DB exists by running createDB.py before using this
'''

#%% Imports and Vars

import sqlite3

dbFilename = 'pkmn_cards.db'

#%% Functions
# Returns "true" boolean value for input values with 'y', 'true', or '1'
def convToBool(input):
    return input.lower() in ('y', 'true', '1')

# Get user input for all fields in this DB table
def getInput():
    retDict = dict()
    retDict['dexNum'] = int(input('Pokedex Number: '))
    retDict['seriesNum'] = input('Series Info: ')
    retDict['isFullArt'] = convToBool(input('Full Art? (Y/N): '))
    retDict['isFoil'] = convToBool(input('Normal Foil? (Y/N): '))
    retDict['isRevFoil'] = convToBool(input('Reverse Foil? (Y/N): '))
    retDict['notes'] = input('Additional Notes (if needed): ')

    return retDict

# Process and potentially insert the entry received from the user
def insertItem(connection, userInput):
    cursor = connection.cursor()

    dexNumExistQuery = '''SELECT *
                          FROM pokemonInfo
                          WHERE pokemonInfo.dexNum = ?'''
    # For params with just 1 param, need to have a trailing ',' to force it to be a tuple
    queryParams = (userInput['dexNum'],)

    cursor.execute(dexNumExistQuery, queryParams)
    dexNumExistResult = cursor.fetchall()

    # Check if dexNum (primary and foreign key) exists in the pokemonInfo table
    # If it doesn't, console output and exit (without any insertion)
    if (len(dexNumExistResult) == 0):
        print("ERROR: Dex Number '" + str(userInput['dexNum']) + "' does not exist in the pokemonInfo table.")
        exit()

    # If it does, insert this new entry into the DB -or- increment the counter if already exists in table
    cardExistsQuery = '''SELECT *
                         FROM cardInfo
                         WHERE dexNum = ?
                         AND seriesNum = ?
                         AND isFullArt = ?
                         AND isFoil = ?
                         AND isReverseFoil = ?'''
    queryParams = (userInput['dexNum'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])

    cursor.execute(cardExistsQuery, queryParams)
    cardExistsResult = cursor.fetchall()

    # If card exists and there aren't any notes, then just increment the amount by 1
    if (len(cardExistsResult) >= 1 and len(userInput['notes']) == 0):
        sqlUpdateCmd = '''UPDATE cardInfo
                          SET amount = amount + 1
                          WHERE dexNum = ?
                          AND seriesNum = ?
                          AND isFullArt = ?
                          AND isFoil = ?
                          AND isReverseFoil = ?'''
        queryParams = (userInput['dexNum'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])

        cursor.execute(sqlUpdateCmd, queryParams)
    
    # If card exists and there are notes, increment amount by 1 and append to the notes
    elif (len(cardExistsResult) >= 1 and len(userInput['notes']) >= 1):
        sqlUpdateCmd = '''UPDATE cardInfo
                          SET amount = amount + 1, notes = notes + " // " + ?
                          WHERE dexNum = ?
                          AND seriesNum = ?
                          AND isFullArt = ?
                          AND isFoil = ?
                          AND isReverseFoil = ?'''
        queryParams = (userInput['notes'], userInput['dexNum'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])

        cursor.execute(sqlUpdateCmd, queryParams)
        
    # If the card does not exist, add a new entry into the DB with amount = 1
    else:
        sqlInsertCmd = '''INSERT INTO cardInfo(dexNum, seriesNum, amount, isFullArt, isFoil, isReverseFoil, notes)
                          VALUES(?, ?, ?, ?, ?, ?, ?)'''
        newEntryParams = (userInput['dexNum'], userInput['seriesNum'], 1, userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'], userInput['notes'])

        cursor.execute(sqlInsertCmd, newEntryParams)

    connection.commit()

#%% Main

def main():
    connection = sqlite3.connect(dbFilename)
    userInput = getInput()
    insertItem(connection, userInput)

#%% Root

if __name__ == '__main__':
    main()
