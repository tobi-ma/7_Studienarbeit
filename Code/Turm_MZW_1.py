from math import ceil
import timeit
start = timeit.default_timer()
import pandas as pd

def import_allgemein(file_name):
   # Daten aus CSV-Datei importieren
   delimiter = ';'
   data = pd.read_csv(file_name, names=['variable', 'value'], sep=delimiter)
   data = data.set_index("variable", drop=False)
   print("CSV " + file_name + " importiert \n")
   return data



# Turmregal
# AllgemeindeDaten

anzahl_schichten = 2
arbeitszeit = 8
lohnkosten = 50000
verteilzeitfaktor = 12
kalk_zinsen = 6
abschreibungsdauer_LM = 15   # die gibt das Finanzamt vor. soll das nicht hardcoded bleiben?
abschreibungsdauer_FM_unstetig = 8
abschreibungsdauer_FM_stetig = 14
abschreibungsdauer_LHM = 2
wartungskosten = 5
energiekosten = 5
miete = 36

# LagerstrukturDaten
anz_klt_pro_tablar = 10
faecheranzahl_min = 48
lagerlaenge_max = 10
lagerhoehe_max = 7.5
lagerbreite_max = 10
gangbreite = 2
exponentialfaktor = 2
lagerleistung_min = 20
tiefe_lhm = 0.32
breite_lhm = 1.26
hoehe_lhm = 0.46
stueckkosten_lhm = 10
ay = 1
vy = 2
t_auf = 2
t_ab = 2
anz_gassen = 0
tiefe = 0.64
breite = 1.26
hoehe = 7.36
stueckkosten_turm = 60000

####################

# Lagerkonfiguration

facher_pro_LM = (hoehe // hoehe_lhm) * anz_klt_pro_tablar
volumen_lagerfach = tiefe_lhm * breite_lhm * hoehe_lhm
gassenbreite = 2 * tiefe + gangbreite
gassenlaenge = (lagerlaenge_max // breite) * breite
facheranzahl_max = (2 * gassenlaenge) / breite

if anz_gassen == 0:  # nicht so sinnvoll.... (TM) Also raus? (FR)
    gassenanzahl = faecheranzahl_min / (facheranzahl_max * facher_pro_LM)
else:
    gassenanzahl = anz_gassen

LM_min = faecheranzahl_min / facher_pro_LM

print(facher_pro_LM)
print(volumen_lagerfach)
print(gassenbreite)
print(gassenlaenge)
print(facheranzahl_max)
print(gassenanzahl)  # Rueckkopplung mit manueller Eingabe fuer anz_gassen sehr unelegant!
print(LM_min)

#####################
# Kosten

kosten_LM = stueckkosten_turm * ceil(LM_min)
kosten_LHM = stueckkosten_lhm * facher_pro_LM * ceil(LM_min)
kosten_fordermittel = 0  # laut excel in D3-kosten enthalten
invest = kosten_LM + kosten_LHM + kosten_fordermittel
print(invest)

# Betriebskosten

abschreibung_LM = kosten_LM / abschreibungsdauer_LM
abschreibung_LHM = kosten_LHM / abschreibungsdauer_LHM
abschreibung_FM = kosten_fordermittel / abschreibungsdauer_FM_unstetig
abschreibung_jahrl = abschreibung_LM + abschreibung_LHM + abschreibung_FM
print(abschreibung_jahrl)

# Kalkulatorische Zinsen

kalk_zinsenen_jahrl = 0.5 * (kalk_zinsen / 100) * invest
wartung = invest * (wartungskosten / 100)
energie = invest * (energiekosten / 100)
flache = gassenbreite * gassenlaenge * ceil(gassenanzahl)
Miete = flache * miete  # m in EUR pro Flache; M in EUR
print(kalk_zinsenen_jahrl)
print(wartung)
print('Energiekosten = ' + str(energie))  # mach ich so jetzt alle?
print(Miete)
betriebskosten = abschreibung_jahrl + kalk_zinsenen_jahrl + wartung + energie + Miete
print(betriebskosten)

# Kommissionierleistung

wegzeit = (2 / exponentialfaktor) * ((hoehe - hoehe_lhm) / vy) + (2 * vy / ay)
t_einzelspiel = ((hoehe - hoehe_lhm) / vy) + 2 * (vy / ay)
t_einzel_plus = wegzeit + t_auf + t_ab
t_einzel_ex = (2 / exponentialfaktor) * ((hoehe - hoehe_lhm) / vy) + (2 * vy / ay)
t_einzel_ex_plus = t_einzel_ex + t_auf + t_ab
zw_ankunft = t_einzel_ex_plus
# kommissionierleistung pro Turm
if lagerleistung_min > ceil((LM_min / (t_einzelspiel / 3600))):
    print('fuer die definierte Leistung werden mehr Regale benoetigt')
    print('Romanes eunt Domus')
else:
    komm_pro_turm = 1 / (zw_ankunft / 3600)

print('Wegzeit ' + str(wegzeit))
print('zwischenankunftszeit ' + str(zw_ankunft))
print('kommissionierleistung pro Turm ' + str(komm_pro_turm))
print('EinzelspielZeit ' + str(t_einzelspiel))
print('Einzelspielzeit samt anderer ' + str(t_einzel_plus))
print('einzelspielzeit exponentialverteilung ' + str(t_einzel_ex))
print('Einzelspielzeit exponentialverteilung samt anderer ' + str(t_einzel_ex_plus))

# Zusammenfassung
komm_ges = 'zu klein'
# kommissionierleistung aller Turme
if komm_pro_turm * ceil(LM_min) < lagerleistung_min:
    print('Gassenanzahl manuell erhohen. Lagerleistung zu gering')
else:
    komm_ges = komm_pro_turm * ceil(LM_min)
TCO = invest + (abschreibung_jahrl + kalk_zinsenen_jahrl + wartung + energie + Miete) * 10

print('gesamte Kommissionierleistung ' + str(komm_ges))
print('TCO Turm ' + str(TCO))

end = timeit.default_timer()
runtime = end - start
print('runtime ' + str(runtime))