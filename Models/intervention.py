class Intervention:

    def __init__(self, commentaire, duree_minutes, incident_id, technicien_id, id = None, date_intervention = None):
        self.id = id
        self.commentaire = commentaire
        self.duree_minutes = duree_minutes
        self.date_intervention = date_intervention
        self.incident_id = incident_id
        self.technicien_id = technicien_id

    def __str__(self):
        return (f"[{self.id}] | Commentaire : {self.commentaire} | Duree : {self.duree_minutes} | ID de l'incident : {self.incident_id} | "
                f"ID du technicien : {self.technicien_id} | Date intervention : {self.date_intervention} | ")