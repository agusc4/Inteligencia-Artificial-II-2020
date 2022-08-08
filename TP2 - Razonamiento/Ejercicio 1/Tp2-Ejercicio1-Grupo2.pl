        /* Axiomas (invariantes del dominio) */

    diagnosticar():-
        tot(); writeln('Ingrese "menu." para mas opciones').        
    menu() :-
        writeln('\n'),
        writeln('\t Evaluacion y Mantenimiento de la Valvula de Seguridad de la Estacion.\nObtener pasos a seguir en base al diagnostico: \n'),
        writeln('\t 1 - Espesor de la valvula y oxidacion.\n\t 2 - Funcionamiento del piloto.
    \t 3 - Fuga de gas en la union asiento-orificio.\n\t 4 - Diagnostico COMPLETO (pueden repetirse pasos).\n'), read(Opcion), ejec(Opcion).
    ejec(Opcion):-  Opcion==1, rIzq(), menu();
                    Opcion==2, rCen(), menu();
                    Opcion==3, rDer(), menu();
                    Opcion==4, tot(), menu();
                    (Opcion=\=1,Opcion=\=2, Opcion=\=3, Opcion=\=4),writeln('Revision finalizada (Reingrese "menu." para otro diagnostico).');
                    writeln('    '), menu().
                    
rIzq():-  verificar(thickness_less_than_the_treshold_limit).
rCen():-  verificar(piloto).
rDer():-  verificar(leakage_fixed_with_the_wrench_at_joints).                  
tot():-
    verificar(thickness_less_than_the_treshold_limit), verificar(effects_of_dazzling_and_rusting),
    verificar(piloto),verificar(leakage_prevention_between_sit_and_orifice),verificar(safety_valve_spring),
    verificar(control_valve_sensors_blocked),verificar(valve_status_closed), verificar(relief_valve_ok_with_10_percent_more_pressure),
    verificar(safety_valve_has_continuous_evacuation),verificar(preventable_leakage_between_sit_and_orifice),
    verificar(safety_spring_effective),verificar(control_and_pressure_sensor_pipes_blocked),verificar(apropiate_line_gas_pressure),
    verificar(leakage_fixed_with_the_wrench_at_joints),verificar(gas_leakage_at_joint).

desconocido(X):- estado(X, D), D==desconocido.  /* Entrega todos los estados no conocidos. */

/* rama izquierda*/
verificar(thickness_less_than_the_treshold_limit):-
    estado(thickness_less_than_the_treshold_limit, yes), writeln('Sin efectos de deterioro externo.\n
        Espesor menor al limite. Reportar equipo para inspeccion inmediata.');
    estado(thickness_less_than_the_treshold_limit, no), writeln('Sin efectos de deterioro externo.\n
        Espesor mayor al limite. La condicion del equipo es adecuada.');
    (estado(thickness_less_than_the_treshold_limit,desconocido),writeln('Verificar el espesor de la valvula.')),
    (estado(effects_of_dazzling_and_rusting,no); verificar(effects_of_dazzling_and_rusting)).

verificar(effects_of_dazzling_and_rusting):-
    estado(effects_of_dazzling_and_rusting, yes), writeln('Hay efectos de deterioro externo. Se requiere mantenimiento de pintura.');
    estado(effects_of_dazzling_and_rusting, desconocido), writeln('Verificar si hay oxidacion o deslumbre en el exterior de la unidad.').

/* rama central izquierda*/
verificar(piloto) :- 
    estado(piloto, yes), writeln('El piloto funciona correctamente, ajustar valvula de seguridad segun instrucciones.');
    estado(piloto, no), writeln('Realizar un servicio completo al piloto y reinstalar.');
    estado(piloto, desconocido), writeln('Verificar el estado del piloto.'),
    (estado(leakage_prevention_between_sit_and_orifice, yes),writeln('Hay una fuga de prevención entre asiento-orificio.');
    verificar(leakage_prevention_between_sit_and_orifice)).
                
verificar(leakage_prevention_between_sit_and_orifice) :- 
    estado(leakage_prevention_between_sit_and_orifice, no), writeln('Reemplazar asiento-orificio y poner valvula en circuito.');
    estado(leakage_prevention_between_sit_and_orifice, desconocido), writeln('Verificar prevencion de fuga entre asiento y orificio.'),
    (estado(safety_valve_spring, yes), writeln('Correcto funcionamiento del resorte de seguridad.'); 
    verificar(safety_valve_spring)).

verificar(safety_valve_spring) :- 
    estado(safety_valve_spring, no), writeln('Dar mantenimiento al resorte de seguridad y la valvula.');
    estado(safety_valve_spring, desconocido), writeln('Verificar el resorte de la valvula de seguridad.'), 
    (estado(control_valve_sensors_blocked, no); 
    verificar(control_valve_sensors_blocked)).

verificar(control_valve_sensors_blocked) :- 
    estado(control_valve_sensors_blocked, yes), writeln('Tuberias de control y sensado de presion BLOQUEADAS. Limpiar y revisar las tuberias de sensado.');
    estado(control_valve_sensors_blocked, desconocido), writeln('Verificar los sensores de la valvula de control.'),
    (estado(valve_status_closed, no); verificar(valve_status_closed)).
                
verificar(valve_status_closed) :- 
    estado(valve_status_closed, yes), writeln('Colocar valvula de seguridad en posicion "Abierta".');
    estado(valve_status_closed, desconocido), writeln('Verificar el Estado de la valvula de seguridad.'),
    (estado(relief_valve_ok_with_10_percent_more_pressure, no); verificar(relief_valve_ok_with_10_percent_more_pressure)).
                
verificar(relief_valve_ok_with_10_percent_more_pressure) :- 
    estado(relief_valve_ok_with_10_percent_more_pressure, yes), writeln('Funcionamiento alivio ante sobrepesion del 10%, APROPIADO.'); 
    estado(relief_valve_ok_with_10_percent_more_pressure, desconocido),
    writeln('Verificar valvula de alivio ante incremento del 10% de presion.'),
    (estado(safety_valve_has_continuous_evacuation, no);verificar(safety_valve_has_continuous_evacuation)).
            
verificar(safety_valve_has_continuous_evacuation) :- 
    estado(safety_valve_has_continuous_evacuation, desconocido), 
    writeln('Verificar la evacuacion de la valvula de escape.').

/* rama central derecha*/

verificar(preventable_leakage_between_sit_and_orifice) :-
    estado(preventable_leakage_between_sit_and_orifice, no), writeln('Reemplazar asiento-orificio y poner valvula en circuito.');
    estado(preventable_leakage_between_sit_and_orifice, yes), writeln('Hay una fuga prevenible entre asiento- orificio.\n
        Ajustar la valvula de seguridad según las instrucciones.');
    estado(preventable_leakage_between_sit_and_orifice, desconocido),writeln('Verificar la fuga prevenible entre asiento-orificio.'),
    (estado(safety_spring_effective, yes);verificar(safety_spring_effective)).

verificar(safety_spring_effective):-
    estado(safety_spring_effective,no), writeln('Reemplazar el resorte de seguridad.');
    estado(safety_spring_effective, desconocido), writeln('Verificar la efectividad del resorte de seguridad.'),
    ( estado(control_and_pressure_sensor_pipes_blocked, no); verificar(control_and_pressure_sensor_pipes_blocked)).

verificar(control_and_pressure_sensor_pipes_blocked) :-
    estado(control_and_pressure_sensor_pipes_blocked, yes), writeln('Tuberias de control y sensado de presion BLOQUEADAS. Limpiar y reparar fallas de las tuberias de sensado.');
    estado(control_and_pressure_sensor_pipes_blocked, desconocido),writeln('Verificar las tuberias de control y sensado de presion.'),
    ( estado(apropiate_line_gas_pressure,yes); verificar(apropiate_line_gas_pressure)).

verificar(apropiate_line_gas_pressure) :-
    estado(apropiate_line_gas_pressure, no), writeln('Ajustar regulador de presion de linea de acuerdo a las instrucciones.');
    estado(apropiate_line_gas_pressure, desconocido),writeln('Verificar la presion de linea de gas.'),
    (estado(safety_valve_has_continuous_evacuation,yes), writeln('Valvula de seguridad posee una evacuacion continua.');
    verificar(safety_valve_has_continuous_evacuation)).


/* rama derecha*/

verificar(leakage_fixed_with_the_wrench_at_joints):-
    estado(leakage_fixed_with_the_wrench_at_joints, yes), writeln('Fuga corregida con una llave, en la unión.\n
        Reportar a la Unidad de Inspeccion Tecnica.');
    estado(leakage_fixed_with_the_wrench_at_joints, no), writeln('Enviar reporte al departamento de reparaciones para solucionar la falla.');
    estado(leakage_fixed_with_the_wrench_at_joints, desconocido),
    writeln('Verificar la correccion de la fuga en la union, con una llave inglesa.'),
    (estado(gas_leakage_at_joint,yes);verificar(gas_leakage_at_joint)).

verificar(gas_leakage_at_joint):-
    estado(gas_leakage_at_joint, no), writeln('La valvula de seguridad esta libre de perdidas de gas.');
    estado(gas_leakage_at_joint, desconocido), writeln('Verificar la fuga de gas en la union.').

/* Ground Facts de instancia variables (podrian resolverse mediante sensado, de forma externa a la consola actual;
    o agregando la información interactivamente por un usuario a través de la consola a la base de conocimientos )). */

/* rama izquierda*/
estado(thickness_less_than_the_treshold_limit,desconocido).
estado(effects_of_dazzling_and_rusting,desconocido).
/* rama central izquierda*/
estado(piloto, yes).
estado(leakage_prevention_between_sit_and_orifice, no).
estado(safety_valve_spring, yes).
estado(control_valve_sensors_blocked, yes).
estado(valve_status_closed, no).
estado(relief_valve_ok_with_10_percent_more_pressure, no).
/* rama central derecha*/
estado(preventable_leakage_between_sit_and_orifice,desconocido).
estado(safety_valve_spring,desconocido).
estado(control_and_pressure_sensor_pipes_blocked, desconocido).
estado(apropiate_line_gas_pressure, desconocido).
estado(safety_valve_has_continuous_evacuation, no).
/* rama derecha*/
estado(leakage_fixed_with_the_wrench_at_joints, desconocido).
estado(gas_leakage_at_joint,no).
