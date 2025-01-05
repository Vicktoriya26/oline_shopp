from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
load_dotenv()
import os

from db_scripts import DatabaseManager

app = Flask(__name__)  # Створюємо веб–додаток Flask
app.secret_key = os.getenv('SECRET_KEY')
db = DatabaseManager("blog.db")

IMG_PATH = os.path.dirname(__file__) + os.sep + "static" + os.sep + "img"


@app.context_processor
def get_categories():
    categories = db.get_all_categories()
    return dict(categories=categories)

@app.route("/")  # Вказуємо url-адресу для виклику функції
def index():
    products = db.get_all_products()
    return render_template("index.html", products=products)


@app.route("/products/<int:products_id>")  # Вказуємо url-адресу для виклику функції
def products_page(products_id):
    products = db.get_products(products_id)
    return render_template("products_page.html", products=products) 



@app.route("/categories/<int:category_id>")  # Вказуємо url-адресу для виклику функції
def category_page(category_id):
    products = db.get_products(category_id)
    return render_template("index.html", products=products) 

@app.route("/products/new", methods=["GET", "POST"])
def new_products():
    if request.method == 'POST':
        image = request.file['image']
        image.save(IMG_PATH + image.filename)
        db.add_products(request.form['title'], request.form['content'],
                        image.filename, 1, request.form['category'])
        flash("Статтю додано")
    else:
        flash("Виберіть статтю заповніть всі поля.")
    return render_template("new_products.html") 


@app.route("/search")  # Вказуємо url-адресу для виклику функції
def search():
    products = db.get_all_products()

    if request.method == 'GET':
        query = request.args.get("query")
        products = db.search_products(query)

    return render_template("index.html", products=products)





if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # автоматичне оновлення шаблонів
    app.run(debug=True)  # Запускаємо веб-сервер з цього файлу в режимі налагодження
