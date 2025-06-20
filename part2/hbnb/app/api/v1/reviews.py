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
    def post(self):
        """Register a new review"""
        data = api.payload
        if not data:
            return {"error": "No data provided"}, 400

        #get the place before instanciating the review
        place = facade.get_place(data["place_id"])
        if not place:
            return {"error": "Place not found"}, 404

        userlist = facade.get_users_list()
        check = any(user.get("id") == data['user_id'] for user in userlist)
        if not check:
            return {'Error': 'No valid ID provided'}, 400
        if data["user_id"] == place.owner:
            return {"error": "Cannot review your own place!"}, 403

        try:
            new_review = facade.create_review(data)
            place.add_review(new_review)
            return {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "user_id": new_review.user_id,
                "place_id": new_review.place_id
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