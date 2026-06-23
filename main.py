from menu.auth import Auth

class Application:

    def demarrer(self):
        auth = Auth()
        auth.connexion()

if __name__ == "__main__":
    app = Application()
    app.demarrer()
