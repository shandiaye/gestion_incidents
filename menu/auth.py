from DAO.utilisateur_dao import UtilisateurDAO


class Auth:

    def __init__(self):
        self.dao = UtilisateurDAO()

    def connexion(self):
        print("=" * 40)
        print("   CONNEXION - Gestion des Tickets")
        print("=" * 40)

        tentatives = 3

        while tentatives > 0:
            login = input("Login : ").strip()
            mot_de_passe = input("Mot de passe : ").strip()

            try:
                utilisateur = self.dao.get_by_login(login)
            except Exception as erreur:
                print(f"Erreur lors de la connexion : {erreur}")
                return None

            if utilisateur is not None and utilisateur.password == UtilisateurDAO.hacher_mot_de_passe(mot_de_passe):
                print(f"\nBienvenue {utilisateur.prenom} {utilisateur.nom} "
                      f"({utilisateur.role}) !\n")
                return utilisateur

            tentatives -= 1
            print(f"Login ou mot de passe incorrect. "
                  f"Tentatives restantes : {tentatives}\n")

        print("Nombre de tentatives depasse. Fermeture de l'application.")
        return None
