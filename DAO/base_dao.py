from abc import ABC, abstractmethod
from Database.connexion import connection


class BaseDAO(ABC):
    def __init__(self):
        # On recupere l'instance unique de connexion (Singleton du chef)
        self.conn = connection()

    @abstractmethod
    def get_all(self):
        """Retourne tous les enregistrements de la table."""
        pass

    @abstractmethod
    def get_by_id(self, id):
        """Retourne un enregistrement par son ID."""
        pass

    @abstractmethod
    def delete_by_id(self, id):
        """Supprime un enregistrement par son ID."""
        pass