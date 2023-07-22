import psycopg2

from Character import Character


class DBconnection:
    def __init__(self, tn):
        self.db = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="password",
            database="parsertang",
            port=5433
        )
        self.db.set_session(autocommit=True)
        self.cursor = self.db.cursor()
        self.tablename = tn
        self.next_id = 0

    def amount_rows(self):
        self.cursor.execute("""
                    SELECT MAX(cid)
                    FROM {0};
                    """.format(self.tablename.casefold().replace('\'', '\'\'')))
        res = self.cursor.fetchone()[0]
        print(res)
        if res is None:
            return 0
        else:
            return res

    def get_db_cursor(self):
        return self.cursor

    def close_connection(self):
        self.cursor.close()
        self.db.close()

    def select_all_from_table(self):
        self.cursor.execute("SELECT * FROM {0}".format(self.tablename.replace('\'', '\'\'')))
        data = self.cursor.fetchall()
        list = []
        for instance in data:
            list.append(Character(instance[1], instance[2], instance[3], instance[4]))
        return list

    def select_where_from_table(self,cond1, cond2):
        self.cursor.execute("SELECT * FROM {0} WHERE {1}='{2}'".format(self.tablename.replace('\'', '\'\''), cond1,cond2))
        data = self.cursor.fetchall()
        list = []
        for instance in data:
            list.append(Character(instance[1], instance[2], instance[3], instance[4]))
        return list


    def update_class(self,newval,cond1,cond2):
        self.cursor.execute("UPDATE {0} SET {2} = '{1}' WHERE {2}='{3}';".format(self.tablename.replace('\'', '\'\''), newval,cond1,cond2))

    def delete_char(self, cond1,cond2):
        self.cursor.execute("DELETE FROM {0} WHERE {1}='{2}';".format(self.tablename.replace('\'', '\'\''), cond1,cond2))

    def delete_all(self):
        self.cursor.execute("DELETE FROM {0} WHERE cid>0;".format(self.tablename.replace('\'', '\'\'')))

    def insert_into_table(self, characters):
        if isinstance(characters, list):
            for character in characters:
                self.next_id = self.amount_rows() + 1
                self.cursor.execute('''
                     INSERT INTO {0}
                     VALUES ({1}, '{2}','{3}','{4}','{5}');
                     '''.format(self.tablename.replace('\'', '\'\''), self.next_id,
                                character.name.replace('\'', '\'\''),
                                character.surname.replace('\'', '\'\''),
                                character.race.replace('\'', '\'\''), character.clas.replace('\'', '\'\'')))
        else:
            self.next_id = self.amount_rows() + 1
            self.cursor.execute('''
                          INSERT INTO {0}
                          VALUES ({1}, '{2}','{3}','{4}','{5}');
                          '''.format(self.tablename.replace('\'', '\'\''), self.next_id,
                                     characters.name.replace('\'', '\'\''), characters.surname.replace('\'', '\'\''),
                                     characters.race.replace('\'', '\'\''), characters.clas.replace('\'', '\'\'')))

    def create_table(self):
        if not (self.checkTableExists()):
            self.cursor.execute('''CREATE TABLE {0}(  
                  CID SERIAL UNIQUE,  
                  CName varchar(255),  
                  CSurname varchar(255),
                  CRase varchar(255),
                  CClas varchar(255));
            '''.format(self.tablename.replace('\'', '\'\'')))

    def checkTableExists(self):
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}';
            """.format(self.tablename.casefold().replace('\'', '\'\'')))
        if self.cursor.fetchone()[0] == 1:
            return True
        else:
            return False
