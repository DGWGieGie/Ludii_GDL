import re
from Ludii_Keyword import Keyword
import CONSTANT as CS

"""
class Equipment
 translate equipment of ludii
"""
class Equipment(Keyword.KeyTranslation):
    def translate(self):
        context = "; " *80 + "\n" + ";; Initial State\n" + "; " *80 + "\n"
        self.flag_init = False

        for var in self.ludii:
            if var[1:6] == "board":
                self.type_board, self.size_board = self.translate_board(var[7:-1])

            elif var[1:6] == "piece":
                self.flag_init = self.translate_piece(var[7:-1])

            elif var[1:8] == "regions":
                context += self.translate_init_True(var[9:-1])
                self.flag_init = True

        if not self.flag_init:
            context += self.translate_init_False()

        else:
            context += "(index 1) (index 2) (index 3) (index 4) (index 5) (index 6) (index 7) (index 8)\n"
            context += "(++ 1 2)  (++ 2 3)  (++ 3 4)  (++ 4 5)  (++ 5 6)  (++ 6 7)  (++ 7 8)"

        context += f"(init (control {CS.GAME_PLAYER[0]}))\n\n"
        return context



    def translate_board(self, ludii_board):
        if re.search("\(square ([0-9]*)\)", str.lower(ludii_board)):
            return "square", int(re.search("\(square ([0-9]*)\)", str.lower(ludii_board))[1])
        return None, None

    def translate_piece(self, ludii_piece):
        if re.search("\"[Disc|Cross]+\" P[0-9]*", ludii_piece):
            return False
        return False

    # no limitation of init
    def translate_init_False(self):
        # translating square type
        context = ""
        if self.type_board == "square":
            for i in range(1, self.size_board +1):
                for j in range(1, self.size_board +1):
                    context += f"(init (cell {i} {j} b))\n"
        return context


    def translate_init_True(self, init_ludii):
        context = ""
        player = re.search("(P[0-9]*) \(sites ([Top|Bottom]+)\)", init_ludii)[1]
        region = re.search("(P[0-9]*) \(sites ([Top|Bottom]+)\)", init_ludii)[2]
        if region == "Top":
            for j in range(1, 3):
                for i in range(1, self.size_board +1):
                    context += f"(init (cellholds {i} {j} {player}))\n"
        elif region == "Bottom":
            for j in range(2):
                for i in range(1, self.size_board +1):
                    context += f"(init (cellholds {i} {self.size_board -j} {player}))\n"
        return context