import { useState } from "react";
import { getRecommendations } from "../api";

/*
  THE FIX IS HERE:
  We are now correctly receiving 'isLoading' as a prop from App.jsx
*/
export default function MovieForm({ onResult, setIsLoading, isLoading }) {
  // Use state for all form fields
  const [formData, setFormData] = useState({
    description: "",
    movie_type: "Hollywood", // Default value
    release_pref: "Classic / Old", // Default value
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.description.trim()) {
      setError("Please enter a description for your movie preference.");
      return;
    }
    
    setIsLoading(true); // Tell App.jsx we are loading
    setError("");
    onResult([]); // Clear previous results

    try {
      // Use the *corrected* api.js function
      const data = await getRecommendations(formData);
      onResult(data.movies);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false); // Tell App.jsx we are done
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-gray-800 p-8 rounded-2xl shadow-xl">
      <form onSubmit={handleSubmit} className="flex flex-col gap-6">
        
        {/* Description Input */}
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-300 mb-2">
            What are you in the mood for?
          </label>
          <input
            type="text"
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="e.g., A sci-fi movie with time travel and a lot of philosophy..."
            className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white
                       placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Movie Type Radio Buttons */}
        <fieldset>
          <legend className="block text-sm font-medium text-gray-300 mb-2">
            Movie Type
          </legend>
          <div className="flex flex-wrap gap-x-6 gap-y-2">
            {["Hollywood", "Bollywood", "South Indian", "Any"].map((type) => (
              <div key={type} className="flex items-center">
                <input
                  type="radio"
                  id={type}
                  name="movie_type"
                  value={type}
                  checked={formData.movie_type === type}
                  onChange={handleChange}
                  className="h-4 w-4 accent-blue-500" // Styles the radio button itself
                />
                <label htmlFor={type} className="ml-2 block text-sm text-gray-200">
                  {type}
                </label>
              </div>
            ))}
          </div>
        </fieldset>

        {/* Release Preference Radio Buttons */}
        <fieldset>
          <legend className="block text-sm font-medium text-gray-300 mb-2">
            Release Preference
          </legend>
          <div className="flex flex-wrap gap-x-6 gap-y-2">
            {["Newly Released", "Classic / Old", "Any"].map((pref) => (
              <div key={pref} className="flex items-center">
                <input
                  type="radio"
                  id={pref}
                  name="release_pref"
                  value={pref}
                  checked={formData.release_pref === pref}
                  onChange={handleChange}
                  className="h-4 w-4 accent-blue-500"
                />
                <label htmlFor={pref} className="ml-2 block text-sm text-gray-200">
                  {pref}
                </label>
              </div>
            ))}
          </div>
        </fieldset>

        {/* Submit Button */}
        <div>
          <button
            type="submit"
            disabled={isLoading} // <-- This line now works
            className="w-full bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg
                       transition-all duration-200
                       hover:bg-blue-700
                       disabled:bg-gray-500 disabled:cursor-not-allowed"
          >
            {isLoading ? "Generating..." : "Get Recommendations"}
          </button>
        </div>
        
        {/* Error Message */}
        {error && <p className="text-red-400 text-sm text-center">{error}</p>}
      </form>
    </div>
  );
}