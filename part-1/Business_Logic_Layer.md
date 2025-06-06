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
