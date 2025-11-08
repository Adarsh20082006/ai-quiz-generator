import { useEffect, useState } from "react";
import { useLocation, useParams, useNavigate } from "react-router-dom";
import { getQuizById } from "../services/api";
import QuizDisplay from "../components/QuizDisplay";

export default function QuizDetail() {
    const { id } = useParams();
    // const { state } = useLocation(); // may contain { quiz }
    const [quiz, setQuiz] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!quiz) {
            getQuizById(id)
                .then((data) => setQuiz(data))
                .catch(() => setError("Failed to load quiz. Please try again."))
                .finally(console.log("Got the individual quiz data"));
        }
    }, [id]);

    return (
        <div className="min-h-screen p-4 max-w-3xl mx-auto">
            <div className="flex justify-between items-center mb-3">
                <h2 className="text-2xl font-bold">Quiz</h2>
                <div className="flex gap-2">
                    <button
                        className="bg-emerald-500 border-transparent hover:bg-emerald-600 text-white px-3 py-1 rounded"
                        onClick={() => navigate("/take_quiz", { state: { quiz } })}
                        disabled={!quiz}
                    >
                        Take Quiz
                    </button>
                    <button
                        className="bg-slate-700 border-transparent hover:bg-slate-600 text-slate-100 px-4 py-2 rounded-lg shadow transition"
                        onClick={() => navigate("/")}
                    >
                        Dashboard
                    </button>
                </div>
            </div>
            <QuizDisplay quiz={quiz} />
        </div>
    );
}
