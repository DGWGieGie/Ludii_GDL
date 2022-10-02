from Ludii_Keyword import Keyword
import CONSTANT as CS

"""
class Players

 translate the players
   Ludii Format: ***players \<int | string>***
     players: keyword
     \<int | string>: define the players
       if using *int*, it define the size of players
       if using *string*, it define the name of players
"""
class Players(Keyword.KeyTranslation):
    def translate(self):
        '''
        translate the players description from ludii to GDL
        :param players: a list that including the name of player
        return string-based GDL
        '''
        context = ";" * 80 + "\n" + ";; Roles\n" + ";" * 80 + "\n"

        if self.ludii.isdigit():
            self.num_pl = int(self.ludii)
        else:
            self.num_pl = self.StringP2DigitP()

        for index in range(self.num_pl):
            context += f"(role {CS.GAME_PLAYER[index]})\n"
        context += "\n"

        context += self.translate_turn()
        return context

    def StringP2DigitP(self):
        count = 0
        for var in self.ludii:
            if var == "(":
                count += 1
        return count

    def translate_turn(self):
        """
        translate the mode
        :param players: the list of player
        return string-based GDL that including the turn mode
        """
        context = ";" * 80 + "\n" + ";; Game Mode\n" + ";" * 80 + "\n"
        for i in range(self.num_pl):
            context += f"(<= (next (control {CS.GAME_PLAYER[i]})) (true (control {CS.GAME_PLAYER[(i + 1) % self.num_pl]})))\n"
        context += "\n"
        return context