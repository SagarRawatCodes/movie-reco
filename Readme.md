# 🎬 Smart Movie Finder (FastAPI + Gemini + React)

An intelligent, full-stack movie recommendation app built with **FastAPI (Python)** for the backend and **React + Vite** for the frontend.

Users can type natural queries like:

> “Action movies with a strong female lead”  
> “Romantic Indian movies on Netflix”  
> “Hollywood thrillers with AI or robots”

The app uses **Google Gemini API** to understand your description and recommend 5 movies — including:
- 🎞️ Movie Title  
- 🌍 Industry (Hollywood / Bollywood / South / Other)  
- ⭐ IMDb Rating (approx.)  
- 📺 Platforms where you can stream it  
- 🧾 Short Description  
- 🖼️ Poster (if available)

---

## 🚀 Features

✅ Natural-language movie recommendations using **Gemini**  
✅ FastAPI backend with CORS setup  
✅ React + Vite modern frontend  
✅ Attractive responsive movie cards  
✅ IMDb rating & streaming platform badges  
✅ Easy `.env` configuration for API keys  
✅ Works locally or can be deployed (frontend to Vercel / backend to Render or Railway)

---

## 🏗️ Project Structure

movie-recommender/
├─ backend/
│ ├─ app/
│ │ ├─ main.py # FastAPI backend
│ │ └─ models.py # optional (for database)
│ ├─ .env # environment variables
│ ├─ requirements.txt
│ └─ README.md
└─ frontend/
├─ src/
│ ├─ App.jsx
│ ├─ main.jsx
│ ├─ api.js
│ └─ components/
│ ├─ MovieForm.jsx
│ └─ MovieList.jsx
├─ package.json
├─ vite.config.js
└─ public/

yaml
Copy code

---

## ⚙️ Backend Setup (FastAPI + Gemini)

### 1️⃣ Create a virtual environment
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate     # (Windows)
# source .venv/bin/activate  # (macOS/Linux)
2️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Create .env file in backend/
ini
Copy code
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=models/text-bison-001
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
(You can get a free Gemini API key from Google AI Studio)

4️⃣ Run the backend
bash
Copy code
uvicorn app.main:app --reload  ||  .\start_backend.bat
The server should start on:

http://127.0.0.1:8000

🧩 Frontend Setup (React + Vite)
1️⃣ Install dependencies
bash
Copy code
cd frontend
npm install
2️⃣ Run the frontend
bash
Copy code
npm run dev
The app runs on:

http://localhost:5173 (or 5174)
