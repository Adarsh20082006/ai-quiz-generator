import axios from "axios";

export const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const previewArticle = async (url) => {
    const { data } = await axios.post(`${API_BASE}/generate_quiz`, { url });
    return data; // { title, available_sections }
};

async function generateQuiz(payload) {
  try {
    const response = await axios.put(
      "https://ai-quiz-generator-dqj9.onrender.com/generate_quiz",
      payload,
      { headers: { "Content-Type": "application/json" } }
    );

    // ✅ If success
    return response.data;

  } catch (error) {
    console.error("Quiz generation failed:", error);

    let userMessage = "⚠️ Something went wrong while generating your quiz.";

    if (error.response) {
      // Backend responded with error code
      if (error.response.status === 500) {
        userMessage = "⚙️ The AI quiz generator ran out of memory. This is due to the free Render plan’s 512MB limit, not your input. Please retry after a minute or simplify your article.";
      } else if (error.response.status === 502) {
        userMessage = "🚧 Server temporarily unavailable — likely due to Render’s free-tier memory limit. Please retry shortly.";
      } else if (error.response.status === 429) {
        userMessage = "💸 The API quota for AI requests was exceeded. Please try again later.";
      } else {
        userMessage = `⚠️ Server Error (${error.response.status}): ${error.response.data.detail || "Unexpected issue."}`;
      }
    } else if (error.request) {
      // No response received (backend crashed)
      userMessage = "🚧 The server didn’t respond — possibly out of memory on Render’s free plan. Try again after a few moments.";
    } else {
      // Other errors
      userMessage = "⚙️ Unknown error occurred. Please try again.";
    }

    alert(userMessage);
    throw error;
  }
}

export const getHistory = async () => {
    const { data } = await axios.get(`${API_BASE}/history`);
    return data; // [{id,url,title,date_generated}, ...]
};

export const getQuizById = async (id) => {
    const { data } = await axios.get(`${API_BASE}/quiz/${id}`);
    return data; // full quiz JSON
};
