// Import our new component
import MovieCard from './MovieCard'; 

// Skeleton card for the loading state (same as before)
const SkeletonCard = () => (
  <div className="bg-gray-800 rounded-2xl shadow-lg overflow-hidden animate-pulse">
    <div className="w-full h-96 bg-gray-700"></div>
    <div className="p-4">
      <div className="h-6 bg-gray-700 rounded w-3/4 mb-2"></div>
      <div className="h-4 bg-gray-700 rounded w-1/4"></div>
      <div className="flex flex-wrap gap-2 mt-4">
        <div className="h-5 bg-gray-700 rounded-full w-20"></div>
        <div className="h-5 bg-gray-700 rounded-full w-24"></div>
      </div>
    </div>
  </div>
);

export default function MovieList({ movies, isLoading }) {
  
  // Show 5 skeleton cards while loading
  if (isLoading) {
    return (
      <div className="mt-12 flex flex-wrap justify-center gap-6">
        {[...Array(5)].map((_, i) => (
          <div className="w-full sm:w-64" key={i}> {/* Width for skeleton */}
            <SkeletonCard />
          </div>
        ))}
      </div>
    );
  }

  // Show nothing if there are no movies and it's not loading
  if (movies.length === 0) {
    return null;
}

  return (
    // This is the main grid for the movie cards
    // We use flex-wrap and justify-center to center the cards
    <div className="mt-12 flex flex-wrap justify-center gap-6">
      
      {movies.map((m) => (
        // We set a width here to control the card size
        <div className="w-full sm:w-64" key={m.title}>
          {/* Render the new MovieCard component */}
          <MovieCard movie={m} />
        </div>
      ))}
    </div>
  );
}