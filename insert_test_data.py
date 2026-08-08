from Database.connexion import connection

conn = connection()
cursor = conn.get_cursor()

try:
    cursor.execute("""INSERT INTO utilisateur (login , password, nom, prenom, email, role, service)
            VALUES ('shaNdiaye', '1234' , 'Ndiaye', 'Aicha', 'aicha@gmail.com',  'ADMIN' , 'Informatique'),
                   ('aba', 'shaaba', 'Abdallah', 'Diouf', 'aba@gmail.com', 'TECHNICIEN', 'Informatique'),
                   ('mmbaye', '1234', 'Mbaye', 'Moussa', 'moussa@gmail.com', 'UTILISATEUR', 'Comptabilité');       
    """)

    cursor.execute("""INSERT INTO incident (titre, description, priorite, utilisateur_id)
        VALUES 
            ('Problème réseau', 'Impossible de se connecter à internet', 'HAUTE', 3),
            ('PC lent', 'Mon ordinateur est très lent depuis ce matin', 'MOYENNE', 3),
            ('Imprimante HS', 'L imprimante ne fonctionne plus', 'BASSE', 3);
    """)

    cursor.execute("""INSERT INTO intervention (commentaire, duree_minutes, incident_id, technicien_id)
        VALUES 
            ('Redémarrage du routeur, problème résolu', 30, 1, 2),
            ('Nettoyage du disque dur et suppression des fichiers inutiles', 45, 2, 2),
            ('Remplacement de la cartouche d imprimante', 20, 3, 2);
    """)

    conn.commit()
    print("Données insérées avec succès !")
except Exception as e:
    conn.rollback()
    print(f"Erreur : {e}")
finally:
    conn.fermer()