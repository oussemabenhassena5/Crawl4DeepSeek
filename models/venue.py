from pydantic import BaseModel


class Venue(BaseModel):
    """
    Represents the data structure of a Venue.
    """

    name: str
    location: str
    price: str
    capacity: str
    rating: float
    reviews: int
    description: str
