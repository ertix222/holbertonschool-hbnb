from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(401, 'No input data')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user

        Returns:
            dict: JSON of the new user
        """
        try:
            user_data = api.payload
            if not user_data:
                return {"error": "No data input"}, 401

            # Simulate email uniqueness check
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 409

            for i in user_data:
                if not isinstance(user_data[i], str):
                    return {'error': 'Invalid input data'}, 400

            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
                }, 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    @api.response(400, 'Invalid input data')
    def get(self):
        """retrieve a list of all users

        Returns:
            list: List of JSON of all users
        """
        try:
            users = facade.get_all_users()
            return [
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                    } for user in users], 200
        except Exception as e:
            return {"error": str(e)}, 400


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def get(self, user_id):
        """Get user details by ID

        Args:
            user_id (str): The user's ID

        Returns:
            dict: The JSON of the fetched user
        """
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
                }, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(401, 'No input data')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user

        Args:
            user_id (str): The user's ID

        Returns:
            dict: JSON of the updated user
        """
        try:
            user_data = api.payload
            if not user_data:
                return {"error": "No data input"}, 401

            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            for i in user_data:
                if not isinstance(user_data[i], str):
                    return {'error': 'Invalid input data'}, 400

            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
                }
        except Exception as e:
            return {"error": str(e)}, 400
