# [HBnB - BL and API](https://intranet.hbtn.io/projects/3211)
**Part 2: Implementation of Business Logic and API Endpoints**

## 0. Project Setup and Package Initialization
Set the part 2's minimal structure as such [(see instructional documentation)](https://github.com/Holberton-Uy/hbnb-doc/blob/main/part2/task_00_init.md) :
```bash
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

## 1. Core Business Logic Classes
Set the business logic's classes according to the concepts ([see part 1](../../part-1/Business_Logic_Layer.md)) and to the [instructional documentation](https://github.com/Holberton-Uy/hbnb-doc/blob/main/part2/task_01_bl.md) :
- Added **`BaseModel` Class [(see base module)](app/models/basemodel.py)**:
    - A pseudo-abstract (actually a superclass) to process general attributes and methods, such as :
        - `id` (String): Unique identifier for each object
        - `created_at` (DateTime): Timestamp when the object is created. Saved only once when the object is constructed.
        - `update()`: For the moment, it only updates the `updated_at` attribute of the object by calling `save()` :
            - `save()`: Barely updates the `updated_at` attribute of the object.
            - `updated_at` (DateTime): Timestamp when the object is last updated.
        - `delete()`: *(To be added)*

- **`User` Class [(see user module)](app/models/user.py)**:
    - `first_name`: User's non empty first name. Maximum length of 50 characters. Everyone has a first name right?
    - `last_name`: User's non empty last name. Maximum length of 50 characters. Everyone has a last name right?
    - `email`: User's unique electronic mail adress. You can't be on HBnB without an email (also we hope there won't be SQL injections).
    - `is_admin`: What if the user is an administrator? Defaults to `False` for obvious purposes.
    - **Relationships:**
        - `places`: All places the user owns. Implemented with `add_place()`, called upon a `Place` construction.

- **`Place` Class [(see place module)](app/models/place.py)**:
    - `title`: Place's non empty title. Maximum length of 100 characters.
    - `description`: Place's optional description. Describes the place independently of other attributes.
    - `price`: Place's price per night. Must be positive (let's asssume renting places in HBnB is never free).
    - `latitude`: Place's GPS latitude coordinates from -90° to 90° (positive is from equator to north pole).
    - `longitude`: Place's GPS longitude coordinates from -180 to 180° (positive is from Greenwich meridian to date change line).
    - `owner`: Place's owner. It must be an exisiting instance of the aforementioned `User` class.
    - **Relationships:**
        - `reviews`: All place reviews list. Implemented with `add_review()`, called upon a `Review` construction.
        - `amenities`: All place amenities list. Implemented with `add_amenity()`, and can be printed with `list_amenities()`.

- **`Review` Class [(see place module)](app/models/place.py)**:
    - `text`: Review non empty text.
    - `rating`: Rating within the review, from 1 to 5.
    - `place`: The reviewed place. It must be an exisiting instance of the aforementioned `Place` class.
    - `user`: Review writer. It must be an exisiting instance of the aforementioned `User` class.

- **`Amenity` Class [(see place module)](app/models/amenity.py)**:
    - `name`: The non empty name given to the amenity. Maximum length of 50 characters.
        - Maybe implement a way to avoid dupes? (in the database?)
    - **Relationships:**
        - `places`: List of places tied to the amenity. Implemented with `add_place()`, and prints the instance with `__str__()`.
