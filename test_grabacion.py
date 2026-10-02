import sounddevice as sd
from scipy.io.wavfile import write
import time


MICROFONO = 11
DURACION = 8
FRECUENCIA = 48000
CANALES = 2


print("====================================")
print("       PRUEBA DE GRABACIÓN")
print("====================================")
print()

print("Micrófono seleccionado:")
print(sd.query_devices(MICROFONO)["name"])

print()
print("Configuración:")
print(f"Frecuencia: {FRECUENCIA} Hz")
print(f"Canales: {CANALES}")
print()

input("Presiona ENTER para comenzar...")

print()
print("3...")
time.sleep(1)

print("2...")
time.sleep(1)

print("1...")
time.sleep(1)

print()
print("🎙️  GRABANDO AHORA")
print("Habla durante 8 segundos.")
print()

audio = sd.rec(
    int(DURACION * FRECUENCIA),
    samplerate=FRECUENCIA,
    channels=CANALES,
    dtype="int16",
    device=MICROFONO
)

sd.wait()

print()
print("✓ Grabación terminada.")
print()

write(
    "prueba_voz.wav",
    FRECUENCIA,
    audio
)

print("Archivo creado:")
print("prueba_voz.wav")