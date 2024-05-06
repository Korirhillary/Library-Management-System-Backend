from flask_restful import Resource , fields , marshal_with, reqparse
from flask_jwt_extended import jwt_required , get_jwt_identity
from models import Report , User, Book, db
import datetime




report_fields = {
    "id" :fields.Integer,
    "user_id":fields.Integer,
    "Book_id":fields.Integer,
    "status":fields.String,
    "issued_at":fields.DateTime,
    "returned_at":fields.DateTime


}


response_field = {
    "message":fields.String,
    "status":fields.String,
    "report":fields.Nested(report_fields)
}


class ReportsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("Book_id", required =True ,help = "book_id is required")
    parser.add_argument("status", required =True ,help = "status is required")
    # parser.add_argument("issued_at", required =True ,help = "issued_at is required")
    # parser.add_argument("returned_at", required =True ,help = "returned_at is required")

   



    @marshal_with(report_fields)
    def get(self ,id= None):
        if id:
            report = Report.query.filter_by(id=id).first()
            if report:
                return report
            else:
                return{"message" :"Report not found" }, 404  
        else:
             reports = Report.query.all()
             return reports
             
           
       


    @jwt_required()
    @marshal_with(response_field)
    def post(self):
        data = ReportsResource.parser.parse_args()
        current_user_id = get_jwt_identity()
        data['user_id'] = current_user_id
        allStatuses ="pending" or "issued" or "returned"
        data["status"] = allStatuses
        user = User.query.filter_by(id = current_user_id).first()
        bookId = data["Book_id"]
        book = Book.query.filter_by(id=bookId).first()
    
        report= Report(**data)
        print(report)


        try:
            db.session.add(report)
           
            db.session.commit()
            return {'message':"successfully added your report", "status" : "success", "report":report},201
        except Exception as e:
                    print(f"An error occurred: {e}")
                    return {"message":"Fail to add report"},400


    #    @jwt_required()
    # @admin_required 
    def delete(self, id):
        try:
            report = Report.query.filter_by(id=id).first()

            if report:
                db.session.delete(report)
                db.session.commit()
                return {"message": "Report deleted Successfully", 'status': 'SUCCESS'  }
            else:
                return {"message": "No Report Found", 'status': 'FAILED TO DELETE'}
        except Exception as e:
            return {'message': "Failed To Delete The Report"}

