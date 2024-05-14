from flask_sqlalchemy import  SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import logging

db =SQLAlchemy()

bcrypt = Bcrypt()


class User (db.Model):
    __tablename__="users"
    id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String  )
    email=db.Column(db.String )
    password=db.Column(db.String )
    role =db.Column(db.Enum('admin','member'),  default='member')
    created_at = db.Column(db.DateTime() )

    reports = db.relationship("Report", back_populates="user")
    inquiries = db.relationship("Inquiry", back_populates="user")
    responses = db.relationship("Response", back_populates="user")
    requests = db.relationship("Request", back_populates="user")

    def check_password(self, plain_password):
        try:

            return bcrypt.check_password_hash(self.password, plain_password)


        except ValueError as e:
            logging.error(f"Error checking password for user {self.username}: {e}")
            return False

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'email': self.email,
        }



class Book (db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key= True)
    title = db.Column(db.String , nullable = False)
    image_url= db.Column(db.String ,nullable = False)
    Author = db.Column(db.String ,nullable = False)
    Description =db.Column(db.String ,nullable = False)
    Category =db.Column(db.String ,nullable = False)
    status = db. Column(db.String, nullable = False)
    Due_date =db.Column(db.String ,nullable =False)

    reports = db.relationship("Report", back_populates="book")
    requests = db.relationship("Request", back_populates="book")

class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String, db.ForeignKey("users.username") , nullable = False )
    book_title = db.Column(db.String,  db.ForeignKey("books.title") , nullable = False ) 
    request_date = db.Column(db.String, nullable=False)
    return_date = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')
    user = db.relationship("User", back_populates="requests")
    book = db.relationship("Book", back_populates="requests")

class ContactUs(db.Model):
    __tablename__ = "contact_us"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    created_at =  db.Column(db.TIMESTAMP, server_default=db.func.now())


class Publisher (db.Model):
    __tablename__ ="publishers"  
    id = db.Column(db.Integer, primary_key = True)
    Year_of_publication =db.Column(db.Date, nullable = False)
    Name = db.Column(db.String , nullable = False)

class Report (db.Model):
    __tablename__ ="reports"
    id = db.Column(db.Integer ,primary_key = True)
    user_id = db.Column(db.Integer ,  db.ForeignKey("users.id") , nullable = False )
    Book_id =db.Column(db.Integer , db.ForeignKey("books.id"), nullable = False)
    status = db. Column(db.String ,nullable = False, server_default= "pending")
    issued_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    returned_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    user = db.relationship("User",back_populates ="reports") 
    book = db.relationship("Book",back_populates ="reports") 

class Inquiry (db.Model):
     __tablename__ ="inquiries"   
     id = db.Column(db.Integer, primary_key = True)
     user_id =db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
     username = db.Column(db.String,nullable=False)
     message = db.Column(db.String,nullable =False)

     user = db.relationship("User",back_populates ="inquiries") 


class Response (db.Model):
    __tablename__ ="responses"
    id =db.Column(db.Integer ,primary_key =True)
    user_id = db.Column(db.Integer , db.ForeignKey("users.id") , nullable =False)
    username = db.Column(db.String,nullable=False)
    feedback =db.Column(db.String  ,nullable =False)

    user = db.relationship("User",back_populates ="responses") 