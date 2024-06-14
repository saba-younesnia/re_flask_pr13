class User:
    def select_user(self,db):
        result = db.execute("select * from users")
        data = result.fetchall()
        return data
