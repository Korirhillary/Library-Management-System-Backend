from flask_sqlalchemy import  SQLAlchemy

db =SQLAlchemy()

class User (db.Model):
    __tablename__="users"
    id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.varchar ,nullable = False )
    email=db.Column(db.varchar , nullable =False)
    password=db.Column(db.varchar ,nullable =False)
    role =db.Column(db.Enum('admin','user'),nullable = False , default='user')
    created_at = db.Column(db.DateTime(), nullable=False)


class Book (db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key= True)
    title = db.Column(db.text , nullable = False)
    image_url= db.Column(db.Varchar ,nullable = False)
    Author = db.Column(db.text ,nullable = False)
    Description =db.Column(db.text ,nullable = False)
    Category =db.Column(db.text ,nullable = False)
    status =db.Colum(db.text ,nullable = False)
    Due_date =db.Column(db.date ,nullable =False)

class Publisher (db.Model):
    __tablename__ ="publishers"  
    id = db.Column(db.interger, primary_key = True)
    Year_of_publication =db.Column(db.date, nullable = False)
    Name = db.Column(db.text , nullable = False)

class Reports (db.Model):
    __tablename__ ="reports"
    id = db.Column(db.interger ,primary_key = True)
    user_id = db.Column(db.interger ,nullable = False)
    Book_id =db.Column(db.interger ,nullable = False)
    status = db. Column(db.varchar ,nullable = False)
    issued_at = db.Column(db.timestamp , nullable = False)
    returned_at = db.Column(db.timestamp ,nullable = False)

class Inquiries (db.Model):
     __tablename__ ="inquiries"   
     id = db.Column(db.interger,Primary_key = True)
     user_id =db.Column(db.interger,nullable = False)
     message = db.Column(db.varchar,nullable =False)


class Response (db.Model):
    __tablename__ ="responses"
    id =db.Column(db.interger ,primary_key =True)
    user_id = db.Colum(db.interger ,nullable =False)
    feedback =db.Column(db.interger  ,nullable =False)
