import numpy as np
import openpyxl as px
import matplotlib.pyplot as plt

""" Este código se enfoca en los siguientes ítems del Trabajo Práctico:
    - Resolución de un problema de Regresión, utilizando ReLU o Sigmoide (con pérdida con MSE)
    como función de activación de la capa oculta. Además de Cross-Validation y control de Correlación.
    - Utilización de datos obtenidos de un dataset real (VER ABAJO).
    - Graficación de la evaluación de la función Loss a lo largo de las EPOCHS.
    - Realizar un Barrido de Parámetros del algoritmo."""

""" El conjunto de datos contiene 9500 puntos de datos recopilados de una central eléctrica 
    de ciclo combinado durante 6 años (2006-2011). Las características consisten en las 
    variables ambientales promedio por hora: Temperatura (T), Vacío de escape (V),
    Presión ambiente (AP) y Humedad relativa (RH), para predecir la producción neta 
    de energía eléctrica (EP) por hora de la planta. """

def get_data(fila_inicial,fila_final):
    ### Abre el archivo con los datos. Guarda las variables de entrada en "var" y su resultado,
    ### la salida, como "pe".
    arc = px.load_workbook('Dat9500.xlsx')
    data=arc["Sheet1"]
    dim=int(fila_final-fila_inicial)
    var=np.zeros((dim, 5))
    i=0
    ini=fila_inicial
    fin=fila_final
    for row in data.rows:
        j=0
        for cell in row:
            if ini < fin:
                var[i][j]=data.cell(row=ini+1,column=j+1).value
            j+=1
        i+=1
        ini+=1
    ### Normalizo y centro todas las variables para que estén en escalas iguales.
    var_cen = var - var.mean(axis=0)
    var_norm = var_cen / var_cen.max(axis=0)
    variables=var_norm[:,0:4]
    pe=var_norm[:,4]        ### La última columna es el resultado (target) de cada ejemplo.
    arc.close()
    return variables,pe

def inic_pesos(n_entrada, n_capa_oc):
    randomgen = np.random.default_rng()

    w1 = 0.1 * randomgen.standard_normal((n_entrada, n_capa_oc))
    b1 = 0.1 * randomgen.standard_normal((1, n_capa_oc))

    w2 = 0.1 * randomgen.standard_normal((n_capa_oc,1))
    b2 = 0.1 * randomgen.standard_normal((1,1))

    return {"w1": w1, "b1": b1, "w2": w2, "b2": b2}

def ejec_forw(x,pesos):
    # Funcion de entrada (a.k.a. "regla de propagacion") para la primera capa oculta
    z = x.dot(pesos["w1"]) + pesos["b1"]
    # Funcion de activacion Sigmoide ( h=f(z) )
    #h = 1/(1+np.exp(-z))
    #funcion activacion relu
    h = np.maximum(0, z)
    # Salida de la red (funcion de activacion lineal).
    y = h.dot(pesos["w2"]) + pesos["b2"]
    return {"z": z, "h": h, "y": y}

def test(xt,tt,pesos):
    n=len(xt)
    test_ffw = ejec_forw(xt, pesos)
    yt = test_ffw["y"]
    lwt=np.zeros((n,1))
    LWt=0
    for j in range(n):
        lwt[j]=(tt[j]-yt[j])
        LWt+=(lwt[j]**2)
    LWt/=n
    return LWt

def train(x, t,xv,tv, pesos, graf, l_rate, epochs,nv):
    # x (nxm): n ejemplos para m entradas.
    # t (nx1): salida correcta (target) para n ejemplos
    # pesos: pesos (W y b)
    # Cantidad de filas (i.e. cantidad de ejemplos)
    n = len(x)
    LW=[]        ### Vectores para graficar Loss de Train y Valid
    ix=[]
    LWv=[]
    ixv=[]
    val=10000    ### Solo es un valor muy grande, no importa cuánto. Luego se actualiza.
    k=-1
    for i in range(epochs+1):
        # Ejecucion de la red hacia adelante
        res_ffw = ejec_forw(x, pesos)
        y = res_ffw["y"]
        h = res_ffw["h"]
        z = res_ffw["z"]
        # LOSS
        ### Calculo de la funcion de perdida global con MSE.
        lw=np.zeros((n,1))
        aux=0
        for j in range(n):
            lw[j]=(t[j]-y[j])
            aux+=(lw[j]**2)
        aux/=n
        LW.append(aux)
        ix.append(i)

        # Extraemos los pesos a variables locales
        w1 = pesos["w1"]
        b1 = pesos["b1"]
        w2 = pesos["w2"]
        b2 = pesos["b2"]

        # Ajustamos los pesos: Backpropagation
        ### Corregidas derivadas al utilizar MSE y la función Sigmoide o ReLU como 
        ### activación de la capa oculta.
        dL_dy = -2*lw/n
        dL_dw2 = h.T.dot(dL_dy)                         # Ajuste para w2
        dL_db2 = np.sum(dL_dy, axis=0, keepdims=True)   # Ajuste para b2
        dL_dh = dL_dy.dot(w2.T)        
        
        dL_dz = dL_dh         ### Para usar ReLU
        dL_dz[z <= 0] = 0     ###  ReLU
        #dh_dz = h.T.dot((1-h))  ### SIGMOIDE. El calculo dL/dz = dL/dh * sigma(x)*(1-sigma(x))
        #dL_dz = dL_dh.dot(dh_dz)### Sigmoide

        dL_dw1 = x.T.dot(dL_dz)                         # Ajuste para w1
        dL_db1 = np.sum(dL_dz, axis=0, keepdims=True)   # Ajuste para b1

        # Aplicamos el ajuste a los pesos (Gradiente Descendiente)
        w1 += -l_rate * dL_dw1
        b1 += -l_rate * dL_db1
        w2 += -l_rate * dL_dw2
        b2 += -l_rate * dL_db2

        # Actualizamos la estructura de pesos
        pesos["w1"] = w1
        pesos["b1"] = b1
        pesos["w2"] = w2
        pesos["b2"] = b2

        ### Mostramos y validamos solo cada "nv" epochs
        if i %nv == 0:
            # print("Training Loss EPOCH", i, " :", LW[i])
            LWv.append(test(xv,tv,pesos))   ### Función "test" pero con datos de validación
            ixv.append(i)
            # print("Loss en validación      :", LWv[k])
            er_abs=(np.abs(LW[i]-LWv[k]))/LW[i]
            if LWv[k] <= val:          ### Actualiza el valor de "Loss" actual
                val=LWv[k]
            elif LWv[k] > (val*1.5):   ### Tolerancia del 50% por oscilación
                if LWv[k] > (val*2):   ### Corto por Overfitting
                    print("\t ERROR - Parada Temprana en EPOCH", i," por Overfitting (oscilación mayor al 100%).")
                    break
                else:
                    ### Advertencia de Overfitting
                    print("\t AVISO - Posible Overfitting (oscilación mayor al 50%).")
            if i>0:                     ### No reviso CORRELATION en la primer EPOCH
                if  (er_abs> 0.2):      ### Diferencia del 20% entre Train. y Valid.
                    if er_abs > 1:      ### Diferencia del 100% - Corta por Correlation
                        print("\t ERROR - Parada Temprana en EPOCH", i," por no Correlación.")
                        break
                    else:
                        ### Advertencia de Correlación
                        print("\t AVISO - Posible error de Correlación (mayor al 20%).")
    if graf:
        plt.figure()
        plt.title("Loss luego del Entrenamiento")
        plt.plot(ix,LW,label="Entrenamiento")
        plt.plot(ixv,LWv,label="Validación")
        plt.legend(loc="upper right")
        plt.show()
    print ("Menor LOSS en entrenamiento:",LW[i][0])
    return LW[i][0]
    
def proceso(param,DATA,ultimo=False):
    ### Guardo los datos en variables locales
    x = DATA["x"]
    t = DATA["t"]
    xv = DATA["xv"]
    tv = DATA["tv"]
    xt = DATA["xt"]
    tt = DATA["tt"]
    graf=ultimo     ### Solo grafica en la ejecución final
    pesos = inic_pesos(n_entrada=param[1], n_capa_oc=param[2])
    valor=train(x, t, xv, tv, pesos, graf,l_rate=param[3], epochs=param[4], nv=param[5])
    if ultimo==True:
        LWt=test(xt,tt,pesos)
        print("Loss en Test: ", LWt)
    return valor

def barrido(hip,DATA): ##parametros 1 corresponden a learning rate. parametros 2 corresponden a N_capa_oculta
    ini1=hip[0]
    ini2=int(hip[1])
    final1=hip[2]
    final2=int(hip[3])
    step1=hip[4]
    step2=int(hip[5])
    param=hip[6]
    registro=[100000,0,0]   ### Variable a actualizar en la ejecución
    if ini1<0: #if para asegurarse no salir de los extremos deseados
        ini1=0.001  # Mínimo Learning Rate
    if ini2<0:
        ini2=1      # Mínimas neuronas
    if final1>1:
        final1=1
    n1=int((final1-ini1)/step1)
    n2=int((final2-ini2)/step2)
    learn=np.linspace(ini1,final1,n1)
    neur=np.linspace(ini2,final2,n2)
    for i in learn:
        param[3]=i
        for j in neur:
            param[2]=int(j)
            print("Learning rate actual: {0:.3f}".format(i))
            print("N° nuer. ocu. actual:",int(j))
            aux=proceso(param,DATA)
            if aux<registro[0]:
                registro[0]=aux
                registro[1]=i
                registro[2]=int(j)
            print("Actualización de registro:",registro,"\n")
    return registro
        
def inicializar():
    ### Inicializo los valores y parámetros del problema. 
    ### Entrego una sola lista "param" con todos los parámetros.
    param=[]
    PORC_DATA_TRAIN=80  ### param[0]. De 0 a 100. El resto lo divide en 2 para valid y test.
    N_ENTRADA=4         ### param[1]
    N_OCULTAS=1         ### param[2]
    LEARNING_RATE=0.1   ### param[3]
    EPOCHS=500          ### param[4]
    N_valid=EPOCHS/10   ### param[5]

    param.append(PORC_DATA_TRAIN)
    param.append(N_ENTRADA)
    param.append(N_OCULTAS)
    param.append(LEARNING_RATE)
    param.append(EPOCHS)
    param.append(N_valid)

    ### Genero los 3 conjuntos de datos, con " param[0] ", por única vez.
    fi_train=1
    ff_train=int(param[0]*95)
    ff_valid=int(ff_train + (100-param[0])*0.5*95)
    ff_test=9501
    print("Obteniendo datos del archivo adjunto . . .\n")
    x ,t = get_data(fi_train,ff_train)  ### Coinciden las filas finales e inicialess porque el código
    xv,tv= get_data(ff_train,ff_valid)  ### de generación aumenta en uno la fila inicial.
    xt,tt= get_data(ff_valid,ff_test)
    DATA={"x": x, "t": t, "xv": xv, "tv": tv, "xt": xt, "tt": tt} ### Dic. de datos

    ### hiper...=[ini1, ini2, final1, final2, step1, step2, param]
    hiperparametros=[LEARNING_RATE,N_OCULTAS,1.1,101,0.1,10,param]
    au=barrido(hiperparametros,DATA)    # Primer barrido de parametros. Con sus valores, 
    hiperparametros[0]=au[1]-0.25       # q serian los mejores, armo un intervalo
    hiperparametros[1]=au[2]-10         # con paso mas pequeño alrededor de ese punto.
    hiperparametros[2]=au[1]+0.25
    hiperparametros[3]=au[2]+10
    hiperparametros[4]=0.01
    hiperparametros[5]=1
    print("Un barrido completo. Registro:",au,"\n")
    au2=barrido(hiperparametros,DATA)   # Segundo barrido con paso mas pequeño
    param[2]=au2[2]     ### Actualizo los últimos valores obtenidos
    param[3]=au2[1]
    proceso(param,DATA,True)  # Por ultimo con el mejor par de valores encontrado
    # corro el proceso pero con los datos de testeo incluidos
    print("Mejor Learning Rate: {0:.3f}".format(param[3]))
    print("Neuronas capa ocul.: ", param[2],"\n")

inicializar()