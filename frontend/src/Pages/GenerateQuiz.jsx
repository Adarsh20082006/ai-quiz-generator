import { useState } from "react";
import { previewArticle, generateQuiz } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function GenerateQuiz() {
    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [preview, setPreview] = useState(null); // {title, available_sections}
    const [difficulty, setDifficulty] = useState("Medium");
    const [selectedSections, setSelectedSections] = useState([]);
    const navigate = useNavigate();

    const handlePreview = async () => {
        setLoading(true);
        try {
            const data = await previewArticle(url);
            setPreview(data);
        } catch (e) {
            alert(e?.response?.data?.detail || "Invalid URL");
        } finally {
            setLoading(false);
        }
    };

    const toggleSection = (sec) => {
        setSelectedSections(prev =>
            prev.includes(sec) ? prev.filter(s => s !== sec) : [...prev, sec]
        );
    };

    const handleGenerate = async () => {
        setLoading(true);
        try {
            const quiz = await generateQuiz({ url, difficulty, sections: selectedSections });
            // quiz.id should come from backend. Navigate to detail page:
            const id = quiz.id || 0;
            navigate(`/quiz/${id}`, { state: { quiz } });
        } catch (e) {
            alert(e?.response?.data?.detail || "Failed to generate quiz");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen p-4 max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold mb-4">Generate Quiz</h2>

            <div className="bg-yellow-100  border rounded-xl p-4 shadow">
                <label className="text-sm font-medium">Wikipedia URL</label>
                <input
                    className="w-full border rounded p-2 mt-1"
                    placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                />

                <button
                    onClick={handlePreview}
                    className="mt-3 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    disabled={loading || !url}
                >
                    {loading ? "Checking..." : "Validate & Preview"}
                </button>

                {preview && (
                    <>
                        <div className="mt-4">
                            <p className="text-sm">Title:</p>
                            <h3 className="font-semibold">{preview.title}</h3>
                        </div>

                        <div className="mt-4">
                            <label className="text-sm font-medium">Difficulty</label>
                            <select
                                className="w-full border rounded p-2 mt-1"
                                value={difficulty}
                                onChange={(e) => setDifficulty(e.target.value)}
                            >
                                <option>Easy</option>
                                <option>Medium</option>
                                <option>Hard</option>
                            </select>
                        </div>

                        <div className="mt-4">
                            <p className="text-sm font-medium mb-2">Focus Sections (optional)</p>
                            <div className="flex flex-wrap gap-2">
                                {preview.available_sections?.map((sec, i) => (
                                    <button
                                        key={i}
                                        onClick={() => toggleSection(sec)}
                                        className={`text-sm border rounded px-2 py-1 ${selectedSections.includes(sec) ? "text-cyan-300 border-b-blue-200 bg-gray-800" : "bg-gray-800 text-white"
                                            }`}
                                    >
                                        {sec}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <button
                            onClick={handleGenerate}
                            className="mt-4 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                            disabled={loading}
                        >
                            {loading ? "Generating..." : "Submit & Generate Quiz"}
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}
