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
