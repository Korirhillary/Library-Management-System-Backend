from flask_restful import Resource , fields , marshal_with, reqparse
from flask_jwt_extended import jwt_required , get_jwt_identity
from models import Report , User, Book, db


report_fields = {
    "id" :fields.Integer,
    "user_id":fields.Integer,
    "Book_id":fields.Integer,
    "title": fields.String,
    "image_url": fields.String,
    "Author" : fields.String,
    "Description":fields.String,
    "isued_at":fields.DateTime,
    "returned_at":fields.String

}

response_field = { 
    "message":fields.String,
    "status":fields.String,
    "report":fields.Nested(report_fields)
}

class ReportsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("Book_id", required = True , help = "Book_id is required")
    parser.add_argument("returned_at" , required = True , help = "returned_at is required")


    @marshal_with(report_fields)
    def get(self ,user_id):
        report = Report.query.get(user_id)
        if report:
            return report
        else:
            return{"message" :"Report not found" }, 404
        

    @jwt_required()
    def post(self):
        data = ReportsResource.parser.parse_args() 
        current_user_id = get_jwt_identity()
        data['user_id'] = current_user_id
        user = User.query.filter_by(id = current_user_id).first()
        bookId = data["Book_id"] 
        book = Book.query.filter_by(id=bookId).first()
        data['title'] = book.title
        data['image_url'] = book.image_url
        data['Author'] = book.Author
        data['Description'] = book.Description
        report= Report(**data)

        try:
            db.session.add(report)
            
            db.session.commit()
            return {'message':'successfully added your report'},201
        except Exception as e:
                    print(f"An error occurred: {e}")
                    return {"message":"Fail to add report"},400

        