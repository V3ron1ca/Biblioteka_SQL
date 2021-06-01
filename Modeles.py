from models import create_connection,execute_sql, create_projects_sql, update_projects, add_projects, save_and_close

filename = "database.db"


class TodosSQLite:
    def __init__(self):
        connection = self.get_connetion()
        execute_sql(connection, create_projects_sql)
        save_and_close(connection)

    def get_connetion(self):
        return create_connection(filename)

    def all(self):
        connection = self.get_connetion()
        cursor = execute_sql(connection, "SELECT * FROM projects;")
        all = cursor.fetchall()
        save_and_close(connection)
        return [{"id" : x[0], "title" : x[1], "description" : x[2], "done"  : bool(x[3]) } for x in all]

    def get(self, id):
        connection = self.get_connetion()
        result =  execute_sql(connection, f"SELECT * FROM projects WHERE id = {id} LIMIT 1;").fetchall()
        save_and_close(connection)
        if result:
            return [{"id" : x[0], "title": x[1], "description": x[2], "done": bool(x[3])} for x in result][0]

    def create(self, data):
        connection = self.get_connetion()
        add_projects(connection, (data["title"], data["description"], data["done"]))
        save_and_close(connection)

    def update(self, id, data):
        connection = self.get_connetion()
        result = update_projects(connection, (data["title"], data["description"], data["done"], id))
        save_and_close(connection)
        return result is not None




