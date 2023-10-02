class Error:
    def __init__(self, description, row, column):
        self.description = description
        self.row = row
        self.column = column
        
    def print(self):
        print(self.description, self.column, self.row)

    def sent(self):
        return [self.description, self.column, self.row]