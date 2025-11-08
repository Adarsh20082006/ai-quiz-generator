import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import QuizDisplay from "../components/QuizDisplay";

export default function Scorecard() {
    const { state } = useLocation(); // contains { score, total, quiz, answers }
    const navigate = useNavigate();

    if (!state) return null;
    const { score, total, quiz, answers } = state;
    const [viewSubmission, setViewSubmission] = useState(false);

    // Get performance message
    const getMessage = () => {
        const ratio = score / total;
        if (ratio >= 0.8) return "Excellent! 🎉";
        if (ratio >= 0.5) return "Nice work! 👍";
        return "Keep practicing! 💪";
    };

    // View submission toggle
    if (viewSubmission) {
        return (
            <div className="min-h-screen bg-slate-800 p-4">
                <div className="max-w-3xl mx-auto ">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-2xl font-bold text-slate-50">
                            Your Submission Review
                        </h2>
                        <button
                            onClick={() => setViewSubmission(false)}
                            className="bg-slate-700 hover:bg-slate-600 border-transparent
border-transparent text-slate-100 px-4 py-2 rounded-lg shadow transition"
                        >
                            Back to Score
                        </button>
                    </div>
                    <QuizDisplay quiz={quiz} answers={answers} />
                </div>
            </div>
        );
    }

    // Score summary view
    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6">
            <div className="bg-slate-600 rounded-xl shadow-lg border border-slate-800 w-full max-w-md p-6 text-center">
                <h2 className="text-3xl font-bold text-slate-50 mb-2">Your Score</h2>
                <p className="text-4xl font-extrabold text-yellow-400">
                    {score} / {total}
                </p>
                <p className="text-slate-200 mt-2 text-lg">{getMessage()}</p>

                <div className="mt-6 flex flex-col sm:flex-row justify-center gap-3">
                    <button
                        onClick={() => setViewSubmission(true)}
                        className="bg-emerald-500 hover:bg-emerald-600 border-transparent text-white px-4 py-2 rounded-lg shadow-sm"
                    >
                        View Submission
                    </button>
                    <button
                        onClick={() => navigate("/")}
                        className="bg-slate-800 hover:bg-slate-900 border-transparent text-white px-4 py-2 rounded-lg shadow-sm"
                    >
                        Back to Dashboard
                    </button>
                </div>
            </div>
        </div>
    );
}
