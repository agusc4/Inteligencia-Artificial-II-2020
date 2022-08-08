import numpy as np
import openpyxl as px
import matplotlib.pyplot as plt

""" Este código se enfoca en los siguientes ítems del Trabajo Práctico:
- Resolución de un problema de Regresión, utilizando ReLU o Sigmoide (con pérdida con MSE)
como función de activación de la capa oculta. Además de Cross-Validation y control de Correlación.
- Utilización de datos obtenidos de un dataset real (VER ABAJO).
- Graficación de la evaluación de la función Loss a lo largo de las EPOCHS."""

# https://archive.ics.uci.edu/ml/datasets/Combined+Cycle+Power+Plant
""" El conjunto de datos contiene 9500 puntos de datos recopilados de una central eléctrica de ciclo
combinado durante 6 años (2006-2011). Las características consisten en las variables ambientales promedio 
por hora: Temperatura (T), Vacío de escape (V), Presión ambiente (AP) y Humedad relativa (RH),
para predecir la producción neta de energía eléctrica (EP) por hora de la planta. """

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
    pe=var_norm[:,4]        ### La última columna es el resultado de cada medición.
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
    
    # h = 1/(1+np.exp(-z)) #Sigmoide
    h = np.maximum(0, z) #ReLU

    # Salida de la red (funcion de activacion lineal).
    y = h.dot(pesos["w2"]) + pesos["b2"]
    return {"z": z, "h": h, "y": y}

def train(x, t,xv,tv, pesos, l_rate, epochs,nv):
    # x (nxm): n ejemplos para m entradas.
    # t (mx1): salida correcta (target) para n ejemplos
    # pesos: pesos (W y b)
    # Cantidad de filas (i.e. cantidad de ejemplos)
    n = len(x)
    LW=[]        ### Vectores para graficar Loss de Train y Valid
    ix=[]
    LWv=[]
    ixv=[]
    val=10000       ### Solo es un valor muy grande, no importa cuánto. Luego se actualiza.
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
        dL_dz[z <= 0] = 0     ### ReLU
        # dh_dz = h.T.dot((1-h))  ### SIGMOIDE. El calculo dL/dz = dL/dh * sigma(x)*(1-sigma(x))
        # dL_dz = dL_dh.dot(dh_dz)### Sigmoide

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

        # Mostramos y validamos solo cada "nv" epochs
        if i %nv == 0:
            print("Training Loss epoch", i, " :", LW[i])
            LWv.append(test(xv,tv,pesos))   ### Función "test" pero con datos de validación
            ixv.append(i)
            print("Loss en validación      :", LWv[k])
            er_abs=(np.abs(LW[i]-LWv[k]))/LW[i]
            if LWv[k] <= val:          ### Actualiza el valor de "Loss" actual
                val=LWv[k]
            elif LWv[k] > (val*1.5):   ### Tolerancia del 50% por oscilación
                if LWv[k] > (val*2):   ### Corto por Overfitting
                    print("\t ERROR - Parada Temprana en epoch", i," por Overfitting (oscilación mayor al 100%).\n")
                    break
                else:
                    ### Advertencia de Overfitting
                    print("\t AVISO - Posible Overfitting (oscilación mayor al 50%).")
            if i>0:                     ### No reviso CORRELATION en la primer EPOCH
                if  (er_abs> 0.2):      ### Diferencia del 20% entre Train. y Valid.
                    if er_abs > 1:      ### Diferencia del 100% - Corta por Correlation
                        print("\t ERROR - Parada Temprana en epoch", i," por no Correlación\n")
                        break
                    else:
                        ### Advertencia de Correlación
                        print("\t AVISO - Posible error de Correlación (mayor al 20%).")
            print("\n")
    plt.figure()
    plt.title("Loss luego del Entrenamiento")
    plt.plot(ix,LW,label="Entrenamiento")
    plt.plot(ixv,LWv,label="Validación")
    plt.legend(loc="upper right")
    plt.show()

def test(xt,tt,pesos):
    n=len(xt)
    valid_ffw = ejec_forw(xt, pesos)
    yt = valid_ffw["y"]
    lwt=np.zeros((n,1))
    LWt=0
    for j in range(n):
        lwt[j]=(tt[j]-yt[j])
        LWt+=(lwt[j]**2)
    LWt/=n
    return LWt

def proceso(param):
    ### Genero los 3 conjuntos de datos, con " param[0] ".
    fi_train=1
    ff_train=int(param[0]*95)
    ff_valid=int(ff_train + (100-param[0])*0.5*95)
    ff_test=9501
    print("Obteniendo datos del archivo adjunto . . .\n")
    x ,t = get_data(fi_train,ff_train)  ### Coinciden las filas finales e inicios porque el código
    xv,tv= get_data(ff_train,ff_valid)  ### de generación aumenta en un la fila inicial.
    xt,tt= get_data(ff_valid,ff_test)

    pesos = inic_pesos(n_entrada=param[1], n_capa_oc=param[2])
    train(x, t, xv, tv, pesos, l_rate=param[3], epochs=param[4], nv=param[5])
    LWt=test(xt,tt,pesos)
    print("Loss en Test: ", LWt)

def inicializar():
    ### Inicializo los valores y parámetros del problema. 
    ### Entrego una sola lista "param" con todos los parámetros.
    param=[]
    PORC_DATA_TRAIN=80  ### param[0]. De 0 a 100. El resto lo divide en 2 para valid y test.
    N_ENTRADA=4         ### param[1]
    N_OCULTAS=91        ### param[2]
    LEARNING_RATE=0.443   ### param[3]
    EPOCHS=500          ### param[4]
    N_valid=EPOCHS/10   ### param[5]

    param.append(PORC_DATA_TRAIN)
    param.append(N_ENTRADA)
    param.append(N_OCULTAS)
    param.append(LEARNING_RATE)
    param.append(EPOCHS)
    param.append(N_valid)
  
    proceso(param)

inicializar()