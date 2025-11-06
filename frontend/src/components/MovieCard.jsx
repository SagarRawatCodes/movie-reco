import { useState } from 'react';

// We create a new component for the card to manage its own state
export default function MovieCard({ movie }) {
  // This state only applies to this one card
  const [isExpanded, setIsExpanded] = useState(false);

  // Helper function to format the date
  const formatReleaseDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch (error) {
      return dateString; // Fallback if date is invalid
    }
  };

  return (
    <div 
      className="bg-gray-800 rounded-2xl shadow-lg overflow-hidden
                 transform transition-all duration-300
                 hover:scale-105 hover:shadow-2xl
                 flex flex-col" // Added flex-col to keep footer at bottom
    >
      {/* Movie Poster */}
      <img 
        src={movie.poster_url || 'https://placehold.co/500x750/2D3748/E2E8F0?text=No+Image'} 
        alt={movie.title} 
        className="w-full h-96 object-cover" 
      />
      
      {/* Movie Info */}
      <div className="p-4 flex flex-col flex-grow"> {/* Added flex-grow */}
        <div className="flex justify-between items-start gap-2">
          {/* Title */}
          <h3 className="text-xl font-bold text-white mb-1">
            {movie.title}
          </h3>
          
          {/* --- THIS IS THE FIX --- */}
          {/* Rating - Replaced the star icon with a simple text label */}
          {movie.rating > 0 && (
            <div className="flex-shrink-0 bg-yellow-400 text-black text-sm font-bold px-3 py-0.5 rounded-full">
              <span>Rating: {movie.rating.toFixed(1)}</span>
            </div>
          )}
          {/* --- END OF FIX --- */}

        </div>
        
        {/* Release Date */}
        <div className="mt-2">
          <span className="text-xs font-medium text-gray-400">Release Date:</span>
          <span className="text-sm text-gray-200 ml-2">{formatReleaseDate(movie.release_date)}</span>
        </div>

        {/* Watch Platforms */}
        {movie.watch_on && movie.watch_on.length > 0 && (
          <div className="mt-3">
            <span className="text-xs font-medium text-gray-400 mb-2 block">
              Watch on:
            </span>
            <div className="flex flex-wrap gap-2">
              {movie.watch_on.slice(0, 3).map((platform) => (
                <span
                  key={platform}
                  className="inline-block bg-gray-700 text-gray-300 text-xs 
                             font-medium px-2.5 py-1 rounded-full"
                >
                  {platform}
                </span>
              ))}
            </div>
          </div>
        )}
        
        {/* This spacer div pushes the "See More" button to the bottom */}
        <div className="flex-grow"></div> 

        {/* "See More" / "See Less" Section */}
        <div className="mt-4">
          {!isExpanded && (
            <button
              onClick={() => setIsExpanded(true)}
              className="text-blue-400 text-sm font-medium hover:text-blue-300"
            >
              See More...
            </button>
          )}
          
          {isExpanded && (
            <div className="text-sm text-gray-300 space-y-3">
              <p>{movie.overview || "No description available."}</p>
              <button
                onClick={() => setIsExpanded(false)}
                className="text-blue-400 text-sm font-medium hover:text-blue-300"
              >
                See Less
              </button>
            </div>
          )}
        </div>
        
      </div>
    </div>
  );
}