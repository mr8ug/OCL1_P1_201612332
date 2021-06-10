from abstract.Instruccion import Instruccion
from parser.Excepcion import Excepcion
from parser.Tipo import TIPO, OperadorAritmetico

class Aritmetica(Instruccion):
    def __init__(self, operador, OpIzq, OpDer, fila, columna):
        self.operador= operador
        self.OperacionIzq=OpIzq
        self.OperacionDer=OpDer
        self.fila = fila
        self.columna = columna
        self.tipo = None
    
    def interpreter(self, tree, table):
        izq = self.OperacionIzq.interpreter(tree, table)
        if isinstance(izq, Excepcion): return izq

        if self.OperacionDer != None:
            der = self.OperacionDer.interpreter(tree,table)
            if isinstance(der, Excepcion): return der



        if self.operador == OperadorAritmetico.MAS:
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo,izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo,izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo,izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de oepracion para + (suma/concatenacion). ",self.fila,self.columna)

        
        elif self.operador == OperadorAritmetico.MENOS:
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo erroneo de operacion para -.", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.UMENOS: #negacion unitaria
            if self.OperacionIzq.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return - self.obtenerVal(self.OperacionIzq.tipo, izq)

            elif self.OperacionIzq.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return - self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para - (UNARIO).", self.fila,self.columna)
        return Excepcion("Semantico", "Tipo de Operacion no Especificado.", self.fila, self.columna)

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)

        elif tipo == TIPO.DECIMAL:
            return float(val)

        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)
