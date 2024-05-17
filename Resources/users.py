from models import User, db, bcrypt
from flask_restful import Resource, fields,marshal_with,abort ,reqparse
from flask_jwt_extended import jwt_required , get_jwt_identity, create_access_token, create_refresh_token
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




user_fields = {
    "id" : fields.Integer,
    "username" : fields.String,
    "email" : fields.String,
    "password" : fields.String,
    "role":fields.String,
    "created_at":fields.DateTime
    
}

response_fields ={
    "message":fields.String,
    "status":fields.String,
    "user":fields.Nested(user_fields)
}

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help="username is required")
    parser.add_argument('email', required=True, help=" email is required")
    parser.add_argument('password', required=True, help=" password is required")
    parser.add_argument('role', required=True, help="role is required")


    @marshal_with(user_fields)
    def get(self, id=None):
        if id:
            
            user = User.query.filter_by(id=id).first() 
            if user is not None:
                print(user)
                return user, 200
            else:
                abort(400, error ="User does not exist")
        else:
            users =User.query.all()
            return users
        
    
    @marshal_with(response_fields)
    def post(self):
        data =UserRegister.parser.parse_args()
        data['password']= bcrypt.generate_password_hash(data['password'],rounds=10).decode('utf-8')
        roles =["member", "admin"]
        if data['role'] not in roles :
            abort(400, error="Invalid role")
        user = User(**data)
        email = User.query.filter_by(email=data['email']).first()

        if email:
            abort(403, error="Email address already exists")
       
        try:
            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully"}, 201
        except Exception as e:
            print(f"Error during user creation: {str(e)}")
            db.session.rollback() 
            abort(500, error="Unsuccessful creation")


    def delete(self,id):
        user = User.query.filter_by(id = id).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit()

                return {"message":"User deleted"}
            except:
                return {"message":"User unable to be deleted"}
        else:
            return {"message":"User not found"}




class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help=" email is required")
    parser.add_argument('password', required=True, help=" password is required")

    def post(self):
        data =Login.parser.parse_args()
        user =User.query.filter_by(email =data["email"]).first()
        if user:
            checked_password =user.check_password(data["password"])
            if checked_password:
                user_json =user.to_json()
                access =create_access_token(identity =user_json["id"])
                refresh_token =create_refresh_token(identity =user_json["id"])
                return {"message": "login successful",
                    "status": "success",
                    "access_token": access,
                    "refresh_token": refresh_token,
                    "user": user_json
                }, 200
            else:
                return {"message": "invalid email/password", "status": "fail"}, 403
        else:
            return {"message": "invalid email/password", "status": "fail"}, 403
    



class Borrow(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', type=int, required=True, help="book_id is required")

    @jwt_required()
    def post(self):
        data = Borrow.parser.parse_args()
        user_id = get_jwt_identity()
        try:
            send_borrow_request_email(user_id)
            return {"message": "Borrow request sent for approval."}, 200
        except Exception as e:
            print('Error sending borrow request:', e)
            return {"error": "Internal server error."}, 500

def send_borrow_request_email(user_id):
    users = User.query.all()
    sender_user = User.query.get(user_id)
    if sender_user:
        sender_email = sender_user.email
         # Initialize receiver_email variable
        # Not recommended, consider more secure methods for storing passwords
        for user in users:
            if user.role == "admin":
                receiver_email = user.email
                password = user.password
                break  # Break out of the loop once admin is found
        if receiver_email:
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = 'Borrow Request Approval'
            body = f'A user ({sender_user.username}) has requested to borrow a book. Please review and approve.'
            message.attach(MIMEText(body, 'plain'))
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                server.quit()
                print("Borrow request email sent successfully.")
            except Exception as e:
                print(f'Error sending borrow request email: {str(e)}')
        else:
            print("No admin found to send the borrow request email.")
    else:
        print("Sender user not found.")


    

    

    