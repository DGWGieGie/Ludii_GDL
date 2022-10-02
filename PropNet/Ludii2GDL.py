from Ludii_Keyword import Rules as RL
from Ludii_Keyword import Players as PL
from Ludii_Keyword import Game as GM
from Ludii_Keyword import Equipment as EQ
import ReadFile as RF

"""
class Ludii2GDLTranslation
 translate the Ludii to GDL and write into file
"""
class Ludii2GDLTranslation:
    def __init__(self, filename):
        self.filename = filename
        self.ludii = RF.ReadFile(filename).GameInfo

    def convert2GDL(self):
        game_info = GM.Game(self.ludii['name'])
        players_info = PL.Players(self.ludii['players'])
        equipment_info = EQ.Equipment(self.ludii['equipment'])
        rules_info = RL.Rules(self.ludii['rules'], players_info.num_pl, equipment_info.size_board,
                           equipment_info.type_board)

        self.getGDLFile(game_info.gdl, players_info.gdl, equipment_info.gdl, rules_info.gdl)
        print("translate completed")

    def getGDLFile(self, game_gdl, players_gdl, equipment_gdl, rules_gdl):
        with open(self.filename.replace(".lud", ".gdl"), 'w+') as fp:
            fp.write(game_gdl)
            fp.write(players_gdl)
            fp.write(equipment_gdl)
            fp.write(rules_gdl)
