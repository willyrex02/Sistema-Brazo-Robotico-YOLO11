import sounddevice as sd
import speech_recognition as sr
import numpy as np
import time

from voice.voice_controller import ControladorVoz


# ==========================================
# CONFIGURACIÓN DEL MICRÓFONO
# ==========================================

MICROFONO = 11
DURACION = 8
FRECUENCIA = 48000
CANALES = 2


# ==========================================
# CONTROLADOR DE COMANDOS
# ==========================================

controlador = ControladorVoz()


# ==========================================
# ENCABEZADO
# ==========================================

print()
print("============================================")
print("          CONTROL POR VOZ - PRUEBA")
print("============================================")
print()

print("Micrófono:")
print(sd.query_devices(MICROFONO)["name"])

print()

input("Presiona ENTER para comenzar...")


# ==========================================
# CUENTA REGRESIVA
# ==========================================

print()

print("3...")
time.sleep(1)

print("2...")
time.sleep(1)

print("1...")
time.sleep(1)

print()
print("🎙️  ESCUCHANDO...")
print("Habla ahora.")
print()


# ==========================================
# GRABAR AUDIO
# ==========================================

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
print("Procesando voz...")
print()


# ==========================================
# CONVERTIR ESTÉREO → MONO
# ==========================================

audio_mono = np.mean(
    audio,
    axis=1
).astype(np.int16)


audio_bytes = audio_mono.tobytes()


# ==========================================
# CREAR AUDIO PARA SPEECHRECOGNITION
# ==========================================

datos_audio = sr.AudioData(
    audio_bytes,
    FRECUENCIA,
    2
)


# ==========================================
# RECONOCIMIENTO
# ==========================================

reconocedor = sr.Recognizer()


try:

    texto = reconocedor.recognize_google(
        datos_audio,
        language="es-MX"
    )

    print("🗣️ Tú dijiste:")
    print()
    print(f'   "{texto}"')
    print()


    # ======================================
    # INTERPRETAR COMANDO
    # ======================================

    comando = controlador.procesar_comando(
        texto
    )


    if comando:

        print("✓ COMANDO RECONOCIDO")
        print()
        print(f"   {comando}")
        print()


    else:

        print("⚠️ No reconocí un comando del brazo.")
        print()


except sr.UnknownValueError:

    print("❌ No pude entender lo que dijiste.")


except sr.RequestError as error:

    print("❌ Error al conectar con el reconocimiento de voz.")
    print(error)