import re
from Ludii_Keyword import Keyword
import CONSTANT as CS
"""
class Rules
  translate the rules of game including(start, play, end)
   Ludii format: ***play \<moves>***
     play: keyword
     \<moves>: the legal moves of playing rules
"""
class Rules(Keyword.KeyTranslation):
    def __init__(self, ludii, num_pl, size_board, type_board):
        self.ludii = ludii
        self.num_pl = num_pl
        self.size_board = size_board
        self.type_board = type_board
        self.gdl = self.translate()

    def translate(self):
        context = ""
        for var in self.ludii:
            if var[1:5] == "play":  # should be change as keyword variable
                context += self.translate_play(var)

            elif var[1:4] == "end":
                context += self.translate_end(var)
        return context

    def translate_play(self, keyword_play):
        lm = LudiiMove(keyword_play[5:-1], self.num_pl)
        return lm.legalMoveGDL + lm.MoveUpdate

    def translate_end(self, keyword_end):
        le = LudiiEnd(keyword_end[5:-1], self.size_board, self.num_pl)
        return le.winCondition + le.reward + le.terminal


"""
class LudiiMove
 translate ***move*** operator
   add function
"""
class LudiiMove:
    def __init__(self, ludii, num_pl):
        self.ludii = ludii
        self.num_pl = num_pl
        self.legalMoveGDL, self.MoveUpdate = self.translate()

    def translate(self):
        if self.ludii[7:10] == "Add":  # should be change as keyword
            return self.translate_Add(self.ludii[11:-1])
        elif self.ludii.strip() == "(forEach Piece)":  # StepForwardToEmpty
            return self.translate_StepForwardToEmpty("StepForwardToEmpty")  # should be change
        return "Legal Action None\n", "Update none\n"

    def translate_Add(self, keyword_add):
        if keyword_add == "(to (sites Empty))":
            # translating legal action
            context_LegalAction = ";" * 80 + "\n" + ";; Legal Action\n" + ";" * 80 + "\n"
            context_LegalAction += "(<= open (true (cell ?m ?n b)))"
            for i in range(self.num_pl):
                context_LegalAction += f"(<= (legal {CS.GAME_PLAYER[(i + 1) % self.num_pl]} noop) (true (control {CS.GAME_PLAYER[i]})))\n"
            context_LegalAction += "(<= (legal ?w (mark ?x ?y)) (true (cell ?x ?y b)) (true (control ?w)))\n\n"

            # translating move update
            context_Update = ";" * 80 + "\n" + ";;  Move & Update\n" + ";" * 80 + "\n"
            for i in range(self.num_pl):
                context_Update += f"(<= (next (cell ?m ?n {CS.CELL_MART[i]})) (does {CS.GAME_PLAYER[i]} (mark ?m ?n)) (true (cell ?m ?n b)))\n"

            # update mark cell
            context_Update += "(<= (next (cell ?m ?n ?w)) (true (cell ?m ?n ?w)) (distinct ?w b))\n"
            context_Update += "(<= (next (cell ?m ?n b)) (does ?w (mark ?j ?k)) (true (cell ?m ?n b)) (or (distinct ?m ?j) (distinct ?n ?k)))\n\n"
        return context_LegalAction, context_Update

    def translate_StepForwardToEmpty(self, keyword_forEach):
        if keyword_forEach == "StepForwardToEmpty":
            context_LegalAction = ";" * 80 + "\n" + ";; Legal Action\n" + ";" * 80 + "\n"
            for i in range(self.num_pl):
                context_LegalAction += f"(<= (legal {CS.GAME_PLAYER[(i + 1) % self.num_pl]} noop) (true (control {CS.GAME_PLAYER[i]})))\n"

            for i in range(self.num_pl):
                context_LegalAction += f"(<= (legal {CS.GAME_PLAYER[i]} (move {CS.STEPFORWARDTOEMPTY[i][0]})) (true (control {CS.GAME_PLAYER[i]})) (true (cellholds {CS.STEPFORWARDTOEMPTY[i][1]} {CS.GAME_PLAYER[i]})) (++ {CS.STEPFORWARDTOEMPTY[i][2]}) (cellempty {CS.STEPFORWARDTOEMPTY[i][3]}))\n"
                context_LegalAction += f"(<= (legal {CS.GAME_PLAYER[i]} (move {CS.STEPFORWARDTOEMPTY[i][4]})) (true (control {CS.GAME_PLAYER[i]})) (true (cellholds {CS.STEPFORWARDTOEMPTY[i][5]} {CS.GAME_PLAYER[i]})) (++ {CS.STEPFORWARDTOEMPTY[i][6]}) (++ {CS.STEPFORWARDTOEMPTY[i][7]}) (not (true (cellholds {CS.STEPFORWARDTOEMPTY[i][8]} {CS.GAME_PLAYER[i]}))))\n"
                context_LegalAction += f"(<= (legal {CS.GAME_PLAYER[i]} (move {CS.STEPFORWARDTOEMPTY[i][9]})) (true (control {CS.GAME_PLAYER[i]})) (true (cellholds {CS.STEPFORWARDTOEMPTY[i][10]} {CS.GAME_PLAYER[i]})) (++ {CS.STEPFORWARDTOEMPTY[i][11]}) (++ {CS.STEPFORWARDTOEMPTY[i][12]}) (not (true (cellholds {CS.STEPFORWARDTOEMPTY[i][13]} {CS.GAME_PLAYER[i]}))))\n"
            context_LegalAction += "\n"

            context_Update = ";" * 80 + "\n" + ";;  Move & Update\n" + ";" * 80 + "\n"

            context_Update += "(<= (next (cellholds ?x2 ?y2 ?player)) (role ?player) (does ?player (move ?x1 ?y1 ?x2 ?y2)))\n"
            context_Update += "(<= (next (cellholds ?x3 ?y3 ?state)) (true (cellholds ?x3 ?y3 ?state)) (role ?player) (does ?player (move ?x1 ?y1 ?x2 ?y2)) (distinctcell ?x1 ?y1 ?x3 ?y3) (distinctcell ?x2 ?y2 ?x3 ?y3))\n"
            context_Update += "(<= (cell ?x ?y) (index ?x) (index ?y))\n"
            context_Update += "(<= (cellempty ?x ?y) (cell ?x ?y) (not (true (cellholds ?x ?y P1))) (not (true (cellholds ?x ?y P2))))\n"
            context_Update += "(<= (distinctcell ?x1 ?y1 ?x2 ?y2) (cell ?x1 ?y1) (cell ?x2 ?y2) (distinct ?x1 ?x2))\n"
            context_Update += "(<= (distinctcell ?x1 ?y1 ?x2 ?y2) (cell ?x1 ?y1) (cell ?x2 ?y2) (distinct ?y1 ?y2))\n\n"

        return context_LegalAction, context_Update
        pass


"""
class LudiiEnd
   translate ***end*** operator
   ludii format: ***is line \<int>***
"""


class LudiiEnd:
    def __init__(self, ludii, size_board, num_pl):
        self.ludii = ludii
        self.size_board = size_board
        self.num_pl = num_pl
        self.winCondition, self.reward, self.terminal = self.translate()

    def translate(self):
        print(self)
        if self.ludii[1:3] == "if":
            return self.translate_if(self.ludii[4:-1])

        elif self.ludii[2:10] == "ReachWin":
            winCondition_GDL, terminal_key = LudiiWinCondition(self.ludii, self.size_board, 0,
                                                               self.num_pl).translate_reachWin()
            reward_GDL = LudiiReward(terminal_key, self.num_pl).translate()
            terminal_GDL = LudiiTerminalKey(terminal_key, self.num_pl).translate()
            return winCondition_GDL, reward_GDL, terminal_GDL

        return "winCondition None\n", "Reward None\n", "Terminal None\n"

    def translate_if(self, end_if):
        list_end = self.getEnds_if(end_if)
        winCondition_GDL = ""
        reward_GDL = ""
        terminal_GDL = ""
        terminal_key = ""
        for var in list_end:
            if re.search("\(is Line ([1-9]*)\)$", var):
                winCondition_GDL, terminal_key = LudiiWinCondition(var, self.size_board,
                                                                   re.search("\(is Line ([1-9]*)\)$", var)[1],
                                                                   self.num_pl).translate_line()
                terminal_GDL = LudiiTerminalKey(terminal_key, self.num_pl).translate()

            elif var[1:7] == "result":
                reward_GDL = LudiiReward(terminal_key, self.num_pl).translate()

        return winCondition_GDL, reward_GDL, terminal_GDL

    def getEnds_if(self, end_if):
        list_end = []
        string_end = ""
        count = 0

        for var in end_if:
            string_end += var
            if var == "(":
                count += 1

            elif var == ")":
                count -= 1

            if count == 0 and string_end != " ":
                list_end.append(string_end.strip())
                string_end = ""
        return list_end


class LudiiWinCondition:
    def __init__(self, ludii, size_board, length_line, num_pl):
        self.ludii = ludii
        self.size_board = size_board
        self.length_line = int(length_line)
        self.num_pl = num_pl

    def translate_line(self):
        context = ";" * 80 + "\n" + ";; Win Condition\n" + ";" * 80 + "\n"
        if self.size_board == self.length_line:
            contextRow = "(<= (row ?m ?x)"
            contextCol = "(<= (column ?n ?x)"
            contextDia1 = "(<= (diagonal ?x)"
            contextDia2 = "(<= (diagonal ?x)"

            for i in range(self.size_board):
                contextRow += f" (true (cell ?m {i + 1} ?x))"
                contextCol += f" (true (cell {i + 1} ?n ?x))"
                contextDia1 += f" (true (cell 1 {i + 1} ?x))"
                contextDia2 += f" (true (cell 1 {self.size_board - i} ?x))"

            contextRow += ")\n"
            contextCol += ")\n"
            contextDia1 += ")\n"
            contextDia2 += ")\n"

            context += contextRow + contextCol + contextDia1 + contextDia2 + "\n"
            context += "(<= (line ?x) (row ?m ?x))\n(<= (line ?x) (column ?m ?x))\n(<= (line ?x) (diagonal ?x))\n\n"
            return context, "line"

    def translate_reachWin(self):
        context = ";" * 80 + "\n" + ";; Win Condition\n" + ";" * 80 + "\n"
        for i in range(self.num_pl):
            context += f"(<= {CS.GAME_PLAYER[i]}win (index ?x) (true (cellholds ?x {(i - 1) % self.size_board + 1} {CS.GAME_PLAYER[i]})))\n"
            context += f"(<= {CS.GAME_PLAYER[i]}win (not {CS.GAME_PLAYER[(i + 1) % self.num_pl]}cell))\n"
            context += f"(<= {CS.GAME_PLAYER[i]}cell (cell ?x ?y) (true (cellholds ?x ?y {CS.GAME_PLAYER[i]})))\n"
        context += "\n"
        return context, "ReachWin"


class LudiiTerminalKey:
    def __init__(self, terminal_key, num_pl):
        self.terminal_key = terminal_key
        self.num_pl = num_pl

    def translate(self):
        if self.terminal_key == "line":
            context = ";" * 80 + "\n" + ";;; End\n" + ";" * 80 + "\n"
            for i in range(self.num_pl):
                context += f"(<= terminal(line {CS.CELL_MART[i]}))\n"
            context += "(<= terminal(not open))\n\n"  # draw

        elif self.terminal_key == "ReachWin":
            context = ";" * 80 + "\n" + ";;; End\n" + ";" * 80 + "\n"
            for i in range(self.num_pl):
                context += f"(<= terminal {CS.GAME_PLAYER[i]}win)\n"
        return context


class LudiiReward:
    def __init__(self, reward_key, num_pl):
        self.reward_key = reward_key
        self.num_pl = num_pl

    def translate(self):
        context = ";" * 80 + "\n" + ";;; Reward\n" + ";" * 80 + "\n"
        if self.reward_key == "line":
            for i in range(len(CS.TERMINAL_CONDITION)):
                for j in range(self.num_pl):
                    if CS.PLAYERREWARD[CS.TERMINAL_CONDITION[i]] == 100:
                        context += f"(<= (goal {CS.GAME_PLAYER[j]} {CS.PLAYERREWARD[CS.TERMINAL_CONDITION[i]]}) (line {CS.CELL_MART[j]}))\n"
                    elif CS.PLAYERREWARD[CS.TERMINAL_CONDITION[i]] == 0:
                        context += f"(<= (goal {CS.GAME_PLAYER[j]} {CS.PLAYERREWARD[CS.TERMINAL_CONDITION[i]]}) (line {CS.CELL_MART[j - 1]}))\n"
                    else:
                        context += f"(<= (goal {CS.GAME_PLAYER[j]} {CS.PLAYERREWARD[CS.TERMINAL_CONDITION[i]]}) "
                        for z in range(self.num_pl):
                            context += f"(not (line {CS.CELL_MART[z]})) "
                        context += "(not open))\n"

        elif self.reward_key == "ReachWin":
            for i in range(len(CS.TERMINAL_CONDITION)):
                for j in range(self.num_pl):
                    if CS.PLAYERREWARD[CS.TERMINAL_CONDITION[i]] == 100:
                        context += f"(<= (goal {CS.GAME_PLAYER[j]} {CS.PLAYERREWARD[CS.TERMINAL_CONDITION[i]]}) {CS.GAME_PLAYER[j]}win)\n"
                    elif CS.PLAYERREWARD[CS.TERMINAL_CONDITION[i]] == 0:
                        context += f"(<= (goal {CS.GAME_PLAYER[j]} {CS.PLAYERREWARD[CS.TERMINAL_CONDITION[i]]}) {CS.GAME_PLAYER[(j + 1) % self.num_pl]}win)\n"

        return context + "\n"


