from spiel.spielobjekte.basisobjekt import BasisObjekt
from spiel.spielobjekte.erzmine import Erzmine
from spiel.spielobjekte.lager import Lager
from spiel.spielobjekte.tankstelle import Tankstelle


class LKW(BasisObjekt):
    def __init__(self, bild, x, y):
        super().__init__(x, y, bild)
        self.geschwindigkeit = 5
        self.energie = 100
        self.geladenes_erz = 0

    def aktualisieren(self):
        self.rect.topleft = (self.x, self.y)

    def kollision(self, objekt):
        if isinstance(objekt, Erzmine):
            self.erzmine_kollision(objekt)
        elif isinstance(objekt, Lager):
            self.lager_kollision(objekt)
        elif isinstance(objekt, Tankstelle):
            self.tankstelle_kollision()

    def erzmine_kollision(self, erzmine):
        if self.geladenes_erz < 50:
            self.geladenes_erz += 50
            erzmine.kollision(self)

    def lager_kollision(self, lager):
        if self.geladenes_erz >= 50:
            self.geladenes_erz -= 50
            lager.kollision(self)

    def tankstelle_kollision(self):
        self.energie = 100

    def bewegen(self, richtung):
        if richtung == "links":
            self.x -= self.geschwindigkeit
            self.energie_verbrauchen()
        elif richtung == "rechts":
            self.x += self.geschwindigkeit
            self.energie_verbrauchen()
        elif richtung == "oben":
            self.y -= self.geschwindigkeit
            self.energie_verbrauchen()
        elif richtung == "unten":
            self.y += self.geschwindigkeit
            self.energie_verbrauchen()
        self.aktualisieren()

    def energie_verbrauchen(self):
        self.energie -= 0.1

    def set_ui_info(self):
        return [
            f'Energie: {int(self.energie)}%',
            f'Geladenes Erz: {self.geladenes_erz}'
        ]
