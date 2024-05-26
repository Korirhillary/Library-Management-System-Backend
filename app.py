from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import  db
from flask_restful import Api
from flask_jwt_extended import JWTManager
from Resources.users import UserRegister,Login 
from flask_mail import Mail, Message
from Resources.reports import ReportsResource
from Resources.publishers import PublisherResource
from Resources.books import createBook , getBook, UpdateBook, deleteBook
from Resources.requests import RequestResource
from Resources.contacts import ContactUsResource
import os


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'korir6373@gmail.com'
app.config['MAIL_PASSWORD'] = 'jwvhzbfcwpgdvigx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

CORS(app)
mail =Mail(app)
db.init_app(app) 
api = Api(app)
migrate = Migrate(app ,db)
jwt = JWTManager(app)

@app.route("/")
def Home():
    return "Hello world !"

# api.add_resource(Users ,'/users' ,'/users/<int:id>')
api.add_resource(UserRegister ,'/register' ,'/register/<int:id>')
api.add_resource(Login,'/login')
api.add_resource(createBook,'/books')
api.add_resource(getBook ,'/books','/books/<int:book_id>')
api.add_resource(UpdateBook, "/books/<int:book_id>")
api.add_resource(deleteBook ,'/books/<int:book_id>')
# api.add_resource(ReportsResource , '/reports' , '/reports/<int:user_id>')
api.add_resource(ReportsResource, "/reports", "/reports/<int:id>")
api.add_resource(PublisherResource , '/publishers', '/publishers/<int:id>')
api.add_resource(RequestResource, '/requests', '/requests/<int:request_id>')
api.add_resource(ContactUsResource, '/contacts', '/contact_us/<int:contacts_id>')


if __name__ == "__main__":
    app.run(debug=True , port=5000)
