'''
Simple program that adds a card to the cardInfo TABLE

Make sure DB exists by running createDB.py before using this
'''

#%% Imports and Vars

import pkmnHelperModule

#%% Functions
# Get user input of the Pokemon name or Pokedex number
def getInput():
    userInput = input('Pokemon Name or Dex Number: ')

    if pkmnHelperModule.isInt(userInput):
        pkmnHelperModule.validateDexNum(int(userInput))
        return int(userInput) # if it passes the int check and validation, return the number value
    else:
        return pkmnHelperModule.nameToDexNum(userInput) # else convert it to a dex number and return the dex number
    
# Process and potentially insert the entry received from the user
def queryDB(connection, userInput):
    cursor = connection.cursor()

    query = ''' 
                SELECT  pokemonInfo.dexNum, 
                        pokemonInfo.pokemonName, 
                        cardInfo.seriesNum, 
                        cardInfo.amount, 
                        CASE cardInfo.isFullArt
                            WHEN 1 THEN "Yes"
                            ELSE "No"
                        END AS isFullArt,
                        CASE cardInfo.isFoil
                            WHEN 1 THEN "Yes"
                            ELSE "No"
                        END AS isFoil,
                        CASE cardInfo.isReverseFoil
                            WHEN 1 THEN "Yes"
                            ELSE "No"
                        END AS isReverseFoil, 
                        cardInfo.notes
                FROM pokemonInfo
                LEFT JOIN cardInfo ON pokemonInfo.dexNum = cardInfo.dexNum
                WHERE pokemonInfo.dexNum = ?
            '''
    queryParams = (userInput,)
    
    cursor.execute(query, queryParams)
    queryResult = cursor.fetchall()
 
    if (len(queryResult) == 0):
        print("ERROR: No matches found.")
        exit()
    else:
        userFriendlyFieldNames = ('Pokedex Number', 'Pokemon Name', 'Series', 'Amount', 'Is Full Art?', 'Is Foil?', 'Is Reverse Foil?', 'Notes')
        print ('-' * 40)
        # Iterate through columns for each row
        for row in queryResult:
            print ('-' * 20)
            for j in range(len(userFriendlyFieldNames)):
                print(userFriendlyFieldNames[j] + ": " + str(row[j]))
            print ('-' * 20)
        print ('-' * 40)

#%% Main

def main():
    connection = pkmnHelperModule.dbConnect()
    userInput = getInput()
    queryDB(connection, userInput)
    connection.close()

#%% Root

if __name__ == '__main__':
    main()
