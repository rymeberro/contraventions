import sqlite3




class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('contraventions.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_contraventions(self):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CONTRAVENTIONS")
        contraventions = cursor.fetchall()
        return contraventions


    def insert_contravention(self, dict):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into contraventions (proprietaire, categorie, etablissement, adresse, ville, description,  date_infraction, date_jugement, montant ) "
                        "values(?, ?, ?, ?, ?, ?, ?, ?, ?)"), (dict["proprietaire"], dict["categorie"], dict["etablissement"], dict["adresse"], dict["ville"], dict["description"], dict["date_infraction"], dict["date_jugement"], dict["montant"]))
        connection.commit()

    def get_contraventionsBySearch(self, seachText):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(("select * from contraventions where (proprietaire || etablissement || adresse ) like ? "), ('%'+seachText+'%',))
        contraventions = cursor.fetchall()
        return contraventions

    def get_contraventionsByEtablissement(self, etablissement):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(("select * from contraventions where etablissement like ? "), (etablissement,))
        contraventions = cursor.fetchall()
        return contraventions 

    def get_nbrContraventionsByEtablissement(self, etablissement):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(("select etablissement, count(*) from contraventions where etablissement like ? group by etablissement"), (etablissement,))
        contraventions = cursor.fetchall()
        return contraventions

    def get_contraventionsByDateSearch(self, date_debut, date_fin):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(("SELECT * , COUNT(*) as nbrContraventions, date(substr((substr(date_infraction,    instr(date_infraction, ' ') + 1)),    instr((substr(date_infraction,    instr(date_infraction, ' ') + 1)), ' ') + 1) ||'-'|| CASE substr((substr(date_infraction,    instr(date_infraction, ' ') + 1)), 1, instr((substr(date_infraction,    instr(date_infraction, ' ') + 1)), ' ') - 1) WHEN 'janvier' THEN '01' WHEN 'février' THEN '02'WHEN 'mars' THEN '03'WHEN 'avril' THEN '04'WHEN 'mai' THEN '05' WHEN 'juin' THEN '06' WHEN 'juillet' THEN '07' WHEN 'août' THEN '08' WHEN 'septembre' THEN '09' WHEN 'octobre' THEN '10' WHEN 'novembre' THEN '11' WHEN 'décembre' THEN '12' END ||'-'|| substr(date_infraction, 1, instr(date_infraction, ' ') - 1)  ) AS isodate from contraventions  where isodate BETWEEN date(?) and date(?) group by etablissement ")
        , (date_debut, date_fin, ))
        contraventions = cursor.fetchall()
        return contraventions

    def get_list_etablissements(self):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT etablissement from contraventions group by etablissement ")
        etablissements = cursor.fetchall()
        return etablissements

    """def create_user(self, utilisateur, email, salt, hashed_password):
        cursor = self.get_connection().cursor()
        cursor.execute(("insert into users(utilisateur, email, salt, hash)" " values(?, ?, ?, ?)"), (utilisateur, email, salt, hashed_password))
        connection.commit()
    """

    def create_user(self, utilisateur, email, salt, hashed_password):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into users(utilisateur, email, salt, hash)" " values(?, ?, ?, ?)"), (utilisateur, email, salt, hashed_password))
        connection.commit()

    def get_users(self):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users

    def read_all_contraventions(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from contraventions limit 3")
        contraventions = cursor.fetchall()
        return [Contravention(one_contravention[0], one_contravention[1]) for one_contravention in contraventions]

    def get_user_login_info(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute(("select salt, hash from users where email=?"),
                       (email,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]

    def save_session(self, id_session, email):
        connection = self.get_connection()
        connection.execute(("insert into sessions(id_session, utilisateur) "
                            "values(?, ?)"), (id_session, email))
        connection.commit()

    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute(("delete from sessions where id_session=?"),
                           (id_session,))
        connection.commit()

    def get_account_infos(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute(("select utilisateur from users where email=?"),(email,))
        utilisateur = cursor.fetchone()
        return utilisateur


    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute(("select utilisateur from sessions where id_session=?"),
                       (id_session,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]
