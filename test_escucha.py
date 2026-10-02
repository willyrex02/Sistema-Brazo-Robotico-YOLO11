import sounddevice as sd
import speech_recognition as sr


MICROFONO = 11
DURACION = 8
FRECUENCIA = 44100


print("====================================")
print("          CONTROL POR VOZ")
print("====================================")
print()

input("Presiona ENTER para comenzar...")

print()
print("🎙️  ESCUCHANDO...")
print("Habla ahora.")
print()

audio = sd.rec(
    int(DURACION * FRECUENCIA),
    samplerate=FRECUENCIA,
    channels=1,
    dtype="int16",
    device=MICROFONO
)

sd.wait()

print()
print("✓ Grabación terminada.")
print("Procesando voz...")
print()

audio_bytes = audio.tobytes()

datos_audio = sr.AudioData(
    audio_bytes,
    FRECUENCIA,
    2
)

reconocedor = sr.Recognizer()

try:

    texto = reconocedor.recognize_google(
        datos_audio,
        language="es-MX"
    )

    print()
    print("🗣️ Tú dijiste:")
    print(f'"{texto}"')

except sr.UnknownValueError:

    print()
    print("❌ No pude entender lo que dijiste.")

except sr.RequestError as error:

    print()
    print("❌ Error al conectar con el servicio de reconocimiento:")
    print(error)