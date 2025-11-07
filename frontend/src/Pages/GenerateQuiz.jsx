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
    const [checkingStatus, setCheckingStatus] = useState("NOT STARTED"); // NOT STARTED | STARTED | SUCCESS | FAILED
    const navigate = useNavigate();

    // store active timeout so we can cancel it if modal closes
    const pollTimeoutRef = useRef(null);

    const isWikipediaUrl = (url) => {
        try {
            const parsed = new URL(url);
            return parsed.hostname.includes("wikipedia.org");
        } catch {
            return false;
        }
    };

    const handlePreview = async () => {
        if (!isWikipediaUrl(url)) {
            setError("Please enter a valid Wikipedia URL.");
            return;
        }

        setError("");
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

    const toggleSection = (sec) => {
        setSelectedSections((prev) =>
            prev.includes(sec) ? prev.filter((s) => s !== sec) : [...prev, sec]
        );
    };

    const handleGenerate = async () => {
        setLoading(true);
        setModalOpen(true);
        setCheckingStatus("STARTED");

        try {
            const quizData = await generateQuiz({
                url,
                difficulty,
                sections: selectedSections,
            });

            // ✅ Once quiz generated successfully:
            if (quizData && quizData.id) {
                setQuiz(quizData);
                setCheckingStatus("SUCCESS");

                // close modal and go to quiz display immediately
                setModalOpen(false);
                navigate(`/quiz/${quizData.id}`, { state: { quiz: quizData } });
                return;
            }

            // If response didn’t contain quiz data
            setCheckingStatus("FAILED");
            alert("Something went wrong — no quiz data received.");
            setModalOpen(false);
        } catch (e) {
            setCheckingStatus("FAILED");
            alert(e?.response?.data?.detail || "Failed to generate quiz");
            setModalOpen(false);
        } finally {
            setLoading(false);
        }
    };

    // simple local poll that checks if quiz is set with an id and then navigates.
    const startLocalPoll = () => {
        // clear any existing timeout
        if (pollTimeoutRef.current) clearTimeout(pollTimeoutRef.current);

        const attempt = () => {
            if (quiz && quiz.id) {
                // success: close modal and go to detail view
                setModalOpen(false);
                setCheckingStatus("NOT STARTED");
                navigate(`/quiz/${quiz.id}`, { state: { quiz } });
                return;
            }
            // retry shortly (kept small for snappy UX; adjust if you like)
            pollTimeoutRef.current = setTimeout(attempt, 300);
        };

        // kick off first attempt after a tiny delay (gives React time to set state)
        pollTimeoutRef.current = setTimeout(attempt, 200);
    };

    // clear timeout if component unmounts
    useEffect(() => {
        return () => {
            if (pollTimeoutRef.current) clearTimeout(pollTimeoutRef.current);
        };
    }, []);

    return (
        <div className="min-h-screen p-4 max-w-2xl mx-auto">
            {/* Header */}
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
                    className="w-full border border-slate-300 rounded p-2 mt-1 focus:ring-2 focus:ring-blue-400 focus:outline-none"
                    placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    readOnly={!!preview}
                />
                {error && (
                    <p className="text-red-600 text-sm mt-2 font-medium animate-fadeIn">
                        {error}
                    </p>
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
                                className="w-full border rounded p-2 mt-1 bg-white focus:ring-2 focus:ring-blue-400 focus:outline-none"
                                value={difficulty}
                                onChange={(e) => setDifficulty(e.target.value)}
                                readOnly={!!quiz}
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
                                        className={`text-sm border rounded px-2 py-1 transition ${selectedSections.includes(sec)
                                            ? "text-cyan-300 border-blue-200 bg-gray-800"
                                            : "bg-gray-800 text-white"
                                            }`}
                                    >
                                        {sec}
                                    </button>
                                ))}
                            </div>
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

            {/* Modal: summary while generating; closes automatically on success */}
            <Modal
                isOpen={modalOpen}
                onClose={() => {
                    // user wants to stop waiting; close modal and clear any timer
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
                        <h3 className="text-lg font-semibold text-slate-800">
                            Take a moment to revise before your quiz!
                        </h3>
                        {preview?.summary ? (
                            <p className="text-sm text-slate-600 leading-relaxed bg-slate-100 border border-slate-200 rounded-lg p-3">
                                {preview.summary}
                            </p>
                        ) : (
                            <p className="text-sm text-slate-600 leading-relaxed bg-slate-100 border border-slate-200 rounded-lg p-3">
                                {preview?.available_sections?.length
                                    ? `This article covers: ${preview.available_sections
                                        .slice(0, 3)
                                        .join(", ")} and more...`
                                    : "Analyzing key sections of the Wikipedia article..."}
                            </p>
                        )}
                        <div className="flex items-center space-x-3 text-sm text-slate-500">
                            <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                            <p>Generating questions, please wait...</p>
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
