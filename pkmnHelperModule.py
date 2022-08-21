#%% Imports and Vars

import sqlite3

#%% Functions

# Establishes connection to DB and returns DB connection
def dbConnect():
    dbFilename = 'pkmn_cards.db'
    connection = sqlite3.connect(dbFilename)
    return connection

# Returns "true" boolean value for input values with 'y', 'true', or '1'
def convToBool(input):
    return input.lower() in ('y', 'true', '1')

# Check whether Pokedex number is out of the range of existing Pokemon
# If out of range, error and exit | Otherwise do nothing
def validateDexNum(input):
    numberOfPokemon = 905
    if (input <= 0 or input > numberOfPokemon):
        print("ERROR: Pokedex number " + str(input) + " out of bounds from known Pokedex range (1-" + str(numberOfPokemon) + ")")
        exit()

# Try to convert the value into an int, if it's able to then return true
def isInt(userInput):
    try:
        int(userInput)
        return bool(1)
    except ValueError:
        return bool(0)
    
# Given a user input of a name, return the Pokedex number
def nameToDexNum(userInput):
    connection = dbConnect()
    cursor = connection.cursor()

    # Ensure the query matches case to the input by using lower() on both
    query = ''' 
                SELECT dexNum
                FROM pokemonInfo
                WHERE lower(pokemonName) like ? 
            '''
    queryParams = ('%' + userInput.lower() + '%',)

    cursor.execute(query, queryParams)
    queryResult = cursor.fetchall()

    if (len(queryResult) == 0):
        print("ERROR: No matches found.")
        exit()
    
    if (len(queryResult) > 1):
        print("ERROR: More than one match found. Check inputs and try again.")
        print("Returned Pokedex numbers: ")
        for row in queryResult:
            print(row)
        exit()
    
    return queryResult[0][0]
