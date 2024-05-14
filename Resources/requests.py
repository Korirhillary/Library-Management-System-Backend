from flask_restful import Resource, reqparse, fields, marshal_with
from models import db, Request, User, Book
from flask import request


class RequestResource(Resource):
   
    parser = reqparse.RequestParser()
    parser.add_argument("user_id", type=int, required=True, help="User ID is required")
    parser.add_argument("book_id", type=int, required=True, help="Book ID is required")
    parser.add_argument("request_date", type=str, required=True, help="Request date is required")
    parser.add_argument("return_date", type=str, required=False, help="Return date is optional")
       
    request_fields = {
        "id": fields.Integer,
        "user_id": fields.Integer,
        "book_id": fields.Integer,
        "request_date": fields.String,
        "return_date": fields.String,
        "status": fields.String,
        "user": fields.Nested({
            "id": fields.Integer,
            "username": fields.String
        }),
        "book": fields.Nested({
            "id": fields.Integer,
            "title": fields.String,
            "image_url": fields.String,
            "author": fields.String
        })
    }


    @marshal_with(request_fields)
    def get(self, request_id=None):
        if request_id:
            request = Request.query.get(request_id)
            if request:
                return request
            else:
                return {"message": "Request not found"}, 404
        else:
            all_requests = Request.query.all()
            return all_requests


    @marshal_with(request_fields)
    def post(self):
        args = self.parser.parse_args()
        request = Request(**args, status='pending')  # Set default status to 'pending'
        db.session.add(request)
        db.session.commit()
        return request, 201


    def delete(self, request_id):
        request = Request.query.get(request_id)
        if request:
            db.session.delete(request)
            db.session.commit()
            return {"message": "Request deleted successfully"}, 200
        else:
            return {"message": "Request not found"}, 404


    def put(self, request_id):
        action = request.args.get('action')
        if action not in ['approve', 'reject']:
            return {"message": "Invalid action"}, 400


        request_obj = Request.query.get(request_id)
        if request_obj:
            if action == 'approve':
                request_obj.status = 'Approved'
            elif action == 'reject':
                request_obj.status = 'Rejected'
            db.session.commit()
            return {"message": "Request status updated successfully"}, 200
        else:
            return {"message": "Request not found"}, 404

