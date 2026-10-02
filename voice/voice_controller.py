class ControladorVoz:

    def __init__(self):
        self.escuchando = False

    def iniciar_escucha(self):
        self.escuchando = True

        print("Escucha iniciada")

    def detener_escucha(self):
        self.escuchando = False

        print("Escucha detenida")

    def procesar_comando(self, texto):

        texto = texto.lower()

        if "base" in texto and "derecha" in texto:

            return "BASE_DERECHA"

        if "base" in texto and "izquierda" in texto:

            return "BASE_IZQUIERDA"

        if "hombro" in texto and "arriba" in texto:

            return "HOMBRO_ARRIBA"

        if "hombro" in texto and "abajo" in texto:

            return "HOMBRO_ABAJO"

        if "codo" in texto and "arriba" in texto:

            return "CODO_ARRIBA"

        if "codo" in texto and "abajo" in texto:

            return "CODO_ABAJO"

        if "muñeca" in texto and "derecha" in texto:

            return "MUNECA_DERECHA"

        if "muñeca" in texto and "izquierda" in texto:

            return "MUNECA_IZQUIERDA"

        if "abrir" in texto and "garra" in texto:

            return "GARRA_ABRIR"

        if "cerrar" in texto and "garra" in texto:

            return "GARRA_CERRAR"

        if "detener" in texto:

            return "DETENER"

        return None