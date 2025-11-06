import { useEffect, useState } from "react";
import { useLocation, useParams, useNavigate } from "react-router-dom";
import { getQuizById } from "../services/api";
import QuizDisplay from "../components/QuizDisplay";

export default function QuizDetail() {
    const { id } = useParams();
    const { state } = useLocation(); // may contain { quiz }
    const [quiz, setQuiz] = useState(state?.quiz || null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!quiz) {
            getQuizById(id).then(setQuiz).catch(() => alert("Failed to load quiz"));
        }
    }, [id, quiz]);

    return (
        <div className="min-h-screen p-4 max-w-3xl mx-auto">
            <div className="flex justify-between items-center mb-3">
                <h2 className="text-2xl font-bold">Quiz</h2>
                <div className="flex gap-2">
                    <button
                        className="bg-green-600 text-white px-3 py-1 rounded"
                        onClick={() => navigate("/take_quiz", { state: { quiz } })}
                        disabled={!quiz}
                    >
                        Take Quiz
                    </button>
                    <button
                        className="bg-gray-900 text-white px-3 py-1 rounded"
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
