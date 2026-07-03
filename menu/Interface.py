class Interface:

    def __init__(self, utilisateur):
        self.utilisateur = utilisateur
        self.incidents = []
        self.utilisateurs = []

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
        statut = input("Statut : ")
        priorite = input("Priorité : ")

        incident = {
            "id": len(self.incidents) + 1,
            "titre": titre,
            "description": description,
            "statut": statut,
            "priorite": priorite
        }

        self.incidents.append(incident)

        print("Incident créé avec succès.")

    def voir_mes_incidents(self):
        print("\n--- Mes incidents ---")

        if not self.incidents:
            print("Aucun incident trouvé.")
            return

        for incident in self.incidents:
            print(
                f"ID: {incident['id']} | "
                f"Titre: {incident['titre']} | "
                f"Statut: {incident['statut']} | "
                f"Priorité: {incident['priorite']}"
            )

    def voir_detail_incident(self):
        print("\n--- Détail d'un incident ---")

        id_incident = int(input("Entrer l'ID de l'incident : "))

        for incident in self.incidents:
            if incident["id"] == id_incident:
                print(f"ID : {incident['id']}")
                print(f"Titre : {incident['titre']}")
                print(f"Description : {incident['description']}")
                print(f"Statut : {incident['statut']}")
                print(f"Priorité : {incident['priorite']}")
                return

        print("Incident introuvable.")

    def filtrer_par_statut(self):
        print("\n--- Filtrer par statut ---")

        statut = input("Statut recherché : ")

        trouve = False

        for incident in self.incidents:
            if incident["statut"].lower() == statut.lower():
                print(incident)
                trouve = True

        if not trouve:
            print("Aucun incident trouvé.")

    def filtrer_par_priorite(self):
        print("\n--- Filtrer par priorité ---")

        priorite = input("Priorité recherchée : ")

        trouve = False

        for incident in self.incidents:
            if incident["priorite"].lower() == priorite.lower():
                print(incident)
                trouve = True

        if not trouve:
            print("Aucun incident trouvé.")



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

        trouve = False

        for incident in self.incidents:
            if incident["statut"] in ["OUVERT", "EN_COURS"]:
                print(incident)
                trouve = True

        if not trouve:
            print("Aucun incident trouvé.")

    def prendre_en_charge(self):
        print("\n--- Prendre en charge un incident ---")

        id_incident = int(input("ID de l'incident : "))

        for incident in self.incidents:
            if incident["id"] == id_incident:
                if incident["statut"] != "OUVERT":
                    print("Seul un incident OUVERT peut être pris en charge.")
                    return
                incident["statut"] = "EN_COURS"
                print("Incident pris en charge.")
                return

        print("Incident introuvable.")

    def ajouter_intervention(self):
        print("\n--- Ajouter une intervention ---")

        id_incident = int(input("ID de l'incident : "))
        commentaire = input("Commentaire : ")
        duree = input("Durée (minutes) : ")

        for incident in self.incidents:
            if incident["id"] == id_incident:

                if incident["statut"] not in ["OUVERT", "EN_COURS"]:
                    print("Impossible : l'incident doit être OUVERT ou EN_COURS.")
                    return

                if "interventions" not in incident:
                    incident["interventions"] = []

                incident["interventions"].append({
                    "commentaire": commentaire,
                    "duree": duree
                })

                print("Intervention ajoutée.")
                return

        print("Incident introuvable.")

    def resoudre_incident(self):
        print("\n--- Résoudre un incident ---")

        id_incident = int(input("ID de l'incident : "))

        for incident in self.incidents:
            if incident["id"] == id_incident:
                if incident["statut"] != "EN_COURS":
                    print("Seul un incident EN_COURS peut être résolu.")
                    return
                incident["statut"] = "RESOLU"
                print("Incident résolu.")
                return

        print("Incident introuvable.")

    def fermer_incident(self):
        print("\n--- Fermer un incident ---")

        id_incident = int(input("ID de l'incident : "))

        for incident in self.incidents:
            if incident["id"] == id_incident:

                if incident["statut"] == "RESOLU":
                    incident["statut"] = "FERME"
                    print("Incident fermé.")
                else:
                    print("L'incident doit être résolu avant fermeture.")

                return

        print("Incident introuvable.")

    def consulter_historique(self):
        print("\n--- Historique des incidents traités ---")

        trouve = False

        for incident in self.incidents:
            if incident["statut"] in ["RESOLU", "FERME"]:
                print(incident)
                trouve = True

        if not trouve:
            print("Aucun historique trouvé.")



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

        trouve = False

        for incident in self.incidents:
            if incident["statut"] in ["OUVERT", "EN_COURS"]:
                print(incident)
                trouve = True

        if not trouve:
            print("Aucun incident trouvé.")

    def ajouter_utilisateur(self):
        print("\n--- Ajouter un utilisateur ---")

        nom = input("Nom : ")
        prenom = input("Prénom : ")
        login = input("Login : ")
        email = input("Email : ")
        role = input("Rôle (UTILISATEUR / TECHNICIEN / ADMIN) : ")
        service = input("Service : ")

        utilisateur = {
            "id": len(self.utilisateurs) + 1,
            "nom": nom,
            "prenom": prenom,
            "login": login,
            "email": email,
            "role": role,
            "service": service
        }

        self.utilisateurs.append(utilisateur)

        print("Utilisateur ajouté.")

    def afficher_utilisateurs(self):
        print("\n--- Utilisateurs ---")

        if not self.utilisateurs:
            print("Aucun utilisateur enregistré.")
            return

        for utilisateur in self.utilisateurs:
            print(utilisateur)

    def modifier_utilisateur(self):
        print("\n--- Modifier un utilisateur ---")

        id_user = int(input("ID utilisateur : "))

        for utilisateur in self.utilisateurs:
            if utilisateur["id"] == id_user:
                print("Laisser vide pour ne pas modifier un champ.")

                nom = input(f"Nom ({utilisateur['nom']}) : ")
                prenom = input(f"Prénom ({utilisateur['prenom']}) : ")
                email = input(f"Email ({utilisateur['email']}) : ")
                role = input(f"Rôle ({utilisateur['role']}) : ")
                service = input(f"Service ({utilisateur['service']}) : ")

                if nom:
                    utilisateur["nom"] = nom
                if prenom:
                    utilisateur["prenom"] = prenom
                if email:
                    utilisateur["email"] = email
                if role:
                    utilisateur["role"] = role
                if service:
                    utilisateur["service"] = service

                print("Utilisateur modifié avec succès.")
                return

        print("Utilisateur introuvable.")

    def supprimer_utilisateur(self):
        print("\n--- Supprimer un utilisateur ---")

        id_user = int(input("ID utilisateur : "))

        for utilisateur in self.utilisateurs:
            if utilisateur["id"] == id_user:
                self.utilisateurs.remove(utilisateur)
                print("Utilisateur supprimé.")
                return

        print("Utilisateur introuvable.")

    def consulter_tous_incidents(self):
        print("\n--- Tous les incidents ---")

        if not self.incidents:
            print("Aucun incident trouvé.")
            return

        for incident in self.incidents:
            print(incident)

    def stat_incidents_par_statut(self):
        print("\n--- Nombre d'incidents par statut ---")

        if not self.incidents:
            print("Aucun incident trouvé.")
            return

        statuts = ["OUVERT", "EN_COURS", "RESOLU", "FERME"]

        for statut in statuts:
            total = 0
            for incident in self.incidents:
                if incident["statut"] == statut:
                    total += 1
            print(f"{statut} : {total}")

    def stat_incidents_par_priorite(self):
        print("\n--- Nombre d'incidents par priorité ---")

        if not self.incidents:
            print("Aucun incident trouvé.")
            return

        priorites = ["BASSE", "MOYENNE", "HAUTE", "CRITIQUE"]

        for priorite in priorites:
            total = 0
            for incident in self.incidents:
                if incident["priorite"] == priorite:
                    total += 1
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
