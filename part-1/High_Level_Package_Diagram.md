```mermaid
---
title: High-Level Package Diagram
---
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
