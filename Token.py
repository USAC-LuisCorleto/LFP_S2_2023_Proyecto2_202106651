class Token:
    def __init__(self, lexeme, type, row, column):
        self.lexeme = lexeme
        self.type = type
        self.row = row
        self.column = column
    
    def print(self):
        print("{:<15} {:<15} {:<5} {:<5}".format(self.lexeme, self.type, self.row, self.column))