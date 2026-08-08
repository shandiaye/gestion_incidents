import psycopg2
from Database.config import DB_CONFIG

class connection:
    conn = None
    def __new__(cls):
        if cls.conn is None:
            try:
                cls.conn = super().__new__(cls) #la on va creer un objet de type connection qu'on va stocker dans conn
                cls.conn.pg_conn = psycopg2.connect(**DB_CONFIG) #on se connecte a postgres avec les infos de config.py...pg_conn = connection a pgsql renvoye par psycopg2
                cls.conn.pg_conn.autocommit = False #d'abord gerer les erreurs avec des commit et rollback
                print("Connection reussie !")
            except Exception as e:
                print(f"Erreur de connextion {e}!")
                cls.conn = None
                return None
        return cls.conn


    #a partir de la on va utiliser self car l'objet connection existe deja
    def commit(self):
        return self.pg_conn.commit()

    def get_cursor(self):
        return self.pg_conn.cursor()

    def rollback(self):
        return self.pg_conn.rollback()

    def fermer(self):
        self.pg_conn.close()
        connection.conn = None
        print("Connection fermee")

#self.conn = l'objet de connection or pg_conn = la connection elle meme renvoye par psycopg2