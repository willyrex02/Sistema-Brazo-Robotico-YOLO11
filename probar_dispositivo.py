import sounddevice as sd


MICROFONO = 11

print("Información del dispositivo:")
print("--------------------------------")

dispositivo = sd.query_devices(MICROFONO)

print(dispositivo)