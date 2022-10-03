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
  
KEYWORD-4: forEach, ColumnSize, IsEnemyAt, StepForwardToEmpty, ReachWin. 
  
### Game  
Format: ***Game*** \<string>
 + \<string>: the name of Game
  
### Players
Format: ***Players*** <int|list>
 + <int|list>:
   * **int**: the number of players
   * **list**: the list of players
 
### Equipment
Format: ***Equipment*** <information>
 + <information>: the ludii that including basic information of game

#### Board
 Format: Board (<square|line> <int>)
 + <square|line>:
  * square: square game
  * line: line game
 + <int>: the size of game:  
 if it is board game, the size is NxN; if it is line game, the size is 1xN. 
 
#### Piece
 Format: Piece \<string> <KEYWORD.>
  + \<string>: the name of Piece
  + <KEYWORD>: 
   * if ***<KEYWORD>*** is ***<P1|P2|etc.>***, it indicates the the player-1 is <string>
   * if ***<KEYWORD>*** is <Each>, it indicates that all piece in this game is <string>(it always is 'Pawn')

#### Regions
 
 
 



   * regions: the location of information of game; eg. the Player-1 location, Player-2 location. it is ***optional keyword***
     + format: ((regions <P1|P2|etc> (sites <Top|Bottom>)))
       * regions: the keyword
       * <P1|P2|etc>: the player
       * sites <Top|Bottom>: the ***PX*** sites the Top or Bottom
         + ***sites*** is a keyword, for two players games, the location only contain ***Top & Bottom***; for more than two player games(chinese checker), more location will be included
 + rules: the rule information of game
   * start: the initial information of game
     + format (start {(place (location inforamtion), etc)})
       * start: the keyword
       * last part will be explained on ***Appendix Section***
   * play: the legal move information of game
     + format: (play MOVE-KEYWORD)
       * play: the keyword
       * MOVE-KEYWORD: the legal move; including ***move, flip, etc***; it could include other keyword, see ***Appendix Section***
   * end: the terminal inforamtion of game
     + format: (end END-KEYWORD)
       * end: the keyword
       * END-KEYWORD: the terminal rule
    
         
         
         
         
     
