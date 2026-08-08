class Incident:

    def __init__(self, titre, description, priorite, utilisateur_id, statut="OUVERT",id = None ,date_creation = None ):
        self.id = id
        self.titre = titre
        self.description = description
        self.priorite = priorite
        self.statut = statut
        self.date_creation = date_creation
        self.utilisateur_id = utilisateur_id

    def __str__(self):
        return (f"[{self.id}] Titre : {self.titre} | Description : {self.description} | Priorite : {self.priorite} "
                f"| Statut : {self.statut} | Date de creation : {self.date_creation} | Utilisateur id : {self.utilisateur_id}" )
