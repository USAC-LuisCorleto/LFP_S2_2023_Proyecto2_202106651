from graphviz import Digraph
from Instrucciones.ContarSi import ContarSi
from Instrucciones.Max import Max
from Instrucciones.Min import Min
from Instrucciones.Promedio import Promedio
from Instrucciones.Suma import Suma
import uuid, copy

class Sintáctico:
    def __init__(self, tokens = [], mistakes = []):
        self.mistakes = mistakes
        self.tokens = tokens
        self.tokens.reverse()
        self.reserved = ["Claves", "Registros", "imprimir", "imprimirln", "conteo", "promedio", "contarsi", "datos", "max", "min", "exportarReporte", "sumar", "puntoycoma"]
        self.vector = []
        self.keys = []
        self.functionContarSi = ContarSi()
        self.functionMax = Max()
        self.functionMin = Min()
        self.functionPromedio = Promedio()
        self.functionSuma = Suma()
        self.temporary = ""
        self.graph = Digraph('Arbol', format='png')
        self.start = ""

    def createNode(self, tag:str) -> str:
        id = str(uuid.uuid1())
        self.graph.node(id,tag)
        return id
    
    def addNodeC(self, parentNode, childNode:str):
        self.graph.edge(parentNode, childNode)

    def addError(self, obtained, expected, row, column):
        self.mistakes.append(
            "<ERROR SINTACTICO> Se obtuvo {}, se esperaba {}. Fila: {}, Columna: {}".format(
                obtained,
                expected,
                row,
                column
            ) 
        )
        temp = self.tokens[-1]
        while temp.type.upper() not in self.reserved:
            temp = self.tokens.pop()

    def analyze(self):
        self.startAn()
        return(self.temporary, self.mistakes, self.graph)
    
    def startAn(self):
        self.start = self.createNode('startAn')
        self.instructionsAn()

    def instructionsAn(self):
        instruct = self.createNode('instructions')
        self.addNodeC(self.start, instruct)
        self.start = instruct
        self.instructionAn()
        self.instructionsAnode2()

    def instructionsAnode2(self):
        try:
            temp = self.tokens[-1]
            if temp.type.upper() in self.reserved:
                self.instructionAn()
                self.instructionsAnode2()
            else:
                self.addError(temp.type, "Instrucción", temp.row, temp.column)
                self.instructionAn()
                self.instructionsAnode2()
        except IndexError:
            pass
        except Exception as e:
            print("Error en instructionsAnode2")
            print(e)
            pass

    def instructionAn(self):
        try:
            temp = self.tokens[-1]
            if temp.type == 'imprimir':
                self.printAn()
            elif temp.tpye == 'imprimirln':
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
        except IndexError:
            pass
        except Exception as e:
            print("Error en instructionAn")
            print(e)
            pass
    
    def printAn(self):
        cadena = None
        temp = self.tokens.pop()
        if temp.tpye == "imprimir":
            printNd = temp.lexeme
            temp = self.tokens.pop()

            if temp.type == "Paréntesis de apertura":
                parentesisAp = temp.lexeme
                temp = self.tokens.pop()

                if temp.type == "Cadena":
                    cadena = copy.deepcopy(temp.lexeme)
                    cadena = cadena.replace('"', '')
                    self.temporary += cadena
                    cadenaLx = temp.lexeme
                    temp = self.tokens.pop()

                    if temp.type == "Paréntesis de cierre":
                        parentesisCi = temp.lexeme
                        temp = self.tokens.pop()

                        if temp.type == "Punto y coma":
                            nodeInstruction = self.createNode('Instrucción')
                            node0 = self.createNode('imprimir')
                            node10 = self.createNode(printNd)
                            self.addNodeC(node0, node10)
                            node1 = self.createNode('Paréntesis de apertura')
                            node2 = self.createNode(parentesisAp)
                            self.addNodeC(node1, node2)
                            node3 = self.createNode('Cadena')
                            node4 = self.createNode(cadenaLx)
                            self.addNodeC(node3, node4)
                            node5 = self.createNode('Paréntesis de cierre')
                            node6 = self.createNode(parentesisCi)
                            self.addNodeC(node5, node6)
                            node7 = self.createNode('Punto y coma')
                            node8 = self.createNode(temp.lexeme)
                            self.addNodeC(node7, node8)
                            node9 = self.createNode('Instrucción - imprimir')
                            self.addNodeC(node9, node0)
                            self.addNodeC(node9, node1)
                            self.addNodeC(node9, node3)
                            self.addNodeC(node9, node5)
                            self.addNodeC(node9, node7)
                            self.addNodeC(self.start, nodeInstruction)
                            self.addNodeC(nodeInstruction, node9)
                            self.start = nodeInstruction

                        else:
                            self.tokens.append(temp)
                            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Cadena", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
        else:
            self.tokens.append(temp)
            self.addError(temp.type, "imprimir", temp.row, temp.column)

    def printlnAn(self):
        cadena = None
        temp = self.tokens.pop()
        if temp.type == "imprimirln":
            printNd = temp.lexeme
            temp = self.tokens.pop()

            if temp.type == "Paréntesis de apertura":
                parentesisAp = temp.lexema
                temp = self.tokens.pop()

                if temp.type == "Cadena":
                    cadenaLx = copy.deepcopy(temp.lexeme)
                    cadena = temp.lexeme
                    cadena = cadena.replace('"', '')
                    self.temporary += "\n" + cadena
                    temp = self.tokens.pop

                    if temp.type == "Paréntesis de cierre":
                        parentesisCi = temp.lexeme
                        temp = self.tokens.pop()

                        if temp.type == "Punto y coma":
                            nodeInstruction = self.createNode('Instrucción')
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
                            node11 = self.createNode('Instrucción - imprimirln')
                            self.addNodeC(node11, node0)
                            self.addNodeC(node11, node3)
                            self.addNodeC(node11, node5)
                            self.addNodeC(node11, node7)
                            self.addNodeC(node11, node9)
                            self.addNodeC(self.start, nodeInstruction)
                            self.addNodeC(nodeInstruction, node11)
                            self.start = nodeInstruction
                        else:
                            self.tokens.append(temp)
                            self.addError(temp.tpye, "Punto y coma", temp.row, temp.column)
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Cadena", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
        else:
            self.tokens.append(temp)
            self.addError(temp.type, "imprimirln", temp.row, temp.column)

    def keysAn(self):
        rowTemp = []
        temp = self.tokens.pop()
        
        if temp.type == "Claves":
            temp = self.tokens.pop()
            
            if temp.type == "Igual":
                temp = self.tokens.pop()

                if temp.type == "Corchete de apertura":
                    finish = False
                    while finish is False:
                        temp = self.tokens.pop()

                        if temp.type == "Cadena":
                            cadena = temp.lexeme
                            cadena = cadena.replace('"', '')
                            rowTemp.append(cadena)
                            temp = self.tokens.pop()

                            if temp.type == "Coma":
                                continue
                            elif temp.type == "Corchete de cierre":
                                finish = True
                            else:
                                self.tokens.append(temp)
                                self.addError(temp.type, "Punto y coma - Corchete de cierre", temp.row, temp.column)

                        else:
                            self.tokens.append(temp)
                            self.addError(temp.type, "Cadena", temp.row, temp.column)
                            break
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Corchete de cierre", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Igual", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Claves", temp.row, temp.column)
            self.keys = rowTemp

    def recordsAn(self):
        temp = self.tokens.pop()

        if temp.type == "Registros":
            temp = self.tokens.pop()

            if temp.type == "Igual":
                temp = self.tokens.pop()

                if temp.type == "Corchete de apertura":
                    records = True
                    while records:
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
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Corchete de apertura", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Igual", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Registros", temp.row, temp.column)

    def countingAn(self):
        temp = self.tokens.pop()

        if temp.type == "conteo":
            count = temp.lexeme
            temp = self.tokens.pop()

            if temp.type == "Paréntesis de apertura":
                parentesisAp = temp.lexeme
                temp = self.tokens.pop()

                if temp.type == "Paréntesis de cierre":
                    parentesisCi = temp.lexeme
                    temp = self.tokens.pop()

                    if temp.type == "Punto y coma":
                        rows = len(self.vector)
                        columns = len(self.vector[0])
                        count = int(rows)*int(columns)
                        self.temporary += "\n>>>" + str(count)
                        nodeInstruction = self.createNode('Instrucción')
                        node0 = self.createNode('conteo')
                        node1 = self.createNode(count)
                        self.addNodeC(node0, node1)
                        node2 = self.createNode('Paréntesis de apertura')
                        node3 = self.createNode(parentesisAp)
                        self.addNodeC(node2, node3)
                        node4 = self.createNode('Paréntesis de cierre')
                        node5 = self.createNode(parentesisCi)
                        self.addNodeC(node4, node5)
                        node7 = self.createNode('Punto y coma')
                        node8 = self.createNode(temp.lexeme)
                        self.addNodeC(node7, node8)
                        node9 = self.createNode('Instrucción - conteo')
                        self.addNodeC(node9, node0)
                        self.addNodeC(node9, node9)
                        self.addNodeC(node9, node5)
                        self.addNodeC(node9, node7)
                        self.addNodeC(self.start, nodeInstruction)
                        self.addNodeC(nodeInstruction, node9)
                        self.start = nodeInstruction
                    
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Punto y coma", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
        else:
            self.tokens.append(temp)
            self.addError(temp.type, "conteo", temp.row, temp.column)

    def averageAn(self):
        cadena = None
        temp = self.tokens.pop()
        
        if temp.type == "promedio":
            average = temp.lexeme
            temp = self.tokens.pop()

            if temp.type == "Paréntesis de apertura":
                parentesisAp = temp.lexeme
                temp = self.tokens.pop()

                if temp.type == "Cadena":
                    cadenaLx = temp.lexeme
                    cadena = temp.lexeme
                    temp = self.tokens.pop()

                    if temp.type == "Paréntesis de cierre":
                        parentesisCi = temp.lexeme
                        temp = self.tokens.pop()

                        if temp.type == "Punto y coma":
                            res = self.functionPromedio.promedio(self.vector, self.keys, cadena)
                            if res is None:
                                print("Error")
                            else:
                                self.temporary += "\n>>>" + res
                                nodeInstruction = self.createNode('Instrucción')
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
                                node10 = self.createNode('Instrucción - promedio')
                                self.addNodeC(node10, node0)
                                self.addNodeC(node10, node2)
                                self.addNodeC(node10, node4)
                                self.addNodeC(node10, node6)
                                self.addNodeC(node10, node8)
                                self.addNodeC(self.start, nodeInstruction)
                                self.addNodeC(nodeInstruction, node10)
                                self.start = nodeInstruction

                        else:
                            self.tokens.append(temp)
                            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Cadena", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
        else:
            self.tokens.append(temp)
            self.addError(temp.type, "promedio", temp.row, temp.column)

    def contarsiAn(self):
        field = None
        value = None
        temp = self.tokens.pop()

        if temp.type == "contarsi":
            contarsi = temp.lexeme
            temp = self.tokens.pop()

            if temp.type == "Paréntesis de apertura":
                parentesisAp = temp.lexeme
                temp = self.tokens.pop()

                if temp.type == "Cadena":
                    cadena1 = temp.lexeme
                    field = temp.lexeme
                    temp = self.tokens.pop()

                    if temp.type == "Coma":
                        comma = temp.lexeme
                        temp = self.tokens.pop()

                        if temp.type == "Cadena" or temp.type == "Decimal" or temp.type == "Entero":
                            value = temp.lexeme
                            cadena2 = temp.lexeme
                            temp = self.tokens.pop()

                            if temp.type == "Paréntesis de cierre":
                                parentesisCi = temp.lexeme
                                temp = self.tokens.pop()

                                if temp.type == "Punto y coma":
                                    res = self.functionContarSi.contarSi(self.vector, self.keys, field, value)
                                    if res is None:
                                        print("Error en contarSi")
                                    else:
                                        self.temporary += "\n>>>" + res
                                        nodeInstruction = self.createNode('Instrucción')
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
                                        node14 = self.createNode('Instrucción - contarsi')
                                        self.addNodeC(node14, node0)
                                        self.addNodeC(node14, node2)
                                        self.addNodeC(node14, node4)
                                        self.addNodeC(node14, node6)
                                        self.addNodeC(node14, node8)
                                        self.addNodeC(node14, node10)
                                        self.addNodeC(node14, node12)
                                        self.addNodeC(self.start, nodeInstruction)
                                        self.addNodeC(nodeInstruction, node14)
                                        self.start = nodeInstruction

                                else:
                                    self.tokens.append(temp)
                                    self.addError(temp.type, "Punto y coma", temp.row, temp.column)
                            else:
                                self.tokens.append(temp)
                                self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
                        else:
                            self.tokens.append(temp)
                            self.addError(temp.type, "Cadena - Decimal - Entero", temp.row, temp.column)
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Coma", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Cadena", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
        else:
            self.tokens.append(temp)
            self.addError(temp.type, "contarsi", temp.row, temp.column)

    def dataAn(self):
        temp = self.tokens.pop()

        if temp.type == "datos":
            data = temp.lexeme
            temp = self.tokens.pop()

            if temp.type == "Paréntesis de apertura":
                parentesisAp = temp.lexeme
                temp = self.tokens.pop()

                if temp.type == "Paréntesis de cierre":
                    parentesisCi = temp.lexeme
                    temp = self.tokens.pop()

                    if temp.type == "Punto y coma":
                        nodeInstruction = self.createNode('Instrucción')

                        node0 = self.createNode('datos')
                        node1 = self.createNode(data)
                        self.addNodeC(node0, node1)

                        node2 = self.createNode('Paréntesis de apertura')
                        node3 = self.createNode(parentesisAp)
                        self.addNodeC(node2, node3)

                        node4 = self.createNode('Paréntesis de cierre')
                        node5 = self.createNode(parentesisCi)
                        self.addNodeC(node4, node5)

                        node6 = self.createNode('Punto y coma')
                        node7 = self.createNode(temp.lexeme)
                        self.addNodeC(node6, node7)

                        node8 = self.createNode('Instrucción - datos')
                        self.addNodeC(node8, node0)
                        self.addNodeC(node8, node2)
                        self.addNodeC(node8, node4)
                        self.addNodeC(node8, node6)

                        self.addNodeC(self.start, nodeInstruction)
                        self.addNodeC(nodeInstruction, node8)
                        self.start = nodeInstruction
                    
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Punto y coma", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Parénteisis de apertura", temp.row, temp.column)
        else:
            self.tokens.append(temp)
            self.addError(temp.type, "datos", temp.row, temp.column)

    def sumarAn(self):
        cadena = None
        temp = self.tokens.pop()

        if temp.type == "sumar":
            sum = temp.lexeme
            temp = self.tokens.pop()

            if temp.type == "Paréntesis de apertura":
                parentesisAp = temp.lexeme
                temp = self.tokens.pop()

                if temp.type == "Cadena":
                    cadenaLx = temp.lexeme
                    cadena = temp.lexeme
                    temp = self.tokens.pop()

                    if temp.type == "Paréntesis de cierre":
                        parentesisCi = temp.lexeme
                        temp = self.tokens.pop()

                        if temp.type == "Punto y coma":
                            res = self.functionSuma.sumar(self.vector, self.keys, cadena)
                            if res is None:
                                print("Error en suma")
                            else:
                                self.temporary += "\n>>>" + res
                                nodeInstruction = self.createNode('Instrucción')
                                node0 = self.createNode('sumar')
                                node1 = self.createNode(sum)
                                self.addNodeC(node0, node1)
                                node2 = self.createNode('Paréntesis de apertura')
                                node3 = self.createNode(parentesisAp)
                                self.addNodeC(node2, node3)
                                node4 = self.createNode('Cadena')
                                node5 = self.createNode(temp.lexeme)
                                self.addNodeC(node4, node5)
                                node6 = self.createNode('Paréntesis de cierre')
                                node7 = self.createNode(parentesisCi)
                                self.addNodeC(node6, node7)
                                node8 = self.createNode('Punto y coma')
                                node9 = self.createNode(cadenaLx)
                                self.addNodeC(node8, node9)
                                node10 = self.createNode('Instrucción - sumar')
                                self.addNodeC(node10, node0)
                                self.addNodeC(node10, node2)
                                self.addNodeC(node10, node4)
                                self.addNodeC(node10, node6)
                                self.addNodeC(node10, node8)
                                self.addNodeC(self.start, nodeInstruction)
                                self.addNodeC(nodeInstruction, node10)
                                self.start = nodeInstruction
                        else:
                            self.tokens.append(temp)
                            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Cadena", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
        else:
            self.tokens.append(temp)
            self.addError(temp.type, "sumar", temp.row, temp.column)
    
    def maxAn(self):
        cadena = None
        temp = self.tokens.pop()

        if temp.type == "max":
            maximum = temp.lexeme
            temp = self.tokens.pop()

            if temp.type == "Paréntesis de apertura":
                parentesisAp = temp.lexeme
                temp = self.tokens.pop()

                if temp.type == "Cadena":
                    cadenaLx = temp.lexeme
                    cadena = temp.lexeme
                    temp = self.tokens.pop()

                    if temp.type == "Paréntesis de cierre":
                        parentesisCi = temp.lexeme
                        temp = self.tokens.pop()

                        if temp.type == "Punto y coma":
                            res = self.functionMax.max(self.vector, self.keys, cadena)
                            if res is None:
                                print("Error en max")
                            else:
                                self.temporary += "\n>>>" + res
                                nodeInstruction = self.createNode('Instrucción')
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
                                node10 = self.createNode('Instrucción - max')
                                self.addNodeC(node10, node0)
                                self.addNodeC(node10, node2)
                                self.addNodeC(node10, node4)
                                self.addNodeC(node10, node6)
                                self.addNodeC(node10, node8)
                                self.addNodeC(self.start, nodeInstruction)
                                self.addNodeC(nodeInstruction, node10)
                                self.start = nodeInstruction
                        else:
                            self.tokens.append(temp)
                            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Cadena", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
        else:
            self.tokens.append(temp)
            self.addError(temp.type, "max", temp.row, temp.column)

    def minAn(self):
        cadena = None
        temp = self.tokens.pop()
        if temp.type == "min":
            minimum = temp.lexeme
            temp = self.tokens.pop()

            if temp.type == "Paréntesis de apertura":
                parentesisAp = temp.lexeme
                temp = self.tokens.pop()

                if temp.type == "Cadena":
                    cadenaLx = temp.lexeme
                    cadena = temp.lexeme
                    temp = self.tokens.pop()

                    if temp.type == "Paréntesis de cierre":
                        parentesisCi = temp.lexeme
                        temp = self.tokens.pop()

                        if temp.type == "Punto y coma":
                            res = self.functionMin.min(self.vector, self.keys, cadena)
                            if res is None:
                                print("Error en min")
                            else:
                                self.temporary += "\n>>>" + res
                                nodeInstruction = self.createNode('Instrucción')
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
                                node10 = self.createNode('Instrucción - min')
                                self.addNodeC(node10, node0)
                                self.addNodeC(node10, node2)
                                self.addNodeC(node10, node4)
                                self.addNodeC(node10, node6)
                                self.addNodeC(node10, node8)
                                self.addNodeC(self.start, nodeInstruction)
                                self.addNodeC(nodeInstruction, node10)
                                self.start = nodeInstruction
                        else:
                            self.tokens.append(temp)
                            self.addError(temp.type, "Punto y coma", temp.row, temp.column)
                    else:
                        self.tokens.append(temp)
                        self.addError(temp.type, "Paréntesis de cierre", temp.row, temp.column)
                else:
                    self.tokens.append(temp)
                    self.addError(temp.type, "Cadena", temp.row, temp.column)
            else:
                self.tokens.append(temp)
                self.addError(temp.type, "Paréntesis de apertura", temp.row, temp.column)
        else:
            self.tokens.append(temp)
            self.addError(temp.type, "min", temp.row, temp.column)

    def reportAn(self):
        pass