import math
from random import randint
from time import time
from matplotlib import pyplot

class Node:
    def __init__(self, pos, meta,
                 padre=None):  # el nodo esta compuesto de su ubicacion, cual es su padre, y los valores de f,g y h
        self.pos = pos
        self.padre = padre

        if self.padre == None:
            self.g = 0
            self.meta =tuple(meta)
        else:
            self.g = self.padre.g + 1
            self.meta = self.padre.meta

        self.h = distancia(self.pos, self.meta)
        self.f = self.g + self.h


def distancia(a, b):  ## se calcula la distancia euclidiana entre dos puntos

    var0 = (a[0] - b[0]) ** 2
    var1 = (a[1] - b[1]) ** 2
    resultado = math.sqrt(var0 + var1)
    return resultado


class aestrella:  ##clase que resuelve todo el problema
    def __init__(self, inicio, meta, filas, columnas):
        self.inicio = inicio
        self.var = (filas *6 - 1, columnas*4 - 1)
        self.meta = tuple(meta)
        self.listb = []
        self.listaa = []
        self.listac = []
        self.filas = filas
        self.columnas = columnas
        self.expan = 0

    def bloqueado(self):
        a = 1
        b = 1
        est=[]
        for j in range(self.columnas):
            a=1
            for i in range(self.filas):
                self.listb.append((a, b))
                self.listb.append((a + 1, b))
                self.listb.append((a, b + 1))
                self.listb.append((a + 1, b + 1))
                self.listb.append((a+2, b))
                self.listb.append((a + 2, b + 1))
                self.listb.append((a+3, b))
                self.listb.append((a + 3, b + 1))
                a = a + 6
            b = b + 4
        est=self.listb
        return est

    def iniciar(self):
        self.listac.append(Node(self.inicio, self.meta))
        self.listaa += self.crearhijo(Node(self.inicio, self.meta, self.listac[0]))
        while self.final():
            self.buscar()
        self.camino = self.desplazamiento()
        return self.camino

    def crearhijo(self,
                  node):  ##Expande un nodo analizando sus vecinos en sus posiciones verticales y horizontales. No busca en diagonal.
        self.expan += 1
        vecinospos = []
        vecinos = []
        for v in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vecinospos.append((node.pos[0] + v[0], node.pos[1] + v[1]))

        for pos in vecinospos:
            if pos in self.listb:
                vecinospos.remove(pos)

        for pos in vecinospos:
            if pos[0] < 0 or pos[1] < 0:
                vecinospos.remove(pos)

        for pos in vecinospos:
            if (pos[0] > (self.var[0]))or(pos[1]>(self.var[1])):
                vecinospos.remove(pos)

        for pos in vecinospos:
            vecinos.append(Node(pos, self.meta, node))

        return vecinos

    def repetidos(self, node,
                  lista):  # revisa si un nodo en particular esta en una lista. devolviendo true (1) o false (0)
        for i in range(len(lista)):
            if node.pos == lista[i].pos:
                return 1

        return 0

    def fmenor(
            self):  # el llamado a la funcion analiza la lista abierta, busca el nodo con menor valor de f, lo agrega a la lista cerrada y lo borra de la lista abierta.
        if self.listaa:
            a = self.listaa[0]  # esta funcion se utiliza en buscar
            n = 0
            for i in range(1, len(self.listaa)):
                if self.listaa[i].f < a.f:
                    a = self.listaa[i]
                    n = i
            self.listac.append(a)  # se agrega a lista cerrada
            del self.listaa[n]  # se borra de lista abierta

    def final(self):  # si la meta esta dentro de la lista abierta devuelve false para romper el while
        for i in range(len(self.listaa)):
            if self.meta == self.listaa[i].pos:
                return 0

        return 1

    def trayectoria(self):  # se utiliza en la funcion buscar

        for i in range(len(self.candidatos)):  # con la lista de nodos vecinos al ultimo elemento de la listac
            if self.repetidos(self.candidatos[i],
                              self.listac):  # si uno de estos vecinos ya se encuentra en la listac se continua el programa
                continue
            elif not self.repetidos(self.candidatos[i],
                                    self.listaa):  # si uno de los candidatos no esta en la lista abierta se lo agrega a ella
                self.listaa.append(self.candidatos[i])
            else:
                if self.ultimolc.g + 1 < self.candidatos[
                    i].g:  # si ya esta en la lista abierta, se compara el valor de los candidatos con el de el ultimolc+1
                    for j in range(len(self.listaa)):
                        if self.candidatos[i].pos == self.listaa[j].pos:
                            del self.listaa[j]
                            self.listaa.append(self.candidatos[i])
                            break

    def buscar(self):  # se pone en lista cerrada el elemento de menor f de la lista abierta

        self.fmenor()
        self.ultimolc = self.listac[-1]  # se identifica el ultimo elemento de la lsita cerrada
        self.candidatos = self.crearhijo(
            self.ultimolc)  # se analizan los nodos vecinos y son llamados candidatos para seguir la busqueda
        self.trayectoria()  # es el camino de todos los nodos visitados no el directo

    def desplazamiento(self):
        for i in range(len(self.listaa)):
            if self.meta == self.listaa[i].pos:
                objetivo = self.listaa[i]

        camino = []

        while objetivo.padre != None:
            camino.append(objetivo.pos)
            objetivo = objetivo.padre
        camino.reverse()
        return camino
def graficar(dim,tiempos,nodos,dist):
    pyplot.subplot(131)
    pyplot.plot(dim, tiempos, 'ro-')
    pyplot.grid()
    pyplot.xlabel('Dimensiones del almacén (NxN)')
    pyplot.ylabel('Tiempo')
    pyplot.title('Tiempo en función del espacio de búsqueda')
    pyplot.subplot(132)
    pyplot.plot(dim, nodos, 'bo-')
    pyplot.grid()
    pyplot.xlabel('Dimensiones del almacén (NxN)')
    pyplot.ylabel('Nodos expandidos')
    pyplot.title('Promedio de Nodos expandidos')
    pyplot.subplot(133)
    pyplot.plot(dim, dist, 'go-')
    pyplot.grid()
    pyplot.xlabel('Dimensiones del almacén (NxN)')
    pyplot.ylabel('Distancia recorrida')
    pyplot.title('Promedio de Distancias recorridas')
    pyplot.show()

if __name__ == "__main__":
    filas = int(input("Filas de estantes: "))
    columnas = int(input("Columnas de estantes: "))

    # tiempo=[]      ### Descomentar para evaluar desempeño
    # nodos=[]
    # dista=[]
    # it=50
    # log = [1,5,10,15,20,25,30,35,40,45,50]
    # for i in log:
    #     print(i)
    #     filas=i
    #     columnas=i
    #     sum1 = 0
    #     sum2 = 0
    #     sum3=0
    #     for j in range(it):
             ### Ajustar indentación TODO dentro del "for" para que funcione
    inicio = tuple()
    inicio = (randint(0, filas * 6 - 1), randint(0, columnas * 4 - 1))
    meta = tuple()
    meta = (randint(0, filas * 6 - 1), randint(0, columnas * 4 - 1))
    y = aestrella(inicio, meta, filas, columnas)
    check=y.bloqueado()
    while (meta in check) or (inicio in check) or (meta==inicio):
        inicio = (randint(0, filas * 6 - 1), randint(0, columnas * 4 - 1))
        meta = (randint(0, filas * 6 - 1), randint(0, columnas * 4 - 1))
    yy=aestrella(inicio,meta,filas,columnas)
    yy.bloqueado()
    start_time = time()
    resultado = yy.iniciar()
    dist=len(resultado)-1
    lapso=time()-start_time     ### Todo hasta esta linea dentro del "for". Alinear con las líneas de abajo

        #     sum3+=dist        ### Descomentar para evaluar desempeño
        #     sum1+=lapso
        #     sum2+=yy.expan
        # sum1=sum1/it
        # sum2=sum2/it
        # sum3=sum3/it
        # dista.append(sum3)
        # tiempo.append(sum1)
        # nodos.append(sum2)
    # print("Tiempos promedios: ", tiempo)
    # print("Promedio de nodos expandidos: ",nodos)
    # print("Promedio de distancias recorridas: ", dista)
    # print("Graficación")
    # graficar(log,tiempo,nodos,dista)

    print("El Espacio del Almacén es de ", filas * 6, "filas y", columnas * 4, "columnas.") ### Comentar para evaluar desempeño
    print("Punto de Inicio",inicio)
    print("Punto de Llegada: ",meta)
    print("Los lugares ocupados por las Estanterías son: \n", check)
    print("El camino a realizar es: \n", resultado)
    print("La distancia en pasos es de: ", dist)
    print("Cantidad de nodos expandidos: ", yy.expan)
    print("Tiempo de ejecución: ",lapso,"s.")
