import os
import hashlib

user_file= 'users.txt'

def hash_salasana(salasana):
    return hashlib.sha256(salasana.encode()).hexdigest()


def users_olemassa(käyttäjänimi):
    if not os.path.exists(user_file):
        return False
    with open(user_file, 'r') as f:
        return any(line.startswith()(f"{käyttäjänimi}:") for line in f)

def register():
    käyttäjänimi = input(" Anna käyttäjänimi: ")
    if users_olemassa(käyttäjänimi):
        print("Käyttäjä on jo olemassa")
        return
    salasana = input(" Anna uusi salasana: ")
    with open(user_file, 'a') as f:
        f.write(f"{käyttäjänimi}:{hash_salasana(salasana)}\n")
        print("Rekisteröidytty onnistuneesti")

def login():
    if not os.path.exists(user_file):
        print("Ei rekisteröityjä käyttäjiä")

    käyttäjänimi=input("Anna käyttäjänimi: ")
    salasana=input("Anna salasana: ")
    hashed = hash_salasana(salasana)
    with open(user_file, 'r') as f:
        for line in f:
            if line.strip() == f"{käyttäjänimi}:{hashed}":
                print(" Kirjauduttu onnistuneesti")
                return
        print("Kirjautuminen epäonnistui")


def main():
    options = {'1':register, '2':login, '3': exit}
    while True:
        print ("\n1.Register \n2.Login\n3.Exit")
        choice=input("valitse vaihtoehto: ")
        action = options.get(choice)
        if action:
            action()

        else:
            print(" Ei ole vaihtoehto")

if __name__ == "__main__":
    main()