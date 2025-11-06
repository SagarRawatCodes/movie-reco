from pydantic import BaseModel
from typing import List, Optional

class MovieItem(BaseModel):
    title: str
    overview: Optional[str] = None
    poster_url: Optional[str] = None
    release_date: Optional[str] = None
    rating: Optional[float] = None
    watch_on: Optional[List[str]] = None

# --- UPDATED ---
# This model now accepts all our new form fields
class RecommendRequest(BaseModel):
    description: str
    movie_type: str
    release_pref: str

class RecommendResponse(BaseModel):
    # This will just return the original description
    preference: str 
    movies: List[MovieItem]