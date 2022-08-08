import math
from random import randint
import sys
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
    var2 = (a[2] - b[2]) ** 2
    resultado = math.sqrt(var0 + var1 + var2)
    return resultado


class aestrella:  ##clase que resuelve todo el problema
    def __init__(self, inicio, meta, entorno,obsta):
        self.inicio = inicio
        self.var = entorno
        self.cant=obsta
        self.meta = tuple(meta)
        self.listb = []
        self.listaa = []
        self.listac = []
        self.expan=0
        self.Tbloq=0

    def bloqueado(self):
        start_time = time()
        obs = []
        aux1 = tuple()
        aux2 = []
        k = 0
        while k < self.cant:
            aux1 = (randint(0, esp), randint(0, esp), randint(0, esp))
            while aux1 == inicio or aux1 == meta:
                aux1 = (randint(0, esp), randint(0, esp), randint(0, esp))
            aux2 = Node(aux1, meta, None)
            if self.repetidos(aux2, obs):
                k -= 1
            else:

                self.listb.append(aux2.pos)
                obs.append(aux2)
            k += 1
        self.listb.sort()
        est=self.listb
        self.Tbloq=time()-start_time
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
        self.expan+=1
        vecinospos = []
        vecinos = []
        for v in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            vecinospos.append((node.pos[0] + v[0], node.pos[1] + v[1], node.pos[2] + v[2]))

        for pos in vecinospos:
            if pos in self.listb:
                vecinospos.remove(pos)
        i=0
        while i<len(vecinospos):
            i+=1
            for pos in vecinospos:
                if (pos[0] < 0) or (pos[1] < 0) or (pos[2] < 0):
                    i-=1
                    vecinospos.remove(pos)
        i = 0
        while i < len(vecinospos):
            i += 1
            for pos in vecinospos:
                if (pos[0] > (self.var)) or (pos[1]>(self.var)) or (pos[2]>(self.var)):
                    i -= 1
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
        else:
            print("\nNo hay un camino posible.")
            print("Nodos expandidos: ", self.expan)
            lapso = time() - start_time
            print("Tiempo de ejecución: ", lapso, "s.")
            sys.exit()

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
                if self.ultimolc.g + 1 < self.candidatos[i].g:  # si ya esta en la lista abierta, se compara el valor de los candidatos con el de el ultimolc+1
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
        aux=[0,0,0]

        while objetivo.padre != None:
            aux=[0,0,0]
            for i in (0,1,2):
                aux[i]=int(180*objetivo.pos[i]/self.var)
            objetivo = objetivo.padre
            camino.append(aux)
        camino.reverse()
        return camino

if __name__ == "__main__":
    esp = int(float(input("Ingrese el 'PASO' en grados (0 a 180): ")))   ### Descomentar para funcionamiento normal
    if esp<1:
        esp=1
    if esp>180:
        esp=180
    esp=180//esp
    pje = float(input("Ingrese porcentaje del espacio cubierto por obstáculos: "))
    total = (esp + 1) ** 3
    inicio=tuple()                        
    inicio = (randint(0, esp), randint(0, esp), randint(0, esp))
    meta=tuple()
    meta = (randint(0, esp), randint(0, esp), randint(0, esp))
    while meta == inicio:
        meta = (randint(0, esp), randint(0, esp), randint(0, esp))
    ini=[0,0,0]
    met=[0,0,0]
    for i in (0,1,2):
        ini[i]=int((180/esp)*inicio[i])
        met[i]=int((180/esp)*meta[i])
    print("Posición articular inicial: ", ini)
    print("Posición final: ", met)
    if pje < 0:  ### En estos dos "if" solo corrigen el valor ingresado
        pje = 0
        cant=0
    else:
        if pje >= 100:
            pje = 100
            cant = total-2
        else:
            cant = int((total * pje // 100))
            if cant<0:
                cant=0
            if cant>total-2:
                cant=total-2
    print("Tripletas de ángulos en el espacio: ",total)
    print("Cantidad de obstáculos: ",cant)
    if (cant==total-2) and (distancia(inicio,meta)):
        print("\nNo hay un camino posible. Demasiados obstáculos.")
    else:
        yy = aestrella(inicio, meta, esp, cant)
        obs=yy.bloqueado()
        aux=[0,0,0]
        obsta=[]
        if obs:
            for i in range(len(obs)):
                aux=[0,0,0]
                for j in (0,1,2):
                    aux[j]=int(180*obs[i][j]/esp)
                if True:
                    obsta.append(aux)

            print("Los Obstáculos están en: \n", obsta)
        print("Tiempo en crear los obstáculos: ", yy.Tbloq, "s.")
        start_time = time()
        resultado = yy.iniciar()
        print("El camino es:\n", resultado)           ### Descomentar para funcionamiento normal
        dist=len(resultado)                           ### Alinear con líneas anteriores
        print("La distancia recorrida es: ",dist-1)
        print("Cantidad de nodos expandidos: ",yy.expan)
        lapso = time() - start_time
        print("Tiempo de ejecución: ", lapso, "s.")

    ### Descomentar para probar desempeño
    # paso=30
    # t=[]
    # it=10
    # inicio = (0, 0, 0)
    # pje=[30,35,40,45,50]
    # for j in pje:
    #     sumT = 0
    #     esp = 180 // paso
    #     total = (esp + 1) ** 3
    #     meta = (esp, esp, esp)
    #     cant = int((total * j // 100))
    #     for k in range(it):
    #         y = aestrella(inicio, meta, esp, cant)
    #         y.bloqueado()
    #         start_time = time()
    #         resultado = y.iniciar()
    #         lapso=time()-start_time
    #         sumT+=lapso
    #     sumT=sumT/it
    #     t.append(sumT)
    #     print(t)
    # print(t)




