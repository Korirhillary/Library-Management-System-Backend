from flask_restful import Resource,fields ,marshal_with ,reqparse
from models import Book ,db

book_fields = {
    "id" :fields.Integer,
    "title": fields.String,
    "image_url": fields.String,
    "Author" : fields.String,
    "Description":fields.String,
    "Category": fields.String,
    "status" : fields.String,
    "initialCount": fields.Integer,
    "Due_date": fields.String
}

response_field = { 
    "message":fields.String,
    "status": fields.String,
    "book":fields.Nested(book_fields)
}

class createBook(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title" , required = True , help = "title is required")
    parser.add_argument("image_url" , required = True , help = "image_url is required")
    parser.add_argument("Author" , required = True , help = "Author is required")
    parser.add_argument("Description" , required = True , help = "Description is required")
    parser.add_argument("Category" , required = True , help = "Category is required")
    parser.add_argument("status" , required = True , help = "status is required")  
    parser.add_argument("initialCount" , required = True , help = "initialCount is required")
    parser.add_argument("Due_date" , required = True , help = "Due_date is required")

    @marshal_with(response_field)
    def post(self):
        data = createBook.parser.parse_args()
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
        
        return{"message" :"Book created successfully" ,"status":"success" , "Book": book}

class getBook(Resource):
    def get(self, book_id = None):
        if book_id:
            book =Book.query.get(book_id)  
            if book:
                book_data ={
                    "id":book.id,
                    "title":book.title,
                    "image_url":book.image_url,
                    "Author":book.Author,
                    "Description":book.Description,
                    "Category":book.Category,
                    "status":book.status,
                    "initialCount":book.initialCount,
                    "Due_date":book.Due_date
                } 
                return book_data ,201
            else:
                return{"message":"Book not found"},400
        else:
            all_books = Book.query.all()
            books_data =[{
                    "id":book.id,
                    "title":book.title,
                    "image_url":book.image_url,
                    "Author":book.Author,
                    "Description":book.Description,
                    "Category":book.Category,
                    "status":book.status,
                    "initialCount":book.initialCount,
                    "Due_date":book.Due_date
            }for book in all_books]
            return books_data ,201
        
class UpdateBook(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title")
    parser.add_argument("image_url")
    parser.add_argument("Author")
    parser.add_argument("Description")
    parser.add_argument("Category")
    parser.add_argument("status")
    parser.add_argument("initialCount")
    parser.add_argument("Due_date")

    @marshal_with(response_field)
    def patch(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"message": "Book not found", "status": "fail"}, 404

        data = UpdateBook.parser.parse_args()
        for key, value in data.items():
            if value is not None:
                setattr(book, key, value)

        db.session.commit()
        return {"message": "Book updated successfully", "status": "success", "book": book}

        
class deleteBook(Resource):
    def delete(self,book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book deleted successfully", "status" :"success"} ,200
        else:
            return {"message":"Book not found", "status":"fail"}, 404
