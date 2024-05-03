import pygame
import sys

from UI import UI
from spiel.spielobjekte.erzmine import Erzmine
from spiel.spielobjekte.lager import Lager
from spiel.spielobjekte.landeplatz import Landeplatz
from spiel.spielobjekte.lkw import LKW
from spiel.spielobjekte.basisobjekt import bild_laden
from spiel.spielobjekte.tankstelle import Tankstelle

# Pygame initialisieren
pygame.init()

bildschirm = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Erzsammler")
clock = pygame.time.Clock()

# Erzmine, Lager, Tankstelle, Landeplatz und LKW erstellen
erzmine_bild = bild_laden("erzmine")
erzmine = Erzmine(erzmine_bild, 200, 200, 1000)

lager_bild = bild_laden("lager")
lager = Lager(lager_bild, 600, 200, 0)

tankstellen_bild = bild_laden("tankstelle")
tankstelle = Tankstelle(tankstellen_bild, 400, 100)

landeplatz_bild = bild_laden("landeplatz")
landeplatz = Landeplatz(landeplatz_bild, 600, 400, 0)

lkw_bild = bild_laden("lkw")
lkw = LKW(lkw_bild, 400, 300)

# Eine Liste für alle Spielobjekte
spielobjekte = [erzmine, lager, tankstelle, landeplatz, lkw]

# Tastenzustände
tasten = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_UP: False,
    pygame.K_DOWN: False
}

ui = UI(spielobjekte)

läuft = True
while läuft:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            läuft = False
        elif ereignis.type == pygame.KEYDOWN:
            if ereignis.key in tasten:
                tasten[ereignis.key] = True
        elif ereignis.type == pygame.KEYUP:
            if ereignis.key in tasten:
                tasten[ereignis.key] = False

    # Bewegung des LKWs basierend auf Tastenzuständen
    if tasten[pygame.K_LEFT]:
        lkw.bewegen("links")
    if tasten[pygame.K_RIGHT]:
        lkw.bewegen("rechts")
    if tasten[pygame.K_UP]:
        lkw.bewegen("oben")
    if tasten[pygame.K_DOWN]:
        lkw.bewegen("unten")

    # Kollisionen überprüfen
    if pygame.sprite.collide_mask(lkw, erzmine):
        lkw.kollision(erzmine)

    if pygame.sprite.collide_mask(lkw, lager):
        lkw.kollision(lager)

    if pygame.sprite.collide_mask(lkw, tankstelle):
        lkw.kollision(tankstelle)

    bildschirm.fill((255, 255, 255))

    for objekt in spielobjekte:
        objekt.zeichnen(bildschirm)
    ui.zeichnen(bildschirm)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
