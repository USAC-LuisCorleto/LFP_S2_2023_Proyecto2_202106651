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
        self.reserved = ["Claves", "Registros", "imprimir", "imprimirln", "conteo", "promedio", "contarsi", "datos", "max", "min", "exportarReporte", "sumar"]

    def addToken(self, character, token, row, column):
        self.tokensTable.append(Token(character, token, row, column))
        self. temporary = ''

    def addError(self, character, row, column):
        self.mistakesTable.append(Error('El carácter ' + character + ' no fue reconocido en el lenguaje.', row, column))
        self.temporary = ''

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
            self.addToken(str(character), "Llav de cierre", self.row, self.column)
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
        if self.temporary in self.reserved:
            return True
        else:
            return False
        
    def analyzer(self, cadena):
        self.tokensTable = []
        self.mistakesTable = []
        i = 0

        while i < len(cadena):
            if self.state == 0:
                if cadena[i].isalpha():
                    self.temporary += cadena[i]
                    self.column += 1
                    self.state = 1
                
                elif cadena[i].isdigit():
                    self.temporary += cadena[i]
                    self.column += 1
                    self.state = 2

                elif cadena[i] in self.symbols:
                    self.identifySymbol(cadena[i])
                
                elif cadena[i] == '"':
                    self.temporary += cadena[i]
                    self.column += 1
                    self.state = 5

                elif cadena[i] == '#':
                    self.column += 1
                    self.state = 7

                elif cadena[i] == "'":
                    self.temporary += cadena[i]
                    self.column += 1
                    self.state = 9
                
                elif cadena[i] == '\n':
                    self.row += 1
                    self.column = 1

                elif cadena[i] == '\r':
                    pass

                else:
                    self.temporary += cadena[i]
                    self.addError(self.temporary, self.row, self.column)
                    self.column += 1
            elif self.state == 1:
                if cadena[i].isalpha():
                    self.temporary += cadena[i]
                    self.column += 1
                else:
                    if self.identifyReserved():
                        self.addToken(self.temporary.strip(), f"Instrucción - {self.temporary.strip()}", self.row, self.column)
                        self.state = 0
                        self.column += 1
                        i -=1
                    else:
                        self.addError(self.temporary, self.row, self.column)
                        self.state = 0
                        self.column += 1
                        i -= 1

            elif self.state == 2:
                if cadena[i].isdigit():
                    self.temporary += cadena[i]
                    self.column += 1

                elif cadena[i] == ".":
                    self.temporary += cadena[i]
                    self.column += 1
                    self.state = 3

                else:
                    self.addToken(self.temporary, 'Entero', self.row, self.column)
                    self.state = 0
                    self.column += 1
                    i -= 1

            elif self.state == 3:
                if cadena[i].isdigit():
                    self.temporary += cadena[i]
                    self.column += 1
                else:
                    self.addToken(self.temporary, 'Decimal', self.row, self.column)
                    self.state = 0
                    self.column += 1
                    i -= 1
            
            elif self.state == 5:
                if cadena[i] != "\"":
                    self.temporary += cadena[i]
                    self.column += 1
                else:
                    self.temporary += cadena[i]
                    self.addToken(self.temporary, "Cadena", self.row, self.column)
                    self.state = 0
                    self.column += 1

            elif self.state == 7:
                if cadena[i] == '\n':
                    self.state = 0
                    self.row += 1
                    self.column = 1
                else:
                    self.column += 1

            elif self.state == 9:
                if cadena[i] == "'":
                    self.temporary += cadena[i]
                    self.state = 10
                    self.column += 1
                else:
                    self.addError(self.temporary, self.row, self.column)
                    self.state = 0
                    self.column += 1
                    i -= 1

            elif self.state == 10:
                if cadena[i] == "'":
                    self.temporary += cadena[i]
                    self.state = 11
                    self.column += 1
                else:
                    self.addError(self.temporary, self.row, self.column)
                    self.state = 0
                    self.column += 1
                    i -= 1
            
            elif self.state == 11:
                if cadena[i] == "'":
                    self.temporary += cadena[i]
                    self.state = 12
                    self.column += 1
                elif cadena[i] == '\n':
                    self.temporary += cadena[i]
                    self.row += 1
                    self.column = 1
                else:
                    self.temporary += cadena[i]
                    self.column += 1
            
            elif self.state == 12:
                if cadena[i] == "'":
                    self.temporary += cadena[i]
                    self.state = 13
                    self.column += 1
                else:
                    self.addError(self.temporary, self.row, self.column)
                    self.state = 0
                    self.column += 1
                    i -= 1

            elif self.state == 13:
                if cadena[i] == "'":
                    self.temporary = ""
                    self.state = 0
                    self.column += 1
                else:
                    self.addError(self.temporary, self.row, self.column)
                    self.state = 0
                    self.column += 1
                    i -= 1

            i += 1
        res = [self.tokensTable, self.mistakesTable]
        return res
    
    def printTokens(self):
        print("Tokens:")
        print("{:<35} {:<35} {:<30} {:<25}".format("Lexema", "Tipo", "Fila", "Columna"))
        print("-" * 100)
        for token in self.tokensTable:
            token.print()

autom = Léxico()
with open('Prueba.bizdata', 'r') as archivo:
    contenido = archivo.read()
autom.analyzer(contenido)
autom.printTokens()
