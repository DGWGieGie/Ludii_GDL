import Utils as ul
import re


class Translator:
    def __init__(self, fileName):
        self.info = ul.loadLudii("Ludii_File/"+fileName)
        self.players = self.extractPlayers()
        self.board = self.extractBoard()
        self.end = self.extractEnd()

    def extractPlayers(self):
        """
        extract players information
        """
        list_pl = []
        for var in self.info['equipment']:
            gName = re.search(".*(P\d*)", var)
            if gName:
                list_pl.append(gName.group(1))
        return list_pl

    def extractBoard(self):
        """
        extract board information
        """
        for var in self.info['equipment']:
            board = re.search("board \((.*)\){2}", var)
            if board:
                return board.group(1)

    def extractEnd(self):
        list_end = []
        for var in self.info['rules']:
            if "(end" in var:
                list_end.append(var)
        return list_end

    def translating(self, file_folder):
        with open(file_folder + self.info['game'] + '.gdl', 'w+') as fp:
            # translating game name
            fp.write(ul.translateGame(self.info['game']))

            # translating players
            fp.write(ul.translatePlayers(self.players))

            # translating game type
            # turn-based game
            fp.write(ul.translateMode(self.players))

            # translating board
            fp.write(ul.translateBoard(self.board, self.players[0]))

            # translating winCondition
            fp.write(ul.translatedWinCondition(self.end, self.board))

            # translating legal action
            fp.write(ul.translatedLegalAction(self.players, self.board))

            # translating move & update
            fp.write(ul.translatedMoveAndUpdate(self.players))

            # translating end (reward & terminal)
            fp.write(ul.translatedEnd(self.end, self.players))
        pass