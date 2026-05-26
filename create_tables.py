from Database.connexion import connection

#on va recuperer la connection et notre stylo cursor
conn = connection()
cursor = conn.get_cursor()

try :
    cursor.execute("""
    
        CREATE TABLE IF NOT EXISTS utilisateur(
            id SERIAL PRIMARY KEY, 
            login VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR (255) NOT NULL,
            nom VARCHAR (50) NOT NULL,
            prenom VARCHAR (50) NOT NULL,
            email VARCHAR (50) NOT NULL,
            role VARCHAR (30) NOT NULL CHECK (role IN('UTILISATEUR', 'TECHNICIEN', 'ADMIN')),
            service VARCHAR(50),
            date_creation DATE DEFAULT CURRENT_DATE
        );
        
        
        CREATE TABLE IF NOT EXISTS incident(
            id SERIAL PRIMARY KEY,
            titre VARCHAR(50) NOT NULL,
            description TEXT NOT NULL,
            priorite VARCHAR(30) NOT NULL CHECK (priorite IN ('BASSE', 'MOYENNE', 'HAUTE', 'CRITIQUE')),
            statut VARCHAR (20) NOT NULL DEFAULT 'OUVERT' CHECK (statut IN('OUVERT', 'EN_COURS', 'RESOLU', 'FERME')),
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            utilisateur_id int NOT NULL,
        
            CONSTRAINT FK_incident_utilisateur
                FOREIGN KEY (utilisateur_id)
                REFERENCES utilisateur(id)
                ON DELETE CASCADE 
        
        );
        
        CREATE TABLE IF NOT EXISTS intervention(
            id SERIAL PRIMARY KEY,
            commentaire TEXT NOT NULL,
            duree_minutes INTEGER NOT NULL CHECK (duree_minutes >= 0),
            date_intervation TIMESTAMP DEFAULT NOW(),
            incident_id INTEGER NOT NULL REFERENCES incident(id),
            technicien_id INTEGER NOT NULL REFERENCES utilisateur(id)
            );
    """)

    conn.commit() #pour la sauvegarde
    print("Tables crees avec succes !")
except Exception as e :
    conn.rollback() #pour annuler l'action en cas d'erreur
    print(f"Erreur lors de la creation : {e}")
finally:
    conn.fermer()

