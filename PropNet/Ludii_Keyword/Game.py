from Ludii_Keyword import Keyword

"""
class Game
  translate the game name
   Ludii Format: ***game \<string>***
     game: keyword
     \<string>: define the name of game, it's string-based
"""
class Game(Keyword.KeyTranslation):

    '''
    translate the game name from ludii to GDL
    :param gameName: the name of game
    return string-based GDL
    '''
    def translate(self):
        context = ";" * 80 + "\n" + f";;; {self.ludii}\n" + ";" * 80 + "\n"
        return context
