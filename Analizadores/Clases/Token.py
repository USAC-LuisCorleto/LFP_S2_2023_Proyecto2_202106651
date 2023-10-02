class Token:
    def __init__(self, lexeme, type, row, column):
        self.lexeme = lexeme
        self.type = type
        self.row = row
        self.column = column
        
    def print(self):
        print("{:<35} {:<35} {:<30} {:<25}".format(self.lexeme, self.type, self.row, self.column))

    def sent(self):
        return [self.lexeme, self.type, self.row, self.column]