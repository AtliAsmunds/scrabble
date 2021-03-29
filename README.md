# Scrabble

*The game is made for 1920 x 1080 resolution (100% scaling). If the display is set to another resolution the game might not display properly.*

## Game Rules

*NOTE: This game is in Icelandic*

* **2-4 Players**

The game is played on a 15x15 scrabble board and all words are checked on the [BÍN](https://bin.arnastofnun.is/)
dataset for Icelandic words and their declensions. In this version all words are allowed if they exist in the data.

Players starts with 7 letters drawn from a letter pouch of 100 letters, of which two are blank.
Each turn a player can choose to:

* Play a word
* Switch a number of letters on hand from the pouch
* Pass the turn

Words are only to be played horizontally or vertically and the first play of the game should touch
the center of the board (the star), with next plays only being valid if they connect to a word on the table.
Player's score is calculated by adding together the score for each of the letters of the word made along with
bonus modifiers (listed below). If player is able to play out all of his seven letters in one turn 50 extra
points will be added to their score.

A certain blank letter can always be played but counts for zero points. When put on the table the player will
be prompted to change its letter value. It can be changed multiple times by moving it to a different tile.

When switching letters from the pouch one should note that the blank letters "value" is "0" if one wishes to
switch it out.

### Game over

The game ends either when the pouch is empty and a player has played all of their letters, or if all players
have passed their turn two times in a row.
When the game ends those players still posessing any letters will have their score decreased by the sum of the
letters scores on hand/rack.

### Letters

Letter    |Score|Nr. of tiles
----------|-----|------------
A         | 1   | 11
Á         | 3   | 2
B         | 5   | 1
D         | 5   | 1
Ð         | 2   | 4
E         | 3   | 3
É         | 7   | 1
F         | 3   | 3
G         | 3   | 3
H         | 4   | 1
I         | 1   | 7
Í         | 4   | 1
J         | 6   | 1
K         | 2   | 4
L         | 2   | 5
M         | 2   | 3
N         | 1   | 7
O         | 5   | 1
Ó         | 3   | 2
P         | 5   | 1
R         | 1   | 8
S         | 1   | 7
T         | 2   | 6
U         | 2   | 6
Ú         | 4   | 1
V         | 5   | 1
X         | 10  | 1
Y         | 6   | 1
Ý         | 5   | 1
Þ         | 7   | 1
Æ         | 4   | 2
Ö         | 6   | 1
0 (blank) | 0   | 2

### Bonuses

Tile Mark|Function
---------|--------
2l       | Double letter score
3l       | Triple letter score
2w       | Double word score
3w       | Triple word score