import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List, Optional
from contextlib import asynccontextmanager

# Import Gemini, Schemas, and DB models
import google.generativeai as genai
from .schemas import MovieItem, RecommendRequest, RecommendResponse
from .models import save_recommendation

# Import the engine and metadata from database.py
from .database import engine, metadata

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini client
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)


# This function runs ONCE when your app starts up
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App startup: Creating database tables...")
    metadata.create_all(bind=engine)
    print("App startup: Database tables created.")
    yield
    # Code here would run on app shutdown


# Tell FastAPI to use our new lifespan function
# This line is now corrected (lifespan=lifespan)
app = FastAPI(title="Smart Movie Finder", lifespan=lifespan)

# Add your Vercel frontend URL to this "allow list"
origins = [
    "http://localhost:5173",  # For your local development
    "https.movie-reco-bice.vercel.app"  # For your live Vercel app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Use the list of origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 3. UPDATED Helper function to call Gemini ---
def get_gemini_recommendations(prompt: str, movie_type: str, release_pref: str) -> List[MovieItem]:
    """
    Gets movie recommendations from Gemini.
    Asks for JSON with title, year, and overview.
    """

    model = genai.GenerativeModel('gemini-2.5-flash')

    # This prompt asks for a JSON object.
    gemini_prompt = f"""
    Based on the user's request, give me a list of 5 movie recommendations.

    User's detailed description: "{prompt}"
    Movie Type (region): "{movie_type}"
    Release Preference: "{release_pref}"

    You MUST return your answer as a valid JSON array.
    Each object in the array must have ONLY these three keys: "title", "year", and "overview".
    The "overview" should be a short, 1-2 sentence description.

    Example JSON format:
    [
      {{
        "title": "Movie Title One",
        "year": 1999,
        "overview": "A short, 1-2 sentence overview of the movie."
      }},
      {{
        "title": "Movie Title Two",
        "year": 2005,
        "overview": "Another short overview for the second movie."
      }}
    ]
    """

    try:
        response = model.generate_content(gemini_prompt)
        
        # Clean the response text to get only the JSON
        json_text = response.text.strip().lstrip("```json").rstrip("```")

        # Parse the JSON string into a Python list of dictionaries
        movies_list = json.loads(json_text)

        # Convert the list of dicts into a list of MovieItem objects
        movie_items = [MovieItem(**movie) for movie in movies_list]

        return movie_items

    except Exception as e:
        print(f"⚠️ Gemini Error (or JSON parse error): {e}")
        try:
            print(f"Raw response from Gemini: {response.text}")
        except:
            pass # response object might not exist
        raise HTTPException(status_code=500, detail="Gemini API error or invalid JSON response.")


# --- 4. The main recommendation endpoint ---
@app.post("/recommend", response_model=RecommendResponse)
async def recommend_movies(request: RecommendRequest):
    """
    The main endpoint.
    1. Gets all recommendations (including details) from Gemini.
    2. Saves to the DB and returns.
    """
    print(f"Received request: {request.dict()}")

    movie_details_list = get_gemini_recommendations(
        prompt=request.description,
        movie_type=request.movie_type,
        release_pref=request.release_pref
    )
    
    if not movie_details_list:
        raise HTTPException(status_code=404, detail="Could not get recommendations from AI.")

    print(f"Gemini suggested: {[m.title for m in movie_details_list]}")

    try:
        input_summary = f"Desc: {request.description}, Type: {request.movie_type}, Pref: {request.release_pref}"
        save_recommendation(
            user_input=input_summary, 
            movies=[m.dict() for m in movie_details_list]
        )
    except Exception as e:
        print(f"⚠️ DB Save Error: {e}")
        
    return RecommendResponse(
        preference=request.description, 
        movies=movie_details_list
    )

# A simple root endpoint to check if it's running
@app.get("/")
def read_root():
    return {"message": "Smart Movie Finder API is running! (Gemini-Only Edition)"}