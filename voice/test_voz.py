from voice.voice_controller import ControladorVoz


controlador = ControladorVoz()


comandos = [
    "brazo mueve la base a la derecha",
    "brazo mueve la base a la izquierda",
    "sube el hombro",
    "baja el hombro",
    "abre la garra",
    "cierra la garra",
    "detener brazo"
]


for texto in comandos:

    resultado = controlador.procesar_comando(texto)

    print(
        f"Texto: {texto}"
    )

    print(
        f"Comando: {resultado}"
    )

    print("----------------------")