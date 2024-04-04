from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Publisher, db

publisher_fields = {
    'id': fields.Integer,
    'Name': fields.String,
    'Year_of_publication': fields.Integer
}

class PublisherResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Name', required=True, help='Name is required')
    parser.add_argument('Year_of_publication', required=True, help='Year of publication is required')

    @marshal_with(publisher_fields)
    def get(self, id=None):
        if id:
            publisher = Publisher.query.filter_by(id=id).first()
            return publisher
        else:
            publishers = Publisher.query.all()
            return publishers

    @jwt_required()
    @marshal_with(publisher_fields)
    def post(self):
        data = PublisherResource.parser.parse_args()
        publisher = Publisher(**data)

        try:
            db.session.add(publisher)
            db.session.commit()
            return {'message': 'Successfully added publisher'}, 201
        except Exception as e:
            print(f'An error occurred: {e}')
            return {'message': 'Publisher not added'}, 400

    @jwt_required()
    def patch(self, id):
        data = PublisherResource.parser.parse_args()
        # Convert the Year_of_publication string to an integer
        data['Year_of_publication'] = int(data['Year_of_publication'])

        publisher = Publisher.query.get(id)

        if publisher:
            for key, value in data.items():
                setattr(publisher, key, value)
            try:
                db.session.commit()
                return {'message': 'Publisher updated successfully'}
            except:
                return {'message': 'Publisher unable to be updated'}
        else:
            return {'message': 'Publisher not found'}

    @jwt_required()
    def delete(self, id):
        publisher = Publisher.query.get(id)

        if publisher:
            try:
                db.session.delete(publisher)
                db.session.commit()
                return {"message": "Publisher deleted successfully"}
            except:
                return {"message": "Publisher unable to be deleted"}
        else:
            return {"message": "Publisher not found"}