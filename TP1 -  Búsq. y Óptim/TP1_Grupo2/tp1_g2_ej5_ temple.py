import math
import numpy as np
from matplotlib import pyplot as plt
from random import randint, uniform,random

class Node:
    def __init__(self, pos, meta, padre=None):
        self.pos = pos
        self.padre = padre

        if self.padre == None:
            self.g = 0
            self.meta = tuple(meta)
        else:
            self.g = self.padre.g + 1
            self.meta = self.padre.meta

        self.h = distancia(self.pos, self.meta)
        self.f = self.g + self.h


def distancia(a, b):  

    var0 = (a[0] - b[0]) ** 2
    var1 = (a[1] - b[1]) ** 2
    resultado = math.sqrt(var0 + var1)
    return resultado


class aestrella: 
    def __init__(self, inicio, meta, entorno):
        self.inicio = inicio
        self.var = entorno
        self.meta = (meta[0],meta[1])
        self.listb = []
        self.listaa = []
        self.listac = []


    def bloqueado(self, filas, columnas):
        a = 1
        
        for j in range(columnas):
            b=1
            for i in range(filas):
                self.listb.append((a, b))
                self.listb.append((a + 1, b))
                self.listb.append((a, b + 1))
                self.listb.append((a + 1, b + 1))
                self.listb.append((a, b + 2))
                self.listb.append((a + 1, b + 2))
                self.listb.append((a, b + 3))
                self.listb.append((a + 1, b + 3))
                b = b + 6

            a = a + 4


    def iniciar(self):

        self.listac.append(Node(self.inicio, self.meta))
        self.listaa += self.crearhijo(Node(self.inicio, self.meta, self.listac[0]))
        
        while self.final():
            self.buscar()
                    
        self.camino = self.desplazamiento()
        return len(self.camino)

    def crearhijo(self, node):  
        vecinospos=[]
        vecinos=[]
        for v in [(-1,0),(1,0),(0,-1),(0,1)]:
            vecinospos.append((node.pos[0] + v[0], node.pos[1] + v[1]))

        for pos in vecinospos:
            if pos in self.listb:
                vecinospos.remove(pos)

        for pos in vecinospos:
            if pos[0] < 0 or pos[1] < 0:
                vecinospos.remove(pos)

        for pos in vecinospos:
            if pos[0] > self.var[0] or pos[1] > self.var[1]:
                vecinospos.remove(pos)

        for pos in vecinospos:
            vecinos.append(Node(pos, self.meta, node))

        return vecinos

    def repetidos(self, node, lista):  
        for i in range(len(lista)):
            if node.pos == lista[i].pos:
                return 1

        return 0

    def fmenor(self):  
        a = self.listaa[0]  
        n = 0
        for i in range(1, len(self.listaa)):
            if self.listaa[i].f < a.f:
                a = self.listaa[i]
                n = i
        self.listac.append(a)  
        del self.listaa[n]  

    def final(self):  
        for i in range (len(self.listaa)):
            if self.meta == self.listaa[i].pos:
                return 0

        return 1

    def trayectoria(self):  

        for i in range(len(self.candidatos)):  
            if self.repetidos(self.candidatos[i],
                              self.listac):  
                continue
            elif not self.repetidos(self.candidatos[i],
                                    self.listaa):  
                self.listaa.append(self.candidatos[i])
            else:
                if self.ultimolc.g + 1 < self.candidatos[i].g: 
                    for j in range(len(self.listaa)):
                        if self.candidatos[i].pos == self.listaa[j].pos:
                            del self.listaa[j]
                            self.listaa.append(self.candidatos[i])
                            break

    def buscar(self):
        self.fmenor()
        self.ultimolc = self.listac[-1]  
        self.candidatos = self.crearhijo(self.ultimolc)  
        
        self.trayectoria()  

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

class Recolector:
    def __init__(self, objetos, filas, columnas):  
        self.listobj = objetos 
        self.filas=filas
        self.columnas=columnas
        self.listestantes =[]
        self.articulos=[] 
        self.target=[] 
        self.mapa = [4*columnas, 6*filas]

    def calcd(self):
        self.estantes(self.filas, self.columnas)
        self.calcpos()
        caminod = 0


        for i in range(len(self.target)):
            if i == 0:
                meta=self.target[i]
                a = aestrella([0, 0], meta, self.mapa)
                a.bloqueado(self.filas, self.columnas)
                caminod = a.iniciar() + caminod
            if i > 0:
                meta=self.target[i]
                a = aestrella(self.target[i-1], meta, self.mapa)
                a.bloqueado(self.filas, self.columnas)
                caminod = a.iniciar() + caminod
            if i == len(self.target):
                meta=(0,0)
                a = aestrella(self.target[i], meta, self.mapa)
                a.bloqueado(self.filas, self.columnas)
                caminod = a.iniciar() + caminod
        return caminod


    def calcpos(self):
        aux=[]
        for n in self.listobj:
            for elemento in self.listestantes:
                if n in elemento:
                    self.articulos.append(elemento)   
        for n in self.articulos:
            if n[1] % 2 == 0:
                aux = n[0]
                aux =(aux[0] + 1, aux[1])
                self.target.append(aux)

            if n[1] % 2 != 0:
                aux = n[0]
                aux = (aux[0] - 1, aux[1])
                self.target.append(aux)



    def estantes(self, filas, columnas):
        a = 1
        n = 1
        for j in range(columnas):
            b = 1
            for i in range(filas):
                self.listestantes.append(((a, b), n))
                self.listestantes.append(((a + 1, b), n + 1))
                self.listestantes.append(((a, b + 1), n + 2))
                self.listestantes.append(((a + 1, b + 1), n + 3))
                self.listestantes.append(((a, b + 2), n + 4))
                self.listestantes.append(((a + 1, b + 2), n + 5))
                self.listestantes.append(((a, b + 3), n + 6))
                self.listestantes.append(((a + 1, b + 3), n + 7))
                b = b + 6
                n = n + 8
            a = a + 4

class Temple:

    def __init__(self, Ti, Si, enfriamiento, tfinal):
        self.soluini = Si
        self.tempi = Ti
        self.enfriamiento = enfriamiento
        self.tfinal = tfinal
        
    def parametrosrecolector(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas

    def calculo(self, evaluar):
        self.evaluar = evaluar
        q = Recolector(self.evaluar, self.filas, self.columnas)
        costo=q.calcd()
        return costo


    def permutacion(self, x, n):
        i = randint(0, n - 1)
        j = randint(0, n - 1)

        while i == j:
            j = randint(0, n - 1)

        aux = x[j]
        x[j] = x[i]
        x[i] = aux
        return x


    def graficar(self, vector):
        it = len(vector[0])
        tpo = np.linspace(0, 1, it)
        prom = [None] * it
        M = len(vector)

        for i in range(it):
            sum = 0
            for m in range(M):
                plt.plot(tpo, vector[m])
                plt.xlabel("Iteraciones")
                plt.ylabel("Costo")

                sum = sum + vector[m][i]
            prom[i] = sum/M
        plt.plot(tpo, prom, 'b--', label="COSTO PROMEDIO")
        plt.legend(loc=1)
        plt.text(0.6, 75, '150 TEMPLES')
        plt.text(0.6, 72.5, '5 OBJETOS')

        print(prom)
        plt.show()


    def iniciar(self):
        temp = self.tempi
        j = 0
        costo = []
        vect_temperatura = []
        vect_temperatura.append(temp)
        vecinos=[]
        permutado=self.soluini
        vecinos.append(permutado)
        s1=self.calculo(vecinos[0])
        costo.append(s1)

        while temp >= self.tfinal:
            j=j+1
            permutado = self.permutacion(permutado, len(permutado))
            vecinos.append(permutado)
            s2 = self.calculo(vecinos[j])
            if s1 >= s2:
                s1 = s2
            else:
                e=math.exp((s1-s2)/temp)
                if e > random():
                    s1 = s2
                    #print(e)
                    #print(math.exp(((s1-s2)/temp)))


            temp=temp*self.enfriamiento
            vect_temperatura.append(temp)
            costo.append(s1)

        m_costo.append(costo)

        return m_costo

if __name__ == "__main__":
    partida = [0, 0]
    objetos = [7, 48, 28, 31, 15] #, 43, 23, 13, 9, 27, 37, 18, 10, 35, 5
    resultado=[]
    filas = 3
    columnas = 2
    m_sol = []
    m_costo = []

    M=0
    while M<150:
        t = Temple(30000, objetos, 0.8, 0.0000001)
        t.parametrosrecolector(filas, columnas)
        m_costo = t.iniciar()
        M=M+1

    t.graficar(m_costo)

