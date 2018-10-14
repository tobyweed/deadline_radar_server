from flask_restful import Resource, request
from models import Deadline, User, DeadlineSchema, UserSchema
from dateutil import parser
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity, get_raw_jwt)

deadline_schema = DeadlineSchema()
user_schema = UserSchema()


'''
================AUTH RESOURCES================
'''

#register new user
class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        user = user_schema.load(data)
        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists.'. format(data['username'])}

        new_user = User(
            username = user.data['username'],
            password = User.generate_hash(user.data['password']),
            email = user.data['email']
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            return {
                'message': 'User {} was created.'.format( data['username']),
                'access_token': access_token
            }
        except:
            return {'message': 'Something went wrong.'}, 500

#log in with a username and password
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = user_schema.load(data)
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist.'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            try:
                access_token = create_access_token(identity = data['username'])
                return {
                    'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token
                    }
            except:
                return { 'message': 'Something went wrong.' }, 500
        else:
            return {'message': 'Wrong password.'}


'''
================OTHER RESOURCES================
'''

class CreateDeadline(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()

        #get current user
        current_user_jwt = get_jwt_identity()
        current_user = User.find_by_username(current_user_jwt)

        # create deadline out of json
        deadline = deadline_schema.load(data)
        #convert all datetime strings into strings which marshmallow can load (marshmallow requires ISO 8601 format INCLUDING SECONDS)
        try:
            data['date'] = str(parser.parse(data['date']))
        except:
            data['events'][i]['start_date'] = None

        new_deadline = Deadline(
            name = deadline.data['name'],
            type = deadline.data['type'],
            date = deadline.data['date'],
            priority = deadline.data['priority'],
            num_of_hours = deadline.data['num_of_hours']
        )

        # append create deadline to current user
        current_user.deadlines.append(new_deadline)

        try:
            new_deadline.save_to_db()
            current_user.save_to_db()
            ret = deadline_schema.dump(new_deadline)
            print(ret.data['id'])
            return {"id":ret.data['id']},200
        except:
            return {'message':'Something went wrong.'},500

class OneDeadline(Resource):
    @jwt_required
    def get(self, id):
        deadline = Deadline.find_by_id(id)
        if not deadline:
            return {'message': 'A deadline with that id does not exist.'}
        #get the name of the user trying to do the updating
        current_user_name = get_jwt_identity()
        user = User.find_by_username(current_user_name)
        #return a helpful message if the user is trying to edit an account which is not their own
        if not current_user_name == deadline.user_name:
            return {'message': 'That deadline belongs to another user account; you are not authorized to access it.'}

        #serialize deadline
        deadline_dump = deadline_schema.dump(deadline)
        try:
            return deadline_dump
        except:
            return {'message': 'Something went wrong.'}, 500

class AllDeadlines(Resource):
    @jwt_required
    def get(self):
        current_user_name = get_jwt_identity()
        ids = Deadline.find_all_ids_of_user(current_user_name);
        print(ids)
        try:
            return [i[0] for i in ids]
        except:
            return {'message': 'Something went wrong.'}, 500
