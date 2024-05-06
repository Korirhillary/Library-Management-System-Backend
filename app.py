from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import  db
from flask_restful import Api
from flask_jwt_extended import JWTManager
from Resources.users import UserRegister,Login , Borrow, send_borrow_request_email
from flask_mail import Mail, Message
from Resources.inquiries import InquiryResource
from Resources.responses import ResponseResource
from Resources.reports import ReportsResource
from Resources.publishers import PublisherResource
from Resources.books import createBook , getBook ,deleteBook

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nellychepkem2015@gmail.com'
app.config['MAIL_PASSWORD'] = '2121@Ncb'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

CORS(app)

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
api.add_resource(deleteBook ,'/books/<int:book_id>')
api.add_resource(InquiryResource,'/inquiries', '/inquiries/<int:inquiries_id>')
api.add_resource(ResponseResource , '/responses', '/responses/<int:id>')
# api.add_resource(ReportsResource , '/reports' , '/reports/<int:user_id>')
api.add_resource(ReportsResource, "/reports", "/reports/<int:id>")
api.add_resource(PublisherResource , '/publishers', '/publishers/<int:id>')
api.add_resource(Borrow, "/request")
# api.add_resource(send_borrow_request_email, "/request")


if __name__ == "__main__":
    app.run(debug=True , port=5000)
