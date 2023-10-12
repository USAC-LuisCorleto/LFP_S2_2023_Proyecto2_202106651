class Error:
    def __init__(self, description, row, column):
        self.description = description
        self.row = row
        self.column = column
        
    def print(self):
        print("{:<50} {:<75} {:<55} {:<20}\n".format(self.description, self.column, self.row))

    def sent(self):
        return [self.description, self.column, self.row]