import sys
from pathlib import Path

import cv2
import serial
import time

from ultralytics import YOLO

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Ruta del modelo YOLO11 entrenado
MODEL_PATH = Path(__file__).resolve().parent / "modelo" / "best.pt"

# Cámara principal
CAMERA_INDEX = 0

# Confianza mínima para mostrar una detección
CONF_THRESHOLD = 0.5

# ============================================================
# CONFIGURACIÓN ESP32
# ============================================================

SERIAL_PORT = "COM3"
SERIAL_BAUDRATE = 115200


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        # ====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # ====================================================

        self.setWindowTitle(
            "Sistema Inteligente de Clasificación de Plátanos"
        )

        self.resize(1400, 800)

        # ====================================================
        # VARIABLES DEL SISTEMA
        # ====================================================

        self.model = None
        self.cap = None

        self.yolo_activo = False
        self.camara_activa = False

        # ====================================================
        # CONTROL DEL BRAZO
        # ====================================================

        self.esp32 = None

        self.pos_base = 180
        self.pos_hombro = 89
        self.pos_codo = 74
        self.pos_muneca = 70
        self.pos_mano = 0
        self.pos_garra = 50

        # ====================================================
        # CREAR INTERFAZ
        # ====================================================

        self.crear_interfaz()

        self.conectar_esp32()

        # ====================================================
        # CARGAR YOLO
        # ====================================================

        self.cargar_modelo()

        # ====================================================
        # INICIAR CÁMARA
        # ====================================================

        self.iniciar_camara()

        # ====================================================
        # TEMPORIZADOR PARA ACTUALIZAR VIDEO
        # ====================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.actualizar_video
        )

        self.timer.start(30)

    # ========================================================
    # MOVIMIENTO DE SERVOS
    # ========================================================

    def mover_base(self, cambio):

        nueva_posicion = self.pos_base + cambio

        nueva_posicion = max(
            0,
            min(180, nueva_posicion)
        )

        self.pos_base = nueva_posicion

        self.enviar_comando(
            f"BASE:{self.pos_base}"
        )

        self.base_angulo.setText(
            f"Ángulo: {self.pos_base}°"
        )

        self.estado_brazo.setText(
            "Brazo       ● Moviendo base"
        )

    def mover_hombro(self, cambio):

        nueva_posicion = self.pos_hombro + cambio

        nueva_posicion = max(
            89,
            min(169, nueva_posicion)
        )

        self.pos_hombro = nueva_posicion

        self.enviar_comando(
            f"HOMBRO:{self.pos_hombro}"
        )

        self.hombro_angulo.setText(
            f"Ángulo: {self.pos_hombro}°"
        )

        self.estado_brazo.setText(
            "Brazo       ● Moviendo hombro"
        )

    def mover_codo(self, cambio):

        nueva_posicion = self.pos_codo + cambio

        nueva_posicion = max(
            74,
            min(151, nueva_posicion)
        )

        self.pos_codo = nueva_posicion

        self.enviar_comando(
            f"CODO:{self.pos_codo}"
        )

        self.codo_angulo.setText(
            f"Ángulo: {self.pos_codo}°"
        )

        self.estado_brazo.setText(
            "Brazo       ● Moviendo codo"
        )

    def mover_muneca(self, cambio):

        nueva_posicion = self.pos_muneca + cambio

        nueva_posicion = max(
            70,
            min(180, nueva_posicion)
        )

        self.pos_muneca = nueva_posicion

        self.enviar_comando(
            f"MUNECA:{self.pos_muneca}"
        )

        self.muneca_angulo.setText(
            f"Ángulo: {self.pos_muneca}°"
        )

        self.estado_brazo.setText(
            "Brazo       ● Moviendo muñeca"
        )

    def abrir_garra(self):

        self.pos_garra = 100

        self.enviar_comando(
            "GARRA:100"
        )

        self.garra_angulo.setText(
            "Estado: Abierta"
        )

        self.estado_brazo.setText(
            "Brazo       ● Garra abierta"
        )

    def cerrar_garra(self):

        self.pos_garra = 50

        self.enviar_comando(
            "GARRA:50"
        )

        self.garra_angulo.setText(
            "Estado: Cerrada"
        )

        self.estado_brazo.setText(
            "Brazo       ● Garra cerrada"
        )

    # ========================================================
    # CONECTAR ESP32
    # ========================================================

    def conectar_esp32(self):

        try:

            self.esp32 = serial.Serial(
                SERIAL_PORT,
                SERIAL_BAUDRATE,
                timeout=1
            )

            time.sleep(2)

            self.estado_esp32.setText(
                "ESP32       ● Conectado"
            )

            print(
                "ESP32 conectado correctamente."
            )

        except Exception as error:

            self.esp32 = None

            self.estado_esp32.setText(
                "ESP32       ● Desconectado"
            )

            print(
                "ERROR AL CONECTAR ESP32:"
            )

            print(error)

    # ========================================================
    # ENVIAR COMANDO AL ESP32
    # ========================================================

    def enviar_comando(self, comando):

        if self.esp32 is None:
            print(
                "ESP32 no está conectado."
            )
            return

        try:

            comando = comando + "\n"

            self.esp32.write(
                comando.encode("utf-8")
            )

            print(
                "Enviado:",
                comando.strip()
            )

        except Exception as error:

            print(
                "ERROR ENVIANDO COMANDO:"
            )

            print(error)

    # ========================================================
    # CREAR INTERFAZ
    # ========================================================

    def crear_interfaz(self):

        # =================================
        # WIDGET PRINCIPAL
        # =================================

        contenedor = QWidget()

        self.setCentralWidget(
            contenedor
        )

        layout_principal = QVBoxLayout()

        contenedor.setLayout(
            layout_principal
        )

        # =================================
        # ENCABEZADO
        # =================================

        encabezado = QFrame()

        encabezado_layout = QHBoxLayout()

        encabezado.setLayout(
            encabezado_layout
        )

        titulo = QLabel(
            "●  Sistema Inteligente para la Clasificación del Grado de Madurez del Plátano"
        )

        titulo.setObjectName(
            "titulo"
        )

        encabezado_layout.addWidget(
            titulo
        )

        layout_principal.addWidget(
            encabezado
        )

        # =================================
        # CUERPO
        # =================================

        cuerpo = QHBoxLayout()

        layout_principal.addLayout(
            cuerpo
        )

        # =================================
        # MENÚ LATERAL
        # =================================

        menu = QFrame()

        menu_layout = QVBoxLayout()

        menu.setLayout(
            menu_layout
        )

        etiqueta_menu = QLabel(
            "MENÚ"
        )

        etiqueta_menu.setObjectName(
            "seccion"
        )

        menu_layout.addWidget(
            etiqueta_menu
        )

        botones = [
            "🏠  Inicio",
            "📷  Cámara",
            "🤖  YOLO",
            "🕹   Manual",
            "🎙   Voz",
            "⚙   Automático",
            "📊  Historial",
            "⚙  Configuración"
        ]

        for texto in botones:

            boton = QPushButton(
                texto
            )

            menu_layout.addWidget(
                boton
            )

        menu_layout.addStretch()

        boton_emergencia = QPushButton(
            "🛑  PARO DE EMERGENCIA"
        )

        boton_emergencia.setObjectName(
            "emergencia"
        )

        menu_layout.addWidget(
            boton_emergencia
        )

        cuerpo.addWidget(
            menu
        )

        # =================================
        # ÁREA PRINCIPAL
        # =================================

        area_principal = QFrame()

        area_layout = QVBoxLayout()

        area_principal.setLayout(
            area_layout
        )

        # =================================
        # TÍTULO DEL DASHBOARD
        # =================================

        titulo_area = QLabel(
            "DASHBOARD"
        )

        titulo_area.setObjectName(
            "seccion"
        )

        area_layout.addWidget(
            titulo_area
        )

        # =================================
        # TARJETAS SUPERIORES
        # =================================

        tarjetas = QHBoxLayout()

        # =================================
        # TARJETA DE CÁMARA
        # =================================

        tarjeta_camara = QFrame()

        camara_layout = QVBoxLayout()

        tarjeta_camara.setLayout(
            camara_layout
        )

        titulo_camara = QLabel(
            "📷 VIDEO EN VIVO"
        )

        titulo_camara.setObjectName(
            "seccion"
        )

        camara_layout.addWidget(
            titulo_camara
        )

        self.video = QLabel(
            "CÁMARA\nSIN SEÑAL"
        )

        self.video.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.video.setMinimumSize(
            500,
            300
        )

        self.video.setObjectName(
            "video"
        )

        self.video.setScaledContents(
            False
        )

        camara_layout.addWidget(
            self.video
        )

        tarjetas.addWidget(
            tarjeta_camara,
            2
        )

        # =================================
        # TARJETA DE DETECCIÓN
        # =================================

        tarjeta_deteccion = QFrame()

        deteccion_layout = QVBoxLayout()

        tarjeta_deteccion.setLayout(
            deteccion_layout
        )

        titulo_deteccion = QLabel(
            "🤖 DETECCIÓN"
        )

        titulo_deteccion.setObjectName(
            "seccion"
        )

        deteccion_layout.addWidget(
            titulo_deteccion
        )

        self.clase = QLabel(
            "Clase detectada:\n—"
        )

        self.confianza = QLabel(
            "Confianza:\n—"
        )

        self.coordenadas = QLabel(
            "Coordenadas:\n—"
        )

        deteccion_layout.addWidget(
            self.clase
        )

        deteccion_layout.addWidget(
            self.confianza
        )

        deteccion_layout.addWidget(
            self.coordenadas
        )

        deteccion_layout.addStretch()

        tarjetas.addWidget(
            tarjeta_deteccion,
            1
        )

        # =================================
        # TARJETA DE ESTADO
        # =================================

        tarjeta_estado = QFrame()

        estado_layout = QVBoxLayout()

        tarjeta_estado.setLayout(
            estado_layout
        )

        titulo_estado = QLabel(
            "⚙ ESTADO DEL SISTEMA"
        )

        titulo_estado.setObjectName(
            "seccion"
        )

        estado_layout.addWidget(
            titulo_estado
        )

        self.estado_esp32 = QLabel(
            "ESP32       ● Desconectado"
        )

        self.estado_camara = QLabel(
            "Cámara      ● Desconectada"
        )

        self.estado_yolo = QLabel(
            "YOLO11      ● Inactivo"
        )

        self.estado_brazo = QLabel(
            "Brazo       ● Detenido"
        )

        estado_layout.addWidget(
            self.estado_esp32
        )

        estado_layout.addWidget(
            self.estado_camara
        )

        estado_layout.addWidget(
            self.estado_yolo
        )

        estado_layout.addWidget(
            self.estado_brazo
        )

        estado_layout.addStretch()

        tarjetas.addWidget(
            tarjeta_estado,
            1
        )

        # =================================
        # AGREGAR TARJETAS
        # =================================

        area_layout.addLayout(
            tarjetas
        )

        # =================================
        # CONTROL MANUAL DEL BRAZO
        # =================================

        titulo_control = QLabel(
            "🎮 CONTROL MANUAL"
        )

        titulo_control.setObjectName(
            "seccion"
        )

        area_layout.addWidget(
            titulo_control
        )

        controles = QHBoxLayout()

        # =================================
        # BASE
        # =================================

        base_frame = QFrame()

        base_layout = QVBoxLayout()

        base_frame.setLayout(
            base_layout
        )

        base_titulo = QLabel(
            "BASE"
        )

        base_titulo.setObjectName(
            "seccion"
        )

        base_layout.addWidget(
            base_titulo
        )

        base_izquierda = QPushButton(
            "◀"
        )

        base_derecha = QPushButton(
            "▶"
        )

        base_izquierda.clicked.connect(
            lambda: self.mover_base(-5)
        )

        base_derecha.clicked.connect(
            lambda: self.mover_base(5)
        )

        base_angulo = QLabel(
            "Ángulo: 90°"
        )

        base_angulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        base_layout.addWidget(
            base_izquierda
        )

        base_layout.addWidget(
            base_angulo
        )

        base_layout.addWidget(
            base_derecha
        )

        controles.addWidget(
            base_frame
        )

        # =================================
        # HOMBRO
        # =================================

        hombro_frame = QFrame()

        hombro_layout = QVBoxLayout()

        hombro_frame.setLayout(
            hombro_layout
        )

        hombro_titulo = QLabel(
            "HOMBRO"
        )

        hombro_titulo.setObjectName(
            "seccion"
        )

        hombro_layout.addWidget(
            hombro_titulo
        )

        hombro_arriba = QPushButton(
            "▲"
        )

        hombro_abajo = QPushButton(
            "▼"
        )

        hombro_arriba.clicked.connect(
            lambda: self.mover_hombro(5)
        )

        hombro_abajo.clicked.connect(
            lambda: self.mover_hombro(-5)
        )

        hombro_angulo = QLabel(
            "Ángulo: 90°"
        )

        hombro_angulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        hombro_layout.addWidget(
            hombro_arriba
        )

        hombro_layout.addWidget(
            hombro_angulo
        )

        hombro_layout.addWidget(
            hombro_abajo
        )

        controles.addWidget(
            hombro_frame
        )

        # =================================
        # CODO
        # =================================

        codo_frame = QFrame()

        codo_layout = QVBoxLayout()

        codo_frame.setLayout(
            codo_layout
        )

        codo_titulo = QLabel(
            "CODO"
        )

        codo_titulo.setObjectName(
            "seccion"
        )

        codo_layout.addWidget(
            codo_titulo
        )

        codo_arriba = QPushButton(
            "▲"
        )

        codo_abajo = QPushButton(
            "▼"
        )

        codo_arriba.clicked.connect(
            lambda: self.mover_codo(5)
        )

        codo_abajo.clicked.connect(
            lambda: self.mover_codo(-5)
        )

        codo_angulo = QLabel(
            "Ángulo: 90°"
        )

        codo_angulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        codo_layout.addWidget(
            codo_arriba
        )

        codo_layout.addWidget(
            codo_angulo
        )

        codo_layout.addWidget(
            codo_abajo
        )

        controles.addWidget(
            codo_frame
        )

        # =================================
        # MUÑECA
        # =================================

        muneca_frame = QFrame()

        muneca_layout = QVBoxLayout()

        muneca_frame.setLayout(
            muneca_layout
        )

        muneca_titulo = QLabel(
            "MUÑECA"
        )

        muneca_titulo.setObjectName(
            "seccion"
        )

        muneca_layout.addWidget(
            muneca_titulo
        )

        muneca_izquierda = QPushButton(
            "◀"
        )

        muneca_derecha = QPushButton(
            "▶"
        )

        muneca_izquierda.clicked.connect(
            lambda: self.mover_muneca(-5)
        )

        muneca_derecha.clicked.connect(
            lambda: self.mover_muneca(5)
        )

        muneca_angulo = QLabel(
            "Ángulo: 90°"
        )

        muneca_angulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        muneca_layout.addWidget(
            muneca_izquierda
        )

        muneca_layout.addWidget(
            muneca_angulo
        )

        muneca_layout.addWidget(
            muneca_derecha
        )

        controles.addWidget(
            muneca_frame
        )

        # =================================
        # GARRA
        # =================================

        garra_frame = QFrame()

        garra_layout = QVBoxLayout()

        garra_frame.setLayout(
            garra_layout
        )

        garra_titulo = QLabel(
            "GARRA"
        )

        garra_titulo.setObjectName(
            "seccion"
        )

        garra_layout.addWidget(
            garra_titulo
        )

        garra_abrir = QPushButton(
            "ABRIR"
        )

        garra_cerrar = QPushButton(
            "CERRAR"
        )

        garra_abrir.clicked.connect(
            self.abrir_garra
        )

        garra_cerrar.clicked.connect(
            self.cerrar_garra
        )

        garra_angulo = QLabel(
            "Estado: Abierta"
        )

        garra_angulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        garra_layout.addWidget(
            garra_abrir
        )

        garra_layout.addWidget(
            garra_angulo
        )

        garra_layout.addWidget(
            garra_cerrar
        )

        controles.addWidget(
            garra_frame
        )

        area_layout.addLayout(
            controles
        )

        cuerpo.addWidget(
            area_principal,
            1
        )

    # ========================================================
    # CARGAR MODELO YOLO11
    # ========================================================

    def cargar_modelo(self):

        print("=" * 60)
        print("CARGANDO MODELO YOLO11")
        print("=" * 60)

        print(
            f"Ruta del modelo:\n{MODEL_PATH}"
        )

        # -----------------------------------------------
        # Comprobar existencia del modelo
        # -----------------------------------------------

        if not MODEL_PATH.exists():

            print(
                "ERROR: No se encontró el modelo."
            )

            self.estado_yolo.setText(
                "YOLO11      ● Error"
            )

            return

        # -----------------------------------------------
        # Cargar modelo
        # -----------------------------------------------

        try:

            self.model = YOLO(
                str(MODEL_PATH)
            )

            self.yolo_activo = True

            self.estado_yolo.setText(
                "YOLO11      ● Activo"
            )

            print(
                "YOLO11 cargado correctamente."
            )

            print(
                "Clases del modelo:"
            )

            print(
                self.model.names
            )

            print("=" * 60)

        except Exception as error:

            self.model = None

            self.yolo_activo = False

            self.estado_yolo.setText(
                "YOLO11      ● Error"
            )

            print(
                "ERROR AL CARGAR YOLO11:"
            )

            print(
                error
            )

            print("=" * 60)

    # ========================================================
    # INICIAR CÁMARA
    # ========================================================

    def iniciar_camara(self):

        print(
            "Iniciando cámara..."
        )

        # -----------------------------------------------
        # Intento 1: DirectShow
        # -----------------------------------------------

        self.cap = cv2.VideoCapture(
            CAMERA_INDEX,
            cv2.CAP_DSHOW
        )

        # -----------------------------------------------
        # Intento 2: cámara estándar
        # -----------------------------------------------

        if not self.cap.isOpened():

            print(
                "DirectShow no pudo abrir la cámara."
            )

            self.cap.release()

            self.cap = cv2.VideoCapture(
                CAMERA_INDEX
            )

        # -----------------------------------------------
        # Comprobar conexión
        # -----------------------------------------------

        if not self.cap.isOpened():

            print(
                "ERROR: No se pudo abrir la cámara."
            )

            self.camara_activa = False

            self.estado_camara.setText(
                "Cámara      ● Error"
            )

            self.video.setText(
                "CÁMARA\nSIN SEÑAL"
            )

            return

        # -----------------------------------------------
        # Configuración de cámara
        # -----------------------------------------------

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

        self.camara_activa = True

        self.estado_camara.setText(
            "Cámara      ● Conectada"
        )

        print(
            "Cámara conectada correctamente."
        )

    # ========================================================
    # ACTUALIZAR VIDEO
    # ========================================================

    def actualizar_video(self):

        # -----------------------------------------------
        # Comprobar cámara
        # -----------------------------------------------

        if self.cap is None:

            return

        if not self.cap.isOpened():

            return

        # -----------------------------------------------
        # Leer frame
        # -----------------------------------------------

        ret, frame = self.cap.read()

        if not ret:

            self.camara_activa = False

            self.estado_camara.setText(
                "Cámara      ● Error"
            )

            self.video.setText(
                "ERROR\nAL LEER CÁMARA"
            )

            return

        # -----------------------------------------------
        # Frame que se mostrará
        # -----------------------------------------------

        frame_mostrar = frame

        # -----------------------------------------------
        # Ejecutar YOLO11
        # -----------------------------------------------

        if self.model is not None:

            try:

                resultados = self.model.predict(
                    source=frame,
                    conf=CONF_THRESHOLD,
                    verbose=False
                )

                if len(resultados) > 0:

                    resultado = resultados[0]

                    # -----------------------------------
                    # Dibujar detecciones
                    # -----------------------------------

                    frame_mostrar = resultado.plot()

                    # -----------------------------------
                    # Procesar detección
                    # -----------------------------------

                    self.procesar_deteccion(
                        resultado
                    )

                else:

                    self.limpiar_deteccion()

            except Exception as error:

                print(
                    "ERROR EN YOLO11:"
                )

                print(
                    error
                )

                self.limpiar_deteccion()

        else:

            self.limpiar_deteccion()

        # -----------------------------------------------
        # Mostrar frame en la interfaz
        # -----------------------------------------------

        self.mostrar_frame(
            frame_mostrar
        )

    # ========================================================
    # PROCESAR DETECCIONES
    # ========================================================

    def procesar_deteccion(
        self,
        resultado
    ):

        boxes = resultado.boxes

        # -----------------------------------------------
        # No hay detecciones
        # -----------------------------------------------

        if boxes is None or len(boxes) == 0:

            self.limpiar_deteccion()

            return

        # -----------------------------------------------
        # Buscar la detección con mayor confianza
        # -----------------------------------------------

        mejor_confianza = -1.0

        mejor_box = None

        for box in boxes:

            confianza = float(
                box.conf[0].item()
            )

            if confianza > mejor_confianza:

                mejor_confianza = confianza

                mejor_box = box

        # -----------------------------------------------
        # Comprobar detección
        # -----------------------------------------------

        if mejor_box is None:

            self.limpiar_deteccion()

            return

        # -----------------------------------------------
        # Obtener clase
        # -----------------------------------------------

        clase_id = int(
            mejor_box.cls[0].item()
        )

        # -----------------------------------------------
        # Obtener nombre de clase
        # -----------------------------------------------

        if isinstance(
            resultado.names,
            dict
        ):

            nombre_clase = resultado.names.get(
                clase_id,
                str(clase_id)
            )

        else:

            nombre_clase = resultado.names[
                clase_id
            ]

        # -----------------------------------------------
        # Obtener coordenadas
        # -----------------------------------------------

        coordenadas = (
            mejor_box
            .xyxy[0]
            .tolist()
        )

        x1 = int(
            coordenadas[0]
        )

        y1 = int(
            coordenadas[1]
        )

        x2 = int(
            coordenadas[2]
        )

        y2 = int(
            coordenadas[3]
        )

        # -----------------------------------------------
        # Actualizar clase
        # -----------------------------------------------

        self.clase.setText(
            f"Clase detectada:\n"
            f"{nombre_clase}"
        )

        # -----------------------------------------------
        # Actualizar confianza
        # -----------------------------------------------

        self.confianza.setText(
            f"Confianza:\n"
            f"{mejor_confianza:.2%}"
        )

        # -----------------------------------------------
        # Actualizar coordenadas
        # -----------------------------------------------

        self.coordenadas.setText(
            f"Coordenadas:\n"
            f"X1: {x1}  Y1: {y1}\n"
            f"X2: {x2}  Y2: {y2}"
        )

        # -----------------------------------------------
        # Información en consola
        # -----------------------------------------------

        # Se puede descomentar si quieres ver
        # cada detección en la consola.
        #
        # print(
        #     f"Clase: {nombre_clase} | "
        #     f"Confianza: {mejor_confianza:.2%} | "
        #     f"Coordenadas: "
        #     f"({x1}, {y1}, {x2}, {y2})"
        # )

    # ========================================================
    # LIMPIAR INFORMACIÓN DE DETECCIÓN
    # ========================================================

    def limpiar_deteccion(self):

        self.clase.setText(
            "Clase detectada:\n—"
        )

        self.confianza.setText(
            "Confianza:\n—"
        )

        self.coordenadas.setText(
            "Coordenadas:\n—"
        )

    # ========================================================
    # MOSTRAR FRAME EN QT
    # ========================================================

    def mostrar_frame(
        self,
        frame
    ):

        # -----------------------------------------------
        # Convertir BGR -> RGB
        # -----------------------------------------------

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # -----------------------------------------------
        # Obtener dimensiones
        # -----------------------------------------------

        alto, ancho, canales = (
            frame_rgb.shape
        )

        bytes_por_linea = (
            canales * ancho
        )

        # -----------------------------------------------
        # Crear QImage
        # -----------------------------------------------

        imagen = QImage(
            frame_rgb.data,
            ancho,
            alto,
            bytes_por_linea,
            QImage.Format.Format_RGB888
        ).copy()

        # -----------------------------------------------
        # Crear QPixmap
        # -----------------------------------------------

        pixmap = QPixmap.fromImage(
            imagen
        )

        # -----------------------------------------------
        # Ajustar al área de video
        # -----------------------------------------------

        pixmap = pixmap.scaled(
            self.video.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # -----------------------------------------------
        # Mostrar
        # -----------------------------------------------

        self.video.setPixmap(
            pixmap
        )

    # ========================================================
    # CERRAR APLICACIÓN
    # ========================================================

    def closeEvent(
        self,
        event
    ):

        print(
            "Cerrando sistema..."
        )

        # -----------------------------------------------
        # Detener temporizador
        # -----------------------------------------------

        if self.timer.isActive():

            self.timer.stop()

        # -----------------------------------------------
        # Liberar cámara
        # -----------------------------------------------

        if self.cap is not None:

            self.cap.release()

            self.cap = None

        # -----------------------------------------------
        # Aceptar cierre
        # -----------------------------------------------

        event.accept()

        print(
            "Sistema cerrado correctamente."
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    # -----------------------------------------------
    # Cargar style.css
    # -----------------------------------------------

    ruta_css = (
        Path(__file__).resolve().parent
        / "style.css"
    )

    if ruta_css.exists():

        with open(
            ruta_css,
            "r",
            encoding="utf-8"
        ) as archivo:

            estilo = archivo.read()

        app.setStyleSheet(
            estilo
        )

    else:

        print(
            "ADVERTENCIA: No se encontró style.css"
        )

    # -----------------------------------------------
    # Crear ventana
    # -----------------------------------------------

    ventana = VentanaPrincipal()

    ventana.show()

    # -----------------------------------------------
    # Ejecutar aplicación
    # -----------------------------------------------

    sys.exit(
        app.exec()
    )