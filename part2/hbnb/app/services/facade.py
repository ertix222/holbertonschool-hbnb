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

    # ===User facade methods===

    def create_user(self, user_data):
        """Creates a user

        Args:
            user_data (dict): User arguments dictionary

        Returns:
            User: A new user
        """
        try:
            user = User(**user_data)
            if self.user_repo.get_by_attribute('email', user.email):
                raise AttributeError("Email already used")
            self.user_repo.add(user)
            return user
        except Exception as e:
            raise Exception(e)

    def get_user(self, user_id):
        try:
            return self.user_repo.get(user_id)
        except Exception as e:
            raise Exception(e)

    def get_user_by_email(self, email):
        try:
            return self.user_repo.get_by_attribute('email', email)
        except Exception as e:
            raise Exception(e)

    def get_all_users(self):
        try:
            return self.user_repo.get_all()
        except Exception as e:
            raise Exception(e)

    # ===Amenity facade methods===

    def create_amenity(self, amenity_data):
        """Creates an amenity

        Args:
            amenity_data (dict): Amenity arguments dictionary

        Returns:
            Amenity: A new amenity
        """
        try:
            amenity = Amenity(**amenity_data)
            existing_amenity = self.amenity_repo.get_by_attribute('name',
                                                                  amenity.name)
            if existing_amenity:
                return existing_amenity
            self.amenity_repo.add(amenity)
            return amenity
        except Exception as e:
            raise Exception(e)

    def get_amenity(self, amenity_id):
        try:
            return self.amenity_repo.get(amenity_id)
        except Exception as e:
            raise Exception(e)

    def get_amenity_by_name(self, amenity_name):
        try:
            return self.amenity_repo.get_by_attribute('name', amenity_name)
        except Exception as e:
            raise Exception(e)

    def get_all_amenities(self):
        """Retrieve all amenities

        Returns:
            list: List of all amenities
        """
        try:
            return self.amenity_repo.get_all()
        except Exception as e:
            raise Exception(e)

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity

        Args:
            amenity_id (str): The ID of the amenity
            amenity_data (dict): Dictionary of all the amenity args
        """
        try:
            self.amenity_repo.get(amenity_id).update(amenity_data)
        except Exception as e:
            raise Exception(e)

    # ===Place facade methods===

    def create_place(self, place_data):
        try:
            owner = self.user_repo.get_by_attribute('id',
                                                    place_data['owner'].id)
            if not owner:
                raise AttributeError("Owner doesn't exist")
            if not isinstance(owner, User):
                raise TypeError("Owner should be a user")

            place = Place(**place_data)
            self.place_repo.add(place)
            owner.add_place(place)
            return place
        except Exception as e:
            raise Exception(e)

    def get_place(self, place_id):
        """Fetch a place by ID

        Args:
            place_id (str): The place ID

        Return:
            Place: The place corrsponding to the ID
        """
        try:
            place = self.place_repo.get(place_id)
            if not place:
                raise AttributeError("Place not found")
            return place
        except Exception as e:
            raise Exception(e)

    def get_all_places(self):
        try:
            return self.place_repo.get_all()
        except Exception as e:
            raise Exception(e)

    def update_place(self, place_id, place_data):
        try:
            place = self.place_repo.get(place_id)
            if not place:
                raise AttributeError("Place not found")
            place.update(place_data)
            return place
        except Exception as e:
            raise Exception(e)
