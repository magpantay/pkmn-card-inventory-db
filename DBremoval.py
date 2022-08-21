#%% Imports and Vars

import sqlite3

dbFilename = 'pkmn_cards.db'

#%% Functions

# Try to convert the value into an int, if it's able to then return true
def isInt(userInput):
    try:
        int(userInput)
        return bool(1)
    except ValueError:
        return bool(0)

# Returns "true" boolean value for input values with 'y', 'true', or '1'
def convToBool(input):
    return input.lower() in ('y', 'true', '1')

# Get user input for Pokedex number + name
def getInput():
    retDict = dict()
    retDict['numOrName'] = input('Pokemon Name or Dex Number: ')
    retDict['seriesNum'] = input('Series Info: ')
    retDict['isFullArt'] = convToBool(input('Full Art? (Y/N): '))
    retDict['isFoil'] = convToBool(input('Normal Foil? (Y/N): '))
    retDict['isRevFoil'] = convToBool(input('Reverse Foil? (Y/N): '))
    return retDict

# Query the DB, if amount - 1 is 0 then remove the entry otherwise deduct 1 from the amount
def removal(connection, userInput):
    cursor = connection.cursor()

    query = ""
    queryParams = ()

    if (isInt(userInput['numOrName'])):
        query = '''
                    SELECT amount
                    FROM cardInfo
                    WHERE dexNum = ?
                    AND seriesNum = ?
                    AND isFullArt = ?
                    AND isFoil = ?
                    AND isReverseFoil = ?
                '''
        queryParams = (userInput['numOrName'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])

    else:
        query = '''
                    SELECT cardInfo.amount
                    FROM cardInfo
                    LEFT JOIN pokemonInfo ON cardInfo.dexNum = pokemonInfo.dexNum
                    WHERE cardInfo.dexNum = ?
                    AND cardInfo.seriesNum = ?
                    AND cardInfo.isFullArt = ?
                    AND cardInfo.isFoil = ?
                    AND cardInfo.isReverseFoil = ?
                '''
        queryParams = (userInput['numOrName'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])

    cursor.execute(query, queryParams)
    queryResult = cursor.fetchall()

    if (len(queryResult) == 0):
        print("ERROR: No matches found.")
        exit()

    if (len(queryResult) > 1):
        print("ERROR: More than one match found. Check inputs and try again.")

    removalQuery = ""
    removalParams = ()

    # If amount - 1 = 0, delete the row from cardInfo
    if (queryResult[0][0] - 1 == 0):
        if (isInt(userInput['numOrName'])):
            removalQuery =  '''
                                DELETE FROM cardInfo
                                WHERE dexNum = ?
                                AND cardInfo.seriesNum = ?
                                AND cardInfo.isFullArt = ?
                                AND cardInfo.isFoil = ?
                                AND cardInfo.isReverseFoil = ?
                            '''
            removalParams = (userInput['numOrName'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])

        else:
            removalQuery =  '''
                                DELETE FROM cardInfo
                                WHERE dexNum = (
                                    SELECT dexNum
                                    FROM pokemonInfo
                                    WHERE lower(pokemonName) like ?
                                )
                                AND cardInfo.seriesNum = ?
                                AND cardInfo.isFullArt = ?
                                AND cardInfo.isFoil = ?
                                AND cardInfo.isReverseFoil = ?
                            '''
            removalParams = ('%' + userInput['numOrName'].lower() + '%', userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])
    
    # Else, update the row to subtract 1 from the amount
    else:
        if (isInt(userInput['numOrName'])):
            removalQuery =  '''
                                UPDATE cardInfo
                                SET amount = amount - 1
                                WHERE dexNum = ?
                                AND seriesNum = ?
                                AND isFullArt = ?
                                AND isFoil = ?
                                AND isReverseFoil = ?
                            '''
            removalParams = (userInput['numOrName'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])

        else:
            removalQuery =  '''
                                UPDATE cardInfo
                                SET amount = amount - 1
                                WHERE dexNum = (
                                    SELECT dexNum
                                    FROM pokemonInfo
                                    WHERE lower(pokemonName) like ?
                                )
                                AND seriesNum = ?
                                AND isFullArt = ?
                                AND isFoil = ?
                                AND isReverseFoil = ?
                            '''
            removalParams = ('%' + userInput['numOrName'].lower() + '%', userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])

    cursor.execute(removalQuery, removalParams)
    
    connection.commit()
#%% Main

def main():
    connection = sqlite3.connect(dbFilename)
    userInput = getInput()
    removal(connection, userInput)
    connection.close()

#%% Root

if __name__ == '__main__':
    main()
