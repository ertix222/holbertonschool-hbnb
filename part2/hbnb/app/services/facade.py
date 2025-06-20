from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ===User facade placeholder methods===

    def create_user(self, user_data):
        """Placeholder method for creating a user

        Args:
            user_data (dict): User arguments dictionary

        Returns:
            User: A new user
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    # ===Amenity facade placeholder methods===

    def create_amenity(self, amenity_data):
        """Placeholder for logic to create an amenity

        Args:
            amenity_data (dict): Amenity arguments dictionary

        Returns:
            Amenity: A new amenity
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        try:
            return self.amenity_repo.get(amenity_id)
        except Exception as e:
            print(e)

    def get_all_amenities(self):
        """Placeholder for logic to retrieve all amenities

        Returns:
            list: List of all amenities
        """
        try:
            return self.amenity_repo.get_all()
        except Exception as e:
            print(e)

    def update_amenity(self, amenity_id, amenity_data):
        """Placeholder for logic to update an amenity

        Args:
            amenity_id (uuid): The ID of the amenity
            amenity_data (dict): Dictionary of all the amenity args
        """
        try:
            self.amenity_repo.get(amenity_id).update(amenity_data)
        except Exception as e:
            print(e)

    # ===Place facade placeholder methods===

    def get_place(self, place_id):
        """Placeholder method for fetching a place by ID

        Args:
            place_id (uuid): The place ID

        Return:
            Place: The place corrsponding to the ID
        """
        return self.place_repo.get(place_id)
