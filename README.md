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
 + Game: the name of game. 
 + Players: the size of players. 
 + equipment: the basic information of game
   * board: the board information of game
     + format: (board (<type> <int>))
       * board: the keyword
       * type: the type of board, including squre, line, etc.(implement squre and line now)
       * <int>: the size of board, if the type is ***squre***, the size will be N*N, if the type is ***line***, the size will be 1*N
   * piece: the piece information of game
     + format: (piece <string> <KEYWORD>)
       * piece: the keyword
       * string: define the name of this piece
       * <KEYWORD>: 
         + if it is <P1|P2|...>, it indicates that the piece P1 is <string>
         + if it is <Each>, it indicates that all piece in this game is <string>(it always is 'Pawn')
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
    
         
         
         
         
     
