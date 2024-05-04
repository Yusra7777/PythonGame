import math

from spiel.spielobjekte.basisobjekt import BasisObjekt
from spiel.spielobjekte.landeplatz import Landeplatz


class Helikopter(BasisObjekt):
    def __init__(self, bild, x, y, lkw):
        super().__init__(x, y, bild)
        self.lkw = lkw
        self.geschwindigkeit = 2.5
        self.geladenes_erz = 0

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

    def aktualisieren(self):
        self.verfolge_lkw()

    def kollision(self, objekt):
        if isinstance(objekt, self.lkw.__class__):
            self.lkw_kollision(objekt)
        if isinstance(objekt, Landeplatz):
            self.landeplatz_kollision(objekt)

    def lkw_kollision(self, objekt):
        if self.geladenes_erz < 50:
            self.geladenes_erz += 50
            objekt.kollision(self)

    def landeplatz_kollision(self, objekt):
        if self.geladenes_erz == 50:
            self.geladenes_erz -= 50
            objekt.kollision(self)

    def set_ui_info(self):
        return [
            f'Geladenes Erz (H): {self.geladenes_erz}'
        ]
