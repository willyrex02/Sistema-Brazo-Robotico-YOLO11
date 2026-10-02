class ControladorBrazo:

    def __init__(self):

        # =====================================
        # POSICIONES INICIALES
        # =====================================

        self.posiciones = {

            "BASE": 90,
            "HOMBRO": 90,
            "CODO": 90,
            "MUÑECA": 90,
            "MANO": 90,
            "GARRA": 90

        }

        # Límites de seguridad
        self.limites = {

            "BASE": (0, 180),
            "HOMBRO": (0, 180),
            "CODO": (0, 180),
            "MUÑECA": (0, 180),
            "MANO": (0, 180),
            "GARRA": (0, 180)

        }

    # =====================================
    # MOVER ARTICULACIÓN
    # =====================================

    def mover(self, articulacion, grados):

        if articulacion not in self.posiciones:

            print(
                f"⚠️ Articulación desconocida: {articulacion}"
            )

            return False

        minimo, maximo = self.limites[articulacion]

        nueva_posicion = (
            self.posiciones[articulacion]
            + grados
        )

        # =================================
        # SEGURIDAD
        # =================================

        nueva_posicion = max(
            minimo,
            min(maximo, nueva_posicion)
        )

        self.posiciones[articulacion] = nueva_posicion

        print(
            f"🤖 {articulacion}: "
            f"{nueva_posicion}°"
        )

        return True

    # =====================================
    # MOVIMIENTOS
    # =====================================

    def base_derecha(self):

        return self.mover(
            "BASE",
            5
        )

    def base_izquierda(self):

        return self.mover(
            "BASE",
            -5
        )

    def hombro_arriba(self):

        return self.mover(
            "HOMBRO",
            5
        )

    def hombro_abajo(self):

        return self.mover(
            "HOMBRO",
            -5
        )

    def codo_arriba(self):

        return self.mover(
            "CODO",
            5
        )

    def codo_abajo(self):

        return self.mover(
            "CODO",
            -5
        )

    def muneca_derecha(self):

        return self.mover(
            "MUÑECA",
            5
        )

    def muneca_izquierda(self):

        return self.mover(
            "MUÑECA",
            -5
        )

    # =====================================
    # GARRA
    # =====================================

    def abrir_garra(self):

        return self.mover(
            "GARRA",
            5
        )

    def cerrar_garra(self):

        return self.mover(
            "GARRA",
            -5
        )

    # =====================================
    # POSICIÓN INICIAL
    # =====================================

    def posicion_inicial(self):

        for articulacion in self.posiciones:

            self.posiciones[articulacion] = 90

        print(
            "🏠 Brazo regresando a posición inicial"
        )

    # =====================================
    # DETENER
    # =====================================

    def detener(self):

        print(
            "🛑 BRAZO DETENIDO"
        )