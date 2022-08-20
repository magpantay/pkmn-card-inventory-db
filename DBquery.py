'''
Simple program that adds a card to the cardInfo TABLE

Make sure DB exists by running createDB.py before using this
'''

#%% Imports and Vars

import sqlite3

dbFilename = 'pkmn_cards.db'

#%% Functions
# Get user input of the Pokemon name
def getInput():
    userInput = input('Pokemon Name or Dex Number: ')
    return userInput

# Try to convert the value into an int, if it's able to then return true
def isInt(userInput):
    try:
        int(userInput)
        return bool(1)
    except ValueError:
        return bool(0)
    
# Process and potentially insert the entry received from the user
def queryDB(connection, userInput):
    cursor = connection.cursor()

    query = ""
    queryParams = ()

    if (isInt(userInput)):
        query = ''' 
                    SELECT pokemonInfo.dexNum, 
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
    else:
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
                    WHERE lower(pokemonInfo.pokemonName) like ?
                '''
        # For wildcards, need to put it as a param rather than in the query itself
        queryParams = ('%' + userInput.lower() + '%',)
    
    cursor.execute(query, queryParams)
    queryResult = cursor.fetchall()
 
    if (len(queryResult) == 0):
        print("No matches found.")
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
    connection = sqlite3.connect(dbFilename)
    userInput = getInput()
    queryDB(connection, userInput)
    connection.close()

#%% Root

if __name__ == '__main__':
    main()
