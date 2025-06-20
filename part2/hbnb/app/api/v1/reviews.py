from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'No input data')
    def post(self):
        """Register a new review"""
        try:
            data = api.payload
            if not data:
                return {"error": "No data provided"}, 401            
            
            user_id = data['owner_id']
            if not user_id:
                return {"error": "User ID is required"}, 400
            
            place_id = data['place_id']
            if not place_id:
                return {"error": "Place ID is required"}, 400
            
            writer = facade.get_user(user_id)
            if not writer:
                return {"error": "Writer not found"}, 404
            
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404

            userlist = facade.get_all_users()
            user_found = False
            for i in userlist:
                if user_id == i.id:
                    user_found = True
                    break
            if not user_found:
                return {'Error': 'No valid writer ID provided'}, 404

            if data["user_id"] == place.owner.id:
                return {"error": "Cannot review your own place!"}, 403

            data["user"] = writer
            del data["owner_id"]
            data["place"] = place
            del data["place_id"]

            new_review = facade.create_review(data)
            return {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "user_id": new_review.user.id,
                "place_id": new_review.place.id
            }, 201
        except Exception as e:
            return {"Error" : str(e)}, 400


@api.response(200, 'List of reviews retrieved successfully')
def get(self):
    """Retrieve a list of all reviews"""
    return facade.get_all_reviews()


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        obj = facade.get_review(review_id)
        if not obj:
            return {"error": "Review not found"}, 404
        return {"id": obj.id, "text": obj.text,
                "rating": obj.rating, "user_id": obj.user_id,
                "place_id": obj.place_id}, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        pass

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        pass

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        pass