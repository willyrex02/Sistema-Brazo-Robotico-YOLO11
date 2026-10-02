from voice.speech_output import VozSistema


voz = VozSistema()

print("====================================")
print("       PRUEBA DE VOZ DEL SISTEMA")
print("====================================")
print()

voz.hablar(
    "Hola. Sistema de control por voz activado."
)

voz.hablar(
    "Ok. Moviendo la base a la derecha."
)

print()
print("✓ Prueba terminada.")