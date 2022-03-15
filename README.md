# wordle_game

Classic Worlde game with french words

Run main.py to play the game. Need pygame module to run this app.

## Rules:

Guess a random french word with six tries.
In a try, for each caracter it will indicate if the letter is in the right place (green), if it is in the word but not in the right place (orange), or if it is not in the word at all (grey)

![GitHub Logo](/preview.JPG)

## Functionalities:

- Change from 4 to 11 caracters.
- Restart the game
- Give up to get the answer immediatlely

## Database:

Words are cleaned with pandas and numpy in a notebook (extraction.ipynb) using a database from http://www.lexique.org/ which provide useful informations such as frequency of uses and its nature (Verb, adjective ...)
Thoses words are saved in Words directory.
The program will only chose words that are singular and masculine or infinitive verb as a word to guess, but we can use any french word we want to fill the board.


