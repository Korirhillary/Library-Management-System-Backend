from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from models import db, ContactUs
from datetime import datetime

contact_us_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "message": fields.String,
    "created_at": fields.DateTime,
}

class ContactUsResource(Resource):
        
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Name is required")
    parser.add_argument("email", type=str, required=True, help="Email is required")
    parser.add_argument("message", type=str, required=True, help="Message is required")
        

    @marshal_with(contact_us_fields)
    def post(self):
        args = self.parser.parse_args()
        contact_us = ContactUs(**args)
        db.session.add(contact_us)
        db.session.commit()
        return contact_us, 201

    @marshal_with(contact_us_fields)
    def get(self, contact_id=None):
        if contact_id:
            contact_us = ContactUs.query.get(contact_id)
            if contact_us:
                return contact_us
            else:
                return {"message": "Contact us entry not found"}, 404
        else:
            all_contact_us_entries = ContactUs.query.all()
            return all_contact_us_entries

    def delete(self, contact_id):
        contact_us = ContactUs.query.get(contact_id)
        if contact_us:
            db.session.delete(contact_us)
            db.session.commit()
            return {"message": "Contact us entry deleted successfully"}, 200
        else:
            return {"message": "Contact us entry not found"}, 404


