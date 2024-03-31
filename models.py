from flask_sqlalchemy import  SQLAlchemy

db =SQLAlchemy()

class User (db.Model):
    __tablename__="users"
    id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String ,nullable = False )
    email=db.Column(db.String , nullable =False)
    password=db.Column(db.String ,nullable =False)
    role =db.Column(db.Enum('admin','user'),nullable = False , default='user')
    created_at = db.Column(db.DateTime(), nullable=False)

    reports = db.relationship("Report", back_populates="user")
    inquiries = db.relationship("Inquiry", back_populates="user")
    responses = db.relationship("Response", back_populates="user")




class Book (db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key= True)
    title = db.Column(db.String , nullable = False)
    image_url= db.Column(db.String ,nullable = False)
    Author = db.Column(db.String ,nullable = False)
    Description =db.Column(db.String ,nullable = False)
    Category =db.Column(db.String ,nullable = False)
    status =db.Column(db.String ,nullable = False)
    Due_date =db.Column(db.String ,nullable =False)

    reports = db.relationship("Report", back_populates="book")


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
    status = db. Column(db.String ,nullable = False)
    issued_at = db.Column(db.TIMESTAMP , nullable = False)
    returned_at = db.Column(db.TIMESTAMP ,nullable = False)

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
    feedback =db.Column(db.String  ,nullable =False)

    user = db.relationship("User",back_populates ="responses") 
