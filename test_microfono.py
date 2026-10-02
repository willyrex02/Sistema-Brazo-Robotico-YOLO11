import sounddevice as sd


print("Micrófonos/dispositivos de audio disponibles:")
print("---------------------------------------------")

dispositivos = sd.query_devices()

for indice, dispositivo in enumerate(dispositivos):

    if dispositivo["max_input_channels"] > 0:

        print(
            f"{indice}: {dispositivo['name']}"
        )