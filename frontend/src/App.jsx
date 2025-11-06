import { useState } from "react";
import MovieForm from "./components/MovieForm";
import MovieList from "./components/MovieList";

function App() {
  const [movies, setMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleResult = (moviesArr) => {
    setMovies(moviesArr);
  };

  return (
    <div className="max-w-6xl mx-auto my-12 p-6">
      <header className="text-center mb-10">
        <h2 className="text-xl font-semibold text-blue-400">
          Acelucid Assignment
        </h2>
        <h1 className="text-5xl font-bold text-white mt-2">
          🎥 Movie Recommender
        </h1>
      </header>
      
      <main>
        <MovieForm 
          onResult={handleResult} 
          setIsLoading={setIsLoading} 
          isLoading={isLoading} // <-- THIS IS THE NEWLY ADDED LINE
        />
        <MovieList 
          movies={movies} 
          isLoading={isLoading} 
        />
      </main>
    </div>
  );
}

export default App;