from flask_restful import Resource ,fields ,marshal_with,reqparse ,marshal
from flask_jwt_extended import jwt_required , get_jwt_identity
from models import Response ,db,User

response_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'username': fields.String,
    'feedback': fields.String,
    
}

class ResponseResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('feedback', required=True ,help ="feedback is required")
   
    
    @marshal_with(response_fields)
    def get(self, id=None):
    
        if id:
            response = Response.query.filter_by(id = id).first()
            return response
        else:
            responses = Response.query.all()

            return  responses
        

    @jwt_required()
    def post(self):
      data = ResponseResource.parser.parse_args() 
      current_user_id = get_jwt_identity()
      data['user_id'] = current_user_id
      user = User.query.filter_by(id = current_user_id).first()
      data['username'] = user.username
      response = Response(**data)

      try:
          db.session.add(response)
          db.session.commit()
          return {'message':'successfully added your response'},201
      except Exception as e: 
                print(f"An error occurred: {e}")
                return {"message":"Response not sent"},400

      
 
    
    @jwt_required()
    def patch(self,id):
        data = Response.parser.parse_args()
        response = Response.query.get(id)

        if response_fields:
            for key,value in data.items():
                setattr(Response,key,value)
            try:
                db.session.commit()

                return {"message":"Response updated successfully"}
            except:
                return {"message":"Response unable to be updated"}
            
        else:
            return {"message":"Response not found"}
        

    @jwt_required()
    def delete(self,id):
        response = Response.query.filter_by(id = id).first()
        if response:
            try:
                db.session.delete(response)
                db.session.commit()

                return {"message":"Response deleted"}
            except:
                return {"message":"Response unable to be deleted"}
        else:
            return {"message":"Response not found"}
