from kopiopelaaja import *
#Esim jos lokaatio on haluttu lokaatio niin lause on true
#Tämän avulla se koodi millä peli antaa käyttäjälle rahaa

käyttäjänraha = 0

if pelaajan_lokaatio("vesa") == pelaajan_lokaatio("vesa"):
    #Lokaatio on oikea = anna käyttäjälle rahaa
    käyttäjänraha += 10 #rahan määrä pitää vielä määrittää ja käyttäjän raha pitää määrittää jossain tiedostossa
print(käyttäjänraha)

