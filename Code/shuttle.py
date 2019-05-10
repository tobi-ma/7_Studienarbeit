# implementierung
from math import ceil
from math import floor
import timeit
start = timeit.default_timer()
# Allgemeines
from typing import Union  # hat pycharm selbst erganzt. ich weiss nicht was das macht.

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

###################z
# Lagerstruktur

anz_faecher = 50000
lagerhoehe_max = 10
lagerlaenge_max = 100
lagerbreite_max = 10
tiefe_LHM = 400
breite_LHM = 300
hoehe_LHM = 280
gewicht_LHM = 0.5
stueckkosten_LHM = 5.00
tiefe_FM_shuttle = 400
ax_shuttle = 3
vx_shuttle = 5
kosten_FM_shuttle = 10000
ladezeit_shuttle = 2
totzeit_shuttle = 1.5
tiefe_aufzug = 400
ay_aufzug = 1
vy_aufzug = 2.5
kosten_FM_aufzug = 5000.00
ladezeit_aufzug = 2
totzeit_aufzug = 1.5
exponentialfaktor = 2
lagerleistung_min = 1000
spielfaehigkeit = 0.5
laenge_FM = 500
breite_FM = 300
hoehe_FM = 280
gewicht_FM = 100
stueckkosten_LM = 50
gasse_anzahl_vorgabe = 0
liftvariante = 0


#################
# LAGERSTRUKTUR

faecher_pro_ebene = breite_FM / breite_LHM
ebene_pro_lagermittel = hoehe_FM / hoehe_LHM
faecher_pro_ebene = floor(faecher_pro_ebene) * floor(ebene_pro_lagermittel)
LM_uebereinander_max = lagerhoehe_max / (hoehe_FM / 1000)
lagerfach_vol = (tiefe_LHM * breite_LHM * hoehe_LHM) / 10**9
# print('################')
# print(faecher_pro_ebene)
# print(ebene_pro_lagermittel)
# print(faecher_pro_ebene)
# print(LM_uebereinander_max)
# print(lagerfach_vol

lagervol_min = lagerfach_vol * anz_faecher
gasse_breite = (2 * tiefe_LHM + tiefe_FM_shuttle) / 1000
gassen_laenge = lagerlaenge_max - (lagerlaenge_max % (breite_LHM / 1000))
# anz_faecher_max_H
if gasse_anzahl_vorgabe == 0:
    anz_faecher_max_H = lagerbreite_max / gasse_breite
else: anz_faecher_max_H = gasse_anzahl_vorgabe
anz_faecher_max_L = 2 * (gassen_laenge / (breite_LHM / 1000) - 1)
anz_ebenen = ceil(anz_faecher / (anz_faecher_max_H * anz_faecher_max_L))
# gasse_anzahl
if gasse_anzahl_vorgabe == 0:
    gasse_anzahl = anz_faecher / (anz_faecher_max_L * anz_ebenen)
elif gasse_anzahl_vorgabe < (anz_faecher / (anz_faecher_max_L * anz_ebenen)):
    print('Nicht genug kapazitaet fuer gewuenschte Artikelanzhal')
else: gasse_anzahl = gasse_anzahl_vorgabe
gasse_hoehe = lagervol_min / (ceil(gasse_anzahl) * (gasse_breite - (tiefe_FM_shuttle/1000)) * gassen_laenge)\
              - lagervol_min / (ceil(gasse_anzahl) * (gasse_breite - (tiefe_FM_shuttle/1000)) * gassen_laenge)\
              % (hoehe_FM / 1000) + (hoehe_FM / 1000)
# print('gassenhoehe ist ' + str(gasse_hoehe))
# print('tiefe_FM_shuttle ' + str(tiefe_FM_shuttle))
# print('hoehe FM ' + str(hoehe_FM))
# print('lagervol min ' + str(lagervol_min))
# print('gassenbreite ' + str (gasse_breite))
# print('gasse laenge ' + str(gassen_laenge))
# print('gasse_anzahl ' + str(gasse_anzahl))
# print('anzahl faecher max L ' + str(anz_faecher_max_L))
# print('anzahl ebenen ' + str (anz_ebenen))
LM_min = anz_faecher / faecher_pro_ebene
# aufzuege_min
if liftvariante == 0:
    aufzuege_min = ceil(gasse_anzahl) * 2
else: aufzuege_min = ceil(gasse_anzahl)
# benoetigte_shuttles

######################
# Kommissionierleistung

weg_doppel_lift = (hoehe_LHM + (2/3) * (anz_ebenen - 1) * hoehe_LHM) / 1000
doppelspielzeit_lift = 2 * ((weg_doppel_lift / vy_aufzug) + (vy_aufzug / ay_aufzug)) + (vy_aufzug / ay_aufzug)\
                       + 2 * ladezeit_shuttle + 2 * ladezeit_aufzug + 3 * totzeit_aufzug
weg_einzel_lift = (hoehe_LHM + (1/2) * (anz_ebenen - 1) * hoehe_LHM) / 1000
einzelspielzeit_lift = 2 * ((weg_einzel_lift / vy_aufzug) + (vy_aufzug / ay_aufzug))\
                            + 2 * (ladezeit_aufzug + totzeit_aufzug)
weg_einzel_shuttle = (breite_LHM + (1/2) * (anz_faecher_max_L - 1) * breite_LHM) / 1000

print('weg doppel lift ' + str(weg_doppel_lift))
print('doppelspielzeit lift ' + str(doppelspielzeit_lift))
print('weg einzel lift ' + str(weg_einzel_lift))
print('einzelspiel lift ' + str(einzelspielzeit_lift))
print('weg einzel shuttle ' + str(weg_einzel_shuttle))

weg_ges = 2 * ((weg_einzel_shuttle / vx_shuttle) + (vx_shuttle / ax_shuttle)) + 2 * ((weg_einzel_lift / vy_aufzug) +
              (vy_aufzug / ay_aufzug)) + ladezeit_shuttle + exponentialfaktor + 2 * (totzeit_aufzug + totzeit_shuttle)
weg_doppel_shuttle = (breite_LHM + (2 / 3) * (anz_faecher_max_L - 1) * breite_LHM) / 1000
doppelspiel_ges = 2 * ((weg_doppel_shuttle / vx_shuttle) + (vx_shuttle / ax_shuttle)) + (vx_shuttle / ax_shuttle) + \
                  2 * ((weg_doppel_lift / vy_aufzug) + (vy_aufzug / ay_aufzug)) + (vy_aufzug / ay_aufzug) +\
                  2 * ladezeit_shuttle + 2 * ladezeit_aufzug + 3 * (totzeit_shuttle + totzeit_aufzug)
komm_leistung_lift_pro_gasse = 3600 / (spielfaehigkeit * 2 * einzelspielzeit_lift\
                                  + (1 - spielfaehigkeit) * doppelspielzeit_lift)
t_pro_gasse_mittel = (1 - spielfaehigkeit) * weg_ges + (spielfaehigkeit * doppelspiel_ges / 2)
komm_leistung_shuttle_pro_gasse = 3600 / t_pro_gasse_mittel
# shuttles pro gasse
if komm_leistung_lift_pro_gasse / komm_leistung_shuttle_pro_gasse > anz_ebenen:
    print('Lagerbreite verringern, Lifte nicht ausgelastet!')
    exit()
else: shuttles_pro_gasse = komm_leistung_lift_pro_gasse / komm_leistung_shuttle_pro_gasse
# shuttles min
if liftvariante == 0:
    shuttles_min = ceil(gasse_anzahl) * anz_ebenen
else: shuttles_min = ceil(shuttles_pro_gasse) * ceil(gasse_anzahl)
bedienzeit_shuttle_einzel = gassen_laenge / vx_shuttle + 2 * (vx_shuttle / ax_shuttle) + ladezeit_shuttle
bedienzeit_shuttle_doppel = (4 * gassen_laenge) / (3 * vx_shuttle) + (3 * vx_shuttle / ax_shuttle) +\
                            2 * ladezeit_shuttle
doppelspielzeit_shuttle = 2 * ((weg_doppel_shuttle / vx_shuttle) + (vx_shuttle / ax_shuttle)) +\
                          (vx_shuttle / ax_shuttle) + 4 * ladezeit_shuttle + 3 * totzeit_shuttle
einzelspielzeit_shuttle = 2 * ((weg_einzel_shuttle / vx_shuttle) + (vx_shuttle / ax_shuttle)) +\
                          + 2 * (ladezeit_shuttle + totzeit_shuttle)
doppelspiel_shuttle = (2 * ((doppelspielzeit_shuttle / vx_shuttle) + (vx_shuttle / ax_shuttle))) +\
                      (vx_shuttle / ax_shuttle)
doppelspiel_lift = (2 * ((weg_doppel_lift / vy_aufzug) + (vy_aufzug / ay_aufzug))) + (vy_aufzug / ay_aufzug)
bedienzeit_shuttle = (1 - spielfaehigkeit) * bedienzeit_shuttle_einzel + spielfaehigkeit *\
                     (bedienzeit_shuttle_doppel / 2)
zw_ankunftszeit = anz_ebenen * ((gasse_hoehe / vy_aufzug) + (2 * (vy_aufzug / ay_aufzug)) + ladezeit_aufzug)
komm_leistung_pro_ebene = (3600 / zw_ankunftszeit) *\
                          ((1 - ((bedienzeit_shuttle/zw_ankunftszeit) ** 2)) /
                           (1 - ((bedienzeit_shuttle / zw_ankunftszeit) ** 3)))
komm_leistung_pro_gasse = komm_leistung_pro_ebene * anz_ebenen
durchsatz_lift = t_pro_gasse_mittel * ceil(gasse_anzahl)
# komm_leist_ges
if liftvariante == 0:
    komm_leistung_ges = ceil(gasse_anzahl) * komm_leistung_pro_gasse
else: komm_leistung_ges = durchsatz_lift
if komm_leistung_ges < lagerleistung_min:
    print('Lagerleistung unter Anforderung! GAssenanzahl anpassen!')

######################
# Kosten

kosten_LM = LM_min * stueckkosten_LM
kosten_LHM = anz_faecher * stueckkosten_LHM
kosten_foerdermittel = shuttles_min * kosten_FM_shuttle + kosten_FM_aufzug * aufzuege_min
kosten_invest = kosten_LM + kosten_LHM + kosten_foerdermittel
print(kosten_invest)
# Betriebskosten
abschr_LM = kosten_LM / abschreibungsdauer_LM
abschr_LHM = kosten_LHM / abschreibungsdauer_LHM
abschr_FM = kosten_foerdermittel / abschreibungsdauer_FM_unstetig
abschr_jaehrl = abschr_LM + abschr_LHM + abschr_FM
kalk_zinsen_jaehrl = (1 / 2) * (zinsen / 100) * kosten_invest
wartung = kosten_invest * (wartungskosten / 100)
energie = kosten_invest * (energiekosten / 100)
Miete = gasse_breite * gassen_laenge * ceil(gasse_anzahl) * miete
kosten_betrieb = abschr_jaehrl + kalk_zinsen_jaehrl + wartung + energie + Miete
TCO = kosten_invest + (10 * kosten_betrieb)
print(TCO)

end = timeit.default_timer()
runtime = end - start
print('runtime ' + str(runtime))






