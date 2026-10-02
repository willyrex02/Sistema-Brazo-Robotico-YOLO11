import pyttsx3


class VozSistema:

    def __init__(self):
        pass

    def hablar(self, mensaje):

        print(f"🔊 Sistema: {mensaje}")

        motor = pyttsx3.init()

        motor.setProperty(
            "rate",
            165
        )

        motor.setProperty(
            "volume",
            1.0
        )

        motor.say(mensaje)

        motor.runAndWait()

        motor.stop()