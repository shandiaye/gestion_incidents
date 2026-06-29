from DAO.base_dao import BaseDAO
from Models.utilisateur import Utilisateur


class UtilisateurDAO(BaseDAO):
    """
    Gere toutes les operations SQL sur la table utilisateur.
    """

    # ---------- METHODES GENERIQUES (heritees de BaseDAO) ----------

    def get_all(self):
        """Retourne la liste de tous les utilisateurs."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute("SELECT id, login, password, nom, prenom, email, role, service, date_creation FROM utilisateur")
            lignes = cursor.fetchall()
            utilisateurs = []
            for ligne in lignes:
                u = Utilisateur(
                    id=ligne[0], login=ligne[1], password=ligne[2],
                    nom=ligne[3], prenom=ligne[4], email=ligne[5],
                    role=ligne[6], service=ligne[7], date_creation=ligne[8]
                )
                utilisateurs.append(u)
            return utilisateurs
        except Exception as e:
            print(f"Erreur get_all utilisateur : {e}")
            return []

    def get_by_id(self, id):
        """Retourne un utilisateur par son ID, ou None si non trouve."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, login, password, nom, prenom, email, role, service, date_creation FROM utilisateur WHERE id = %s",
                (id,)
            )
            ligne = cursor.fetchone()
            if ligne:
                return Utilisateur(
                    id=ligne[0], login=ligne[1], password=ligne[2],
                    nom=ligne[3], prenom=ligne[4], email=ligne[5],
                    role=ligne[6], service=ligne[7], date_creation=ligne[8]
                )
            return None
        except Exception as e:
            print(f"Erreur get_by_id utilisateur : {e}")
            return None

    def delete_by_id(self, id):
        """
        Supprime un utilisateur par son ID.
        Refuse la suppression s'il a des incidents ou des interventions.
        """
        try:
            # Verification : l'utilisateur a-t-il des incidents ?
            cursor = self.conn.get_cursor()
            cursor.execute("SELECT COUNT(*) FROM incident WHERE utilisateur_id = %s", (id,))
            nb_incidents = cursor.fetchone()[0]

            # Verification : l'utilisateur a-t-il des interventions ?
            cursor.execute("SELECT COUNT(*) FROM intervention WHERE technicien_id = %s", (id,))
            nb_interventions = cursor.fetchone()[0]

            if nb_incidents > 0 or nb_interventions > 0:
                print("Impossible de supprimer : cet utilisateur a des incidents ou des interventions associes.")
                return False

            cursor.execute("DELETE FROM utilisateur WHERE id = %s", (id,))
            self.conn.commit()
            print("Utilisateur supprime avec succes.")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur delete_by_id utilisateur : {e}")
            return False

    # ---------- METHODES SPECIFIQUES ----------

    def ajouter(self, utilisateur):
        """Ajoute un nouvel utilisateur dans la base."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                """INSERT INTO utilisateur (login, password, nom, prenom, email, role, service)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (utilisateur.login, utilisateur.password, utilisateur.nom,
                 utilisateur.prenom, utilisateur.email, utilisateur.role, utilisateur.service)
            )
            self.conn.commit()
            print("Utilisateur ajoute avec succes.")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur ajouter utilisateur : {e}")
            return False

    def modifier(self, utilisateur):
        """Met a jour les informations d'un utilisateur existant."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                """UPDATE utilisateur
                   SET login=%s, password=%s, nom=%s, prenom=%s, email=%s, role=%s, service=%s
                   WHERE id=%s""",
                (utilisateur.login, utilisateur.password, utilisateur.nom,
                 utilisateur.prenom, utilisateur.email, utilisateur.role,
                 utilisateur.service, utilisateur.id)
            )
            self.conn.commit()
            print("Utilisateur modifie avec succes.")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur modifier utilisateur : {e}")
            return False

    def get_by_login(self, login):
        """Retourne un utilisateur par son login, ou None si non trouve."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, login, password, nom, prenom, email, role, service, date_creation FROM utilisateur WHERE login = %s",
                (login,)
            )
            ligne = cursor.fetchone()
            if ligne:
                return Utilisateur(
                    id=ligne[0], login=ligne[1], password=ligne[2],
                    nom=ligne[3], prenom=ligne[4], email=ligne[5],
                    role=ligne[6], service=ligne[7], date_creation=ligne[8]
                )
            return None
        except Exception as e:
            print(f"Erreur get_by_login : {e}")
            return None

    def rechercher(self, mot_cle):
        """Recherche des utilisateurs par nom, login ou service."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                """SELECT id, login, password, nom, prenom, email, role, service, date_creation
                   FROM utilisateur
                   WHERE nom ILIKE %s OR login ILIKE %s OR service ILIKE %s""",
                (f"%{mot_cle}%", f"%{mot_cle}%", f"%{mot_cle}%")
            )
            lignes = cursor.fetchall()
            return [
                Utilisateur(
                    id=l[0], login=l[1], password=l[2], nom=l[3],
                    prenom=l[4], email=l[5], role=l[6], service=l[7], date_creation=l[8]
                ) for l in lignes
            ]
        except Exception as e:
            print(f"Erreur rechercher utilisateur : {e}")
            return []
