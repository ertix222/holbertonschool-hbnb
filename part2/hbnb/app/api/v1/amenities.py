from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'No input data')
    @api.response(409, 'Amenity with the same name already existing')
    def post(self):
        """Register a new amenity"""
        try:
            amenity_data = api.payload
            if not amenity_data:
                return {"error": "No data input"}, 401

            input_amenity_name = amenity_data["name"]
            existing_amenity = facade.get_amenity_by_name(input_amenity_name)
            if existing_amenity:
                return {"error": "Amenity with the same name\
already existing"}, 409

            if not (input_amenity_name
                    and isinstance(input_amenity_name, str)):
                return {"error": "Amenity name must be\
a non-empty string"}, 400
            if input_amenity_name == "" or len(input_amenity_name) > 50:
                return {"error": "Amenity name is empty\
or too long (50 chars)"}, 400

            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
                }, 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(400, 'Invalid input data')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [
                {
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in amenities], 200
        except Exception as e:
            return {"error": str(e)}, 400


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)

            if not amenity:
                return {"error": "Amenity not found"}, 404

            return {
                    'id': amenity.id,
                    'name': amenity.name
                    }, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(401, 'No input data')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            amenity_data = api.payload
            if not amenity_data:
                return {"error": "No data input"}, 401

            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404

            input_amenity_name = amenity_data["name"]
            if not (input_amenity_name
                    and isinstance(input_amenity_name, str)):
                return {"error": "Amenity new name must\
be a non-empty string"}, 400
            if input_amenity_name == "" or len(input_amenity_name) > 50:
                return {"error": "Amenity new name\
is empty or too long (50 chars)"}, 400

            facade.update_amenity(amenity_id, amenity_data)
            return {"message": "Amenity updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
