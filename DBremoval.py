#%% Imports and Vars

import pkmnHelperModule

#%% Functions

# Get user input for Pokedex number + name
def getInput():
    retDict = dict()
    numOrName = input('Pokemon Name or Dex Number: ')

    if (pkmnHelperModule.isInt(numOrName)):
        pkmnHelperModule.validateDexNum(numOrName)
        retDict['num'] = numOrName # if it passes through validateDexNum without exiting, then it's a valid number input
    else:
        retDict['num'] = pkmnHelperModule.nameToDexNum(numOrName)

    retDict['seriesNum'] = input('Series Info: ')
    retDict['isFullArt'] = pkmnHelperModule.convToBool(input('Full Art? (Y/N): '))
    retDict['isFoil'] = pkmnHelperModule.convToBool(input('Normal Foil? (Y/N): '))
    retDict['isRevFoil'] = pkmnHelperModule.convToBool(input('Reverse Foil? (Y/N): '))
    return retDict

# Query the DB, if amount - 1 is 0 then remove the entry otherwise deduct 1 from the amount
def removal(connection, userInput):
    cursor = connection.cursor()

    query = '''
                SELECT amount
                FROM cardInfo
                WHERE dexNum = ?
                AND seriesNum = ?
                AND isFullArt = ?
                AND isFoil = ?
                AND isReverseFoil = ?
            '''
    queryParams = (userInput['num'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])

    cursor.execute(query, queryParams)
    queryResult = cursor.fetchall()

    if (len(queryResult) == 0):
        print("ERROR: No matches found.")
        exit()

    if (len(queryResult) > 1):
        print("ERROR: More than one match found. Check inputs and try again.")
        exit()

    removalQuery = ""
    removalParams = ()

    # If amount - 1 = 0, delete the row from cardInfo
    if (queryResult[0][0] - 1 == 0):
        removalQuery =  '''
                                DELETE FROM cardInfo
                                WHERE dexNum = ?
                                AND cardInfo.seriesNum = ?
                                AND cardInfo.isFullArt = ?
                                AND cardInfo.isFoil = ?
                                AND cardInfo.isReverseFoil = ?
                            '''
        removalParams = (userInput['num'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])
    
    # Else, update the row to subtract 1 from the amount
    else:
        removalQuery =  '''
                            UPDATE cardInfo
                            SET amount = amount - 1
                            WHERE dexNum = ?
                            AND seriesNum = ?
                            AND isFullArt = ?
                            AND isFoil = ?
                            AND isReverseFoil = ?
                        '''
        removalParams = (userInput['num'], userInput['seriesNum'], userInput['isFullArt'], userInput['isFoil'], userInput['isRevFoil'])
        
    cursor.execute(removalQuery, removalParams)
    
    connection.commit()
#%% Main

def main():
    connection = pkmnHelperModule.dbConnect()
    userInput = getInput()
    removal(connection, userInput)
    connection.close()

#%% Root

if __name__ == '__main__':
    main()
