from spiel.spielobjekte.basisobjekt import BasisObjekt
from spiel.spielobjekte.landeplatz import Landeplatz
import math

class Helikopter(BasisObjekt):
    def __init__(self, bild, x, y, lkw):
        super().__init__(x, y, bild)
        self.lkw = lkw
        self.geschwindigkeit = 2.5
        self.geladenes_erz = 0

    def aktualisieren(self):
        self.verfolge_lkw()

    def verfolge_lkw(self):
        lkw_x, lkw_y = self.lkw.position_abrufen()

        richtung_x = lkw_x - self.x
        richtung_y = lkw_y - self.y

        länge = math.sqrt(richtung_x ** 2 + richtung_y ** 2)
        if länge != 0:
            richtung_x /= länge
            richtung_y /= länge

        self.x += richtung_x * self.geschwindigkeit
        self.y += richtung_y * self.geschwindigkeit

    def set_ui_info(self):
        return [
            f'Geladenes Erz (H): {self.geladenes_erz}'
        ]