from flask_restful import Resource , fields ,marshal_with ,reqparse
from flask_jwt_extended import jwt_required , get_jwt_identity
from models import Inquiry,User ,db

inquiry_fields ={
    "id" : fields.Integer,
    "user_id":fields.Integer,
    "username": fields.String,
    "message":fields.String
}






class InquiryResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("message" , required = True , help ="message is required") 


    @marshal_with(inquiry_fields)
    def get(self ,inquiries_id):
        inquiry = Inquiry.query.get(inquiries_id)
        if inquiry:
            return inquiry
        else:
            return{"message" :"Inquiry not found" }, 404
        

    @jwt_required()
    def post(self):
        data = InquiryResource.parser.parse_args() 
        current_user_id = get_jwt_identity()
        data['user_id'] = current_user_id
        user = User.query.filter_by(id = current_user_id).first()
        data['username'] = user.username
        inquiry= Inquiry(**data)

        try:
            db.session.add(inquiry)
            
            db.session.commit()
            return {'message':'successfully sent your inquiry'},201
        except Exception as e:
                    print(f"An error occurred: {e}")
                    return {"message":"User already sent an inquiry with this user_id"},400

    
    def delete(self,inquiries_id):
        inquiry = Inquiry.query.get(inquiries_id)
        if inquiry:
            try:
                db.session.delete(inquiry)
                db.session.commit()

                return {"message":"Inquiry deleted"}
            except:
                return {"message":"Inquiry unable to be deleted"}
        else:
            return {"message":"Inquiry not found"}
