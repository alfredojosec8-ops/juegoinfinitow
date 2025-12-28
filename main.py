from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.clock import Clock
import random
import os

Window.size = (400, 700)

class JuegoInfinito(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ======================
        # ESTADO
        # ======================
        self.clicks = 0
        self.mostrando_video = False
        self.video_evento = None
        self.indice_video = 0

        # ======================
        # UI
        # ======================
        self.label = Label(
            text="Clicks: 0",
            size_hint=(None, None),
            size=(250, 50),
            pos=(10, Window.height - 60),
            font_size=24
        )
        self.add_widget(self.label)

        # ======================
        # ARCHIVOS
        # ======================
        self.imagenes = self.cargar("assets/fotos", [".jpg", ".jpeg", ".png"])
        self.videos = self.cargar("assets/videos", [".mp4"])

        if not self.imagenes:
            raise Exception("❌ No hay imágenes")
        if not self.videos:
            raise Exception("❌ No hay videos")

        # ======================
        # CONFIG
        # ======================
        self.cada_cuantos_clicks = 10

        # ======================
        # OBJETO
        # ======================
        self.objeto = Image(
            source=random.choice(self.imagenes),
            size_hint=(None, None),
            size=(150, 150),
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.objeto)
        self.objeto.bind(on_touch_down=self.tocar_imagen)

        Clock.schedule_interval(self.mover_objeto, 0.8)
        self.mover_objeto(0)

    # ======================
    def cargar(self, carpeta, extensiones):
        return [
            os.path.join(carpeta, f)
            for f in os.listdir(carpeta)
            if f.lower().endswith(tuple(extensiones))
        ]

    # ======================
    def mover_objeto(self, *args):
        if self.mostrando_video:
            return

        self.objeto.source = random.choice(self.imagenes)
        self.objeto.pos = (
            random.randint(0, Window.width - self.objeto.width),
            random.randint(0, Window.height - self.objeto.height - 80)
        )

    # ======================
    def tocar_imagen(self, instance, touch):
        if self.mostrando_video:
            return False

        if instance.collide_point(*touch.pos):
            self.clicks += 1
            self.label.text = f"Clicks: {self.clicks}"
            self.mover_objeto()

            if self.clicks % self.cada_cuantos_clicks == 0:
                self.mostrar_video()

            return True
        return False

    # ======================
    # VIDEO
    # ======================
    def mostrar_video(self):
        self.mostrando_video = True
        self.remove_widget(self.objeto)

        ruta = self.videos[self.indice_video]
        self.indice_video = (self.indice_video + 1) % len(self.videos)

        self.video = Video(
            source=ruta,
            state="play",
            size_hint=(1, 1)
        )
        self.video.allow_stretch = True
        self.video.keep_ratio = False

        # 👆 TOCAR PARA SALIR (CLAVE)
        self.video.bind(on_touch_down=self.cerrar_video)

        self.add_widget(self.video)

        # ⏱️ SEGURIDAD ABSOLUTA
        self.video_evento = Clock.schedule_once(
            self.cerrar_video, 45
        )

    # ======================
    def cerrar_video(self, *args):
        if not self.mostrando_video:
            return

        self.mostrando_video = False

        if self.video_evento:
            self.video_evento.cancel()
            self.video_evento = None

        if hasattr(self, "video") and self.video in self.children:
            self.remove_widget(self.video)

        self.add_widget(self.objeto)

    # ======================
    # TOQUE GLOBAL (POR SI ACASO)
    # ======================
    def on_touch_down(self, touch):
        if self.mostrando_video:
            self.cerrar_video()
            return True
        return super().on_touch_down(touch)

class JuegoApp(App):
    def build(self):
        return JuegoInfinito()

if __name__ == "__main__":
    JuegoApp().run()
