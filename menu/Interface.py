from DAO.utilisateur_dao import UtilisateurDAO
from DAO.incident_dao import IncidentDAO
from DAO.intervention_dao import InterventionDAO
from Models.utilisateur import Utilisateur
from Models.incident import Incident
from Models.intervention import Intervention


class Interface:

    def __init__(self, utilisateur):
        self.utilisateur = utilisateur
        self.dao = UtilisateurDAO()          
        self.incident_dao = IncidentDAO()    
        self.intervention_dao = InterventionDAO()  

    def afficher_menu_principale(self):
        print("Bienvenue au système de gestion des tickets d'incidents!")

    def afficher_menu(self):
        role = self.utilisateur.role

        if role == "UTILISATEUR":
            self.menu_utilisateur()

        elif role == "TECHNICIEN":
            self.menu_technicien()

        elif role == "ADMIN":
            self.menu_admin()


    def menu_utilisateur(self):
        while True:
            print("\n--- MENU UTILISATEUR ---")

            print("1. Creer un incident")
            print("2. Voir mes incidents")
            print("3. Voir le detail d'un incident")
            print("4. Filtrer mes incidents par statut")
            print("5. Filtrer mes incidents par priorite")
            print("0. Quitter")

            choix = input("Choix : ")

            if choix == "1":
                self.creer_incident()

            elif choix == "2":
                self.voir_mes_incidents()

            elif choix == "3":
                self.voir_detail_incident()

            elif choix == "4":
                self.filtrer_par_statut()

            elif choix == "5":
                self.filtrer_par_priorite()

            elif choix == "0":
                print("Au revoir")
                break

            else:
                print("Choix invalide")

    def creer_incident(self):
        print("\n--- Création d'un incident ---")

        titre = input("Titre : ")
        description = input("Description : ")
        priorite = input("Priorité : ")

        nouvel_incident = Incident(
            titre=titre,
            description=description,
            priorite=priorite,
            utilisateur_id=self.utilisateur.id
        )

        self.incident_dao.ajouter(nouvel_incident)

    def voir_mes_incidents(self):
        print("\n--- Mes incidents ---")

        incidents = self.incident_dao.get_by_utilisateur(self.utilisateur.id)

        if not incidents:
            print("Aucun incident trouvé.")
            return

        for incident in incidents:
            print(
                f"ID: {incident.id} | "
                f"Titre: {incident.titre} | "
                f"Statut: {incident.statut} | "
                f"Priorité: {incident.priorite}"
            )

    def voir_detail_incident(self):
        print("\n--- Détail d'un incident ---")

        id_incident = int(input("Entrer l'ID de l'incident : "))

        incident = self.incident_dao.get_by_id(id_incident)

        if incident is None or incident.utilisateur_id != self.utilisateur.id:
            print("Incident introuvable.")
            return

        print(f"ID : {incident.id}")
        print(f"Titre : {incident.titre}")
        print(f"Description : {incident.description}")
        print(f"Statut : {incident.statut}")
        print(f"Priorité : {incident.priorite}")

    def filtrer_par_statut(self):
        print("\n--- Filtrer par statut ---")

        statut = input("Statut recherché : ").upper()

        incidents = self.incident_dao.filtrer_par_statut(statut, utilisateur_id=self.utilisateur.id)

        if not incidents:
            print("Aucun incident trouvé.")
            return

        for incident in incidents:
            print(f"ID: {incident.id} | Titre: {incident.titre} | Statut: {incident.statut} | Priorité: {incident.priorite}")

    def filtrer_par_priorite(self):
        print("\n--- Filtrer par priorité ---")

        priorite = input("Priorité recherchée : ").upper()

        incidents = self.incident_dao.filtrer_par_priorite(priorite, utilisateur_id=self.utilisateur.id)

        if not incidents:
            print("Aucun incident trouvé.")
            return

        for incident in incidents:
            print(f"ID: {incident.id} | Titre: {incident.titre} | Statut: {incident.statut} | Priorité: {incident.priorite}")



    def menu_technicien(self):
        while True:
            print("\n--- MENU TECHNICIEN ---")
            print("1. Consulter tous les incidents OUVERTS ou EN_COURS")
            print("2. Prendre en charge un incident")
            print("3. Ajouter une intervention")
            print("4. Résoudre un incident")
            print("5. Fermer un incident")
            print("6. Consulter l'historique des incidents traités")
            print("0. Quitter")

            choix = input("Choix : ")

            if choix == "1":
                self.consulter_incidents()

            elif choix == "2":
                self.prendre_en_charge()

            elif choix == "3":
                self.ajouter_intervention()

            elif choix == "4":
                self.resoudre_incident()

            elif choix == "5":
                self.fermer_incident()

            elif choix == "6":
                self.consulter_historique()

            elif choix == "0":
                print("Déconnexion...")
                break

            else:
                print("Choix invalide.")

    def consulter_incidents(self):
        print("\n--- Incidents OUVERTS ou EN_COURS ---")

        incidents = self.incident_dao.get_ouverts_et_en_cours()

        if not incidents:
            print("Aucun incident trouvé.")
            return

        for incident in incidents:
            print(f"ID: {incident.id} | Titre: {incident.titre} | Statut: {incident.statut} | Priorité: {incident.priorite}")

    def prendre_en_charge(self):
        print("\n--- Prendre en charge un incident ---")

        id_incident = int(input("ID de l'incident : "))

        self.incident_dao.changer_statut(id_incident, "EN_COURS")

    def ajouter_intervention(self):
        print("\n--- Ajouter une intervention ---")

        id_incident = int(input("ID de l'incident : "))
        commentaire = input("Commentaire : ")
        duree = input("Durée (minutes) : ")

        nouvelle_intervention = Intervention(
            commentaire=commentaire,
            duree_minutes=duree,
            incident_id=id_incident,
            technicien_id=self.utilisateur.id
        )


        self.intervention_dao.ajouter(nouvelle_intervention)

    def resoudre_incident(self):
        print("\n--- Résoudre un incident ---")

        id_incident = int(input("ID de l'incident : "))


        self.incident_dao.changer_statut(id_incident, "RESOLU")

    def fermer_incident(self):
        print("\n--- Fermer un incident ---")

        id_incident = int(input("ID de l'incident : "))


        self.incident_dao.changer_statut(id_incident, "FERME")

    def consulter_historique(self):
        print("\n--- Historique des incidents traités ---")

        resolus = self.incident_dao.filtrer_par_statut("RESOLU")
        fermes = self.incident_dao.filtrer_par_statut("FERME")
        incidents = resolus + fermes

        if not incidents:
            print("Aucun historique trouvé.")
            return

        for incident in incidents:
            print(f"ID: {incident.id} | Titre: {incident.titre} | Statut: {incident.statut} | Priorité: {incident.priorite}")



    def menu_admin(self):
        while True:
            print("\n--- MENU ADMIN ---")
            print("1. Consulter les incidents OUVERTS ou EN_COURS")
            print("2. Prendre en charge un incident")
            print("3. Ajouter une intervention")
            print("4. Résoudre un incident")
            print("5. Fermer un incident")
            print("6. Historique des incidents traités")

            print("\n--- Gestion Utilisateurs ---")
            print("7. Ajouter un utilisateur")
            print("8. Afficher les utilisateurs")
            print("9. Modifier un utilisateur")
            print("10. Supprimer un utilisateur")

            print("\n--- Rapports ---")
            print("11. Consulter tous les incidents")
            print("12. Nombre d'incidents par statut")
            print("13. Nombre d'incidents par priorité")
            print("14. Temps moyen de résolution")
            print("15. Top 3 techniciens les plus actifs")
            print("16. Statistiques par technicien")
            print("17. Taux de résolution sous 48h")

            print("0. Quitter")

            choix = input("Choix : ")

            if choix == "1":
                self.consulter_incidents_ouverts()

            elif choix == "2":
                self.prendre_en_charge()

            elif choix == "3":
                self.ajouter_intervention()

            elif choix == "4":
                self.resoudre_incident()

            elif choix == "5":
                self.fermer_incident()

            elif choix == "6":
                self.consulter_historique()

            elif choix == "7":
                self.ajouter_utilisateur()

            elif choix == "8":
                self.afficher_utilisateurs()

            elif choix == "9":
                self.modifier_utilisateur()

            elif choix == "10":
                self.supprimer_utilisateur()

            elif choix == "11":
                self.consulter_tous_incidents()

            elif choix == "12":
                self.stat_incidents_par_statut()

            elif choix == "13":
                self.stat_incidents_par_priorite()

            elif choix == "14":
                self.temps_moyen_resolution()

            elif choix == "15":
                self.top_3_techniciens()

            elif choix == "16":
                self.stats_par_technicien()

            elif choix == "17":
                self.taux_resolution_48h()

            elif choix == "0":
                print("Déconnexion...")
                break

            else:
                print("Choix invalide.")

    def consulter_incidents_ouverts(self):
        print("\n--- Incidents OUVERTS ou EN_COURS ---")

        incidents = self.incident_dao.get_ouverts_et_en_cours()

        if not incidents:
            print("Aucun incident trouvé.")
            return

        for incident in incidents:
            print(f"ID: {incident.id} | Titre: {incident.titre} | Statut: {incident.statut} | Priorité: {incident.priorite}")



    def ajouter_utilisateur(self):
        print("\n--- Ajouter un utilisateur ---")

        nom = input("Nom : ")
        prenom = input("Prénom : ")
        login = input("Login : ")
        password = input("Mot de passe : ")
        email = input("Email : ")
        role = input("Rôle (UTILISATEUR / TECHNICIEN / ADMIN) : ")
        service = input("Service : ")

        nouvel_utilisateur = Utilisateur(
            login=login,
            password=password,
            nom=nom,
            prenom=prenom,
            email=email,
            role=role,
            service=service
        )


        self.dao.ajouter(nouvel_utilisateur)

    def afficher_utilisateurs(self):
        print("\n--- Utilisateurs ---")

        utilisateurs = self.dao.get_all()

        if not utilisateurs:
            print("Aucun utilisateur enregistré.")
            return

        for u in utilisateurs:
            print(
                f"ID: {u.id} | Login: {u.login} | Nom: {u.nom} {u.prenom} | "
                f"Email: {u.email} | Rôle: {u.role} | Service: {u.service}"
            )

    def modifier_utilisateur(self):
        print("\n--- Modifier un utilisateur ---")

        id_user = int(input("ID utilisateur : "))

        utilisateur = self.dao.get_by_id(id_user)

        if utilisateur is None:
            print("Utilisateur introuvable.")
            return

        print("Laisser vide pour ne pas modifier un champ.")

        nom = input(f"Nom ({utilisateur.nom}) : ")
        prenom = input(f"Prénom ({utilisateur.prenom}) : ")
        email = input(f"Email ({utilisateur.email}) : ")
        role = input(f"Rôle ({utilisateur.role}) : ")
        service = input(f"Service ({utilisateur.service}) : ")

        if nom:
            utilisateur.nom = nom
        if prenom:
            utilisateur.prenom = prenom
        if email:
            utilisateur.email = email
        if role:
            utilisateur.role = role
        if service:
            utilisateur.service = service


        self.dao.modifier(utilisateur)

    def supprimer_utilisateur(self):
        print("\n--- Supprimer un utilisateur ---")

        id_user = int(input("ID utilisateur : "))

        utilisateur = self.dao.get_by_id(id_user)

        if utilisateur is None:
            print("Utilisateur introuvable.")
            return


        self.dao.delete_by_id(id_user)

    def consulter_tous_incidents(self):
        print("\n--- Tous les incidents ---")

        incidents = self.incident_dao.get_all()

        if not incidents:
            print("Aucun incident trouvé.")
            return

        for incident in incidents:
            print(f"ID: {incident.id} | Titre: {incident.titre} | Statut: {incident.statut} | Priorité: {incident.priorite}")

    def stat_incidents_par_statut(self):
        print("\n--- Nombre d'incidents par statut ---")

        incidents = self.incident_dao.get_all()

        if not incidents:
            print("Aucun incident trouvé.")
            return

        statuts = ["OUVERT", "EN_COURS", "RESOLU", "FERME"]

        for statut in statuts:
            total = sum(1 for incident in incidents if incident.statut == statut)
            print(f"{statut} : {total}")

    def stat_incidents_par_priorite(self):
        print("\n--- Nombre d'incidents par priorité ---")

        incidents = self.incident_dao.get_all()

        if not incidents:
            print("Aucun incident trouvé.")
            return

        priorites = ["BASSE", "MOYENNE", "HAUTE", "CRITIQUE"]

        for priorite in priorites:
            total = sum(1 for incident in incidents if incident.priorite == priorite)
            print(f"{priorite} : {total}")

    def temps_moyen_resolution(self):
        print("\n--- Temps moyen de résolution ---")
        print("Fonctionnalité à connecter à la base de données "
              "(nécessite date_creation et date de résolution).")

    def top_3_techniciens(self):
        print("\n--- Top 3 techniciens les plus actifs ---")
        print("Fonctionnalité à connecter à la base de données "
              "(nécessite la table intervention).")

    def stats_par_technicien(self):
        print("\n--- Statistiques par technicien ---")
        print("Fonctionnalité à connecter à la base de données "
              "(nécessite la table intervention).")

    def taux_resolution_48h(self):
        print("\n--- Taux de résolution sous 48h ---")
        print("Fonctionnalité à connecter à la base de données "
              "(nécessite date_creation et date de résolution).")
