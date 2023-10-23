from Clases.Token import Token
from Clases.Error import Error

class Léxico:
    def __init__(self):
        self.tokensTable = []
        self.mistakesTable = []
        self.row = 1
        self.column = 1
        self.temporary = ''
        self.state = 0
        self.mistakes = []
        self.symbols = [";", ",", "=", "{", "}", "[", "]", "(", ")"]
        self.reserved = ["CLAVES", "REGISTROS", "IMPRIMIR", "IMPRIMIRLN", "CONTEO", "PROMEDIO", "CONTARSI", "DATOS", "MAX", "MIN", "EXPORTARREPORTE", "SUMAR"]
        self.i = 0

    def addToken(self, character, token, row, column):
        self.tokensTable.append(Token(character, token, row, column))
        self. temporary = ''

    def addError(self, character, row, column):
        self.mistakesTable.append(Error('El carácter ' + character + ' no fue reconocido en el lenguaje.', row, column))
        self.temporary = ''
        self.mistakes.append(f"[ERROR LÉXICO] Caracter: '{character}' no fue reconocido en el lenguaje. Fila: '{row}', Columna: '{column}'")

    def identifySymbol(self, character):
        if character == ';':
            self.addToken(str(character), "Punto y coma", self.row, self.column)
        elif character == ',':
            self.addToken(str(character), "Coma", self.row, self.column)
        elif character == '=':
            self.addToken(str(character), "Igual", self.row, self.column)
        elif character == '{':
            self.addToken(str(character), "Llave de apertura", self.row, self.column)
        elif character == '}':
            self.addToken(str(character), "Llave de cierre", self.row, self.column)
        elif character == '[':
            self.addToken(str(character), "Corchete de apertura", self.row, self.column)
        elif character == ']':
            self.addToken(str(character), "Corchete de cierre", self.row, self.column)
        elif character == '(':
            self.addToken(str(character), "Paréntesis de apertura", self.row, self.column)
        elif character == ')':
            self.addToken(str(character), "Paréntesis de cierre", self.row, self.column)

        self.temporary = ''
        self.column += 1

    def identifyReserved(self):
        if self.temporary.upper() in self.reserved:
            return True
        else:
            return False
        
    def analyzer(self, cadena):
        self.tokensTable = []
        self.mistakesTable = []
        self.i = 0

        while self.i < len(cadena):
            if self.state == 0:
                if cadena[self.i].isalpha():
                    self.temporary += cadena[self.i]
                    self.column += 1
                    self.state = 1
                
                elif cadena[self.i].isdigit():
                    self.temporary += cadena[self.i]
                    self.column += 1
                    self.state = 2

                elif cadena[self.i] in self.symbols:
                    self.identifySymbol(cadena[self.i])
                
                elif cadena[self.i] == '"':
                    self.temporary += cadena[self.i]
                    self.column += 1
                    self.state = 5

                elif cadena[self.i] == '#':
                    self.temporary += cadena[self.i]
                    self.column += 1
                    self.state = 7

                elif cadena[self.i] == "'":
                    self.temporary += cadena[self.i]
                    self.column += 1
                    self.state = 9
                
                elif cadena[self.i] == '\n':
                    self.row += 1
                    self.column = 1

                elif cadena[self.i] in ['\t', ' ']:
                    self.column += 1

                elif cadena[self.i] == '\r':
                    pass

                else:
                    self.temporary += cadena[self.i]
                    self.addError(self.temporary, self.row, self.column)
                    self.column += 1

            elif self.state == 1:
                if cadena[self.i].isalpha():
                    self.temporary += cadena[self.i]
                    self.column += 1
                else:
                    if self.identifyReserved():
                        self.addToken(self.temporary.strip(), self.temporary.strip(), self.row, self.column)
                        self.state = 0
                        self.column += 1
                        self.i -=1
                    else:
                        self.addError(self.temporary, self.row, self.column)
                        self.state = 0
                        self.column += 1
                        self.i -= 1

            elif self.state == 2:
                if cadena[self.i].isdigit():
                    self.temporary += cadena[self.i]
                    self.column += 1

                elif cadena[self.i] == ".":
                    self.temporary += cadena[self.i]
                    self.column += 1
                    self.state = 3

                else:
                    self.addToken(self.temporary, 'Entero', self.row, self.column)
                    self.state = 0
                    self.column += 1
                    self.i -= 1

            elif self.state == 3:
                if cadena[self.i].isdigit():
                    self.temporary += cadena[self.i]
                    self.column += 1
                else:
                    self.addToken(self.temporary, 'Decimal', self.row, self.column)
                    self.state = 0
                    self.column += 1
                    self.i -= 1
            
            elif self.state == 5:
                if cadena[self.i] != "\"":
                    self.temporary += cadena[self.i]
                    self.column += 1
                else:
                    self.temporary += cadena[self.i]
                    self.addToken(self.temporary, "Cadena", self.row, self.column)
                    self.state = 0
                    self.column += 1

            elif self.state == 7:
                if cadena[self.i] == '\n':
                    self.state = 0
                    self.row += 1
                    self.column = 1
                else:
                    self.column += 1

            elif self.state == 9:
                if cadena[self.i] == "'":
                    self.temporary += cadena[self.i]
                    self.state = 10
                    self.column += 1
                else:
                    self.addError(self.temporary, self.row, self.column)
                    self.state = 0
                    self.column += 1
                    self.i -= 1

            elif self.state == 10:
                if cadena[self.i] == "'":
                    self.temporary += cadena[self.i]
                    self.state = 11
                    self.column += 1
                else:
                    self.addError(self.temporary, self.row, self.column)
                    self.state = 0
                    self.column += 1
                    self.i -= 1
            
            elif self.state == 11:
                if cadena[self.i] == "'":
                    self.temporary += cadena[self.i]
                    self.state = 12
                    self.column += 1
                elif cadena[self.i] == '\n':
                    self.temporary += cadena[self.i]
                    self.row += 1
                    self.column = 1
                else:
                    self.temporary += cadena[self.i]
                    self.column += 1
            
            elif self.state == 12:
                if cadena[self.i] == "'":
                    self.temporary += cadena[self.i]
                    self.state = 13
                    self.column += 1
                else:
                    self.addError(self.temporary, self.row, self.column)
                    self.state = 0
                    self.column += 1
                    self.i -= 1

            elif self.state == 13:
                if cadena[self.i] == "'":
                    self.temporary = ""
                    self.state = 0
                    self.column += 1
                else:
                    self.addError(self.temporary, self.row, self.column)
                    self.state = 0
                    self.column += 1
                    self.i -= 1

            self.i += 1
        return self.tokensTable, self.mistakes
