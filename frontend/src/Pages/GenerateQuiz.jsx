import { useState, useRef, useEffect } from "react";
import { previewArticle, generateQuiz } from "../services/api";
import { useNavigate } from "react-router-dom";
import Modal from "../components/Modal";

export default function GenerateQuiz() {
    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [preview, setPreview] = useState(null);
    const [difficulty, setDifficulty] = useState("Medium");
    const [selectedSections, setSelectedSections] = useState([]);
    const [quiz, setQuiz] = useState(null);
    const [modalOpen, setModalOpen] = useState(false);
    const [error, setError] = useState("");
    const [fieldErrors, setFieldErrors] = useState({});
    const [checkingStatus, setCheckingStatus] = useState("NOT STARTED"); // NOT STARTED | STARTED | SUCCESS | FAILED
    const navigate = useNavigate();
    const pollTimeoutRef = useRef(null);

    // ✅ Validate Wikipedia URL
    const isWikipediaUrl = (url) => {
        try {
            const parsed = new URL(url);
            return parsed.hostname.endsWith("wikipedia.org");
        } catch {
            return false;
        }
    };

    // ✅ Handle URL Preview Validation
    const handlePreview = async () => {
        const errors = {};
        if (!url.trim()) {
            errors.url = "URL is required.";
        } else if (!isWikipediaUrl(url)) {
            errors.url = "Please enter a valid Wikipedia URL.";
        }

        if (Object.keys(errors).length > 0) {
            setFieldErrors(errors);
            return;
        }

        setError("");
        setFieldErrors({});
        setLoading(true);
        try {
            const data = await previewArticle(url);
            setPreview(data);
        } catch (e) {
            setError(e?.response?.data?.detail || "Something went wrong! Please try again.");
        } finally {
            setLoading(false);
        }
    };

    // ✅ Toggle Section Selection
    const toggleSection = (sec) => {
        setSelectedSections((prev) =>
            prev.includes(sec) ? prev.filter((s) => s !== sec) : [...prev, sec]
        );
    };

    // ✅ Generate Quiz Handler
    const handleGenerate = async () => {
        const errors = {};
        if (!url || !isWikipediaUrl(url)) {
            errors.url = "Invalid or missing Wikipedia URL.";
        }
        if (!difficulty) {
            errors.difficulty = "Please select a difficulty level.";
        }
        if (!selectedSections.length) {
            errors.sections = "Select at least one section to focus on.";
        }

        if (Object.keys(errors).length > 0) {
            setFieldErrors(errors);
            return;
        }

        setLoading(true);
        setModalOpen(true);
        setCheckingStatus("STARTED");

        try {
            const quizData = await generateQuiz({
                url,
                difficulty,
                sections: selectedSections,
            });

            if (quizData && quizData.id) {
                setQuiz(quizData);
                setCheckingStatus("SUCCESS");
                setModalOpen(false);
                navigate(`/quiz/${quizData.id}`, { state: { quiz: quizData } });
                return;
            }

            setCheckingStatus("FAILED");
            setError("Something went wrong — no quiz data received.");
            setModalOpen(false);
        } catch (e) {
            setCheckingStatus("FAILED");
            setError(e?.response?.data?.detail || "Failed to generate quiz");
            setModalOpen(false);
        } finally {
            setLoading(false);
        }
    };

    // ✅ Cleanup polling
    useEffect(() => {
        return () => {
            if (pollTimeoutRef.current) clearTimeout(pollTimeoutRef.current);
        };
    }, []);

    return (
        <div className="min-h-screen p-4 max-w-2xl mx-auto">
            <div className="flex items-center justify-between mb-5">
                <h2 className="text-2xl font-bold text-slate-900">Generate Quiz</h2>
                <button
                    onClick={() => navigate("/")}
                    className="bg-slate-800 hover:bg-slate-900 text-white px-4 py-2 rounded-lg shadow transition"
                >
                    Back to Dashboard
                </button>
            </div>

            <div className="bg-yellow-100 border border-yellow-300 rounded-xl p-4 shadow">
                <label className="text-sm font-medium">Wikipedia URL</label>
                <input
                    className={`w-full border rounded p-2 mt-1 focus:ring-2 focus:ring-blue-400 focus:outline-none ${fieldErrors.url ? "border-red-500" : "border-slate-300"}`}
                    placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    readOnly={!!preview}
                />
                {fieldErrors.url && (
                    <p className="text-red-600 text-sm mt-1">{fieldErrors.url}</p>
                )}

                {!preview && (
                    <button
                        onClick={handlePreview}
                        className="mt-3 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
                        disabled={loading || !url}
                    >
                        {loading ? "Checking..." : "Validate & Preview"}
                    </button>
                )}

                {preview && (
                    <>
                        <div className="mt-4">
                            <p className="text-sm">Title:</p>
                            <h3 className="font-semibold text-slate-800">{preview.title}</h3>
                        </div>

                        <div className="mt-4">
                            <label className="text-sm font-medium">Difficulty</label>
                            <select
                                className={`w-full border rounded p-2 mt-1 bg-white focus:ring-2 focus:ring-blue-400 focus:outline-none ${fieldErrors.difficulty ? "border-red-500" : "border-slate-300"}`}
                                value={difficulty}
                                onChange={(e) => setDifficulty(e.target.value)}
                                readOnly={!!quiz}
                            >
                                <option>Easy</option>
                                <option>Medium</option>
                                <option>Hard</option>
                            </select>
                            {fieldErrors.difficulty && (
                                <p className="text-red-600 text-sm mt-1">{fieldErrors.difficulty}</p>
                            )}
                        </div>

                        <div className="mt-4">
                            <p className="text-sm font-medium mb-2">Focus Sections (optional)</p>
                            <div className="flex flex-wrap gap-2">
                                {preview.available_sections?.map((sec, i) => (
                                    <button
                                        key={i}
                                        onClick={() => toggleSection(sec)}
                                        className={`text-sm border rounded px-2 py-1 transition ${selectedSections.includes(sec)
                                            ? "text-cyan-300 border-blue-200 bg-gray-800"
                                            : "bg-gray-800 text-white"
                                            }`}
                                    >
                                        {sec}
                                    </button>
                                ))}
                            </div>
                            {fieldErrors.sections && (
                                <p className="text-red-600 text-sm mt-1">{fieldErrors.sections}</p>
                            )}
                        </div>

                        <button
                            onClick={handleGenerate}
                            className="mt-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded transition"
                            disabled={loading}
                        >
                            {loading ? "Generating..." : "Submit & Generate Quiz"}
                        </button>
                    </>
                )}
            </div>

            {/* Modal */}
            <Modal
                isOpen={modalOpen}
                onClose={() => {
                    if (pollTimeoutRef.current) clearTimeout(pollTimeoutRef.current);
                    setModalOpen(false);
                }}
                title={
                    checkingStatus === "STARTED"
                        ? "Generating Your Quiz..."
                        : checkingStatus === "FAILED"
                            ? "Something went wrong"
                            : "Preparing Article Summary..."
                }
            >
                {checkingStatus === "STARTED" ? (
                    <div className="space-y-4">
                        {/* Heading */}
                        <h3 className="text-lg font-semibold text-slate-800">
                            Key Points to Revise Before Your Quiz
                        </h3>

                        {/* Summary Points List */}
                        {preview?.summary_points?.length ? (
                            <ul className="text-sm bg-slate-100 border border-slate-200 rounded-lg p-4 space-y-2 text-slate-700 max-h-72 overflow-y-auto shadow-inner">
                                {preview.summary_points.map((pt, i) => (
                                    <li
                                        key={i}
                                        className="flex items-start gap-3 leading-relaxed hover:bg-slate-200/60 rounded-lg p-1 transition"
                                    >
                                        <span className="text-blue-600 font-bold min-w-[20px]">
                                            {i + 1}.
                                        </span>
                                        <span className="text-slate-800">{pt}</span>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="text-sm text-slate-600 leading-relaxed bg-slate-100 border border-slate-200 rounded-lg p-3">
                                {preview?.available_sections?.length
                                    ? `Analyzing sections: ${preview.available_sections
                                        .slice(0, 3)
                                        .join(", ")} and more...`
                                    : "Extracting key insights from the article..."}
                            </p>
                        )}

                        {/* Loader */}
                        <div className="flex items-center space-x-3 text-sm text-slate-500 mt-4">
                            <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                            <p>Generating quiz questions — please wait...</p>
                        </div>
                    </div>
                ) : checkingStatus === "FAILED" ? (
                    <p className="text-sm text-red-600">
                        Failed to generate quiz. Please close and try again.
                    </p>
                ) : null}
            </Modal>

        </div>
    );
}
