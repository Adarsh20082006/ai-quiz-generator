import axios from "axios";

export const API_BASE = import.meta.env.VITE_API_BASE_URL;

//  Fetch Wikipedia article preview
export const previewArticle = async (url) => {
  const { data } = await axios.post(`${API_BASE}/generate_quiz`, { url });
  return data; // { title, available_sections }
};

//  Generate Quiz (Main function with robust error handling)
export async function generateQuiz(payload) {
  try {
    const response = await axios.put(
      `${API_BASE}/generate_quiz`,
      payload,
      { headers: { "Content-Type": "application/json" } }
    );

    return response.data; //  Successful response

  } catch (error) {
    console.error("Quiz generation failed:", error);

    let userMessage = "Something went wrong while generating your quiz!!!";

    if (error.response) {
      const status = error.response.status;

      switch (status) {
        case 500:
          userMessage =
            "The AI quiz generator ran out of memory while processing this request. This happens because Render’s free hosting plan only provides limited memory. Please try again in a few minutes or choose a shorter article.";
          break;
        case 502:
          userMessage =
            "The server is temporarily restarting — usually due to Render’s free-tier memory constraints. Please retry shortly.";
          break;
        case 429:
          userMessage =
            "The AI request quota has been exceeded. Please wait and try again later.";
          break;
        default:
          userMessage = `Server Error (${status}): ${
            error.response.data.detail || "Unexpected issue occurred."
          }`;
      }
    } else if (error.request) {
      userMessage =
        "The server did not respond — likely because it temporarily ran out of memory on Render’s free plan. Please retry in a minute.";
    } else {
      userMessage = "Unexpected error occurred. Please try again.";
    }

    //  Clean, user-friendly alert
    alert(userMessage);
    throw error;
  }
}

//  Fetch all saved quizzes
export const getHistory = async () => {
  const { data } = await axios.get(`${API_BASE}/history`);
  return data; // [{id,url,title,date_generated}, ...]
};

//  Fetch quiz by ID
export const getQuizById = async (id) => {
  const { data } = await axios.get(`${API_BASE}/quiz/${id}`);
  return data; // full quiz JSON
};
