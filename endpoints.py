from flask_restful import Resource, request
from models import Deadline, DeadlineSchema

deadline_schema = DeadlineSchema()

class CreateDeadline(Resource):
    def post(self):
        data = request.get_json()

        # create deadline out of json
        deadline = deadline_schema.load(data)
        new_deadline = Deadline(
            name = deadline.data['name'],
            type = deadline.data['type'],
            date = deadline.data['date'],
            priority = deadline.data['priority'],
            num_of_hours = deadline.data['num_of_hours']
        )

        try:
            new_deadline.save_to_db()
            # ret = promoter_schema.dump(promoter)
            return {'message':'Did it work?'},500
        except:
            return {'message':'Something went wrong.'},500

class OneDeadline(Resource):
    def get(self, id):
        deadline = Deadline.find_by_id(id)
        if not deadline:
            return {'message': 'A deadline with that id does not exist.'}
        #serialize deadline
        deadline_dump = deadline_schema.dump(deadline)
        try:
            return deadline_dump
        except:
            return {'message': 'Something went wrong.'}, 500
