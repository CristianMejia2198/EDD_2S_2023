from nodoB import NodoB
from ramaB import RamaB
import os

class ArbolB():
    def __init__(self):
        self.orden = 3
        self.raiz: RamaB = None

    def insertar(self, valor):
        nuevo = NodoB(valor)
        if self.raiz is None:
            self.raiz = RamaB()
            self.raiz.insertar(nuevo)
        else:
            obj:NodoB = self.insertar_rama(nuevo, self.raiz)
            if obj is not None:
                self.raiz = RamaB()
                self.raiz.insertar(obj)
                self.raiz.hoja = False
        
    def insertar_rama(self, nodo:NodoB, rama:RamaB):
        if rama.hoja:
            rama.insertar(nodo)
            if rama.contador == self.orden:
                return self.dividir(rama)
            else:
                return None
        else:
            temp:NodoB = rama.primero
            while temp is not None:
                if nodo.valor == temp.valor: #comparar codigo de tareas
                    return None
                elif nodo.valor < temp.valor: #comparar codigo de tareas
                    obj:NodoB = self.insertar_rama(nodo, temp.izquierda)
                    if obj is not None:
                        rama.insertar(obj)
                        if rama.contador == self.orden:
                            return self.dividir(rama)
                    return None
                elif temp.siguiente is None:
                    obj:NodoB = self.insertar_rama(nodo, temp.derecha)
                    if obj is not None:
                        rama.insertar(obj)
                        if rama.contador == self.orden:
                            return self.dividir(rama)
                    return None
                temp = temp.siguiente
        return
    
    def dividir(self, rama:RamaB):
        val:NodoB = NodoB(-999)
        aux:NodoB = rama.primero
        temp:NodoB = None
        rderecha:RamaB = RamaB()
        rizquierda:RamaB = RamaB()
        contador = 0

        while aux is not None:
            contador += 1
            if contador < 2:
                temp = NodoB(aux.valor) #enviar todos los valores
                temp.izquierda = aux.izquierda
                if contador == 1:
                    temp.derecha = aux.siguiente.izquierda
                if temp.derecha is not None and temp.izquierda is not None:
                    rizquierda.hoja = False
                rizquierda.insertar(temp)
            elif contador == 2:
                val.valor = aux.valor
            else:
                temp = NodoB(aux.valor) #enviar todos los valores
                temp.izquierda = aux.izquierda
                temp.derecha = aux.derecha
                if temp.derecha is not None and temp.izquierda is not None:
                    rderecha.hoja = False
                rderecha.insertar(temp)
            aux = aux.siguiente
        val.derecha = rderecha
        val.izquierda = rizquierda
        return val
    
    #Reporte de Graphiz
    def graficar(self):
        cadena = ''
        archivo = "arbolB.jpg"
        a = open("arbolB.dot","w")
        if self.raiz is not None:
            cadena += "digraph arbol { \nnode[shape=record]"
            cadena += self.Grafo(self.raiz.primero)
            cadena += self.conexionRamas(self.raiz.primero)
            cadena += "}"
        a.write(cadena)
        a.close()
        os.system("dot -Tjpg arbolB.dot -o " + archivo)
    
    def Grafo(self, rama:NodoB):
        dot = ''
        if rama is not None:
            dot += self.GrafoRamas(rama)
            aux:NodoB = rama
            while aux is not None:
                if aux.izquierda is not None:
                    dot += self.Grafo(aux.izquierda.primero)
                if aux.siguiente is None:
                    if aux.derecha is not None:
                        dot += self.Grafo(aux.derecha.primero)
                aux = aux.siguiente
        return dot

    def GrafoRamas(self, rama:NodoB):
        dot = ''
        if rama is not None:
            aux:NodoB = rama
            dot = dot + "R" + str(rama.valor) + "[label=\"" #rama.valor.Tarea.codigo_tarea || rama.valor.codigo_tarea
            r = 1 
            while aux is not None:
                if aux.izquierda is not None:
                    dot = dot + "<C" + str(r) + ">|"
                    r += 1
                if aux.siguiente is not None:
                    dot = dot + str(aux.valor) + "|" #Cambio de valores
                else:
                    dot = dot + str(aux.valor) #cambio de Valores
                    if aux.derecha is not None:
                        dot = dot + "|<C" + str(r) + ">"
                aux = aux.siguiente
            dot = dot + "\"];\n"
        return dot
    
    def conexionRamas(self, rama:NodoB):
        dot = ''
        if rama is not None:
            aux:NodoB = rama
            actual = "R" + str(rama.valor)
            r = 1
            while aux is not None:
                if aux.izquierda is not None:
                    dot += actual + ":C" + str(r) + " -> " + "R"+ str(aux.izquierda.primero.valor) + ";\n"
                    r += 1
                    dot += self.conexionRamas(aux.izquierda.primero)
                if aux.siguiente is None:
                    if aux.derecha is not None:
                        dot += actual + ":C" + str(r) + " -> " + "R"+ str(aux.derecha.primero.valor) + ";\n"
                        r += 1
                        dot += self.conexionRamas(aux.derecha.primero)
                aux = aux.siguiente
        return dot
    
arbol = ArbolB()

for i in range(16):
    arbol.insertar((i+1))
arbol.graficar()