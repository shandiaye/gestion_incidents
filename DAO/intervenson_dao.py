from DAO.base_dao import BaseDAO
from Models.intervention import Intervention


class InterventionDAO(BaseDAO):
    """
    Gere toutes les operations SQL sur la table intervention.
    """

    # ---------- METHODES GENERIQUES (heritees de BaseDAO) ----------

    def get_all(self):
        """Retourne toutes les interventions."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, commentaire, duree_minutes, date_intervention, incident_id, technicien_id FROM intervention"
            )
            lignes = cursor.fetchall()
            return [self._ligne_vers_intervention(l) for l in lignes]
        except Exception as e:
            print(f"Erreur get_all intervention : {e}")
            return []

    def get_by_id(self, id):
        """Retourne une intervention par son ID, ou None si non trouvee."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, commentaire, duree_minutes, date_intervention, incident_id, technicien_id FROM intervention WHERE id = %s",
                (id,)
            )
            ligne = cursor.fetchone()
            return self._ligne_vers_intervention(ligne) if ligne else None
        except Exception as e:
            print(f"Erreur get_by_id intervention : {e}")
            return None

    def delete_by_id(self, id):
        """Supprime une intervention par son ID."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute("DELETE FROM intervention WHERE id = %s", (id,))
            self.conn.commit()
            print("Intervention supprimee avec succes.")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur delete_by_id intervention : {e}")
            return False

    # ---------- METHODES SPECIFIQUES ----------

    def ajouter(self, intervention):
        """
        Ajoute une intervention sur un incident.
        Verifie que l'incident est OUVERT ou EN_COURS avant d'inserer.
        """
        try:
            # Verification du statut de l'incident
            cursor = self.conn.get_cursor()
            cursor.execute("SELECT statut FROM incident WHERE id = %s", (intervention.incident_id,))
            ligne = cursor.fetchone()

            if not ligne:
                print("Incident introuvable.")
                return False

            if ligne[0] not in ("OUVERT", "EN_COURS"):
                print(f"Impossible d'intervenir : l'incident est en statut '{ligne[0]}'.")
                return False

            cursor.execute(
                """INSERT INTO intervention (commentaire, duree_minutes, incident_id, technicien_id)
                   VALUES (%s, %s, %s, %s)""",
                (intervention.commentaire, intervention.duree_minutes,
                 intervention.incident_id, intervention.technicien_id)
            )
            self.conn.commit()
            print("Intervention ajoutee avec succes.")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur ajouter intervention : {e}")
            return False

    def get_by_incident(self, incident_id):
        """Retourne toutes les interventions d'un incident specifique."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, commentaire, duree_minutes, date_intervention, incident_id, technicien_id FROM intervention WHERE incident_id = %s",
                (incident_id,)
            )
            lignes = cursor.fetchall()
            return [self._ligne_vers_intervention(l) for l in lignes]
        except Exception as e:
            print(f"Erreur get_by_incident : {e}")
            return []

    def get_by_technicien(self, technicien_id):
        """Retourne toutes les interventions d'un technicien specifique."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, commentaire, duree_minutes, date_intervention, incident_id, technicien_id FROM intervention WHERE technicien_id = %s",
                (technicien_id,)
            )
            lignes = cursor.fetchall()
            return [self._ligne_vers_intervention(l) for l in lignes]
        except Exception as e:
            print(f"Erreur get_by_technicien : {e}")
            return []

    # ---------- METHODE UTILITAIRE PRIVEE ----------

    def _ligne_vers_intervention(self, ligne):
        """Convertit une ligne SQL en objet Intervention."""
        return Intervention(
            id=ligne[0], commentaire=ligne[1], duree_minutes=ligne[2],
            date_intervention=ligne[3], incident_id=ligne[4], technicien_id=ligne[5]
        )

    def top_techniciens(self, limite=3):
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                """SELECT u.id, u.nom, u.prenom, COUNT(i.id) AS nb_interventions
                   FROM intervention i
                   JOIN utilisateur u ON i.technicien_id = u.id
                   GROUP BY u.id, u.nom, u.prenom
                   ORDER BY nb_interventions DESC
                   LIMIT %s""",
                (limite,)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Erreur top_techniciens : {e}")
            return []

    def stats_par_technicien(self):
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                """SELECT u.id, u.nom, u.prenom,
                          COUNT(i.id) AS nb_interventions,
                          COALESCE(SUM(i.duree_minutes), 0) AS temps_total,
                          COALESCE(AVG(i.duree_minutes), 0) AS temps_moyen
                   FROM utilisateur u
                   LEFT JOIN intervention i ON i.technicien_id = u.id
                   WHERE u.role = 'TECHNICIEN'
                   GROUP BY u.id, u.nom, u.prenom
                   ORDER BY nb_interventions DESC"""
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Erreur stats_par_technicien : {e}")
            return []