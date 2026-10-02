from robot.robot_controller import ControladorBrazo


brazo = ControladorBrazo()


print("===================================")
print("       PRUEBA CONTROL BRAZO")
print("===================================")
print()


print("Posiciones iniciales:")
print(brazo.posiciones)

print()

print("Moviendo base a la derecha...")
brazo.base_derecha()

print()

print("Moviendo base a la derecha...")
brazo.base_derecha()

print()

print("Moviendo hombro arriba...")
brazo.hombro_arriba()

print()

print("Abriendo garra...")
brazo.abrir_garra()

print()

print("Posiciones actuales:")
print(brazo.posiciones)

print()

print("Regresando a posición inicial...")
brazo.posicion_inicial()

print()

print("Posiciones finales:")
print(brazo.posiciones)