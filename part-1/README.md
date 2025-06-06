# HBnB Part 1 - UML
## 0. High-Level Package Diagram
This high-level package illustrates the three-layer architecture of the HBnB application and the communication between several layers :

The API services (Presentation layer) process the website user's actions and connects with the website's logic models (BusinessLogic layer) via the facade pattern, which in turn process objects to manage and access the website's database (Persistence Layer).

```mermaid
graph TB

A[**Presentation**
    Services
    UserAPI
    PlaceAPI
    ReviewAPI
    AmenityAPI
    Endpoints]

B[**BusinessLogic**
    User models
    Place models
    Review models
    Amenity models]

C[**Persistence**
    Database access
    ]


A --> |Facade Pattern| B
B --> |Database Operations| C
```

## 1. Detailed Class Diagram for Business Logic Layer

This diagram illustrates the core business entities of the HBnB application: User, Place, Review, and Amenity. Each inherits from BaseModel, which defines shared attributes like id, created_at, and updated_at.

Key relationships are shown:

A User can own multiple Places and write multiple Reviews.

A Place belongs to one User, can have many Reviews, and is linked to multiple Amenitys through AmenityPlace.

Reviews connect a User to a Place.

Amenitys can be linked to many Places.


```mermaid
classDiagram

class BaseModel {
    <<abstract>>
    +UUID id
    +DATE created_at
    +DATE updated_at
    +update()
    +delete()
  }
  
  class User {
    +str first_name
    +str last_name
    -str email
    -str password
    +sign_up()
    +login()
    -set_password(password)setter
    -check_password(password)getter
    +write_review()
    +delete()
    +update()
  }
  
  class Place {
    +str name
    +str location
    +float price_by_night
    +str currency
    +float rating
    -UUID user_id
    +get_owner()
    +add_amenity()
    +remove_amenity()
    +show_reviews()
    +update()
    +delete()
  }

  class Review {
    -UUID user_id
    -UUID place_id
    +int rating
    +str comment
    +get_user()
    +get_place()
    +write_review()
    +update()
    +delete()
  }

  class Amenity {
    +str name
    +display(place_id)
    +update()
    +delete()
  }

  class AmenityPlace {
    -UUID amenity_id
    -UUID place_id
  }

BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Amenity
BaseModel <|-- Review

User "1" --> "many" Review : Writes
User "1" --> "many" Place : Owns
Place "1" --> "many" Review : Has
Place "1" --> "1" User : Belongs to
Place "1" --> "many" AmenityPlace
Amenity "1" --> "many" AmenityPlace

```


## 2. Sequence Diagrams for API Calls
These sequence diagrams showcase the detailed process of the requests of the APIs, the logic models as well as the database responses, upon user requests.

### 2-0. User Registration
This sequence diagram correspond to a `POST` request sent by the admin or an anonymous user on the `sign_in/` endpoint route. It checks if the input is correct (especially not empty fields) and if the new user doesn't exist already.

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Business logic
    participant Persistence

    User->>API: POST /sign_in
    API->>Business logic: check_user()
    alt check fails
        Business logic-->>API: Check error
        API-->>User: 400 Bad Request:<br>User format not valid/empty
    else check passes
        Business logic->>Persistence: user_exists()
        alt database select failed
            Persistence-->>Business logic: Failed select request error
            Business logic-->>API: Fetching failed
            API-->>User: 500 Internal Server Error:<br>Fetching failed
        else user already exists
            Persistence-->>Business logic: Not empty select request
            Business logic-->>API: Dupe user error
            API-->>User: 409 Conflict:<br>User already exists
        else user doesn't exist
            Persistence-->>Business logic: Empty select request
            Business logic->>Business logic: hash_password()
            Business logic->>Persistence: Insert user data
            alt database insert failed
                Persistence-->>Business logic: Insert fails
                Business logic-->>API: User not registered
                API-->>User: 500 Internal Server Error:<br>User can't be registered
            else database insert passes
                Persistence-->>Business logic: Insert passes
                Business logic-->>API: User registered
                API-->>User: 201 Created:<br>User registered successfully
            end
        end
    end
```

### 2-1. Place Creation
This sequence diagram correspond to a `POST` request sent by the admin or an anonymous user on the `add_place/` endpoint route. It checks if the input is correct (especially not empty fields) and if the place doesn't correspond to an already existing place.

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Business logic
    participant Persistence

    User->>API: POST /add_place
    API->>Business logic: check_place()
    alt check fails
        Business logic-->>API: Check error
        API-->>User: 400 Bad Request:<br>Place format not valid/empty
    else check passes
        Business logic->>Persistence: place_exists()
        alt database select failed
            Persistence-->>Business logic: Failed select request error
            Business logic-->>API: Fetching failed
            API-->>User: 500 Internal Server Error:<br>Fetching failed
        else place already exists
            Persistence-->>Business logic: Not empty select request
            Business logic-->>API: Dupe place error
            API-->>User: 409 Conflict:<br>Place already exists
        else place doesn't exist
            Persistence-->>Business logic: Empty select request
            Business logic->>Persistence: Insert place data
            alt database insert failed
                Persistence-->>Business logic: Insert fails
                Business logic-->>API: Place not created
                API-->>User: 500 Internal Server Error:<br>Place can't be created
            else database insert passes
                Persistence-->>Business logic: Insert passes
                Business logic-->>API: Place created
                API-->>User: 201 Created:<br>Place created successfully
            end
        end
    end
```

### 2-2. Review Submission
This sequence diagram correspond to a `POST` request sent by the admin or an anonymous user on the `submit_review/` endpoint route. It checks if the input is correct (especially if the review may be empty or may contained bad wording) and if the place the review is submitted on exists.

A user still can post the same review over and over (no spam management) and post a review on a place not visited.

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Business logic
    participant Persistence

    User->>API: POST /submit_review
    API->>Business logic: check_review()
    alt check fails
        Business logic-->>API: Check error
        API-->>User: 400 Bad Request:<br>Review format not valid/empty
    else check passes
        Business logic->>Persistence: place_exists()
        alt database select failed
            Persistence-->>Business logic: Failed select request error
            Business logic-->>API: Fetching failed
            API-->>User: 500 Internal Server Error:<br>Fetching failed
        else place doesn't exist
            Persistence-->>Business logic: Empty select request
            Business logic-->>API: Place doesn't exist
            API-->>User: 404 Not Found:<br>No place to review
        else place exists
            Persistence-->>Business logic: Not empty select request
            Business logic->>Persistence: Insert place data
            alt database insert failed
                Persistence-->>Business logic: Insert fails
                Business logic-->>API: Review not submitted
                API-->>User: 500 Internal Server Error:<br>Review can't be submitted
            else database insert passes
                Persistence-->>Business logic: Insert passes
                Business logic-->>API: Review submitted
                API-->>User: 201 Created:<br>Review submitted successfully
            end
        end
    end
```

### 2-3. Fetching a List of Places
This sequence diagram correspond to a `GET` request sent by the admin or an anonymous user on the `fetch_places/` endpoint route. It checks if the filters are correct, or if the search result isn't empty.

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Business logic
    participant Persistence

    User->>API: GET /fetch_places
    API->>Business logic: check_filters()
    alt check fails
        Business logic-->>API: Check error
        API-->>User: 400 Bad Request:<br>Wrong filters
    else check passes
        Business logic->>Persistence: place_exists()
        alt fetching fails
            Persistence-->>Business logic: Failed select request error
            Business logic-->>API: Fetching failed
            API-->>User: 500 Internal Server Error:<br>Fetching failed
        else places don't exist
            Persistence-->>Business logic: Empty select request
            Business logic-->>API: None
            API-->>User: 404 Not Found:<br>No places found
        else places exist
            Persistence-->>Business logic: Not empty select request
            Business logic-->>API: Place list
            API-->>User: 200 OK:<br>Places found
        end
    end
```
