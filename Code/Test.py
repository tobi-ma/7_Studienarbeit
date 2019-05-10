from math import ceil
import timeit
import pandas as pd

# AllgemeineDaten
def import_allgemein(file_name):
   # Daten aus CSV-Datei importieren
   delimiter = ';'
   data = pd.read_csv(file_name, names=['variable', 'value'], sep=delimiter)
   data = data.set_index("variable", drop=False)
   print("CSV " + file_name + " importiert \n")
   return data


start = timeit.default_timer()



# Turmregal

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

facheranzahl_min = 48   # ae
lagerlange_max = 10   # ae
lagerhohe_max = 7.5   # oe
lagerbreite_max = 10
gangbreite = 2
exponentialfaktor = 2
lagerleistung_min = 20
tiefe_lhm = 0.32
breite_lhm = 1.26
hohe_lhm = 0.46   # oe
stuckkosten_lhm = 10   # ue
ay = 1
vy = 2
t_auf = 2
t_ab = 2
anz_gassen = 0
tiefe = 0.64
breite = 1.26
hohe = 7.36
stuekkosten_turm = 60000   # c

####################

# Lagerkonfiguration

facher_pro_LM = hohe // hohe_lhm
volumen_lagerfach = tiefe_lhm * breite_lhm * hohe_lhm
gassenbreite = 2 * tiefe + gangbreite
gassenlaenge = (lagerlange_max // breite) * breite
facheranzahl_max = (2 * gassenlaenge) / breite

if anz_gassen == 0:  # nicht so sinnvoll.... (TM) Also raus? (FR)
    gassenanzahl = facheranzahl_min / (facheranzahl_max * facher_pro_LM)
else:
    gassenanzahl = anz_gassen

LM_min = facheranzahl_min / facher_pro_LM

print(facher_pro_LM)
print(volumen_lagerfach)
print(gassenbreite)
print(gassenlaenge)
print(facheranzahl_max)
print(gassenanzahl)  # Rueckkopplung mit manueller Eingabe fuer anz_gassen sehr unelegant!
print(LM_min)

#####################
# Kosten

kosten_LM = stuekkosten_turm * ceil(LM_min)
kosten_LHM = stuckkosten_lhm * facher_pro_LM * ceil(LM_min)
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

wegzeit = (2 / exponentialfaktor) * ((hohe - hohe_lhm) / vy) + (2 * vy / ay)
t_einzelspiel = ((hohe - hohe_lhm) / vy) + 2 * (vy / ay)
t_einzel_plus = wegzeit + t_auf + t_ab
t_einzel_ex = (2 / exponentialfaktor) * ((hohe - hohe_lhm) / vy) + (2 * vy / ay)
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

AllgemeineDaten = import_allgemein('AllgemeineDaten.csv')
print(AllgemeineDaten)

# Import allgemeine Daten
AllgemeineDaten = import_allgemein('AllgemeineDaten.csv')

# Informationen bzgl. Produktionsdaten
produktionsdaten = [AllgemeineDaten.loc['anzahl_schichten', 'value'], AllgemeineDaten.loc['arbeitszeit', 'value'],
                    AllgemeineDaten.loc['lohnkosten', 'value'], AllgemeineDaten.loc['verteilzeitfaktor', 'value']]

# Informationen bzgl. der Artikel
artikeldaten = [AllgemeineDaten.loc['artikelgewicht', 'value'], AllgemeineDaten.loc['anzahl_artikel', 'value'],
                AllgemeineDaten.loc['anzahl_LHM_pro_position', 'value']]

# Parameter der Exponentialverteilung
para_lambda = AllgemeineDaten.loc['para_lambda', 'value']
F_hr_gleich = 0.5
F_z_gleich = 1 / 3
F_hr_expo = 1 / para_lambda
F_z_expo = AllgemeineDaten.loc['F_z_expo', 'value']
lagerdaten_faktoren = [para_lambda]


end = timeit.default_timer()
runtime = end - start
print('runtime ' + str(runtime))
