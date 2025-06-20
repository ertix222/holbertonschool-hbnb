from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True,
                              description='ID of the owner'),
    'amenities': fields.List(fields.String,
                             required=True,
                             description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    @api.response(401, 'No input data')
    def post(self):
        """Register a new place"""
        try:
            data = api.payload
            if not data:
                return {"error": "No data input"}, 401

            user_id = data['owner_id']
            if not user_id:
                return {"error": "User ID is required"}, 400

            userlist = facade.get_all_users()
            user_found = False
            for i in userlist:
                if user_id == i.id:
                    user_found = True
                    break
            if not user_found:
                return {'Error': 'No valid owner ID provided'}, 404

            owner = facade.user_repo.get_by_attribute('id', user_id)
            if not owner:
                return {"error": "Owner not found"}, 404

            data["owner"] = owner
            del data["owner_id"]
            place = facade.create_place(data)
            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner.id
                }, 201
        except Exception as e:
            api.abort(400, str(e))

    @api.response(200, 'List of places retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Places not found')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            return [{
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude
                } for p in places], 200
        except Exception as e:
            api.abort(400, str(e))


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, f"Place with id '{place_id}' not found")
            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner": {
                    "id": place.owner.id,
                    "first_name": place.owner.first_name,
                    "last_name": place.owner.last_name,
                    "email": place.owner.email
                    },
                "amenities": [
                    {
                        "id": i.id,
                        "name": i.name
                    } for i in place.amenities]
                }, 200
        except Exception as e:
            api.abort(400, str(e))

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(401, 'No input data')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            data = api.payload
            if not data:
                return {"error": "No data input"}, 401

            place = facade.update_place(place_id, data)
            if not place:
                api.abort(404, f"Place with id '{place_id}' not found")
            return {"message": "Place updated successfully"}, 200
        except Exception as e:
            api.abort(400, str(e))
