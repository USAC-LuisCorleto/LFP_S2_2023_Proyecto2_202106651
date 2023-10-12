class Token:
    def __init__(self, lexeme, type, row, column):
        self.lexeme = lexeme
        self.type = type
        self.row = row
        self.column = column
        
    def print(self):
        print("{:<50} {:<75} {:<55} {:<20}\n".format(self.lexeme, self.type, self.row, self.column))

    def sent(self):
        return [self.lexeme, self.type, self.row, self.column]