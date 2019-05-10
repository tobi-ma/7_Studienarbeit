# implementierung
from math import ceil
from math import floor
# Allgemeines
from typing import Union  # hat pycharm selbst erganzt. ich weiss nicht was das macht.
import timeit
start = timeit.default_timer()

anzahl_schichten = 2
arbeitszeit = 8
lohnkosten = 50000
verteilzeitfaktor = 12.00
zinsen = 6.00
abschreibungsdauer_LM = 15
abschreibungsdauer_FM_unstetig = 8
abschreibungsdauer_FM_stetig = 14
abschreibungsdauer_LHM = 2
wartungskosten = 5.00
energiekosten = 5.00
miete = 36.00

# Lagerstruktur

exponentialfaktor = 2
auftrage_pro_tag = 2000
pos_pro_tag = 12
picks_pro_pos = 1
spielfaehigkeit = 0.5
faecher_min = 50000
lagerhoehe_max = 20
lagerlaenge_max = 48
lagerbreite_max = 180
tiefe_LHM = 1200
breite_LHM = 800
hoehe_LHM = 1500
eigengewicht_LHM = 22.00
kosten_LHM = 23.00
tiefe_FM = 2700
ax = 0.50
vx = 3.67
ay = 0.60
vy = 1.10
kosten_FM = 150000.00
t_gabelspiel = 10
konstanteil = 5
gasse_anzahl_erf = False
gasse_laenge_erf = False
gasse_hoehe_erf = False
gasse_breite_erf = False
tiefe_LM = 1200
breite_LM = 1600
hoehe_LM = 4500
eigengewicht_LM = 100
kosten_LM = 400

laenge_fach = tiefe_LM
breite_fach = breite_LM
hoehe_fach = hoehe_LM
eigengewicht_fach = eigengewicht_LM
kosten_fach = kosten_LM

lange_EPAL = 1200
breite_EPAL = 800
hoehe_EPAL = 1500
eigengewicht_EPAL = 22.00
kosten_EPAL = 23.00

lange_kKLT = 400
breite_kKLT = 300
hoehe_kKLT = 280
eigengewicht_kKLT = 0.50
kosten_kKLT = 5.00

laenge_GKLT = 600
breite_GKLT = 400
hoehe_GKLT = 280
eigengewicht_GKLT = 2.60
kosten_GKLT = 20.00

gassen_anzahl_manuell = False
gassen_breite_manuell = 0
gassen_hoehe_manuell = False
gassen_laenge_manuell = False

# Lagerstruktur
lagerleistung_min = auftrage_pro_tag * pos_pro_tag * picks_pro_pos / (anzahl_schichten * arbeitszeit)
print('minimale Lagerleistung ' + str(lagerleistung_min))
facher_pro_ebene = breite_LM / breite_LHM
anzahl_ebenen = hoehe_LM / hoehe_LHM
anzahl_facher_LM = anzahl_ebenen * facher_pro_ebene
facheranzahl_max_H: Union[float, int] = floor((lagerhoehe_max / (hoehe_LM / 1000)) * anzahl_ebenen)
# hohe_lager_nutz
if gassen_anzahl_manuell == False:
    hohe_lager_nutz = (facheranzahl_max_H * hoehe_LHM) / 1000
else:
    hohe_lager_nutz = gassen_hoehe_manuell

lagerfach_vol = (tiefe_LHM * breite_LHM * hoehe_LHM) / 10 ** 9  # in m hoch 3
lagervol_min = lagerfach_vol * faecher_min
lagerflache_min = lagervol_min / hohe_lager_nutz
# gassen_breite
if gassen_breite_manuell == 0:
    if (tiefe_FM + (2 * tiefe_LHM)) / 1000 <= lagerbreite_max:
        gassen_breite = (tiefe_FM + (2 * tiefe_LHM)) / 1000
    else:
        print('Bitte Mindestbreite für Gasse manuell eintragen')
elif (tiefe_FM + (2 * tiefe_LHM)) / 1000 > gassen_breite_manuell:
    print('Bitte mindestbereiche für eine Gasse wahlen')
else:
    gassen_breite = gassen_breite_manuell
# gassen lange
Temp = lagerflache_min / (gassen_breite - (tiefe_FM / 1000))
if gassen_laenge_manuell != False:
    gassen_lange = gassen_laenge_manuell
elif Temp < lagerlaenge_max - breite_LHM:
    gassen_lange = Temp
else:
    gassen_lange = lagerlaenge_max

regalwandparameter = (vx / vy) * (hohe_lager_nutz / gassen_lange)
facheranzahl_max_L = 2 * floor(gassen_lange / (breite_LHM / 1000))
# gassen_anzahl
if gassen_anzahl_manuell != False:
    gassen_anzahl = gassen_anzahl_manuell
elif ceil(faecher_min / (facheranzahl_max_L * facheranzahl_max_H)) * gassen_breite >= lagerbreite_max:
    print('Maximale Lagerbreite erhöhen!')
else:
    gassen_anzahl = ceil(faecher_min / (facheranzahl_max_H * facheranzahl_max_L))

LM_min = ceil(faecher_min / anzahl_facher_LM)
gassen_max = lagerbreite_max / gassen_breite

#####################
# Kosten

kosten_LM = kosten_LM * ceil(LM_min)
kosten_LHM = kosten_LHM * faecher_min  # hier evtl zwischenvariable fur gemeingültikeit einfuhren
kosten_fordermittel = gassen_anzahl * kosten_FM  # laut excel in D3-kosten enthalten
invest = kosten_LM + kosten_LHM + kosten_fordermittel
print('########')
print('kosten LM ' + str(kosten_LM))
print('Kosten LHM ' + str(kosten_LHM))
print('Fordermittel ' + str(kosten_fordermittel))
print('Investment ' + str(invest))
print('########')

# Betriebskosten

abschreibung_LM = kosten_LM / abschreibungsdauer_LM
abschreibung_LHM = kosten_LHM / abschreibungsdauer_LHM
abschreibung_FM = kosten_fordermittel / abschreibungsdauer_FM_unstetig
abschreibung_jahrl = abschreibung_LM + abschreibung_LHM + abschreibung_FM
print('Abschreibung pro Jahr ' + str(abschreibung_jahrl))

# KalkulatorischeZinsen

kalk_zinsen_jahrl = 0.5 * (zinsen / 100) * invest
wartung = invest * (wartungskosten / 100)
energie = invest * (energiekosten / 100)
# flache = gassen_breite * gassen_lange * ceil(gassen_anzahl)   # reihenfolge umdrehen
Miete = lagerflache_min * miete  # m in EUR pro Flache; M in EUR
print('kalk_zinsen_jahrl ' + str(kalk_zinsen_jahrl))
print('wartung ' + str(wartung))
print('Energiekosten = ' + str(energie))  # mach ich so jetzt alle?
print('Miete ' + str(Miete))
betriebskosten = abschreibung_jahrl + kalk_zinsen_jahrl + wartung + energie + Miete
print('Betriebskosten ' + str(betriebskosten))

# Kommissionierleistungwa

facher_pro_regalwand = ceil(facheranzahl_max_L / 2)
# flache_unter_diagonale
if regalwandparameter >= 1:
    flache_unter_diag = 0.5 * gassen_lange * ((vy / vx) * hohe_lager_nutz)
else:
    flache_unter_diag = (0.5 * hohe_lager_nutz * (vy / vx) * gassen_lange) + (
                hohe_lager_nutz * gassen_lange - (vy / vx) * gassen_lange)
# flache_unter_diag = round(flache_unter_diag, 2)
flache_uber_diag = (hohe_lager_nutz * gassen_lange) - flache_unter_diag
# facher_unter_diag
if regalwandparameter >= 1:
    facher_unter_diag = 0.5 * facher_pro_regalwand * (vy / vx) * facheranzahl_max_H
else:
    facher_unter_diag = 0.5 * facheranzahl_max_H * ((vy / vx) * facher_pro_regalwand) + (
                facheranzahl_max_H * facher_pro_regalwand - (vy / vx) * facher_pro_regalwand)
facher_uber_diag = (facheranzahl_max_H * facher_pro_regalwand) - facher_unter_diag
weg_mittel_unten_F = 1 / flache_unter_diag * ((1 / 3) * (vx ** 2 / vy ** 2) * hohe_lager_nutz ** 3 - (
            (1 / 2) * (vx ** 2 / vy ** 2) * hohe_lager_nutz ** 3) + ((1 / 2) * gassen_lange ** 2 * hohe_lager_nutz))
weg_mittel_oben_F = (1 / 3) * (1 / flache_uber_diag) * (vx / vy) * hohe_lager_nutz ** 3
weg_mittel_unten = (vx / ax) + (weg_mittel_unten_F / vx)
weg_mittel_oben = (vy / ay) + (weg_mittel_oben_F / vy)
# fahrzeit_lagerort
if regalwandparameter < 1:
    fahrzeit_lagerort = 2 * (((flache_unter_diag / (hohe_lager_nutz * gassen_lange)) * (vx / ax)) + (
                (flache_uber_diag / (hohe_lager_nutz * gassen_lange) * (vy / ay)) + (
                    (gassen_lange / vx) * ((0.5) + ((1 / 6) * ((vx / vy) * (gassen_lange / hohe_lager_nutz)) ** 2)))))
elif regalwandparameter == 1:
    fahrzeit_lagerort = (vx / ax) + (vy / ay) * ((4 / 3) * (gassen_lange / vx))
else:
    fahrzeit_lagerort = 2 * (((flache_unter_diag / (hohe_lager_nutz * gassen_lange)) * (vx / ax)) + (
                (flache_uber_diag / (hohe_lager_nutz * gassen_lange) * (vy / ay)) + ((hohe_lager_nutz / vy) * (
                    (0.5) + ((1 / 6) * ((vy / vx) * (gassen_lange / hohe_lager_nutz)) ** 2)))))
# print('#######')
# print('fahrzeit lagerort ' + str(fahrzeit_lagerort))
# print('regalwandparameter ' + str(regalwandparameter))
# print('flache_unter_diag ' + str(flache_unter_diag))
# print('flache_uber_diag ' + str(flache_uber_diag))
# print('facher_unter_diag ' + str(facher_unter_diag))
# print('facher_uber_diag ' + str(facher_uber_diag))
# print('weg_mittel_ unten_F ' + str(weg_mittel_unten_F))
# print('weg_mittel_oben_F ' + str(weg_mittel_oben_F))
# print('weg_mittel_unten ' + str(weg_mittel_unten))
# print('weg_mittel_oben ' + str(weg_mittel_oben))
# print('fahrzeit_lagerort ' + str(fahrzeit_lagerort))

# summe_wege
if regalwandparameter < 1:
    summe_wege = ((flache_unter_diag * vx) / (ax * hohe_lager_nutz * gassen_lange)) + (
                (flache_uber_diag * vy) / (ay * hohe_lager_nutz * gassen_lange)) + ((gassen_lange / vx) * (
                (1 / 3) + ((1 / 6) * regalwandparameter) - ((1 / 30) * regalwandparameter ** 3)))
elif regalwandparameter > 1:
    summe_wege = ((flache_unter_diag * vx) / (ax * hohe_lager_nutz * gassen_lange)) + (
                (flache_uber_diag * vy) / (ay * hohe_lager_nutz * gassen_lange)) + ((hohe_lager_nutz / vy) * (
                (1 / 3) + ((1 / 6) * regalwandparameter) - ((1 / 30) * regalwandparameter ** 3)))
else:
    summe_wege = 0.5 * ((vx / ax) + (vy / ay)) + ((14 / 30) * (gassen_lange / vx))

t_doppel_mittel = fahrzeit_lagerort + summe_wege
t_doppel = konstanteil + (4 * t_gabelspiel) + t_doppel_mittel
t_einzel = konstanteil + (2 * t_gabelspiel) + fahrzeit_lagerort

print('t_doppel_mittel ' + str(t_doppel_mittel))
print('t_doppel ' + str(t_doppel))
print('t_einzel ' + str(t_einzel))




#############
# Zusammenfassung

TCO_HRL = (abschreibung_jahrl + kalk_zinsen_jahrl + wartung + energie + Miete) * 10 + invest
print(TCO_HRL)

end = timeit.default_timer()
runtime = end - start
print('runtime ' + str(runtime))