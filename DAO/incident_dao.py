from DAO.base_dao import BaseDAO
from Models.incident import Incident


class IncidentDAO(BaseDAO):
    """
    Gere toutes les operations SQL sur la table incident.
    """

    # Transitions de statut autorisees
    TRANSITIONS = {
        "OUVERT": ["EN_COURS", "ANNULE"],
        "EN_COURS": ["RESOLU"],
        "RESOLU": ["FERME"],
        "FERME": [],
        "ANNULE": []
    }

    # ---------- METHODES GENERIQUES (heritees de BaseDAO) ----------

    def get_all(self):
        """Retourne tous les incidents (utilise par l'admin)."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id FROM incident"
            )
            lignes = cursor.fetchall()
            return [self._ligne_vers_incident(l) for l in lignes]
        except Exception as e:
            print(f"Erreur get_all incident : {e}")
            return []

    def get_by_id(self, id):
        """Retourne un incident par son ID, ou None si non trouve."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id FROM incident WHERE id = %s",
                (id,)
            )
            ligne = cursor.fetchone()
            return self._ligne_vers_incident(ligne) if ligne else None
        except Exception as e:
            print(f"Erreur get_by_id incident : {e}")
            return None

    def delete_by_id(self, id):
        """
        Supprime un incident par son ID.
        Refuse la suppression s'il a des interventions associees.
        """
        try:
            cursor = self.conn.get_cursor()
            cursor.execute("SELECT COUNT(*) FROM intervention WHERE incident_id = %s", (id,))
            nb = cursor.fetchone()[0]
            if nb > 0:
                print("Impossible de supprimer : cet incident a des interventions associees.")
                return False
            cursor.execute("DELETE FROM incident WHERE id = %s", (id,))
            self.conn.commit()
            print("Incident supprime avec succes.")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur delete_by_id incident : {e}")
            return False

    # ---------- METHODES SPECIFIQUES ----------

    def ajouter(self, incident):
        """Cree un nouvel incident (statut OUVERT par defaut)."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                """INSERT INTO incident (titre, description, priorite, statut, utilisateur_id)
                   VALUES (%s, %s, %s, %s, %s)""",
                (incident.titre, incident.description, incident.priorite,
                 "OUVERT", incident.utilisateur_id)
            )
            self.conn.commit()
            print("Incident cree avec succes.")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur ajouter incident : {e}")
            return False

    def get_by_utilisateur(self, utilisateur_id):
        """Retourne tous les incidents d'un utilisateur specifique."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id FROM incident WHERE utilisateur_id = %s",
                (utilisateur_id,)
            )
            lignes = cursor.fetchall()
            return [self._ligne_vers_incident(l) for l in lignes]
        except Exception as e:
            print(f"Erreur get_by_utilisateur : {e}")
            return []

    def filtrer_par_statut(self, statut, utilisateur_id=None):
        """
        Retourne les incidents filtres par statut.
        Si utilisateur_id est fourni, filtre aussi par utilisateur.
        """
        try:
            cursor = self.conn.get_cursor()
            if utilisateur_id:
                cursor.execute(
                    "SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id FROM incident WHERE statut = %s AND utilisateur_id = %s",
                    (statut, utilisateur_id)
                )
            else:
                cursor.execute(
                    "SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id FROM incident WHERE statut = %s",
                    (statut,)
                )
            lignes = cursor.fetchall()
            return [self._ligne_vers_incident(l) for l in lignes]
        except Exception as e:
            print(f"Erreur filtrer_par_statut : {e}")
            return []

    def filtrer_par_priorite(self, priorite, utilisateur_id=None):
        """
        Retourne les incidents filtres par priorite.
        Si utilisateur_id est fourni, filtre aussi par utilisateur.
        """
        try:
            cursor = self.conn.get_cursor()
            if utilisateur_id:
                cursor.execute(
                    "SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id FROM incident WHERE priorite = %s AND utilisateur_id = %s",
                    (priorite, utilisateur_id)
                )
            else:
                cursor.execute(
                    "SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id FROM incident WHERE priorite = %s",
                    (priorite,)
                )
            lignes = cursor.fetchall()
            return [self._ligne_vers_incident(l) for l in lignes]
        except Exception as e:
            print(f"Erreur filtrer_par_priorite : {e}")
            return []

    def get_ouverts_et_en_cours(self):
        """Retourne tous les incidents OUVERTS ou EN_COURS (pour les techniciens)."""
        try:
            cursor = self.conn.get_cursor()
            cursor.execute(
                "SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id FROM incident WHERE statut IN ('OUVERT', 'EN_COURS')"
            )
            lignes = cursor.fetchall()
            return [self._ligne_vers_incident(l) for l in lignes]
        except Exception as e:
            print(f"Erreur get_ouverts_et_en_cours : {e}")
            return []

    def changer_statut(self, incident_id, nouveau_statut):
        """
        Change le statut d'un incident en respectant les transitions autorisees.
        """
        try:
            incident = self.get_by_id(incident_id)
            if not incident:
                print("Incident introuvable.")
                return False

            # Verification de la transition
            transitions_autorisees = self.TRANSITIONS.get(incident.statut, [])
            if nouveau_statut not in transitions_autorisees:
                print(f"Transition interdite : {incident.statut} → {nouveau_statut}")
                return False

            cursor = self.conn.get_cursor()
            cursor.execute(
                "UPDATE incident SET statut = %s WHERE id = %s",
                (nouveau_statut, incident_id)
            )
            self.conn.commit()
            print(f"Statut mis a jour : {incident.statut} → {nouveau_statut}")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur changer_statut : {e}")
            return False

    # ---------- METHODE UTILITAIRE PRIVEE ----------

    def _ligne_vers_incident(self, ligne):
        """Convertit une ligne SQL en objet Incident."""
        return Incident(
            id=ligne[0], titre=ligne[1], description=ligne[2],
            priorite=ligne[3], statut=ligne[4], date_creation=ligne[5],
            utilisateur_id=ligne[6]
        )
