import sounddevice as sd

MICROFONO = 11

print("====================================")
print("       INFORMACIÓN DEL MICRÓFONO")
print("====================================")

try:
    print()
    print(sd.query_devices(MICROFONO))

    print()
    print("Probando dispositivo...")

    sd.check_input_settings(
        device=MICROFONO,
        channels=1,
        samplerate=44100
    )

    print("✅ El dispositivo acepta esta configuración.")

except Exception as e:

    print()
    print("❌ ERROR:")
    print(e)