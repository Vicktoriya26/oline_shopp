import sqlite3

class DatabaseManager:

    def __init__(self, dbname):
        self.conn = None
        self.cursor = None
        self.dbname = dbname


    def open(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()



    def get_all_products(self):
        self.open()
        self.cursor.execute("""SELECT * FROM products""")
        data = self.cursor.fetchall()
        self.close()
        return data
    
    def get_products(self, products_id):
        self.open()
        self.cursor.execute("""SELECT * FROM products WHERE id=?""", [products_id])
        data = self.cursor.fetchone()
        self.close()
        return data
    
    def get_all_categories(self):
        self.open()
        self.cursor.execute("""SELECT * FROM categories""")
        data = self.cursor.fetchall()
        self.close()
        return data
    
    def get_categories_products(self, category_id):
        self.open()
        self.cursor.execute("""SELECT * FROM products WHERE category_id?""", [category_id])
        data = self.cursor.fetchall()
        self.close()
        return data
    
    def add_products(self, title, content, image, user_id, category_id):
        self.open()
        self.cursor.execute("""INSERT INTO products(title, content, image, user_id, category_id)
                            VALUES(?,?,?,?,?)""", [title, content, image, user_id, int(category_id)])       
        data = self.cursor.fetchall()
        self.close()
        return
    
    def search_products(self, query):
        self.open()
        query = '%' + query + '%'
        self.cursor.execute("""SELECT * FROM products WHERE (title LIKE ? OR content LIKE ?)""", [query, query])
        data = self.cursor.fetchall()
        self.close()