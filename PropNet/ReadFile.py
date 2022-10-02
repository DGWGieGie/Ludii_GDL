"""
class ReadFile
  process the ludii file and format it
"""


class ReadFile:
    def __init__(self, filename):
        self.GameInfo = self.loadLudii(filename)

    """
    load ludii information
    """
    def loadLudii(self, filename):
        flagE = True
        flagR = True
        flagP = True

        info_dict = {}
        for var in self.pre_Process(filename):
            if not flagE:
                info_dict['equipment'] = self.ProcessEquipment(var.strip())
                flagE = True

            if not flagR:
                if var == "(":
                    count_ru += 1
                elif var == ")":
                    count_ru -= 1

                if count_ru == 0 and len(string_ru) > 0:
                    list_ru.append(string_ru.strip() + ")")
                    string_ru = ""
                elif count_ru < 0:
                    info_dict['rules'] = list_ru
                    flagR = True
                else:
                    string_ru += var

            if not flagP:
                if var == "}":
                    info_dict["players"] = string_pl
                    flagP = True
                string_pl += var

            if var.strip() == 'rules':
                list_ru = []
                string_ru = ""
                flagR = False
                count_ru = 0
                pass

            if var.strip() == 'equipment':
                list_eq = []
                string_eq = ""
                count_eq = 0
                flagE = False

            elif flagE and flagR:
                if var == '(' or var == ')':
                    continue
                elif var[:4] == 'game':
                    info_dict["name"] = var.strip()[6:-1]
                elif var[:7] == 'players':
                    if var[8:] == "{":
                        string_pl = ""
                        flagP = False
                    else:
                        info_dict["players"] = var[8:]
        return info_dict

    """
    pre-process ludii information based on '(' & ')'
    """
    def pre_Process(self, filename):
        ludCon = self.readfile(filename)
        list_pre = []
        EQU = True
        stringV = ""
        for var in ludCon:
            if not EQU:
                if var == "{":
                    if count != 0:
                        stringV += var
                    count += 1

                elif var == "}":
                    count -= 1
                    if count != 0:
                        stringV += var

                elif count == 0:
                    list_pre.append(stringV)
                    stringV = ""
                    EQU = True
                else:
                    stringV += var
            else:
                if stringV.strip() == "equipment":
                    list_pre.append(stringV.strip())
                    stringV = ""
                    count = 0
                    EQU = False

                elif var == '(' and EQU:
                    if stringV != "":
                        list_pre.append(stringV)
                        stringV = ""
                    list_pre.append('(')

                elif var == ')' and EQU:
                    list_pre.append(stringV)
                    list_pre.append(")")
                    stringV = ""

                else:
                    stringV += var
        return list_pre

    """
    process 'equipment'(keyword)
    """
    def ProcessEquipment(self, var_eq):
        list_eq = []
        string_eq = ""
        count = 0

        for var in var_eq:
            string_eq += var
            if var == "(":
                count += 1
            elif var == ")":
                count -= 1

            if count == 0 and string_eq.strip() != "":
                list_eq.append(string_eq.strip())
                string_eq = ""
        return list_eq

    """
    read the ludii file
    """
    def readfile(self, fileName):
        '''
        read the file
        :param fileName: the name of file
        return the context of file
        '''
        with open(fileName) as fp:
            content = fp.read().split("\n")
            index = 0
            for i in range(len(content)):
                content[i] = content[i].strip()
                if "//----" in content[i]:
                    index = i
                    break
            return " ".join(content[:index])

