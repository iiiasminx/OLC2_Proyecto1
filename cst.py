from datetime import datetime

# ----------------------------------- OBJ EXPORTACION ---------------------------

class Exporte:
    def __init__(self, interpretacion, tabla_simbolos, grafo, tabla_errores):
        self.interpretacion = interpretacion
        self.tabla_simbolos = tabla_simbolos
        self.grafo = grafo
        self.tabla_errores = tabla_errores

# ------------------------------------- TABLA ERRORES ---------------------------
class NodoError:

    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y %H:%M:%S")
    def __init__(self, contador, descripcion, fila, columna):
        self.contador = contador
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna

# ------------------------------ TABLA DE SÍMBOLOS -----------------------------
class NodoSimbolo:
    def __init__(self, nombre, tipo, ambito, fila, columna):
        self.nombre = nombre
        self.tipo = tipo
        self.ambito = ambito
        self.fila = fila
        self.columna = columna

# ------------------------------------- AST ------------------------------------
class NodoAST:
    def __init__(self):
        texto = ""
        contador = 0

class GrafoCST:    

    def  generarHijos( listahijos ):
        for elemento in listahijos:
            pass