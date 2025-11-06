import os, requests, json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List, Optional
from contextlib import asynccontextmanager # For the lifespan event

# Import Gemini, Schemas, and DB models
import google.generativeai as genai
from .schemas import MovieItem, RecommendRequest, RecommendResponse
from .models import save_recommendation 

# Import the engine and metadata from database.py so we can use them
from .database import engine, metadata


# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Get the Gemini key

# Configure the Gemini client
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY not found in .env file. It is required for posters and ratings.")
    
genai.configure(api_key=GEMINI_API_KEY)


# This function runs ONCE when your app starts up
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This creates the tables safely after all files are loaded
    print("App startup: Creating database tables...")
    metadata.create_all(bind=engine)
    print("App startup: Database tables created.")
    yield
    # Code here would run on app shutdown


# TMDB URLs
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_PROVIDERS_URL = "https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Tell FastAPI to use our new lifespan function
app = FastAPI(title="Smart Movie Finder", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. Helper function to call TMDB and find a movie ---
def search_tmdb(title: str) -> Optional[dict]:
    """Searches TMDB for a movie and returns the first result."""
    params = {"api_key": TMDB_API_KEY, "query": title}
    try:
        r = requests.get(TMDB_SEARCH_URL, params=params, timeout=5)
        r.raise_for_status()
        results = r.json().get("results", [])
        if results:
            return results[0] # Return the top match
    except Exception as e:
        print(f"⚠️ TMDB Search Error for '{title}': {e}")
    return None

# --- 2. *** THIS IS THE CRITICAL FIX *** ---
def get_watch_providers(movie_id: int, movie_type: str) -> List[str]:
    """
    Gets streaming watch providers for a movie.
    It smartly checks the region based on the movie_type.
    """
    
    # Decide which region to check for providers
    if movie_type in ["Bollywood", "South Indian"]:
        region_to_check = "IN" # Check India
    else:
        region_to_check = "US" # Default to US

    url = TMDB_PROVIDERS_URL.format(movie_id=movie_id)
    params = {"api_key": TMDB_API_KEY}
    providers = []
    
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        
        # We look for 'flatrate' (streaming) providers in the chosen region
        results_data = r.json().get("results", {})
        data = results_data.get(region_to_check, {})
        
        if "flatrate" in data:
            providers = [p["provider_name"] for p in data["flatrate"]]
        
        # If no providers found AND we weren't checking US, check "US" as a fallback
        # (This helps find "Hollywood" or "Any" movies that might be tagged "South Indian" by Gemini)
        if not providers and region_to_check != "US":
             data_us = results_data.get("US", {})
             if "flatrate" in data_us:
                 providers = [p["provider_name"] for p in data_us["flatrate"]]

    except Exception as e:
        print(f"⚠️ TMDB Provider Error for ID {movie_id}: {e}")
    
    # Return a unique list
    return list(set(providers))
# --- END OF FIX ---


# --- 3. Helper function to call Gemini ---
def get_gemini_recommendations(prompt: str, movie_type: str, release_pref: str) -> List[str]:
    """Gets movie title recommendations from Gemini."""
    
    # Use the model that we proved works
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # This prompt now uses all the form fields
    gemini_prompt = f"""
    Based on the user's request, give me a list of 5 movie recommendations.

    User's detailed description: "{prompt}"
    Movie Type (region): "{movie_type}"
    Release Preference: "{release_pref}"

    ONLY return the list of 5 movie titles.
    Do not include the year or any other text, just the titles.
    Separate each title with a new line.

    Example:
    The Dark Knight
    Inception
    The Matrix
    """
    
    try:
        response = model.generate_content(gemini_prompt)
        titles = response.text.strip().split('\n')
        # Clean up any potential junk
        return [title.strip() for title in titles if title.strip()]
    except Exception as e:
        print(f"⚠️ Gemini Error: {e}")
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")


# --- 4. The main recommendation endpoint ---
@app.post("/recommend", response_model=RecommendResponse)
async def recommend_movies(request: RecommendRequest):
    """
    The main endpoint.
    1. Gets recommendations from Gemini.
    2. Enriches them with data from TMDB.
    """
    print(f"Received request: {request.dict()}")

    # Step 1: Get movie titles from Gemini
    movie_titles = get_gemini_recommendations(
        prompt=request.description,
        movie_type=request.movie_type,
        release_pref=request.release_pref
    )
    if not movie_titles:
        raise HTTPException(status_code=404, detail="Could not get recommendations from AI.")

    print(f"Gemini suggested: {movie_titles}")

    # Step 2: Get details for each movie from TMDB
    movie_details_list: List[MovieItem] = []
    
    for title in movie_titles:
        movie_data = search_tmdb(title)
        
        if movie_data:
            movie_id = movie_data.get("id")
            # Pass movie_type to our updated helper function
            watch_on = get_watch_providers(movie_id, request.movie_type) if movie_id else []
            
            # Build the MovieItem
            movie_item = MovieItem(
                title=movie_data.get("title", "Unknown Title"),
                overview=movie_data.get("overview", ""),
                poster_url=f"{TMDB_IMAGE_BASE}{movie_data.get('poster_path')}" if movie_data.get('poster_path') else None,
                release_date=movie_data.get("release_date", ""),
                rating=movie_data.get("vote_average", 0.0), # Here's the rating
                watch_on=watch_on                           # Here are the platforms
            )
            movie_details_list.append(movie_item)

    if not movie_details_list:
        raise HTTPException(status_code=404, detail="Could not find details for any recommended movies.")

    # Step 3: Save and return
    try:
        # Create a summary of the user's input for the DB
        input_summary = f"Desc: {request.description}, Type: {request.movie_type}, Pref: {request.release_pref}"
        save_recommendation(
            user_input=input_summary, 
            movies=[m.dict() for m in movie_details_list]
        )
    except Exception as e:
        print(f"⚠️ DB Save Error: {e}") # Don't fail the request if DB save fails
        
    return RecommendResponse(
        preference=request.description, 
        movies=movie_details_list
    )

# A simple root endpoint to check if it's running
@app.get("/")
def read_root():
    return {"message": "Smart Movie Finder API is running!"}