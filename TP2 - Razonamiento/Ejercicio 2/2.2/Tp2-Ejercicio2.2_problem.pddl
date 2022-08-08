(define (problem pedidos)
    (:domain cremas)
    (:objects
        crema_corporal
        crema_dia
        crema_noche
        crema_exfoliante
        paquete1
        paquete2
        paquete3
        paquete4
        paquete5
        estante_corporal
        estante_dia
        estante_noche
        estante_exfoliante
        OK
    )

    (:init

        (tipo-crema crema_corporal)
        (tipo-crema crema_dia)
        (tipo-crema crema_noche)
        (tipo-crema crema_exfoliante)

        (ubicacion estante_corporal)
        (ubicacion estante_dia)
        (ubicacion estante_noche)
        (ubicacion estante_exfoliante)

        (agarre OK)

        (paquete paquete1)
        (paquete paquete2)
        (paquete paquete3)
        (paquete paquete4)
        (paquete paquete5)

        (en crema_corporal estante_corporal)
        (en crema_dia estante_dia)
        (en crema_noche estante_noche)
        (en crema_exfoliante estante_exfoliante)
    )

    (:goal
            ;Paquete 1: Coroporal, Dia, Noche
            ;Paquete 2: Dia, Noche, Exfoliante
            ;Paquete 3: Corporal, Dia, Noche, Exfoliante
            ;Paquete 4: Dia, Noche
            ;Paquete 5: Exfoliante
            
        (and
            (en crema_corporal paquete1)
            (en crema_dia paquete1)
            (en crema_exfoliante paquete1)

            (en crema_dia paquete2)
            (en crema_noche paquete2)
            (en crema_exfoliante paquete2)

            (en crema_corporal paquete3)
            (en crema_dia paquete3)
            (en crema_noche paquete3)
            (en crema_exfoliante paquete3)

            (en crema_dia paquete4)
            (en crema_noche paquete4)

            (en crema_exfoliante paquete5)
        )
    )
)