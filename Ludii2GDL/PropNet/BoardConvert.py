class BoardConvert:
    def __init__(self, boardType, boardSize, initPlayer):
        self.boardType = boardType
        self.boardSize = boardSize
        self.initPlayer = initPlayer

    def convert(self):
        context = ";" * 80 + "\n" + ";; Initial State\n" + ";" * 80 + "\n\n"

        # translating square type
        if self.boardType == "square":
            for i in range(1, self.boardSize + 1):
                for j in range(1, self.boardSize + 1):
                    context += f"(init (cell {i} {j} b))\n"
            context += f"(init (control {self.initPlayer}))\n\n"
        return context
