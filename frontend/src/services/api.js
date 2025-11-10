import axios from "axios";

export const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const previewArticle = async (url) => {
    const { data } = await axios.post(`${API_BASE}/generate_quiz`, { url });
    return data; // { title, available_sections }
};

export const generateQuiz = async ({ url, difficulty, sections }) => {
    const { data } = await axios.put(`${API_BASE}/generate_quiz`, {
        url, difficulty, sections
    });
    return data; // full quiz JSON
};

export const getHistory = async () => {
    const { data } = await axios.get(`${API_BASE}/history`);
    return data; // [{id,url,title,date_generated}, ...]
};

export const getQuizById = async (id) => {
    const { data } = await axios.get(`${API_BASE}/quiz/${id}`);
    return data; // full quiz JSON
};
