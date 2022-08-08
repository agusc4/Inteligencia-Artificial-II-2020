(define (problem paqueteria-aerea) 
(:domain avionmio)
(:objects 
    GOL01
    NRT
    SP
    EZE
    HND
    FRA
    MAD
    LYS
    CARGA01
    CARGA02
    CARGA04
    CARGA05
    CARGA06
    CARGA07
    CARGA10
    CARGA11
    CARGA12
    CARGA14
    CARGA15
    CARGA16
    CARGA21
    CARGA22
    CARGA23
    CARGA24
    CARGA25
    CARGA26
    CARGA27
    CARGA28
    CARGA29
    
)

(:init
    
    (avion GOL01)    
    (aeropuerto NRT)
    (aeropuerto SP)
    (aeropuerto EZE)
    (aeropuerto HND)
    (aeropuerto FRA)
    (aeropuerto LYS)
    (carga CARGA01)
    (carga CARGA02)
    (carga CARGA04)
    (carga CARGA05)
    (carga CARGA06)
    (carga CARGA07)
    (carga CARGA10)
    (carga CARGA11)
    (carga CARGA12)
    (carga CARGA14)
    (carga CARGA15)
    (carga CARGA16)
    (carga CARGA21)
    (carga CARGA22)
    (carga CARGA23)
    (carga CARGA24)
    (carga CARGA25)
    (carga CARGA26)
    (carga CARGA27)
    (carga CARGA28)
    (carga CARGA29)
       
    (en GOL01 SP)   
    (en CARGA01 NRT)
    (en CARGA02 NRT)
    (en CARGA04 NRT)
    (en CARGA05 HND)
    (en CARGA06 HND)
    (en CARGA07 HND)
    (en CARGA10 EZE)
    (en CARGA11 EZE)
    (en CARGA12 EZE)
    (en CARGA14 LYS)
    (en CARGA15 LYS)
    (en CARGA16 LYS)
    (en CARGA21 FRA)
    (en CARGA22 FRA)
    (en CARGA23 FRA)
    (en CARGA24 FRA)
    (en CARGA25 FRA)
    (en CARGA26 SP)
    (en CARGA27 SP)
    (en CARGA28 SP)
    (en CARGA29 SP)
    
)

(:goal 
    (and
        (en CARGA01 SP)
        (en CARGA02 FRA)
        (en CARGA04 EZE)
        (en CARGA05 SP)
        (en CARGA06 FRA)
        (en CARGA07 LYS)      
        (en CARGA10 LYS)
        (en CARGA11 HND)
        (en CARGA12 NRT)
        (en CARGA14 FRA)
        (en CARGA15 EZE)
        (en CARGA16 NRT)
        (en CARGA21 NRT)
        (en CARGA22 HND)
        (en CARGA23 LYS)
        (en CARGA24 SP)
        (en CARGA25 EZE)
        (en CARGA26 LYS)
        (en CARGA27 HND)
        (en CARGA28 NRT)
        (en CARGA29 EZE)
      
        
    )
)

)
