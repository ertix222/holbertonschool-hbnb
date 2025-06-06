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
