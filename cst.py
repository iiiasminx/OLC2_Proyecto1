from datetime import datetime

# ----------------------------------- OBJ EXPORTACION ------------------------------
#-----------------------------------------------------------------------------------

class Exporte:
    def __init__(self, interpretacion, tabla_simbolos, grafo, tabla_errores):
        self.interpretacion = interpretacion
        self.tabla_simbolos = tabla_simbolos
        self.grafo = grafo
        self.tabla_errores = tabla_errores

# ------------------------------------- TABLA ERRORES -----------------------------
#-----------------------------------------------------------------------------------
class NodoError:

    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y %H:%M:%S")
    def __init__(self, contador, descripcion, fila, columna):
        self.contador = contador
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna

# ------------------------------ TABLA DE SÍMBOLOS ---------------------------------
#-----------------------------------------------------------------------------------
class NodoSimbolo:
    def __init__(self, nombre, tipo, ambito, fila, columna):
        self.nombre = nombre
        self.tipo = tipo
        self.ambito = ambito
        self.fila = fila
        self.columna = columna

# ------------------------------------- AST ------------------------------------
#-----------------------------------------------------------------------------------

class GrafoCST:    

    pilahijos = []  #pila de arrays de nodos [[],[],[],[]] lista de listas if u may

    #declaración de nodos
    textoNodo = ""
    pilaNodos = []

    #declaración de relaciones de unos a otros
    pilaLimites = []
    textoEdges = ""

    contador = 0
    texto = []

    #Genera los padres en funcion de los ultimos datos en la pila de Hijos
    #la posición es la posición de la producción en la que está
    #ej UNO : cadena DOS
    #generarpadre(2)
    def generarPadre(self, posicion):
        posicion -= 1
        limites = self.pilahijos.pop()
        
        for temp in limites:
            dictaux = {
                "from" : self.contador + posicion,
                "to" : temp["id"]
            }
            self.pilaLimites.append(dictaux)
            strxx = str(self.contador+posicion) + " -> " + str(temp["id"]) + "\n"
            self.textoEdges += strxx


    #genera los hijos del cosito, solo recibe strings
    def generarHijos(self, *listahijos ): #este es cuando genera solo strings (?)

        hijos = []

        for elemento in listahijos:
            hijo = {
                "id" : self.contador,
                "label": elemento #str(elemento)
            }
            hijos.append(hijo)              #lista de hijos del padre
            self.pilaNodos.append(hijo)     #lista de hijos general -- ESTO ME SIRVE PARA EL INTÉRPRETE
            straux = str(self.contador) + "[label= \"" + str(elemento) +"\"]\n"
            self.textoNodo += straux
            self.contador += 1
        
        self.pilahijos.append(hijos) #pila de arrays de nodos [[],[],[],[]] lista de listas if u may

    def generarTexto(self, txt):
        self.texto.append[txt]


# ----------------------------------INSTRUCCION ------------------------------------
#-----------------------------------------------------------------------------------

class Instruccion:
    def __init__(self, tipo, args):
        self.tipo = tipo
        self.args = args #Este es un arreglo con lo que necesito saber para las instrucciones

# ------------------------------------- COSOS X ------------------------------------
#-----------------------------------------------------------------------------------
class Nodo:
    def __init__(self):
        pass
    pass

class NodoAST:
    def __init__(self, nombre, hijos):
        self.nombre = nombre
        self.hijos = hijos #hijos es una de NodosAST
   
