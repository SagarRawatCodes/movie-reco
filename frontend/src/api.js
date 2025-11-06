const BASE = "http://127.0.0.1:8000"; // Your backend

/**
 * Sends the complete form data to the backend.
 * @param {object} formData - The object { description, movie_type, release_pref }
 */
export async function getRecommendations(formData) {
  console.log("Sending to backend:", formData); // So you can see it's correct

  const resp = await fetch(`${BASE}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // We send the formData object directly
    body: JSON.stringify(formData),
  });

  if (!resp.ok) {
    // Try to parse the error message from FastAPI
    const errorData = await resp.json().catch(() => null);
    console.error("Backend Error:", errorData);

    if (resp.status === 422 && errorData.detail) {
      // This is a validation error
      throw new Error(`Invalid data: ${errorData.detail[0].msg}`);
    }
    
    // A generic error
    throw new Error(errorData?.detail || "Failed to fetch recommendations");
  }

  return resp.json();
}