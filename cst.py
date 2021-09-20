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

            auc = str(elemento).replace('"', '\'')

            straux = str(self.contador) + "[label= \"" + auc +"\"]\n"
            self.textoNodo += straux
            self.contador += 1
        
        self.pilahijos.append(hijos) #pila de arrays de nodos [[],[],[],[]] lista de listas if u may

    def generarTexto(self, txt):
        self.texto.append[txt]



# ------------------------------ TABLA DE SÍMBOLOS ---------------------------------
#-----------------------------------------------------------------------------------
class NodoSimbolo:
    def __init__(self, id, nombre, tipo, ambito, fila, columna):
        self.id = id            # 1-> a= 2;
        self.nombre = nombre    # a
        self.tipo = tipo        # int (?)
        self.ambito = ambito    #global
        self.fila = fila        #5
        self.columna = columna  #21


class TablaSimbolos:

    def __init__(self, simbolos = {}) : #el init recibe un array de símbolos
        self.simbolos = simbolos

    def añadir(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo

    def obtener(self, id, contaerrores, lineno, lexpos) :
        if not id in self.simbolos :
            desc = 'Variable no definida'
            error1 = NodoError(contaerrores, desc, lineno, lexpos)
            return error1

        return self.simbolos[id]

    def actualizar(self, simbolo, contaerrores, lineno, lexpos) :
        if not simbolo.id in self.simbolos :
            desc = 'Variable no definida'
            error1 = NodoError(contaerrores, desc, lineno, lexpos)
            return error1
        else :
            self.simbolos[simbolo.id] = simbolo
   
