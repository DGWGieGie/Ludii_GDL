# Ludii_GDL
Translate Ludii to GDL

## Notebook
code the translator via Jupyter-notebook which is draft version

## PropNet
code the translator as seperate files, but there are some bugs which could lead to failure currently. 
Those bug will be fixed later

## PropNet Directory
 + ReadFile.py: read the ludii file and get the key information
 + CONSTANT.py: containing the constant which is global variables
 + Ludii2GDL.py: calling the translating component(tanslate game, players, equipment, rules) and write GDL file
 + main.py: run the translator
 + Ludii_keyword: translate the Ludii to GDL based on keyword
 + Ludii_file: existing ludii file
 + GDL_file: translated gdl filee

## Keyword implmented
KEYWORD-1: Game, Players, Equipment, Board, Piece, Region, Rules, Start, Play, End. 
  
KEYWORD-2: Square, Line, Each, ForEach, Top, Bottom. 
  
KEYWORD-3: Mover, Empty, Add, Apply, Expand, Remove, ***Stack(BUG, Does not work)***
  
KEYWORD-4: ColumnSize, IsEnemyAt, StepForwardToEmpty, ReachWin. 
  
### Game  
Format: (***Game*** \<string>)
 + \<string>: the name of Game
  
### Players
Format: (***Players*** <int|list>)
 + <int|list>:
   * **int**: the number of players
   * **list**: the list of players
 
### Equipment
Format: (***Equipment*** <information>)
 + <information>: the ludii that including basic information of game

#### Board
 Format: (Board (<square|line> <int>))
 + <square|line>:
  * square: square game
  * line: line game
 + <int>: the size of game:  
 if it is board game, the size is NxN; if it is line game, the size is 1xN. 
 
#### Piece
 Format: (Piece \<string> \<KEYWORD>)
  + \<string>: the name of Piece
  + \<KEYWORD>: 
   * if ***<KEYWORD>*** is ***<P1|P2|etc.>***, it indicates the the player-1 is <string>
   * if ***<KEYWORD>*** is <Each>, it indicates that all piece in this game is <string>(it always is 'Pawn')

#### Regions
 Format: format: ((regions <P1|P2|etc> (sites <Top|Bottom>)))
  + <P1|P2|etc>: the player
  + sites <Top|Bottom>: the ***PX*** sites on the Top or Bottom of board

### Rules
 Format: (Rules \<Ludii>)
  + \<Ludii>: it is ludii that descript the rules of game

 #### Start
  Format: (start {(place \<string-Piece> (<Ludii-Move>), etc})
   + place: a keyword
   + \<string-Piece>: the name of Piece, which is defined on ***keyword-Piece*** 
   + <Ludii-Move>: define the move of game

#### Play
 Format: (play <Ludii-Move>)
  + <Ludii-Move>: define the move of game

#### End
 Format: format: (end <Ludii-End>)
  + <Ludii-End>: define the terminal of game
 

### Square: 
 it is square game
### Line: 
 it is line game
### Top: 
 The Top area of board
### Bottom: 
 the bottom area of board
### Each: 
 define the name of each piece
### ForEach: 
 define the legal move of each piece
### Mover: 
 current players
### Empty: 
 the cell is blank
### Add: 
 add the piece on a cell
   
 Format: (move add(to \<Ludii-Cell>))
  + <Ludii-Cell>: the status of the cell
 
### Apply: 
 excuting the move
   
 Format: (Apply \<Ludii-Move>):
  + \<Ludii-Move>: define the move of game

### Expand: 
 expand direction{From top to bottom; From bottom to Top}
   
 Format: (Expand (sites <Top|Bottom>)):
  + <Top|Bottom>: if it is ***Top***, expanding from bottom to Top; if it is ***Bottom***, expanding from Top to Bottom

### Remove: 
 Any piece owned by the current player can be removed from the board.
   
 Format: (remove (sites <occupied>)):
  + <occupied>: existing piece on this cell

### ***Stack(BUG, Does not work)*** specifies if the piece is added on top of a stack or not.

### ColumnSize: 
 count the size of special column

### IsEnemyAt: 
 judge special cell is empty or not

### StepForwardToEmpty: 
 the legal move for a piece is move forward, including front-left, front & front-right
 
### ReachWin: 
 if mover reaches the opponent's start point, the mover win the game
    
         
         
         
         
     
