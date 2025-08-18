import pymysql
class Database:
    def __init__(self, host='localhost',port='', user='root', password='root', database='shop_db'):
        try:
            self.connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"Connected to database: {database}")
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise
    
    def execute_non_query(self, sql, params=None):
        cursor = self.connection.cursor()
        try:
            affected_rows = cursor.execute(sql, params)
            self.connection.commit()
            return affected_rows
        except:
            self.connection.rollback()
        finally:
            cursor.close()

    def execute_query(self, sql, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close() 

    def execute_single(self, sql, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error executing single query: {e}")
            raise
        finally:
            cursor.close()
    
    def get_last_insert_id(self):
        return self.connection.insert_id()
    
    def close(self):
        self.connection.close()


class User:
    def __init__(self,db: Database):
        self.db = db

    def add_user(self,name, email):
        affected_rows = self.db.execute_non_query("INSERT INTO users (name, email) VALUES (%s, %s)",(name, email))

    def update_user(self, id, name, email):
        affected_rows = self.db.execute_non_query("UPDATE users SET name = %s, email = %s WHERE id = %s",(name, email, id))
        return affected_rows

    def delete_user(self, id):
        affected_rows = self.db.execute_non_query("DELETE FROM users WHERE id = %s",(id))
        return affected_rows

    def get_user_by_email(self, email):
        user = self.db.execute_single("SELECT * FROM users WHERE email = %s",(email))
        return user

    def get_user_by_name(self, name):
        user = self.db.execute_query("SELECT * FROM users WHERE name LIKE %s",(f"%{name}%"))
        return user

    def get_user_by_id(self, id):
        user = self.db.execute_single("SELECT * FROM users WHERE id = %s",(id))
        return user

    def get_users(self):
        users = self.db.execute_query("SELECT * FROM users ")
        return users


if __name__ == '__main__':
    db = Database()
    user = User(db=db)
    affected_rows = user.add_user("Krit2","aaacc@gmail.com")
    print(f"Add user = {affected_rows}")

    find_user = user.get_user_by_email("aaacc@gmail.com")
    print(f"Find user = {find_user}")

    find_user = user.get_user_by_name("Krit")
    print(f"Find user = {find_user}")

    users = user.get_users()
    print(f"All users = {find_user}")

    affected_rows = user.update_user(6,name="Krit", email="AABBCC@gmail.com")
    print(f"Update user = {find_user}")

