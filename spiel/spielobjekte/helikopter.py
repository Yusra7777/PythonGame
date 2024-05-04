from spiel.spielobjekte.basisobjekt import BasisObjekt
from spiel.spielobjekte.landeplatz import Landeplatz
import math

class Helikopter(BasisObjekt):
    def __init__(self, bild, x, y, lkw, landeplatz):
        super().__init__(x, y, bild)
        self.lkw = lkw
        self.landeplatz = landeplatz
        self.geschwindigkeit = 2.5
        self.geladenes_erz = 0
        self.erz_geladen = False

    def position_abrufen(self):
        return self.x, self.y

    def aktualisieren(self):
        self.rect.topleft = (self.x, self.y)
        if self.erz_geladen:
            self.landeplatz_anfliegen()
        else:
            self.verfolge_lkw()

        self.kollision_prüfen()

    def kollision_prüfen(self):
        if self.rect.colliderect(self.landeplatz.rect):  # Prüfen, ob Kollision mit dem Landeplatz vorliegt
            self.landeplatz.erz_hinzufügen(self.geladenes_erz)
            self.geladenes_erz = 0
            self.erz_geladen = False

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

    def landeplatz_anfliegen(self):
        landeplatz_x, landeplatz_y = self.landeplatz.position_abrufen()

        richtung_x = landeplatz_x - self.x
        richtung_y = landeplatz_y - self.y

        länge = math.sqrt(richtung_x ** 2 + richtung_y ** 2)
        if länge != 0:
            richtung_x /= länge
            richtung_y /= länge

        self.x += richtung_x * self.geschwindigkeit
        self.y += richtung_y * self.geschwindigkeit

    def erz_stehlen(self, lkw):
        self.geladenes_erz += 50
        lkw.geladenes_erz -= 50
        self.erz_geladen = True

    def erz_ablegen(self):
        if self.erz_geladen:
            self.landeplatz.erz_hinzufügen(self.geladenes_erz)
            self.geladenes_erz = 0
            self.erz_geladen = False

    def set_ui_info(self):
        return [
            f'Geladenes Erz (H): {self.geladenes_erz}'
        ]