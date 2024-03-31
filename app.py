from flask import Flask
from flask_migrate import Migrate
from models import db
from flask_restful import Api
from Resources.books import createBook , getBook ,deleteBook

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 
api = Api(app)
migrate = Migrate(app ,db)

@app.route("/")
def Home():
    return "Hello world !"

api.add_resource(createBook,'/books')
api.add_resource(getBook ,'/books','/books/<int:book_id>')
api.add_resource(deleteBook ,'/books/<int:book_id>')

if __name__ == "__main__":
    app.run(debug=True , port=5000)
