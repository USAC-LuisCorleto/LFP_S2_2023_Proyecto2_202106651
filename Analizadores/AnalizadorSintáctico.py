from graphviz import Digraph
from Instrucciones.ContarSi import ContarSi
from Instrucciones.Max import Max
from Instrucciones.Min import Min
from Instrucciones.Promedio import Promedio
from Instrucciones.Suma import Suma
from Reportes.ReporteHTML import reportHtml
from texttable import Texttable
import uuid, copy

class Sintáctico:
    def __init__(self, tokens = [], mistakes = []):
        self.mistakes = mistakes
        self.tokens = tokens
        self.tokens.reverse()
        self.reserved = ["CLAVES", "REGISTROS", "IMPRIMIR", "IMPRIMIRLN", "CONTEO", "PROMEDIO", "CONTARSI", "DATOS", "MAX", "MIN", "EXPORTARREPORTE", "SUMAR", "PUNTO Y COMA"]
        self.vector = []
        self.keys = []
        self.functionContarSi = ContarSi()
        self.functionMax = Max()
        self.functionMin = Min()
        self.functionPromedio = Promedio()
        self.functionSuma = Suma()
        self.reportHTML = reportHtml()
        self.temporary = ""
        self.graph = Digraph('Arbol de derivación', format='png')
        self.graph.attr(bgcolor='white', fontname='Helvetica', fontsize='12', rankdir='TB')
        self.graph.attr('node', shape='rectangle', style='filled', color='lightgray', fontcolor='black')
        self.start = ""
        self.nodeInstruction = ""

    def createNode(self, tag:str) -> str:
        id = str(uuid.uuid1())
        self.graph.node(id, tag, color='gray')
        return id
    
    def addNodeC(self, parentNode, childNode:str):
        self.graph.edge(parentNode, childNode, color='black')

    def addError(self, obtained, expected, row, column):
        self.mistakes.append(f"[ERROR SINTÁCTICO] Encontrado: '{obtained}', Se esperaba: '{expected}'. Fila: {row}, Columna: {column}")
        temp = self.tokens[-1]
        while temp.type.upper() not in self.reserved:
            temp = self.tokens.pop()

    def analyze(self):
        self.startAn()
        return(self.temporary, self.mistakes, self.graph)
    
    def startAn(self):
        self.start = self.createNode('Inicio')
        self.nodeInstruction = self.createNode('Instrucción')
        self.instructionsAn()

    def instructionsAn(self):
        instrucciones = self.createNode('Instrucciones')
        self.addNodeC(self.start, instrucciones)
        self.start = instrucciones
        self.addNodeC(self.start, self.nodeInstruction)

        self.instructionAn()
        self.instructionsAn2()

    def instructionsAn2(self):
        try:
            temp = self.tokens[-1]
            if temp.type.upper() in self.reserved:
                self.instructionAn()
                self.instructionsAn2()
            else:
                self.addError(temp.type, "Instrucción", temp.row, temp.column)
                self.instructionAn()
                self.instructionsAn2()
        except IndexError:
            pass
        except Exception:
            pass

    def instructionAn(self):
        try:
            temp = self.tokens[-1]
            if temp.type == 'imprimir':
                self.printAn()
            elif temp.type == 'imprimirln':
                self.printlnAn()
            elif temp.type == 'Claves':
                self.keysAn()
            elif temp.type == 'Registros':
                self.recordsAn()
            elif temp.type == 'conteo':
                self.countingAn()
            elif temp.type == 'promedio':
                self.averageAn()
            elif temp.type == 'contarsi':
                self.contarsiAn()
            elif temp.type == 'datos':
                self.dataAn()
            elif temp.type == 'sumar':
                self.sumarAn()
            elif temp.type == 'max':
                self.maxAn()
            elif temp.type == 'min':
                self.minAn()
            elif temp.type == 'exportarReporte':
                self.reportAn()
            else:
                pass
        except IndexError:
            pass
        except Exception:
            pass
    
    def printAn(self):
        temp = self.tokens.pop()
        if temp.type != "imprimir":
            self.tokens.append(temp)
            self.addError(temp.type, "imprimir", temp.row, temp.column)
            return

        printNd = temp.lexeme
        temp = self.tokens.pop()
        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
            return

        temp = self.tokens.pop()
        if temp.type != "Cadena":
            self.tokens.append(temp)
            self.addError(temp.type, "Cadena", temp.row, temp.column)
            return

        cadena = temp.lexeme.replace('"', '')
        self.temporary += cadena
        cadenaLx = temp.lexeme

        temp = self.tokens.pop()
        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        temp = self.tokens.pop()
        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        node0 = self.createNode('imprimir')
        node10 = self.createNode(printNd)
        self.addNodeC(node0, node10)
        node1 = self.createNode('Paréntesis de apertura')
        node2 = self.createNode('(')
        self.addNodeC(node1, node2)
        node3 = self.createNode('Cadena')
        node4 = self.createNode(cadenaLx)
        self.addNodeC(node3, node4)
        node5 = self.createNode('Paréntesis de cierre')
        node6 = self.createNode(')')
        self.addNodeC(node5, node6)
        node7 = self.createNode('Punto y coma')
        node8 = self.createNode(temp.lexeme)
        self.addNodeC(node7, node8)
        node9 = self.createNode(f'[INSTRUCCIÓN] - imprimir("{cadenaLx}")')
        self.addNodeC(node9, node0)
        self.addNodeC(node9, node1)
        self.addNodeC(node9, node3)
        self.addNodeC(node9, node5)
        self.addNodeC(node9, node7)
        self.addNodeC(self.nodeInstruction, node9)

    def printlnAn(self):
        cadena = None
        temp = self.tokens.pop()

        if temp.type != "imprimirln":
            self.tokens.append(temp)
            self.addError(temp.type, "imprimirln", temp.row, temp.column)
            return

        printNd = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
            return

        parentesisAp = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Cadena":
            self.tokens.append(temp)
            self.addError(temp.type, "Cadena", temp.row, temp.column)
            return

        cadenaLx = copy.deepcopy(temp.lexeme)
        cadena = temp.lexeme
        cadena = cadena.replace('"', '')
        self.temporary += "\n" + cadena
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        parentesisCi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        node0 = self.createNode('imprimirln')
        node2 = self.createNode(printNd)
        self.addNodeC(node0, node2)
        node3 = self.createNode('Paréntesis de apertura')
        node4 = self.createNode(parentesisAp)
        self.addNodeC(node3, node4)
        node5 = self.createNode('Cadena')
        node6 = self.createNode(cadenaLx)
        self.addNodeC(node5, node6)
        node7 = self.createNode('Paréntesis de cierre')
        node8 = self.createNode(parentesisCi)
        self.addNodeC(node7, node8)
        node9 = self.createNode('Punto y coma')
        node10 = self.createNode(temp.lexeme)
        self.addNodeC(node9, node10)
        node11 = self.createNode(f'[INSTRUCCIÓN] - imprimirln("{cadenaLx}")')
        self.addNodeC(node11, node0)
        self.addNodeC(node11, node3)
        self.addNodeC(node11, node5)
        self.addNodeC(node11, node7)
        self.addNodeC(node11, node9)
        self.addNodeC(self.nodeInstruction, node11)

    def keysAn(self):
        rowTemp = []
        temp = self.tokens.pop()

        if temp.type != "Claves":
            self.tokens.append(temp)
            self.addError(temp.type, "Error", temp.row, temp.column)
            return

        node0 = self.createNode('[INSTRUCCIÓN] - Claves[]')
        node1 = self.createNode(temp.lexeme)
        node11 = self.createNode('Claves')
        self.addNodeC(node0, node11)
        self.addNodeC(self.nodeInstruction, node0)
        self.addNodeC(node11, node1)  

        temp = self.tokens.pop()
        if temp.type != "Igual":
            self.tokens.append(temp)
            self.addError(temp.type, "Igual", temp.row, temp.column)
            return

        node2 = self.createNode('Igual')
        node3 = self.createNode(temp.lexeme)
        self.addNodeC(node2, node3)
        self.addNodeC(node0, node2) 

        temp = self.tokens.pop()
        if temp.type != "Corchete de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Corchete de apertura", temp.row, temp.column)
            return

        node4 = self.createNode('Corchete de apertura')
        node5 = self.createNode(temp.lexeme)
        
        self.addNodeC(node4, node5)
        self.addNodeC(node0, node4)  

        while True:
            temp = self.tokens.pop()
            if temp.type == "Cadena":
                cadena = temp.lexeme.replace('"', '')
                rowTemp.append(cadena)

                node8 = self.createNode('Cadena')
                node12 = self.createNode('Coma')
                node7 = self.createNode(cadena)
                node13 = self.createNode(',')
                self.addNodeC(node0, node8)
                self.addNodeC(node0, node12)
                self.addNodeC(node8, node7)
                self.addNodeC(node12, node13)

                temp = self.tokens.pop()
                if temp.type == "Corchete de cierre":
                    node9 = self.createNode('Corchete de cierre')
                    node10 = self.createNode(temp.lexeme)
                    break
                elif temp.type != "Coma":
                    self.tokens.append(temp)
                    self.addError(temp.type, "Coma - Corchete de cierre", temp.row, temp.column)
                    break
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Cadena", temp.row, temp.column)
                break

        self.addNodeC(node0, node9)
        self.addNodeC(node9, node10)
        self.keys = rowTemp

    def recordsAn(self):
        temp = self.tokens.pop()

        if temp.type != "Registros":
            self.tokens.append(temp)
            self.addError(temp.type, "Registros", temp.row, temp.column)
            return

        temp = self.tokens.pop()
        if temp.type != "Igual":
            self.tokens.append(temp)
            self.addError(temp.type, "Igual", temp.row, temp.column)
            return

        temp = self.tokens.pop()
        if temp.type != "Corchete de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Corchete de apertura", temp.row, temp.column)
            return

        while True:
            temp = self.tokens.pop()
            if temp.type == "Llave de apertura":
                rowTemp = []
                fin = False
                while fin is False:
                    temp = self.tokens.pop()

                    if temp.type == "Cadena" or temp.type == "Decimal" or temp.type == "Entero":
                        cadena = temp.lexeme
                        cadena = cadena.replace('"', '')
                        rowTemp.append(cadena)

                        temp = self.tokens.pop()

                        if temp.type == "Coma":
                            continue
                        elif temp.type == "Llave de cierre":
                            fin = True
                        else:
                            self.tokens.append(temp)
                            self.addError(temp.type, "Coma - Llave de cierre", temp.row, temp.column)
                            break
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Cadena", temp.row, temp.column)
                        break
                self.vector.append(rowTemp)

            elif temp.type == "Corchete de cierre":
                break
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Llave de apertura - Corchete de cierre", temp.row, temp.column)
                break

        if temp.type != "Corchete de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Corchete de cierre", temp.row, temp.column)
            return

    def countingAn(self):
        temp = self.tokens.pop()

        if temp.type != "conteo":
            self.tokens.append(temp)
            self.addError(temp.type, "conteo", temp.row, temp.column)
            return

        count = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
            return

        parentesisAp = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        parentesisCi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        rows = len(self.vector)
        columns = len(self.vector[0])
        count = int(rows) * int(columns)

        self.temporary += "\nconteo()"
        self.temporary += "\n>>> " + str(count)

        node0 = self.createNode('conteo')
        node1 = self.createNode(str(count))
        node2 = self.createNode('Paréntesis de apertura')
        node3 = self.createNode(parentesisAp)
        node4 = self.createNode('Paréntesis de cierre')
        node5 = self.createNode(parentesisCi)
        node7 = self.createNode('Punto y coma')
        node8 = self.createNode(temp.lexeme)
        node9 = self.createNode(f'[INSTRUCCIÓN] - conteo())')

        self.addNodeC(node0, node1)
        self.addNodeC(node2, node3)
        self.addNodeC(node4, node5)
        self.addNodeC(node7, node8)
        self.addNodeC(node9, node0)
        self.addNodeC(node9, node2)
        self.addNodeC(node9, node4)
        self.addNodeC(node9, node7)
        self.addNodeC(self.nodeInstruction, node9)

    def averageAn(self):
        cadena = None
        temp = self.tokens.pop()

        if temp.type != "promedio":
            self.tokens.append(temp)
            self.addError(temp.type, "promedio", temp.row, temp.column)
            return

        average = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
            return

        parentesisAp = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Cadena":
            self.tokens.append(temp)
            self.addError(temp.type, "Cadena", temp.row, temp.column)
            return

        cadenaLx = temp.lexeme
        cadena = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        parentesisCi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        res = self.functionPromedio.promedio(self.vector, self.keys, cadena)
        if res is None:
            print("Error")
        else:
            self.temporary += "\npromedio (" + cadenaLx + ")"
            self.temporary += "\n>>> " + res

            node0 = self.createNode('promedio')
            node1 = self.createNode(average)
            self.addNodeC(node0, node1)

            node2 = self.createNode('Paréntesis de apertura')
            node3 = self.createNode(parentesisAp)
            self.addNodeC(node2, node3)

            node4 = self.createNode('Cadena')
            node5 = self.createNode(cadenaLx)
            self.addNodeC(node4, node5)

            node6 = self.createNode('Paréntesis de cierre')
            node7 = self.createNode(parentesisCi)
            self.addNodeC(node6, node7)

            node8 = self.createNode('Punto y coma')
            node9 = self.createNode(temp.lexeme)
            self.addNodeC(node8, node9)

            node10 = self.createNode(f'[INSTRUCCIÓN] - promedio({cadenaLx})')
            self.addNodeC(node10, node0)
            self.addNodeC(node10, node2)
            self.addNodeC(node10, node4)
            self.addNodeC(node10, node6)
            self.addNodeC(node10, node8)
            self.addNodeC(self.nodeInstruction, node10)

    def contarsiAn(self):
        field = None
        value = None
        temp = self.tokens.pop()

        if temp.type != "contarsi":
            self.tokens.append(temp)
            self.addError(temp.type, "contarsi", temp.row, temp.column)
            return

        contarsi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
            return

        parentesisAp = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Cadena":
            self.tokens.append(temp)
            self.addError(temp.type, "Cadena", temp.row, temp.column)
            return

        cadena1 = temp.lexeme
        field = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Coma", temp.row, temp.column)
            return

        comma = temp.lexeme
        temp = self.tokens.pop()                         

        if temp.type not in ["Cadena", "Decimal", "Entero"]:
            self.tokens.append(temp)
            self.addError(temp.type, "Cadena - Decimal - Entero", temp.row, temp.column)
            return

        value = temp.lexeme
        cadena2 = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        parentesisCi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        res = self.functionContarSi.contarSi(self.vector, self.keys, field, value)
        if res is None:
            print("Error en contarSi")
        else:
            self.temporary += "\ncontarsi(" + cadena1 + "," + cadena2 + ")"
            self.temporary += "\n>>> " + res
            node0 = self.createNode('contarsi')
            node1 = self.createNode(contarsi)
            self.addNodeC(node0, node1)
            node2 = self.createNode('Paréntesis de apertura')
            node3 = self.createNode(parentesisAp)
            self.addNodeC(node2, node3)
            node4 = self.createNode('Cadena')
            node5 = self.createNode(cadena1)
            self.addNodeC(node4, node5)
            node6 = self.createNode('Coma')
            node7 = self.createNode(comma)
            self.addNodeC(node6, node7)
            node8 = self.createNode('Cadena')
            node9 = self.createNode(cadena2)
            self.addNodeC(node8, node9)
            node10 = self.createNode('Paréntesis de cierre')
            node11 = self.createNode(parentesisCi)
            self.addNodeC(node10, node11)
            node12 = self.createNode('Punto y coma')
            node13 = self.createNode(temp.lexeme)
            self.addNodeC(node12, node13)
            node14 = self.createNode(f'[INSTRUCCIÓN] - contarsi({cadena1}, {cadena2})')
            self.addNodeC(node14, node0)
            self.addNodeC(node14, node2)
            self.addNodeC(node14, node4)
            self.addNodeC(node14, node6)
            self.addNodeC(node14, node8)
            self.addNodeC(node14, node10)
            self.addNodeC(node14, node12)
            self.addNodeC(self.nodeInstruction, node14)

    def dataAn(self):
        temp = self.tokens.pop()

        if temp.type != "datos":
            self.tokens.append(temp)
            self.addError(temp.type, "datos", temp.row, temp.column)
            return

        data = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Parénteisis de apertura", temp.row, temp.column)
            return

        parentesisAp = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        parentesisCi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        self.impTabla()

        node0 = self.createNode('datos')
        node1 = self.createNode(data)
        node2 = self.createNode('Paréntesis de apertura')
        node3 = self.createNode(parentesisAp)
        node4 = self.createNode('Paréntesis de cierre')
        node5 = self.createNode(parentesisCi)
        node6 = self.createNode('Punto y coma')
        node7 = self.createNode(temp.lexeme)
        node8 = self.createNode(f'[INSTRUCCIÓN] - datos()')

        self.addNodeC(node0, node1)
        self.addNodeC(node2, node3)
        self.addNodeC(node4, node5)
        self.addNodeC(node6, node7)
        self.addNodeC(node8, node0)
        self.addNodeC(node8, node2)
        self.addNodeC(node8, node4)
        self.addNodeC(node8, node6)
        self.addNodeC(self.nodeInstruction, node8)

    def sumarAn(self):
        cadena = None
        temp = self.tokens.pop()

        if temp.type != "sumar":
            self.tokens.append(temp)
            self.addError(temp.type, "sumar", temp.row, temp.column)
            return

        sum = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
            return

        parentesisAp = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Cadena":
            self.tokens.append(temp)
            self.addError(temp.type, "Cadena", temp.row, temp.column)
            return

        cadenaLx = temp.lexeme
        cadena = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        parentesisCi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        res = self.functionSuma.sumar(self.vector, self.keys, cadena)

        if res is None:
            print("Error en suma")
        else:
            self.temporary += "\nsumar (" + cadenaLx + ")"
            self.temporary += "\n>>> " + res

            node0 = self.createNode('sumar')
            node1 = self.createNode(sum)
            node2 = self.createNode('Paréntesis de apertura')
            node3 = self.createNode(parentesisAp)
            node4 = self.createNode('Cadena')
            node5 = self.createNode(cadenaLx)
            node6 = self.createNode('Paréntesis de cierre')
            node7 = self.createNode(parentesisCi)
            node8 = self.createNode('Punto y coma')
            node9 = self.createNode(temp.lexeme)
            node10 = self.createNode(f'[INSTRUCCIÓN] - sumar({cadenaLx})')

            self.addNodeC(node0, node1)
            self.addNodeC(node2, node3)
            self.addNodeC(node4, node5)
            self.addNodeC(node6, node7)
            self.addNodeC(node8, node9)
            self.addNodeC(node10, node0)
            self.addNodeC(node10, node2)
            self.addNodeC(node10, node4)
            self.addNodeC(node10, node6)
            self.addNodeC(node10, node8)
            self.addNodeC(self.nodeInstruction, node10)
    
    def maxAn(self):
        cadena = None
        temp = self.tokens.pop()

        if temp.type != "max":
            self.tokens.append(temp)
            self.addError(temp.type, "max", temp.row, temp.column)
            return

        maximum = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
            return

        parentesisAp = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Cadena":
            self.tokens.append(temp)
            self.addError(temp.type, "Cadena", temp.row, temp.column)
            return

        cadenaLx = temp.lexeme
        cadena = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        parentesisCi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        res = self.functionMax.max(self.vector, self.keys, cadena)
        if res is None:
            print("Error en max")
        else:
            self.temporary += "\nmax (" + cadenaLx + ")"
            self.temporary += "\n>>> " + res
            node0 = self.createNode('max')
            node1 = self.createNode(maximum)
            self.addNodeC(node0, node1)
            node2 = self.createNode('Paréntesis de apertura')
            node3 = self.createNode(parentesisAp)
            self.addNodeC(node2, node3)
            node4 = self.createNode('Cadena')
            node5 = self.createNode(cadenaLx)
            self.addNodeC(node4, node5)
            node6 = self.createNode('Paréntesis de cierre')
            node7 = self.createNode(parentesisCi)
            self.addNodeC(node6, node7)
            node8 = self.createNode('Punto y coma')
            node9 = self.createNode(temp.lexeme)
            self.addNodeC(node8, node9)
            node10 = self.createNode(f'[INSTRUCCIÓN] - max({cadenaLx})')
            self.addNodeC(node10, node0)
            self.addNodeC(node10, node2)
            self.addNodeC(node10, node4)
            self.addNodeC(node10, node6)
            self.addNodeC(node10, node8)
            self.addNodeC(self.nodeInstruction, node10)

    def minAn(self):
        cadena = None
        temp = self.tokens.pop()
        if temp.type != "min":
            self.tokens.append(temp)
            self.addError(temp.type, "min", temp.row, temp.column)
            return

        minimum = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
            return

        parentesisAp = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Cadena":
            self.tokens.append(temp)
            self.addError(temp.type, "Cadena", temp.row, temp.column)
            return

        cadenaLx = temp.lexeme
        cadena = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        parentesisCi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        res = self.functionMin.min(self.vector, self.keys, cadena)
        if res is None:
            print("Error en min")
        else:
            self.temporary += "\nmin (" + cadenaLx + ")"
            self.temporary += "\n>>> " + res
            node0 = self.createNode('min')
            node1 = self.createNode(minimum)
            self.addNodeC(node0, node1)
            node2 = self.createNode('Paréntesis de apertura')
            node3 = self.createNode(parentesisAp)
            self.addNodeC(node2, node3)
            node4 = self.createNode('Cadena')
            node5 = self.createNode(cadenaLx)
            self.addNodeC(node4, node5)
            node6 = self.createNode('Paréntesis de cierre')
            node7 = self.createNode(parentesisCi)
            self.addNodeC(node6, node7)
            node8 = self.createNode('Punto y coma')
            node9 = self.createNode(temp.lexeme)
            self.addNodeC(node8, node9)
            node10 = self.createNode(f'[INSTRUCCIÓN] - min({cadenaLx})')
            self.addNodeC(node10, node0)
            self.addNodeC(node10, node2)
            self.addNodeC(node10, node4)
            self.addNodeC(node10, node6)
            self.addNodeC(node10, node8)
            self.addNodeC(self.nodeInstruction, node10)

    def reportAn(self):
        cadena = None
        temp = self.tokens.pop()

        if temp.type != "exportarReporte":
            self.tokens.append(temp)
            self.addError(temp.type, "exportarReporte", temp.row, temp.column)
            return

        report = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de apertura":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
            return

        parentesisAp = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Cadena":
            self.tokens.append(temp)
            self.addError(temp.type, "Cadena", temp.row, temp.column)
            return

        cadena = temp.lexeme
        cadenaLx = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Paréntesis de cierre":
            self.tokens.append(temp)
            self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            return

        parentesisCi = temp.lexeme
        temp = self.tokens.pop()

        if temp.type != "Punto y coma":
            self.tokens.append(temp)
            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
            return

        report = self.reportHTML.reportHTML(cadena, self.keys, self.vector)
        self.temporary += report
        node0 = self.createNode('exportarReporte')
        node1 = self.createNode(report)
        self.addNodeC(node0, node1)
        node2 = self.createNode('Paréntesis de apertura')
        node3 = self.createNode(parentesisAp)
        self.addNodeC(node2, node3)
        node4 = self.createNode('Cadena')
        node5 = self.createNode(cadenaLx)
        self.addNodeC(node4, node5)
        node6 = self.createNode('Paréntesis de cierre')
        node7 = self.createNode(parentesisCi)
        self.addNodeC(node6, node7)
        node8 = self.createNode('Punto y coma')
        node9 = self.createNode(temp.lexeme)
        self.addNodeC(node8, node9)
        node10 = self.createNode('[INSTRUCCIÓN] - exportarReporte()')
        self.addNodeC(node10, node0)
        self.addNodeC(node10, node2)
        self.addNodeC(node10, node4)
        self.addNodeC(node10, node6)
        self.addNodeC(node10, node8)
        self.addNodeC(self.nodeInstruction, node10)
    
    def impTabla(self):
        if len(self.keys) == 0 or len(self.vector) == 0:
            self.temporary += '\nNo hay valores en la tabla.\n'
        else:
            table = Texttable()
            table.header(self.keys)
            
            for row in self.vector:
                table.add_row(row)
            self.temporary += '\n' + table.draw() + '\n'
