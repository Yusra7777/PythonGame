# Importieren der benötigten Module
import os
import random  # Modul für Zufallszahlen
import pygame  # Pygame-Bibliothek für die Spieleentwicklung
import sys  # Modul für Systemfunktionalitäten

# Initialisierung von Pygame
pygame.init()

# Festlegen der Fenstergröße
BREITE, HÖHE = 800, 600

# Definition von Farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
BRAUN = (139, 69, 19)
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)
BLAU = (0, 0, 255)

spiel_durchlauf_1 = True
spiel_durchlauf_2 = False
spiel_durchlauf_3 = False

# Festlegen der Größe für Spieler und Objekte
SPIELER_GROESSE = 50
OBJEKT_GROESSE = 30

# Initialisierung des Bildschirms
bildschirm = pygame.display.set_mode((BREITE, HÖHE))  # Erstellen des Fensters
pygame.display.set_caption("Erzsammler")  # Titel des Fensters setzen
schrift = pygame.font.SysFont(None, 24) # Schriftart und -größe festlegen


def bild_laden(name):
    basispfad = os.path.dirname(os.path.abspath(__file__))
    bildpfad = os.path.join(basispfad, "bilder", f"{name}.png")

    if not os.path.exists(bildpfad):
        raise FileNotFoundError(f"Das Bild {bildpfad} konnte nicht gefunden werden.")

    try:
        bild = pygame.image.load(bildpfad).convert_alpha()
        return bild
    except pygame.error as e:
        raise IOError(f"Fehler beim Laden des Bildes {name}.png: {e}")

# Festlegen der Spielerposition und -eigenschaften
spieler_bild = bild_laden('lkw')  # Bild des Spielers
spieler_x = 400  # x-Position des Spielers
spieler_y = 300  # y-Position des Spielers
spieler_geschwindigkeit = 1 # Geschwindigkeit, mit der sich der Spieler bewegt
spieler_energie = 100  # Energie des Spielers
gesammelte_objekte = 0  # Anzahl der vom Spieler gesammelten Objekte
abgelegte_objekte = []  # Liste der abgelegten Objekte des Spielers

# Festlegen der Computerposition und -eigenschaften
computer_bild = bild_laden('helikopter')  # Bild des Computers
computer_x = 100  # x-Position des Computers
computer_y = 500  # y-Position des Computers
computer_geschwindigkeit = 0.1  # Geschwindigkeit, mit der sich der Computer bewegt
computer_objekt = None  # Objekt, das der Computer gestohlen hat
computer_abgelegte_objekte = []  # Liste der abgelegten Objekte des Computers

# Festlegen des Landeplatzes des Computers
computer_ablageplatz_x = 100  # Ablage-X-Position des Computers
computer_ablageplatz_y = 500  # Ablage-Y-Position des Computers
computer_landeplatz = bild_laden('landeplatz')  # Bild des Ablageplatzes

# Festlegen der Anfangspositionen der Tankstelle, des Erzobjekts und des Ablageplatzes
tankstelle_x, tankstelle_y = 700, 500  # Position des Energiegebers
tankstelle_bild = bild_laden('tankstelle')  # Bild des Energiegebers

erz_objekt_x, erz_objekt_y = 600, 400  # Position des Sammelobjekts
erz_objekt_bild = bild_laden('erzquelle')  # Bild des Sammelobjekts
erzquelle_vorkommen = 20  # Anzahl der Sammelobjekte

ablageplatz_x, ablageplatz_y = 500, 100  # Position des Ablageplatzes
lager_bild = bild_laden('lager')  # Bild des Ablageplatzes

# Variable zur Verfolgung des Spielstatus
läuft = True  # Solange das Spiel läuft, ist diese Variable True

# Hauptschleife des Spiels
while läuft:
    for ereignis in pygame.event.get():  # Ereignisse abfragen
        if ereignis.type == pygame.QUIT:  # Wenn das Fenster geschlossen wird
            läuft = False  # Spiel beenden

    # Tasteneingaben verarbeiten
    tasten = pygame.key.get_pressed()

    # Spielerbewegungen verarbeiten und Energie abziehen
    if tasten[pygame.K_LEFT] and spieler_energie > 0 and len(abgelegte_objekte) != 16 and len(computer_abgelegte_objekte) != 4:
        spieler_x -= spieler_geschwindigkeit
        spieler_energie -= 0.010
    if tasten[pygame.K_RIGHT] and spieler_energie > 0 and len(abgelegte_objekte) != 16 and len(computer_abgelegte_objekte) != 4:
        spieler_x += spieler_geschwindigkeit
        spieler_energie -= 0.010
    if tasten[pygame.K_UP] and spieler_energie > 0 and len(abgelegte_objekte) != 16 and len(computer_abgelegte_objekte) != 4:
        spieler_y -= spieler_geschwindigkeit
        spieler_energie -= 0.010
    if tasten[pygame.K_DOWN] and spieler_energie > 0 and len(abgelegte_objekte) != 16 and len(computer_abgelegte_objekte) != 4:
        spieler_y += spieler_geschwindigkeit
        spieler_energie -= 0.010

    # Tastenkombinationen für Spieler-Geschwindigkeitseinstellungen
    if tasten[pygame.K_s]:
        if tasten[pygame.K_PLUS] or tasten[pygame.K_EQUALS]:  # Alternative: pygame.K_EQUALS
            spieler_geschwindigkeit = min(spieler_geschwindigkeit + 0.001, 1.0)  # Maximalwert von 1.0
        elif tasten[pygame.K_MINUS]:
            spieler_geschwindigkeit = max(spieler_geschwindigkeit - 0.001, 0.1)  # Minimalwert von 0.1

    # Tastenkombinationen für Computer-Geschwindigkeitseinstellungen
    if tasten[pygame.K_c]:
        if tasten[pygame.K_PLUS] or tasten[pygame.K_EQUALS]:  # Alternative: pygame.K_EQUALS
            computer_geschwindigkeit = min(computer_geschwindigkeit + 0.001, 1.0)  # Maximalwert von 1.0
        elif tasten[pygame.K_MINUS]:
            computer_geschwindigkeit = max(computer_geschwindigkeit - 0.001, 0.1)  # Minimalwert von 0.1

    # Spielerposition einschränken, um innerhalb des Bildschirms zu bleiben
    spieler_x = max(0, min(spieler_x, BREITE - SPIELER_GROESSE))
    spieler_y = max(0, min(spieler_y, HÖHE - SPIELER_GROESSE))

    # Computer folgt dem Spieler oder liefert gestohlene Objekte ab
    if computer_objekt is None:
        if computer_x < spieler_x:
            computer_x += computer_geschwindigkeit
        elif computer_x > spieler_x:
            computer_x -= computer_geschwindigkeit
        if computer_y < spieler_y:
            computer_y += computer_geschwindigkeit
        elif computer_y > spieler_y:
            computer_y -= computer_geschwindigkeit
    else:
        target_x, target_y = computer_ablageplatz_x, computer_ablageplatz_y
        distance = ((computer_x - target_x) ** 2 + (computer_y - target_y) ** 2) ** 0.5
        if distance > 0.1:  # Schwellenwert für die Annäherung
            dx = target_x - computer_x
            dy = target_y - computer_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            if distance != 0:
                computer_x += computer_geschwindigkeit * (dx / distance)
                computer_y += computer_geschwindigkeit * (dy / distance)
        else:
            computer_abgelegte_objekte.append((computer_ablageplatz_x, computer_ablageplatz_y))
            computer_objekt = None

    # Anpassen der Bewegung des Computers nach dem Ablegen eines Objekts
    if computer_objekt is not None:
        target_x, target_y = computer_ablageplatz_x, computer_ablageplatz_y
        distance = ((computer_x - target_x) ** 2 + (computer_y - target_y) ** 2) ** 0.5
        if distance > 0.1:  # Schwellenwert für die Annäherung
            dx = target_x - computer_x
            dy = target_y - computer_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            if distance != 0:
                if distance < computer_geschwindigkeit:  # Falls die Entfernung kleiner ist als die Geschwindigkeit
                    computer_x = target_x
                    computer_y = target_y
                else:
                    computer_x += computer_geschwindigkeit * (dx / distance)
                    computer_y += computer_geschwindigkeit * (dy / distance)
        else:
            computer_abgelegte_objekte.append((computer_ablageplatz_x, computer_ablageplatz_y))
            computer_objekt = None
            # Computer nimmt die Verfolgung des Spielers wieder auf
            target_x, target_y = spieler_x, spieler_y

    # Rechtecke für Kollisionsprüfungen erstellen
    erz_objekt_rechteck = bildschirm.blit(erz_objekt_bild, (erz_objekt_x, erz_objekt_y)) # Rechteck für Erzobjekt
    helikopter_rechteck = bildschirm.blit(computer_bild, (computer_x, computer_y)) # Rechteck für Computer
    lager_rechteck = bildschirm.blit(lager_bild, (ablageplatz_x, ablageplatz_y)) # Rechteck für Ablageplatz
    landeplatz_ablageplatz_rechteck = bildschirm.blit(computer_landeplatz, (computer_ablageplatz_x, computer_ablageplatz_y)) # Rechteck für Landeplatz des Computers
    spieler_rechteck = bildschirm.blit(spieler_bild, (spieler_x, spieler_y)) # Rechteck für Spieler
    tankstelle_rechteck = bildschirm.blit(tankstelle_bild, (tankstelle_x, tankstelle_y)) # Rechteck für Tankstelle

    # Kollisionen mit den Objekten überprüfen und entsprechende Aktionen ausführen
    if spieler_rechteck.colliderect(tankstelle_rechteck):
        spieler_energie = 100

    if spieler_rechteck.colliderect(erz_objekt_rechteck) and gesammelte_objekte < 16:
        gesammelte_objekte += 1
        erzquelle_vorkommen -= 1
        erz_objekt_x = -100

    if spieler_rechteck.colliderect(lager_rechteck) and gesammelte_objekte > 0:
        abgelegte_objekte.append((ablageplatz_x, ablageplatz_y))
        gesammelte_objekte -= 1
        erz_objekt_x = random.randint(0, BREITE - OBJEKT_GROESSE)
        erz_objekt_y = random.randint(0, HÖHE - OBJEKT_GROESSE)

    # Wenn der Computer kein Objekt hat und der Spieler eines hat und sie kollidieren, stiehlt der Computer es
    if computer_objekt is None and gesammelte_objekte > 0 and spieler_rechteck.colliderect(helikopter_rechteck):
        computer_objekt = (erz_objekt_x, erz_objekt_y)
        gesammelte_objekte -= 1
        erz_objekt_x = random.randint(0, BREITE - OBJEKT_GROESSE)
        erz_objekt_y = random.randint(0, HÖHE - OBJEKT_GROESSE)

    # Spielerenergie begrenzen, um sicherzustellen, dass sie zwischen 0 und 100 liegt
    spieler_energie = max(0, min(spieler_energie, 100))

    # Hintergrund zeichnen
    bildschirm.fill(WEISS)

    # Rechtecke für Spieler, Objekte und Ablageplatz zeichnen
    bildschirm.blit(spieler_bild, (spieler_x, spieler_y)) # Spieler zeichnen, um ihn über das png-Bild zu legen
    bildschirm.blit(tankstelle_bild, (tankstelle_x, tankstelle_y)) # Tankstelle zeichnen
    bildschirm.blit(erz_objekt_bild, (erz_objekt_x, erz_objekt_y)) # Erzobjekt zeichnen
    bildschirm.blit(lager_bild, (ablageplatz_x, ablageplatz_y)) # Ablageplatz zeichnen
    bildschirm.blit(computer_bild, (computer_x, computer_y)) # Computer zeichnen
    bildschirm.blit(computer_landeplatz, (computer_ablageplatz_x, computer_ablageplatz_y)) # Landeplatz des Computers zeichnen

    # Textinformationen zum Spielstatus anzeigen
    energie_text = schrift.render(f'Tank: {spieler_energie:.2f}', True, SCHWARZ)
    bildschirm.blit(energie_text, (10, 10))
    objekte_text = schrift.render(f'Beladung: {gesammelte_objekte}', True, SCHWARZ)
    bildschirm.blit(objekte_text, (10, 30))
    abgelegte_objekte_text = schrift.render(f'Gesammeltes Erz(LKW): {len(abgelegte_objekte)}/16', True, SCHWARZ)
    bildschirm.blit(abgelegte_objekte_text, (10, 50))
    computer_abgelegte_objekte_text = schrift.render(f'Gestohlenes Erz(Helikopter): {len(computer_abgelegte_objekte)}/4', True, SCHWARZ)
    bildschirm.blit(computer_abgelegte_objekte_text, (10, 70))
    erquelle_vorkommen_text = schrift.render(f'Verbleibende Erzquellen: {erzquelle_vorkommen}/20', True, SCHWARZ)
    bildschirm.blit(erquelle_vorkommen_text, (10, 90))

    # Textinformationen zur Geschwindigkeit anzeigen
    spieler_geschwindigkeit_text = schrift.render(f'Spieler Geschwindigkeit: {spieler_geschwindigkeit:.2f}', True, SCHWARZ)
    bildschirm.blit(spieler_geschwindigkeit_text, (10, 110))
    computer_geschwindigkeit_text = schrift.render(f'Computer Geschwindigkeit: {computer_geschwindigkeit:.2f}', True, SCHWARZ)
    bildschirm.blit(computer_geschwindigkeit_text, (10, 130))

    if spiel_durchlauf_1:
        level_text = schrift.render("Level 1", True, SCHWARZ)
        bildschirm.blit(level_text, (10, 150))

    if spiel_durchlauf_2:
        level_text = schrift.render("Level 2", True, SCHWARZ)
        bildschirm.blit(level_text, (10, 150))

    if spiel_durchlauf_3:
        level_text = schrift.render("Level 3", True, SCHWARZ)
        bildschirm.blit(level_text, (10, 150))

    # Nachricht anzeigen, wenn die Energie leer ist und die E-Taste zum Aufladen gedrückt wird
    if spieler_energie <= 0:
        nachricht_text = schrift.render("Du hast das Spiel verloren! Drücke 'R' für Restart", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (200, 300))

    if spieler_energie <= 0 and tasten[pygame.K_r]:
        spieler_x = 400
        spieler_y = 300
        spieler_energie = 100
        gesammelte_objekte = 0
        abgelegte_objekte = []
        erz_objekt_x, erz_objekt_y = 600, 400
        gestohlene_objekte = []
        computer_objekt = None
        computer_abgelegte_objekte = []



    # Nachricht anzeigen, wenn alle Objekte abgelegt wurden und die R-Taste zum Neustart gedrückt wird
    if len(abgelegte_objekte) == 16:
        nachricht_text = schrift.render("Glückwunsch, du hast alle das Spiel gewonnen! Drücke 'R' für Restart", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (200, 300))

    # Spiel zurücksetzen, wenn alle Objekte abgelegt wurden und R gedrückt wird
    if len(abgelegte_objekte) == 16 and spiel_durchlauf_1 and tasten[pygame.K_r]:
        spieler_x = 400
        spieler_y = 300
        spieler_energie = 100
        gesammelte_objekte = 0
        erz_objekt_x, erz_objekt_y = 600, 400
        erzquelle_vorkommen = 20
        abgelegte_objekte = []
        gestohlene_objekte = []
        computer_objekt = None
        computer_abgelegte_objekte = []
        spiel_durchlauf_1 = False
        spiel_durchlauf_2 = True

        if len(abgelegte_objekte) == 16 and spiel_durchlauf_2 and not spiel_durchlauf_1:
            spieler_x = 400
            spieler_y = 300
            spieler_energie = 100
            gesammelte_objekte = 0
            erz_objekt_x, erz_objekt_y = 600, 400
            erzquelle_vorkommen = 20
            abgelegte_objekte = []
            gestohlene_objekte = []
            computer_objekt = None
            computer_abgelegte_objekte = []
            computer_geschwindigkeit = 0.25
            spieler_geschwindigkeit = 0.85
            spiel_durchlauf_2 = False
            spiel_durchlauf_3 = True

            if len(abgelegte_objekte) == 16 and spiel_durchlauf_3 and not spiel_durchlauf_1 and not spiel_durchlauf_2:
                spieler_x = 400
                spieler_y = 300
                spieler_energie = 100
                gesammelte_objekte = 0
                erz_objekt_x, erz_objekt_y = 600, 400
                erzquelle_vorkommen = 20
                abgelegte_objekte = []
                gestohlene_objekte = []
                computer_objekt = None
                computer_abgelegte_objekte = []
                computer_geschwindigkeit = 0.40
                spieler_geschwindigkeit = 0.70


    # Nachricht anzeigen, wenn alle Objekte gestohlen wurden und die R-Taste zum Neustart gedrückt wird
    if len(computer_abgelegte_objekte) == 4:
        nachricht_text = schrift.render("Der Computer hat alle Objekte gestohlen! R für restart", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (200, 300))

    # Spiel zurücksetzen, wenn alle Objekte gestohlen wurden und R gedrückt wird
    if len(computer_abgelegte_objekte) == 4 and tasten[pygame.K_r]:
        spieler_x = 400
        spieler_y = 300
        spieler_energie = 100
        gesammelte_objekte = 0
        abgelegte_objekte = []
        gestohlene_objekte = []
        computer_objekt = None
        computer_abgelegte_objekte = []

    # Anzeigen, welches Objekt der Computer gestohlen hat
    if computer_objekt is not None:
        pygame.draw.rect(bildschirm, BLAU, (*computer_objekt, OBJEKT_GROESSE, OBJEKT_GROESSE))

    # Bildschirm aktualisieren
    pygame.display.flip()

# Pygame beenden
pygame.quit()
sys.exit()