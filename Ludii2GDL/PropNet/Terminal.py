import re
import Constant as CT


class Terminal:
    def __init__(self, endInfor, players, winCon, boardInfo):
        self.win_Dict = self.decompositionEnd(endInfor)
        self.players = players
        self.winCon = winCon
        self.boardInfo = boardInfo

    def decompositionEnd(self, Infor):
        if Infor:
            end_dict = {}
            for var in Infor:
                endVar = re.search("\(end \(if \((.*)\) \((.*)\)\)\)", var)
                if endVar:
                    end_dict[endVar.group(1)] = endVar.group(2)
            return end_dict
        else:
            return None

    def convertEndInfo(self):
        context = ";" * 80 + "\n" + ";;; Reward\n" + ";" * 80 + "\n\n"
        for key, var in self.win_Dict.items():
            if "is Line" in key and "result Mover Win" in var:
                # reward
                for i in range(len(CT.TERMINAL_CONDITION)):
                    for j in range(len(self.players)):
                        if CT.PLAYERREWARD[CT.TERMINAL_CONDITION[i]] == 100:
                            context += f"(<= (goal {self.players[j]} {CT.PLAYERREWARD[CT.TERMINAL_CONDITION[i]]}) (line {CT.CELL_MART[j]}))\n"
                        elif CT.PLAYERREWARD[CT.TERMINAL_CONDITION[i]] == 0:
                            context += f"(<= (goal {self.players[j]} {CT.PLAYERREWARD[CT.TERMINAL_CONDITION[i]]}) (line {CT.CELL_MART[j - 1]}))\n"
                        else:
                            context += f"(<= (goal {self.players[j]} {CT.PLAYERREWARD[CT.TERMINAL_CONDITION[i]]}) "
                            for z in range(len(self.players)):
                                context += f"(not (line {CT.CELL_MART[z]})) "
                            context += "(not open))\n"

                # terminal
                context += "\n" + ";" * 80 + "\n" + ";;; End\n" + ";" * 80 + "\n\n"
                for i in range(len(CT.TERMINAL_CONDITION)):
                    if i < len(self.players):
                        context += f"(<= terminal(line {CT.CELL_MART[i]}))\n"
                    else:
                        context += "(<= terminal(not open))\n\n"  # draw
        return context

    def convertWinInfo(self, mode="Line"):
        if mode == "Line" and "square" in self.boardInfo:

            # row
            contextRow = "(<= (row ?m ?x)"
            contextCol = "(<= (column ?n ?x)"
            contextDia1 = "(<= (diagonal ?x)"
            contextDia2 = "(<= (diagonal ?x)"
            for i in range(int(self.boardInfo[7])):
                contextRow += f" (true (cell ?m {i + 1} ?x))"
                contextCol += f" (true (cell {i + 1} ?n ?x))"
                contextDia1 += f" (true (cell 1 {i + 1} ?x))"
                contextDia2 += f" (true (cell 1 {int(self.boardInfo[7]) - i} ?x))"
            contextRow += "\n"
            contextCol += "\n"
            contextDia1 += "\n"
            contextDia2 += "\n"

            context = contextRow + contextCol + contextDia1 + contextDia2 + "\n"
            context += "(<= (line ?x) (row ?m ?x))\n(<= (line ?x) (column ?m ?x))\n(<= (line ?x) (diagonal ?x))\n\n"
        return context

