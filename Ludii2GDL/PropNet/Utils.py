import Constant as CT
from Terminal import Terminal
from BoardConvert import BoardConvert

def loadLudii(fileName):
    '''
    loading Ludii and store the information as dict type
    :param fileName: the filename of game
    return a dict that contain the information of correspond game
    '''
    info = "".join(readfile(fileName).split("//")[:-1]).split("\n")

    info_dict = {}
    for i in range(len(info)):
        if "game" in info[i]:
            info_dict["game"] = info[i].strip()[7:-1]

        elif "players" in info[i]:
            info_dict["players"] = int(info[i].strip()[9:-1])

        elif "equipment" in info[i]:
            list_eq = []
            i += 1
            while "})" not in info[i]:
                list_eq.append(info[i].strip())
                i += 1
            info_dict["equipment"] = list_eq

        elif "rules" in info[i]:
            list_ru = []
            i += 1
            while len(info[i].strip()) > 1:
                list_ru.append(info[i].strip())
                i += 1
            info_dict["rules"] = list_ru
    return info_dict


def readfile(fileName):
    '''
    read the file
    :param fileName: the name of file
    return the context of file
    '''
    with open(fileName) as fp:
        return fp.read()


def translateGame(gameName):
    '''
    translate the game name from ludii to GDL
    :param gameName: the name of game
    return string-based GDL
    '''
    context = ";" * 80 + "\n" + f";;; {gameName}\n" + ";" * 80 + "\n\n"
    return context


def translatePlayers(players):
    '''
    translate the players description from ludii to GDL
    :param players: a list that including the name of player
    return string-based GDL
    '''
    context = ";" * 80 + "\n" + ";; Roles\n" + ";" * 80 + "\n\n"
    #     for i in range(players):
    for var in players:
        context += f"(role {var})\n"
    context += "\n"
    return context


def translateMode(players):
    """
    translate the mode
    :param players: the list of player
    return string-based GDL that including the turn mode
    """
    context = ";" * 80 + "\n" + ";; Game Mode\n" + ";" * 80 + "\n\n"
    for i in range(len(players)):
        context += f"(<= (next (control {players[i]})) (true (control {players[(i + 1) % len(players)]})))\n"
    context += "\n"
    return context


def translateBoard(board, initPlayer):
    """
    translate the board description from ludii to GDL
    it contains init each cell and player
    :param board: the information of board
    :param initPlayer: the player will be controlled first
    return string-based GDL that including init cell & players
    """
    bType, bSize = board.split(" ")
    return BoardConvert(bType, int(bSize), initPlayer).convert()


def translatedEnd(endInfo, playersInfo):
    """
    translate the end description from ludii to GDL
    *keyword 'end' includes reward & terminal in GDL
    :param endInfo: end information
    :param playersInfo: players Information
    return string-based GDL that including reward & terminal
    """
    return Terminal(endInfo, playersInfo, None, None).convertEndInfo()


def translatedWinCondition(winCons, board):
    """
    translate the win-condition(Line) from Ludii to GDL
    :param winCons: end information
    :param board: board information
    """
    context = ";" * 80 + "\n" + ";; Win Condition\n" + ";" * 80 + "\n\n"

    for winCon in winCons:
        if "is Line" in winCon:
            context += Terminal(None, None, winCon, board).convertWinInfo(mode="Line")
    return context


def translatedLegalAction(players, board):
    """
      translate the legal action from Ludii to GDL
      :param players: players information
      :param board: board information
      return string-based GDL that including legal-action information
    """
    context = ";" * 80 + "\n" + ";; Legal Action\n" + ";" * 80 + "\n\n"
    if "square" in board:
        for i in range(len(players)):
            context += f"(<= (legal {players[(i + 1) % len(players)]} noop) (true (control {players[i]})))\n"
        context += "(<= (legal ?w (mark ?x ?y)) (true (cell ?x ?y b)) (true (control ?w)))\n\n"
    return context


def translatedMoveAndUpdate(players):
    """
    translate the move action from Ludii to GDL
    :param players: player information
    return string-based GDL that including move action and update action
    """
    context = ";" * 80 + "\n" + ";;  Move & Update\n" + ";" * 80 + "\n\n"
    for i in range(len(players)):
        context += f"(<= (next (cell ?m ?n {CT.CELL_MART[i]})) (does {players[i]} (mark ?m ?n)) (true (cell ?m ?n b)))\n"

    # update mark cell
    context += "(<= (next (cell ?m ?n ?w)) (true (cell ?m ?n ?w)) (distinct ?w b))\n"
    context += "(<= (next (cell ?m ?n b)) (does ?w (mark ?j ?k)) (true (cell ?m ?n b)) (or (distinct ?m ?j) (distinct ?n ?k)))\n\n"
    return context

