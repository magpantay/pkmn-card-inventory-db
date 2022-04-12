# Pokemon Card Inventory DB

## Purpose

The goal of this project is to have a descriptive and easy-to-query inventory of the Pokemon cards I have in my collection.

Each Pokemon and other card descriptors (ex. card series number, whether they're a foil and/or full-art card) will be stored in a SQL DB.

There will also be a program (likely in Python) written to easily query and modify the contents of the database.

## Proposed DB schema
- Table 1 (Pokemon Info):
  - Pokemon Name (text)
  - Pokedex Number (integer, primary key)
- Table 2 (Card Info):
  - Pokedex Number (integer, foreign key)
  - Card Series Number (text)
  - Amount Owned (integer)
  - Is Full Art? (boolean)
  - Is Foil? (boolean)
  - Is Reverse Foil? (boolean)
  - Additional Notes (text)

## To-dos:

- Get @BleatyBoi up to speed on git  
- Plan the database schema
- Create the database
- Create a script that interfaces with the DB
- Verify and test functionality of script
