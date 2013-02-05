"""
Jan Willem Wijnands
Bin2A
11-1-2013
Dit script maakt vragen die gebruikt zouden kunnen worden voor de aminozuuretoets.
Optioneel slaat het programma ook de antwoorden op.
"""

#Specifiek = eiwit dat voldoet aan een bepaalde eigenschap

#TODO documentatie en consitentie van termen verbeteren
#TODO PEP8 richtlijnen controleren -> variabelen bovenaan zetten
#TODO Gebruik maken van een dictionary -> juiste antwoorden bij vragen antwoorden van vragen opslaan als dictionary?

import random
import datetime
import sys

#In deze matrix staat alle relevante data die gebruikt wordt om de vragen mee te maken
#Elke rij is een aminozuur en elke kolom is een type eigenschap
#0 = soort_aminozuur
#1 = 3 lettercode
#2 = 1 lettercode,
#3 = hydrofobiciteit
#4 = grootte
#5 = lading
#6 = preferentie
Aminozuur_matrix = [
    ["Alanine", "Ala", "A", "Hydrofoob", "Klein", "0", "H"],
    ["Arginine", "Arg", "R", "Hydrofiel", "Groot", "+", "N"],
    ["Asparagine", "Asn", "N", "Hydrofiel", "Middel", "0", "T"],
    ["Asparaginezuur", "Asp", "D", "Hydrofiel", "Middel", "-", "HT"],
    ["Cysteine", "Cys", "C", "Hydrofoob", "klein/middel", "0", "ST"],
    ["Phenylalanine", "Phe", "F", "Hydrofoob", "Groot", "0", "S"],
    ["Glutamine", "Gln", "Q", "Hydrofiel", "Groot", "0", "N"],
    ["Glutaminezuur", "Glu", "E", "Hydrofiel", "Groot", "-", "HS"],
    ["Glycine", "Gly", "G", "Tussenin", "Klein", "0", "T"],
    ["Histidine", "His", "H", "Hydrofiel", "Groot", "0", "N"],
    ["Isoleucine", "Ile", "I", "Hydrofoob", "Middel", "0", "S"],
    ["Leucine", "Leu", "L", "Hydrofoob", "Middel", "0", "HS"],
    ["Lysine", "Lys", "K", "Hydrofiel", "Groot", "+", "HT"],
    ["Methionine", "Met", "M", "Hydrofoob", "Groot", "0", "H"],
    ["Proline", "Pro", "P", "Hydrofoob", "Klein", "0", "T"],
    ["Serine", "Ser", "S", "Tussenin", "Klein", "0", "T"],
    ["Threonine", "Thr", "T", "Tussenin", "Klein", "0", "S"],
    ["Tryptofaan", "Trp", "W", "Hydrofoob", "Groot", "0", "S"],
    ["Tyrosine", "Tyr", "Y", "Hydrofoob", "Groot", "0", "S"],
    ["Valine", "Val", "V", "Hydrofoob", "Klein", "0", "S"]
]

def stop_mogelijkheid(invoer):
    """
    Elke keer als de gebruiker de mogelijkheid krijgt iets in te voeren,
    moet hij of zij ook de mogelijkheid krijgen om te kunnen stoppen met de q toets.
    """
    if invoer.upper() == "Q":
        sys.exit()


def zoek_specifieke_aminozuren(eigenschap, voorwaarde):
    """
    Zoek alle eiwitten die de opgegeven eigenschap /wel/ bevatten
    """

    specifieke_aminozuren = []
    for aminozuur in Aminozuur_matrix:
        #'in' ipv '==' zodat gecombineerde voorwaarden ook als True uit de test komen:
        #if S == HS = False
        #if S in HS = True
        if voorwaarde in aminozuur[eigenschap]:
            specifieke_aminozuren.append(aminozuur)

    return specifieke_aminozuren


def zoek_specifieke_aminozuren_inv(eigenschap, voorwaarde):
    """
    Zoek alle eiwitten die de opgegeven eigenschap /niet/ bevatten
    """

    specifieke_aminozuren = []
    for aminozuur in Aminozuur_matrix:
        #'not in' ipv '!=' zodat gecombineerde voorwaarden ook als False uit de test komen:
        #if S != HS = True
        #if S not in in HS = False
        if voorwaarde not in aminozuur[eigenschap]:
            specifieke_aminozuren.append(aminozuur)

    return specifieke_aminozuren


def init_vraag():
    """
    Deze functie doet niets anders dan een procedure die vaak herhaald wordt in het script uitvoeren
    """

    aminozuur = kies_random_aminozuur()

    #De 3 noteringstypen mogen voor deze vragen gebruikt worden.
    noteringstype = random.randint(0, 2)

    return aminozuur, noteringstype


def kies_random_aminozuur():
    """
    Kiest een random eiwit (rij) uit de Aminozuurmatrix
    """
    return random.choice(Aminozuur_matrix)


def creeer_specifieke_mogelijkheden(eigenschap, voorwaarde, noteringstype, vraag):
    """
    Creer een list en vul deze met het juiste antwoord en twee andere mogelijkheden die niet
    aan dezelfde voorwaarde voldoen als de voorwaarde van het juiste antwoord.
    """

    #Maak een set van de mogelijkheden lijst zodat er geen duplicaten opgenomen kunnen worden
    mogelijkheden = set()

    #Kies het juiste antwoord, deze moet minimaal voorkomen in de mogelijkheden
    random_specifieke_aminozuur = random.choice(zoek_specifieke_aminozuren(eigenschap, voorwaarde))[
                                  noteringstype]
    mogelijkheden.add(random_specifieke_aminozuur)

    #Zolang er geen 3 unieke vragen zijn gemaakt, maak meer vragen
    while len(mogelijkheden) != 3:
        #Voegt random een tweede en derde mogelijkheid toe met dezelfde soort eigenschap uit de matrix.
        #De andere mogelijkheden mogen niet aan dezelfde voorwaarde voldoen als die van het juiste antwoord! -> _inv
        mogelijkheden.add(random.choice(zoek_specifieke_aminozuren_inv(eigenschap, voorwaarde))[noteringstype])

    #Convert de set weer terug in een list
    mogelijkheden = list(mogelijkheden)

    #Shuffle de vragen, anders is A altijd het juiste antwoord
    random.shuffle(mogelijkheden)

    #Het juiste antwoord moet opgezocht worden en opgeslagen worden.
    antwoord = zoek_juiste_antwoord(mogelijkheden, random_specifieke_aminozuur)

    a = mogelijkheden[0]
    b = mogelijkheden[1]
    c = mogelijkheden[2]

    abc = ("A: %s\tB: %s\tC: %s" % (a, b, c))

    return vraag, abc, antwoord


def creeer_aspecifieke_mogelijkheden(aminozuur, eigenschap, vraag):
    """
    Creer een list en vul deze met het juiste antwoord en twee andere mogelijkheden die niet
    aan dezelfde voorwaarde voldoen als de voorwaarde van het juiste antwoord. Bij deze functie maakt
    het niet uit of...
    """

    #Maak een set van de mogelijkheden lijst zodat er geen duplicaten opgenomen kunnen worden
    mogelijkheden = set()

    #Kies het juiste antwoord, deze moet minimaal voorkomen in de mogelijkheden
    juiste_keuze = aminozuur[eigenschap]
    mogelijkheden.add(juiste_keuze)

    #Zolang er geen 3 unieke vragen zijn gemaakt, maak meer vragen
    while len(mogelijkheden) != 3:
        #Kies random aminozuren toe aan de mogelijkheden
        mogelijkheden.add(kies_random_aminozuur()[eigenschap])

    #Convert de set weer terug in een list
    mogelijkheden = list(mogelijkheden)

    #Kies het juiste antwoord, deze moet minimaal voorkomen in de mogelijkheden
    juiste_keuze = aminozuur[eigenschap]

    mogelijkheden.append(juiste_keuze)

    tweede_keuze = kies_random_aminozuur()[eigenschap]
    #Indien de zojuist gekozen tweede keuze al in de lijst met mogelijke keuzes voorkomt, kies een nieuwe!
    while tweede_keuze in mogelijkheden:
        tweede_keuze = kies_random_aminozuur()[eigenschap]
    mogelijkheden.append(tweede_keuze)

    #Hetzelfde geldt voor de derde keuze
    derde_keuze = kies_random_aminozuur()[eigenschap]
    while derde_keuze in mogelijkheden:
        derde_keuze = kies_random_aminozuur()[eigenschap]
    mogelijkheden.append(derde_keuze)

    #Shuffle de vragen, anders is A altijd het juiste antwoord
    random.shuffle(mogelijkheden)

    antwoord = zoek_juiste_antwoord(mogelijkheden, juiste_keuze)

    a = mogelijkheden[0]
    b = mogelijkheden[1]
    c = mogelijkheden[2]

    abc = ("A: %s\tB: %s\tC: %s" % (a, b, c))

    return vraag, abc, antwoord


def zoek_juiste_antwoord(mogelijkheden, juiste_keuze):
    """
    Een beetje een vieze oplossing maar nu eenmaal nodig sinds de mogelijkheden random geshuffeld worden
    """

    if mogelijkheden[0] == juiste_keuze:
        antwoord = "A"
    elif mogelijkheden[1] == juiste_keuze:
        antwoord = "B"
    else:
        antwoord = "C"

    return antwoord


def namen_vraag():
    aminozuur, noteringstype_vraag = init_vraag()

    if noteringstype_vraag == 0:
        #Deze vraag kan uitsluitend met de volledige naam en 3-lettercode noteringstypen gevraagd worden
        noteringstype_vraag = random.choice([0, 1])
        eigenschap_vraag = 2
        vraag = ("Wat is de 1-lettercode van aminozuur %s?" % aminozuur[noteringstype_vraag])
    elif noteringstype_vraag == 1:
        #Deze vraag kan uitsluitend met de volledige naam en 1-lettercode noteringstypen gevraagd worden
        noteringstype_vraag = random.choice([0, 2])
        eigenschap_vraag = 1
        vraag = ("Wat is de 3-lettercode van aminozuur %s?" % aminozuur[noteringstype_vraag])
    else:
        #Deze vraag kan uitsluitend met de 1-letter -en 3-lettercode noteringstypen gevraagd worden
        noteringstype_vraag = random.choice([1, 2])
        eigenschap_vraag = 0
        vraag = ("Wat is de volledige naam van aminozuur %s?" % aminozuur[noteringstype_vraag])

    return creeer_aspecifieke_mogelijkheden(aminozuur, eigenschap_vraag, vraag)


def hydrofobiciteit_vraag(specifiek):
    aminozuur, noteringstype = init_vraag()

    if specifiek:
        vraag = "Wat is de hydrofobiciteit van aminozuur %s?" % aminozuur[noteringstype]
        abc = "A: hydrofoob\tB: tussenin\tC: hydrofiel"

        juiste_antwoord = aminozuur[5]
        if juiste_antwoord == "hydrofoob":
            return vraag, abc, "A"
        elif juiste_antwoord == "tussenin":
            return vraag, abc, "B"
        else:
            return vraag, abc, "C"

    else:
        hydrofobiciteit = random.choice(["Hydrofiel", "Tussenin", "Hydrofoob"])
        if hydrofobiciteit == "Tussenin":
            vraag = "Welk aminozuur heeft een lading welke tussen hydrofoob en hydrofiel in zit? (tussenin)"
        else:
            vraag = ("Welk aminozuur is %s?" % hydrofobiciteit)

        return creeer_specifieke_mogelijkheden(3, hydrofobiciteit, noteringstype, vraag)


def grootte_vraag(specifiek):
    aminozuur, noteringstype = init_vraag()

    if specifiek:
        #Stel 1 op de 4 keer een klein/middel vraag
        if random.randint(0, 3) == 0:
            vraag = "Wat is de grootte van aminozuur %s?" % aminozuur[noteringstype]
            abc = "A: klein\tB: middel\tC: groot"

            juiste_antwoord = aminozuur[4]
            if juiste_antwoord == "+":
                return vraag, abc, "A"
            elif juiste_antwoord == "0":
                return vraag, abc, "B"
            else:
                return vraag, abc, "C"

        else:
            vraag = "Welk aminozuur zit tussen klein en middel in?"

            #Hoewel dit altijd Cysteine is, toch maar dynamisch geprogrammeerd zodat de matrix altijd nog aangepast kan
            #worden. Je weet het maar nooit met wetenschap.
            return creeer_specifieke_mogelijkheden(4, "klein/middel", noteringstype, vraag)

    else:
        #Kies random of er gevraagd wordt of het aminozuur klein, middelgroot of groot is.
        grootte_gevraagd = random.choice(["Klein", "Middel", "Groot"])
        if grootte_gevraagd == "Klein":
            vraag = "Welk aminozuur is klein?"
        elif grootte_gevraagd == "Middel":
            vraag = "Welk aminozuur is middelgroot?"
        else:
            vraag = "Welk aminozuur is groot?"

        return creeer_specifieke_mogelijkheden(4, grootte_gevraagd, noteringstype, vraag)


def lading_vraag(specifiek):
    aminozuur, noteringstype = init_vraag()

    if specifiek:
        vraag = "Wat is de lading van %s?" % aminozuur[noteringstype]
        abc = "A: +\tB: 0\tC: -"

        juiste_antwoord = aminozuur[5]
        if juiste_antwoord == "+":
            return vraag, abc, "A"
        elif juiste_antwoord == "0":
            return vraag, abc, "B"
        else:
            return vraag, abc, "C"

    else:
        lading_gevraagd = random.choice(["+", "0", "-"])
        if lading_gevraagd == "+":
            vraag = "Welk aminozuur is positief geladen bij pH7,4?"
        elif lading_gevraagd == "0":
            vraag = "Welk aminozuur is neutraal geladen bij pH7,4?"
        else:
            vraag = "Welk aminozuur is positief geladen bij pH7,4?"

        return creeer_specifieke_mogelijkheden(5, lading_gevraagd, noteringstype, vraag)

#TODO de mogelijkheden in preferentie vragen in de juiste volgorde gezet worden? Of niet?
def preferentie_vraag(specifiek):
    aminozuur, noteringstype = init_vraag()

    if specifiek:
        vraag = "Wat is de 3D preferentie van aminozuur %s?" % aminozuur[noteringstype]
        return creeer_aspecifieke_mogelijkheden(aminozuur, 6, vraag)

    else:
        #1 van de 4 keer wordt de "Geen preferentie" vraag gesteld
        if random.randint(0, 3) == 0:
            vraag = "Welk aminozuur heeft geen preferentie in 3D?"
            return creeer_specifieke_mogelijkheden(6, "N", noteringstype, vraag)

        else:
            preferenties = ["helix", "strand", "turn"]
            preferentie = random.choice(preferenties)

            vraag = "Welk aminozuur prefereert in 3D een %s?" % preferentie

            #preferentie_vraag[0].upper() = eerste letter van preferentie als hoofdletter
            return creeer_specifieke_mogelijkheden(6, preferentie[0].upper(), noteringstype, vraag)


def print_vraag(vraag):
    """
    Print de volgende twee regels waar een vraag uit bestaat en een harde enter, bijvoorbeeld:
    vraag[0] = Vraag 10: Welk aminozuur is positief geladen bij pH7,4?
    vraag[1]A: Valine    B: Asparaginezuur    C: Proline
    "\n"
    """

    print(vraag[0])
    print(vraag[1])
    print("\n")

#TODO antwoorden op scherm tonen
#TODO fouten opvangen
#Dit is de main functie
def main():
    #Introduceer de variabelen netjes.
    vragen_printen = False
    vragen_opslaan = False
    aantal_vragen = 0

    #Zolang er geen valide menuoptie gekozen is zal er geloopt worden.
    while True:
        print("Welkom bij de Aminozuurtoets maker!")
        print("\n")
        print("Hoe wilt u de gegenereerde vragen terug krijgen?")
        print("\n")
        print("1. Print alleen de vragen op het scherm.")
        print("2. Sla de vragen op in een bestand.")
        print("3. Vragen printen op het scherm en opslaan.")

        inv_gebruiker = input("--> ")
        stop_mogelijkheid(inv_gebruiker)

        if inv_gebruiker == "1":
            vragen_printen = True
            vragen_opslaan = False
            print("\n")
            #Er is een valide valide vraag gekozen, break de while loop.
            break
        elif inv_gebruiker == "2":
            vragen_printen = False
            vragen_opslaan = True
            print("\n")
            break
        elif inv_gebruiker == "3":
            vragen_printen = True
            vragen_opslaan = True
            print("\n")
            break
        else:
            print("Voer 1, 2 of 3 in.")

        print("\n")

    #TODO toch maar even een goeie eigen input functie maken die goed met int en str omgaat en waar je altijd kan q
    while True:
        aantal_vragen = int(input("Hoeveel vragen moeten er gemaakt worden? [minimaal 1 of meer] "))
        #stop_mogelijkheid(aantal_vragen)
        if aantal_vragen <= 0:
            print("Er kan minimaal 1 of meer gemaakt worden.")
        else:
            break

    gecreerde_vragen = []

    for te_creeren_vraag in range(aantal_vragen):
        random_vraagsoort = random.randint(0, 4)

        #Sommige functies die namen creeeren hebben een random getal nodig om
        #te bapelen of de vraag specifiek of aspecifiek gevraagd moet worden.
        randint = random.randint(0, 1)

        if random_vraagsoort == 0:
            vraag = namen_vraag()
        elif random_vraagsoort == 1:
            vraag = grootte_vraag(randint == 0)
        elif random_vraagsoort == 2:
            vraag = lading_vraag(randint == 0)
        elif random_vraagsoort == 3:
            vraag = hydrofobiciteit_vraag(randint == 0)
        elif random_vraagsoort == 4:
            vraag = preferentie_vraag(randint == 0)

        gecreerde_vragen.append(vraag)


    #Hier worden de vragen en antwoorden bestanden gecreerd.
    nu = datetime.datetime.now()
    antwoorden_bestand = open(
        "aminozuurtoets_ant_" + str(len(gecreerde_vragen)) + "_" + str(nu.day) + "_" + str(nu.month) + "_" + str(
            nu.year) + "_" + str(nu.hour) + "_" + str(nu.minute), "w")
    if vragen_opslaan:
        vragen_bestand = open(
            "aminozuurtoets_vr_" + str(len(gecreerde_vragen)) + "_" + str(nu.day) + "_" + str(
                nu.month) + "_" + str(
                nu.year) + "_" + str(nu.hour) + "_" + str(nu.minute), "w")

    for vraag_nummer, vraag in enumerate(gecreerde_vragen):
        antwoorden_bestand.write(str(vraag_nummer + 1) + "\t" + vraag[2])
        antwoorden_bestand.write("\n")

        if vragen_opslaan:
            vragen_bestand.write("Vraag " + str(vraag_nummer + 1) + ": " + vraag[0])
            vragen_bestand.write("\n")
            vragen_bestand.write(vraag[1])
            vragen_bestand.write("\n")
            vragen_bestand.write("\n")

        if vragen_printen:
            print("Vraag " + str(vraag_nummer + 1) + ": " + vraag[0])
            print(vraag[1])
            print("\n")

    if vragen_opslaan:
        vragen_bestand.close()

    #Antwoordenbestand altijd closen
    antwoorden_bestand.close()

#Roep de main functie aan om het circus te starten.
main()
