class Application:

    def demarrer(self):
        auth = Auth()
        utilisateur = auth.connexion()

        if utilisateur is not None:
            interface = Interface(utilisateur)
            interface.afficher_menu_principale()
            interface.afficher_menu()
        else:
            print("Connexion echouee. Fin du programme.")


if __name__ == "__main__":
    app = Application()
    app.demarrer()
