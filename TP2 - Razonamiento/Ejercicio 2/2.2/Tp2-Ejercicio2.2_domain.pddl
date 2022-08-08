(define (domain cremas)
    (:predicates 
        (en ?a ?b)
        (tipo-crema ?crema)
        (ubicacion ?est)
        (paquete ?num_paq)
        (agarre ?pinza)
    )
    
    (:action agarrar
        :parameters (?crema ?estante ?pinza)
        :precondition (and (en ?crema ?estante) (tipo-crema ?crema) (ubicacion ?estante) (agarre ?pinza))
        :effect (and (en ?crema ?pinza))
    )    

    (:action colocar
        :parameters (?crema ?num_paq ?pinza)
        :precondition (and (en ?crema ?pinza) (tipo-crema ?crema) (paquete ?num_paq) (agarre ?pinza))
        :effect (and (not (en ?crema ?pinza)) (en ?crema ?num_paq))
    )
    
)